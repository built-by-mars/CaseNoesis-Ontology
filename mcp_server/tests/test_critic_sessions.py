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
        "scorecard": {},
    }


def test_two_pass_manual_finalize(workspace):
    read, _write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
    )
    assert started["state"] == "awaiting_critic_response"
    sid = started["session_id"]

    submit_manual_critic_response(sid, _empty_critic_response(started))
    # Confirmation revision with identical hash allowed when no critical/high blockers
    revised = submit_critic_revision(sid, graph_path=str(graph), change_summary="confirm")
    assert revised["pass_number"] == 2
    submit_manual_critic_response(sid, _empty_critic_response(revised))

    status = get_critic_review_status(sid)
    assert status["completed_critic_responses"] == 2

    final = finalize_critic_review(sid)
    assert final["accepted"] is True
    assert final["state"] == "finalized"


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


def test_extend_requires_token_and_caps(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    with pytest.raises(CriticSessionError) as exc:
        extend_critic_review(sid, 1, approval_token="wrong")
    assert exc.value.code == "critic_session_extend_denied"

    # Load real token from session file
    session_path = (
        Path(workspace[1] / "critic-sessions" / sid / "session.json")
    )
    token = json.loads(session_path.read_text())["extend_approval_token"]
    extended = extend_critic_review(sid, 2, approval_token=token)
    assert extended["max_total_passes"] == 4

    with pytest.raises(CriticSessionError) as exc2:
        extend_critic_review(sid, 20, approval_token=token)
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
    # Must change artifact to revise while blockers remain
    mutated = json.loads(seeded.read_text())
    mutated["@graph"][0]["uco-core:name"] = "mutated"
    seeded.write_text(json.dumps(mutated), encoding="utf-8")
    revised = submit_critic_revision(sid, graph_path=str(seeded))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    with pytest.raises(CriticSessionError) as exc:
        finalize_critic_review(sid)
    assert exc.value.code == "critic_session_blockers_remain"


def test_handoff_preview_and_write(workspace):
    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(graph_path=str(graph), critic_scope="graph")
    sid = started["session_id"]
    submit_manual_critic_response(sid, _empty_critic_response(started))
    revised = submit_critic_revision(sid, graph_path=str(graph))
    submit_manual_critic_response(sid, _empty_critic_response(revised))
    finalize_critic_review(sid)

    # Use a deterministic finding id from last review
    review = json.loads(
        (write / "critic-sessions" / sid / "review-pass-2.json").read_text()
    )
    finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    if not finding_ids:
        # Fabricate by reading pass-1 if gold has no findings
        review = json.loads(
            (write / "critic-sessions" / sid / "review-pass-1.json").read_text()
        )
        finding_ids = [f["finding_id"] for f in review["merged_findings"][:1]]
    assert finding_ids

    preview = prepare_critic_handoff(
        sid,
        finding_ids,
        operator_id="tester",
        operator_rationale="review recipe guidance",
    )
    assert preview["preview"]["requires_operator_approval"] is True
    assert preview["written_path"] is None

    out = write / "handoff.json"
    written = prepare_critic_handoff(
        sid,
        finding_ids,
        operator_id="tester",
        output_path=str(out),
        approve_write=True,
    )
    assert written["written_path"]
    assert Path(written["written_path"]).is_file()


def test_sampling_fake_context(workspace):
    import asyncio
    from critic.sampling import FakeSampleContext, maybe_sample_critic

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
    assert sampled is not None
    result = submit_manual_critic_response(started["session_id"], sampled)
    assert result["completed_critic_responses"] == 1
