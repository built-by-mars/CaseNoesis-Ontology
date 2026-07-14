"""P0 tests for review_config_sha256 and prompt rebuild verification."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import graph_validator
from critic.schema_util import compute_review_config_sha256
from critic.sessions import (
    CriticSessionError,
    get_critic_review_status,
    rebuild_prompt_package_for_pass,
    session_root,
    start_critic_review,
    submit_manual_critic_response,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"


def _conforming_report(**kwargs) -> graph_validator.GraphValidationReport:
    return graph_validator.GraphValidationReport(
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
        "review_config_sha256": package.get("review_config_sha256"),
        "findings": [],
        "finding_assessments": [],
        "scorecard": {},
    }


def _base_kwargs() -> dict:
    return {
        "critic_scope": "graph",
        "serializer_mode": "auto",
        "extensions": [],
        "profiles": [],
        "force_rdfs_inference": False,
        "extra_ontology_sha256": {},
        "bundle_fingerprint": "fp-base",
        "bundle_resource_hashes": {"core.ttl": "a" * 64},
    }


def test_extension_only_changes_review_config_sha256():
    base = _base_kwargs()
    a = compute_review_config_sha256(**base)
    b = compute_review_config_sha256(**{**base, "extensions": ["cac"]})
    assert a != b


def test_profile_only_changes_review_config_sha256():
    base = _base_kwargs()
    a = compute_review_config_sha256(**base)
    b = compute_review_config_sha256(**{**base, "profiles": ["investigation"]})
    assert a != b


def test_inference_only_changes_review_config_sha256():
    base = _base_kwargs()
    a = compute_review_config_sha256(**base)
    b = compute_review_config_sha256(**{**base, "force_rdfs_inference": True})
    assert a != b


def test_bundle_resource_and_extra_ontology_change_review_config_sha256(tmp_path):
    base = _base_kwargs()
    a = compute_review_config_sha256(**base)
    b = compute_review_config_sha256(
        **{**base, "bundle_resource_hashes": {"core.ttl": "b" * 64}}
    )
    assert a != b

    owl = tmp_path / "extra.ttl"
    owl.write_text("# v1\n", encoding="utf-8")
    from critic.graph_integrity import sha256_file

    h1 = sha256_file(owl)
    c = compute_review_config_sha256(
        **{**base, "extra_ontology_sha256": {f"extra-1:{owl.name}": h1}}
    )
    assert a != c
    owl.write_text("# v2 mutated\n", encoding="utf-8")
    h2 = sha256_file(owl)
    d = compute_review_config_sha256(
        **{**base, "extra_ontology_sha256": {f"extra-1:{owl.name}": h2}}
    )
    assert c != d


def test_session_config_tamper_fails_submit(workspace):
    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    assert started["prompt_package"].get("review_config_sha256")

    session_path = write / "critic-sessions" / sid / "session.json"
    session = json.loads(session_path.read_text(encoding="utf-8"))
    session["config"]["extensions"] = ["cac"]
    session_path.write_text(json.dumps(session, indent=2), encoding="utf-8")

    with pytest.raises(CriticSessionError) as exc:
        submit_manual_critic_response(sid, _empty_critic_response(started))
    assert exc.value.code in {
        "critic_session_prompt_rebuild_mismatch",
        "critic_session_hash_mismatch",
    }


def test_prompt_rebuild_hash_mismatch_fails(workspace):
    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    review_path = write / "critic-sessions" / sid / "review-pass-1.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["prompt_package_hash"] = "0" * 64
    review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")

    with pytest.raises(CriticSessionError) as exc:
        submit_manual_critic_response(sid, _empty_critic_response(started))
    assert exc.value.code == "critic_session_prompt_rebuild_mismatch"
    assert "prompt_package_hash" in str(exc.value)


def test_rebuild_prompt_package_verifies_stored_hashes(workspace):
    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    directory = session_root() / sid
    session = json.loads((directory / "session.json").read_text(encoding="utf-8"))
    rebuilt = rebuild_prompt_package_for_pass(session, directory, 1)
    assert rebuilt["review_config_sha256"] == started["prompt_package"][
        "review_config_sha256"
    ]
    assert rebuilt["prompt_package_hash"] == started["prompt_package"][
        "prompt_package_hash"
    ]

    review_path = directory / "review-pass-1.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["review_config_sha256"] = "f" * 64
    review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
    with pytest.raises(CriticSessionError) as exc:
        rebuild_prompt_package_for_pass(session, directory, 1)
    assert exc.value.code == "critic_session_prompt_rebuild_mismatch"


def test_audit_corruption_fails_status(workspace):
    read, write = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    sid = started["session_id"]
    audit_path = write / "critic-sessions" / sid / "audit.jsonl"
    lines = audit_path.read_text(encoding="utf-8").splitlines()
    last = json.loads(lines[-1])
    last["previous_event_sha256"] = "a" * 64
    body = {k: v for k, v in last.items() if k != "event_sha256"}
    import hashlib

    last["event_sha256"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    lines[-1] = json.dumps(last, sort_keys=True)
    audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(CriticSessionError) as exc:
        get_critic_review_status(sid)
    assert exc.value.code == "critic_session_audit_corrupt"


def test_analyze_artifact_embeds_review_config(workspace):
    read, _ = workspace
    graph = _copy_gold(read)
    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="manual",
        force_rdfs_inference=True,
        extensions=["cac"],
    )
    package = started["prompt_package"]
    assert package["review_config"]["force_rdfs_inference"] is True
    assert package["review_config"]["extensions"] == ["cac"]
    assert package["review_config_sha256"]
    assert (session_root() / started["session_id"] / "config-pass-1.json").is_file()
