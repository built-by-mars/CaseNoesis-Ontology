"""Tests for critic sessions (#76) and handoff (#78)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import graph_validator
from critic.sessions import (
    CriticSessionError,
    extend_critic_review,
    finalize_critic_review,
    get_critic_review_status,
    start_critic_review,
    submit_critic_revision,
    submit_manual_critic_response,
)
from critic.handoff import prepare_critic_handoff
from graph_validator import GraphValidationReport

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"


def _conforming_report(**kwargs) -> GraphValidationReport:
    return GraphValidationReport(
        conforms=True,
        warning_count=0,
        violation_count=0,
        exit_code=0,
        validator_name="case_validate",
        safe_summary="conforms",
        verification_status="complete",
        **kwargs,
    )


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    read = tmp_path / "read"
    write = tmp_path / "write"
    read.mkdir()
    write.mkdir()
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", str(read))
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(write))
    monkeypatch.setenv("CASE_UCO_CRITIC_SESSION_ROOT", str(write / "critic-sessions"))
    monkeypatch.setenv("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    monkeypatch.setattr(
        graph_validator,
        "validate_graph_file",
        lambda *a, **k: _conforming_report(),
    )
    return read, write


def _copy_gold(read: Path) -> Path:
    dest = read / "gold.jsonld"
    dest.write_text(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return dest


def _empty_critic_response(started: dict) -> dict:
    package = started["prompt_package"]
    return {
        "schema_version": "1.2.0",
        "session_id": started["session_id"],
        "pass_number": package["pass_number"],
        "graph_sha256": package["artifact_hashes"]["graph_sha256"],
        "serializer_sha256": package["artifact_hashes"].get("serializer_sha256"),
        "prompt_package_hash": package["prompt_package_hash"],
        "review_request_sha256": package.get("review_request_sha256"),
        "findings": [],
        "finding_assessments": [],
        "scorecard": {},
    }


def _critical_critic_finding(started: dict) -> dict:
    payload = _empty_critic_response(started)
    payload["findings"] = [
        {
            "severity": "critical",
            "category": "investigation_structure",
            "confidence": 0.9,
            "claim_type": "missing_object_link",
            "target": {"node_id": "urn:example:investigation"},
            "evidence": ["model observed missing object"],
            "rationale": "Investigation lacks required object reference",
            "recommended_change": "Add uco-core:object",
            "verification_method": "re-analyze graph",
        }
    ]
    return payload


def test_two_pass_manual_finalize(workspace):
    read, _write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
    )
    assert started["state"] == "awaiting_critic_response"
    assert "extend_approval_challenge" in started
    sid = started["session_id"]

    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    assert revised["pass_number"] == 2
    submit_manual_critic_response(sid, _empty_critic_response(revised))

    status = get_critic_review_status(sid)
    assert status["completed_critic_responses"] == 2

    final = finalize_critic_review(sid)
    assert final["state"] == "finalized"
    assert final["outcome"] in {"accepted", "completed_with_findings"}


def test_pass2_critic_critical_blocks_acceptance(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    submit_manual_critic_response(sid, _critical_critic_finding(revised))
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_blockers_remain"


def test_overcap_additional_iterations_rejected(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    with pytest.raises(CriticSessionError) as exc:
        start_critic_review(
            graph_path=str(graph),
            critic_scope="graph",
            additional_iterations=99,
        )
    assert exc.value.code == "critic_session_pass_cap"


def test_manual_response_rejects_wrong_hash(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    bad = _empty_critic_response(started)
    bad["graph_sha256"] = "0" * 64
    with pytest.raises(CriticSessionError) as exc:
        submit_manual_critic_response(started["session_id"], bad)
    assert exc.value.code in {
        "critic_artifact_hash_mismatch",
        "critic_response_schema_mismatch",
    }


def test_extend_uses_returned_challenge(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    with pytest.raises(CriticSessionError) as exc:
        extend_critic_review(sid, 1, approval_token="wrong")
    assert exc.value.code == "critic_session_extend_denied"

    challenge = started["extend_approval_challenge"]
    extended = extend_critic_review(sid, 2, approval_token=challenge)
    assert extended["max_total_passes"] == 4
    assert extended["extend_approval_challenge"] != challenge

    with pytest.raises(CriticSessionError) as exc2:
        extend_critic_review(
            sid, 20, approval_token=extended["extend_approval_challenge"]
        )
    assert exc2.value.code == "critic_session_pass_cap"


def test_finalize_rejects_open_critical(workspace, monkeypatch):
    read, _ = workspace
    seeded = read / "seeded.jsonld"
    seeded.write_text(
        (FIXTURES / "seeded-defects.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    started = start_critic_review(graph_path=str(seeded), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    mutated = json.loads(seeded.read_text())
    mutated["@graph"][0]["uco-core:name"] = "mutated"
    seeded.write_text(json.dumps(mutated), encoding="utf-8")
    revised = submit_critic_revision(sid, graph_path=str(seeded))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_blockers_remain"


def test_finalize_rejects_post_review_file_modification(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    graph.write_text(graph.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_hash_mismatch"


def test_handoff_preview_and_write(workspace, monkeypatch):
    read, write = workspace
    monkeypatch.setenv("CASE_UCO_CRITIC_HANDOFF_TOKEN", "handoff-secret")
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    finalize_critic_review(sid)

    review = json.loads(
        (write / "critic-sessions" / sid / "review-pass-2.json").read_text()
    )
    finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    if not finding_ids:
        review = json.loads(
            (write / "critic-sessions" / sid / "review-pass-1.json").read_text()
        )
        finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    assert finding_ids

    preview = prepare_critic_handoff(
        sid,
        finding_ids,
        requested_handoff_type="recipe_improvement",
        operator_id="tester",
        operator_rationale="review recipe guidance",
    )
    assert preview["preview"]["requires_operator_approval"] is True
    assert preview["written_path"] is None

    written = prepare_critic_handoff(
        sid,
        finding_ids,
        requested_handoff_type="case_specific",
        operator_id="tester",
        approve_write=True,
        approval_token="handoff-secret",
    )
    assert written["written_path"]
    assert "critic-handoffs/candidates" in written["written_path"].replace("\\", "/")
    assert Path(written["written_path"]).is_file()


def test_sampling_fake_context(workspace):
    import asyncio
    from critic.sampling import FakeSampleContext, maybe_sample_critic
    from critic_tools import tool_start_critic_review_with_sampling

    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="client_sampling",
    )
    payload = _empty_critic_response(started)
    ctx = FakeSampleContext(payload)

    async def _run():
        return await maybe_sample_critic(
            ctx, started["prompt_package"], model_policy="client_sampling"
        )

    sampled = asyncio.run(_run())
    assert sampled.status == "ok"
    user_json = json.loads(ctx.kwargs_history[0]["messages"][0]["content"])
    assert "prompt_package" in user_json
    assert "graph_neighborhoods" in user_json["prompt_package"]
    result = submit_manual_critic_response(started["session_id"], sampled.response)
    assert result["completed_critic_responses"] == 1

    async def _wired_ok():
        class Ctx:
            async def sample(self, **kwargs):
                content = json.loads(kwargs["messages"][0]["content"])
                package = content["prompt_package"]
                resp = {
                    "schema_version": "1.2.0",
                    "session_id": package["session_id"],
                    "pass_number": package["pass_number"],
                    "graph_sha256": package["artifact_hashes"]["graph_sha256"],
                    "serializer_sha256": package["artifact_hashes"].get(
                        "serializer_sha256"
                    ),
                    "prompt_package_hash": package["prompt_package_hash"],
                    "review_request_sha256": package.get("review_request_sha256"),
                    "findings": [],
                    "finding_assessments": [],
                    "scorecard": {},
                }
                return {"text": json.dumps(resp), "model": "fake"}

        return await tool_start_critic_review_with_sampling(
            Ctx(),
            graph_path=str(graph),
            critic_scope="graph",
        )

    wired = asyncio.run(_wired_ok())
    assert wired["ok"] is True
    assert wired["sampling"]["status"] == "ok"
    assert wired["state"] == "awaiting_revision"
