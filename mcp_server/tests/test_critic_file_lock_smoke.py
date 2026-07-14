"""Cross-platform FileLock + manual session smoke (Windows CI evidence)."""

from __future__ import annotations

from pathlib import Path

import graph_validator
from critic.file_lock import FileLock, ensure_lock_file
from critic.sessions import start_critic_review, submit_manual_critic_response
from graph_validator import GraphValidationReport

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"


def test_file_lock_and_manual_session_smoke(tmp_path, monkeypatch):
    lock_path = tmp_path / "session.lock"
    ensure_lock_file(lock_path)
    with open(lock_path, "a+", encoding="utf-8") as handle:
        with FileLock(handle):
            handle.write("locked\n")
            handle.flush()

    read = tmp_path / "read"
    write = tmp_path / "write"
    read.mkdir()
    write.mkdir()
    graph = read / "gold.jsonld"
    graph.write_text(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", str(read))
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(write))
    monkeypatch.setenv("CASE_UCO_CRITIC_SESSION_ROOT", str(write / "critic-sessions"))
    monkeypatch.setenv("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    monkeypatch.setattr(
        graph_validator,
        "validate_graph_file",
        lambda *a, **k: GraphValidationReport(
            conforms=True,
            warning_count=0,
            violation_count=0,
            exit_code=0,
            validator_name="case_validate",
            safe_summary="conforms",
            verification_status="complete",
        ),
    )

    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    package = started["prompt_package"]
    response = {
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
    submitted = submit_manual_critic_response(started["session_id"], response)
    assert submitted["completed_critic_responses"] == 1
    assert submitted["state"] == "awaiting_revision"
