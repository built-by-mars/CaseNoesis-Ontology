"""Provenance sidecar integrity: schema 1.1, workspace policy, sessions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from critic.coverage import check_provenance_manifest
from critic.deterministic import analyze_artifact
from critic.models import CriticArtifactRequest
from critic.sessions import rebuild_prompt_package_for_pass, start_critic_review

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    return read, write


def _write_graph(read: Path) -> Path:
    dest = read / "graph.jsonld"
    dest.write_text(
        (FIXTURES / "gold-charged-with.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return dest


def test_schema11_artifacts_and_output_must_match_graph(workspace):
    read, _write = workspace
    graph = _write_graph(read)
    builder = read / "builder.py"
    builder.write_text("# builder\n", encoding="utf-8")
    recipe = read / "recipe.md"
    recipe.write_text("# recipe\n", encoding="utf-8")
    graph_sha = _sha(graph)
    manifest = read / "build-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.1",
                "artifacts": [
                    {
                        "role": "builder_source",
                        "path": str(builder),
                        "sha256": _sha(builder),
                    },
                    {
                        "role": "modeling_guidance",
                        "path": str(recipe),
                        "sha256": _sha(recipe),
                    },
                    {
                        "role": "output_artifact",
                        "path": str(graph),
                        "sha256": graph_sha,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    findings, executions = check_provenance_manifest(
        manifest,
        project_root=read,
        artifact_hash=graph_sha,
        graph_sha256=graph_sha,
    )
    assert findings == []
    assert executions[0].status == "evaluated"


def test_empty_manifest_fails_closed(workspace):
    read, _write = workspace
    graph = _write_graph(read)
    manifest = read / "empty.json"
    manifest.write_text(json.dumps({"schema_version": "1.1", "artifacts": []}), encoding="utf-8")
    findings, executions = check_provenance_manifest(
        manifest,
        project_root=read,
        artifact_hash=_sha(graph),
        graph_sha256=_sha(graph),
    )
    assert any(f.rule_id == "CRIT-C-PROVENANCE-MANIFEST-EMPTY" for f in findings)
    assert executions[0].status == "failed"


def test_path_outside_workspace_denied(workspace, tmp_path):
    read, _write = workspace
    graph = _write_graph(read)
    outside = tmp_path / "outside.py"
    outside.write_text("x\n", encoding="utf-8")
    manifest = read / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "artifacts": [
                    {
                        "role": "builder_source",
                        "path": str(outside),
                        "sha256": _sha(outside),
                    },
                    {
                        "role": "output_artifact",
                        "path": str(graph),
                        "sha256": _sha(graph),
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    findings, _ = check_provenance_manifest(
        manifest,
        project_root=read,
        artifact_hash=_sha(graph),
        graph_sha256=_sha(graph),
    )
    assert any(
        f.rule_id == "CRIT-C-PROVENANCE-MANIFEST-PATH-DENIED" for f in findings
    )


def test_session_retains_provenance_manifest(workspace, monkeypatch):
    import graph_validator

    read, _write = workspace
    graph = _write_graph(read)
    builder = read / "builder.py"
    builder.write_text("print('build')\n", encoding="utf-8")
    recipe = read / "recipe.md"
    recipe.write_text("# guidance\n", encoding="utf-8")
    graph_sha = _sha(graph)
    manifest = read / "build-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": "1.1",
                "artifacts": [
                    {
                        "role": "builder_source",
                        "path": str(builder),
                        "sha256": _sha(builder),
                    },
                    {
                        "role": "modeling_guidance",
                        "path": str(recipe),
                        "sha256": _sha(recipe),
                    },
                    {
                        "role": "output_artifact",
                        "path": str(graph),
                        "sha256": graph_sha,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    monkeypatch.setattr(
        graph_validator,
        "validate_graph_file",
        lambda *a, **k: graph_validator.GraphValidationReport(
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
        graph_path=str(graph),
        provenance_manifest_path=str(manifest),
        critic_scope="graph",
        model_policy="manual",
        additional_iterations=0,
    )
    assert started["prompt_package"] is not None
    hashes = started["prompt_package"]["artifact_hashes"]
    assert hashes.get("provenance_manifest_sha256") == _sha(manifest)

    from critic.sessions import session_root

    directory = session_root() / started["session_id"]
    session = json.loads((directory / "session.json").read_text(encoding="utf-8"))
    assert session["config"].get("provenance_manifest_path") == str(manifest)
    assert session["latest_artifact_set"].get("provenance_manifest_sha256") == _sha(
        manifest
    )
    rebuilt = rebuild_prompt_package_for_pass(session, directory, 1)
    assert rebuilt["artifact_hashes"]["provenance_manifest_sha256"] == _sha(manifest)


def test_analyze_artifact_binds_manifest_digest(workspace, monkeypatch):
    import graph_validator

    read, _write = workspace
    graph = _write_graph(read)
    builder = read / "builder.py"
    builder.write_text("# b\n", encoding="utf-8")
    recipe = read / "recipe.md"
    recipe.write_text("# r\n", encoding="utf-8")
    graph_sha = _sha(graph)
    manifest = read / "build-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "artifacts": [
                    {
                        "role": "builder_source",
                        "path": str(builder),
                        "sha256": _sha(builder),
                    },
                    {
                        "role": "modeling_guidance",
                        "path": str(recipe),
                        "sha256": _sha(recipe),
                    },
                    {
                        "role": "output_artifact",
                        "path": str(graph),
                        "sha256": graph_sha,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    monkeypatch.setattr(
        graph_validator,
        "validate_graph_file",
        lambda *a, **k: graph_validator.GraphValidationReport(
            conforms=True,
            warning_count=0,
            violation_count=0,
            exit_code=0,
            validator_name="case_validate",
            safe_summary="conforms",
            verification_status="complete",
        ),
    )
    review = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(graph),
            provenance_manifest_path=str(manifest),
            critic_scope="graph",
        )
    )
    assert review.artifact_hashes.provenance_manifest_sha256 == _sha(manifest)
    assert not any(
        f.rule_id.startswith("CRIT-C-PROVENANCE-MANIFEST")
        and f.severity in {"critical", "high"}
        for f in review.deterministic_findings
    )
