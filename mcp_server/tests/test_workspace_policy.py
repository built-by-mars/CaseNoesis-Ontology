"""Tests for the MCP filesystem workspace policy (issue #50).

All fixtures are Tier T0 public-safe synthetic data. The policy is
environment-driven; tests use monkeypatch so no state leaks between tests.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import workspace_policy
from document_processor import process_document_file


@pytest.fixture()
def workspace(tmp_path, monkeypatch):
    """A configured policy: evidence/ read root, case-work/ write root."""

    evidence = tmp_path / "evidence"
    case_work = tmp_path / "case-work"
    outside = tmp_path / "outside"
    for directory in (evidence, case_work, outside):
        directory.mkdir()
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    monkeypatch.setenv(workspace_policy.WRITE_ROOTS_ENV, str(case_work))
    monkeypatch.delenv(workspace_policy.ALLOW_OVERWRITE_ENV, raising=False)
    return {"evidence": evidence, "case_work": case_work, "outside": outside}


def _write_csv(directory: Path, name: str = "records.csv") -> Path:
    source = directory / name
    source.write_text("item,amount\nsynthetic-item,12.50\n", encoding="utf-8")
    return source


def test_no_policy_means_no_restriction(tmp_path, monkeypatch):
    monkeypatch.delenv(workspace_policy.READ_ROOTS_ENV, raising=False)
    monkeypatch.delenv(workspace_policy.WRITE_ROOTS_ENV, raising=False)
    assert workspace_policy.policy_active() is False
    source = _write_csv(tmp_path)
    result = process_document_file(source, tmp_path / "out" / "graph.jsonld")
    assert result.output_path.is_file()


def test_in_workspace_processing_succeeds(workspace):
    source = _write_csv(workspace["evidence"])
    output = workspace["case_work"] / "run1" / "graph.jsonld"
    result = process_document_file(source, output)
    assert result.output_path == output.resolve()
    assert output.is_file()


def test_source_outside_read_roots_rejected(workspace):
    source = _write_csv(workspace["outside"])
    with pytest.raises(ValueError, match="source_outside_read_roots"):
        process_document_file(source, workspace["case_work"] / "graph.jsonld")


def test_output_outside_write_roots_rejected(workspace):
    source = _write_csv(workspace["evidence"])
    with pytest.raises(ValueError, match="output_outside_write_roots"):
        process_document_file(source, workspace["outside"] / "graph.jsonld")


def test_dotdot_traversal_rejected(workspace):
    source = _write_csv(workspace["evidence"])
    sneaky = workspace["case_work"] / ".." / "outside" / "graph.jsonld"
    with pytest.raises(ValueError, match="output_outside_write_roots"):
        process_document_file(source, sneaky)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
def test_symlink_escape_rejected(workspace):
    source = _write_csv(workspace["evidence"])
    escape_link = workspace["case_work"] / "escape"
    escape_link.symlink_to(workspace["outside"])
    with pytest.raises(ValueError, match="output_outside_write_roots"):
        process_document_file(source, escape_link / "graph.jsonld")


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlink semantics")
def test_symlinked_source_escape_rejected(workspace):
    real_source = _write_csv(workspace["outside"])
    link = workspace["evidence"] / "records.csv"
    link.symlink_to(real_source)
    with pytest.raises(ValueError, match="source_outside_read_roots"):
        process_document_file(link, workspace["case_work"] / "graph.jsonld")


def test_overwrite_rejected_by_default_under_policy(workspace):
    source = _write_csv(workspace["evidence"])
    output = workspace["case_work"] / "graph.jsonld"
    output.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="output_exists"):
        process_document_file(source, output)


def test_overwrite_allowed_with_explicit_opt_in(workspace, monkeypatch):
    monkeypatch.setenv(workspace_policy.ALLOW_OVERWRITE_ENV, "1")
    source = _write_csv(workspace["evidence"])
    output = workspace["case_work"] / "graph.jsonld"
    output.write_text("{}", encoding="utf-8")
    result = process_document_file(source, output)
    assert result.output_path.is_file()


def test_source_output_conflict_rejected(tmp_path, monkeypatch):
    monkeypatch.delenv(workspace_policy.READ_ROOTS_ENV, raising=False)
    monkeypatch.delenv(workspace_policy.WRITE_ROOTS_ENV, raising=False)
    source = _write_csv(tmp_path)
    with pytest.raises(ValueError, match="source_output_conflict"):
        process_document_file(source, source)


def test_progress_output_outside_write_roots_rejected(workspace):
    source = _write_csv(workspace["evidence"])
    with pytest.raises(ValueError, match="progress_outside_write_roots"):
        process_document_file(
            source,
            workspace["case_work"] / "graph.jsonld",
            progress_output=workspace["outside"] / "progress.ndjson",
        )


def test_validate_graph_read_policy(workspace):
    """validate_graph reads must stay inside read or write roots."""

    import graph_validator

    if not graph_validator.validator_available():
        pytest.skip("case_validate CLI not installed")

    outside_graph = workspace["outside"] / "graph.jsonld"
    outside_graph.write_text(json.dumps({"@context": {}, "@graph": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="source_outside_read_roots"):
        graph_validator.validate_graph_file(outside_graph)


def test_validate_graph_accepts_write_root_artifacts(workspace):
    """Graphs produced into the case workspace remain validatable."""

    import graph_validator

    if not graph_validator.validator_available():
        pytest.skip("case_validate CLI not installed")

    source = _write_csv(workspace["evidence"])
    output = workspace["case_work"] / "graph.jsonld"
    process_document_file(source, output)
    report = graph_validator.validate_graph_file(output)
    assert report.conforms is not None or report.exit_code is not None


def test_multiple_roots_and_comma_separation(tmp_path, monkeypatch):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    monkeypatch.setenv(workspace_policy.READ_ROOTS_ENV, f"{a},{b}")
    roots = workspace_policy.read_roots()
    assert a.resolve() in roots and b.resolve() in roots
    assert workspace_policy.check_read_path(_write_csv(b)) == (b / "records.csv").resolve()


# ---------------------------------------------------------------------------
# Secure production mode (issue #57)
# ---------------------------------------------------------------------------


@pytest.fixture()
def clean_env(monkeypatch):
    for env in (
        workspace_policy.READ_ROOTS_ENV,
        workspace_policy.WRITE_ROOTS_ENV,
        workspace_policy.ALLOW_OVERWRITE_ENV,
        workspace_policy.SECURE_MODE_ENV,
        workspace_policy.PROFILE_ENV,
        workspace_policy.ALLOW_BROAD_ROOTS_ENV,
    ):
        monkeypatch.delenv(env, raising=False)
    return monkeypatch


def test_secure_mode_requires_both_root_sets(clean_env, tmp_path):
    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    errors = workspace_policy.validate_security_configuration()
    assert "read_roots_unconfigured" in errors
    assert "write_roots_unconfigured" in errors


def test_secure_mode_rejects_broad_and_missing_roots(clean_env, tmp_path):
    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    clean_env.setenv(workspace_policy.READ_ROOTS_ENV, "/")
    clean_env.setenv(workspace_policy.WRITE_ROOTS_ENV, str(tmp_path / "missing"))
    errors = workspace_policy.validate_security_configuration()
    assert "read_root_too_broad" in errors
    assert "write_root_not_directory" in errors


def test_secure_mode_broad_root_acknowledgement(clean_env, tmp_path):
    (tmp_path / "w").mkdir()
    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    clean_env.setenv(workspace_policy.READ_ROOTS_ENV, "/")
    clean_env.setenv(workspace_policy.WRITE_ROOTS_ENV, str(tmp_path / "w"))
    clean_env.setenv(workspace_policy.ALLOW_BROAD_ROOTS_ENV, "1")
    assert workspace_policy.validate_security_configuration() == []


def test_secure_mode_rejects_writable_evidence_roots(clean_env, tmp_path):
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    clean_env.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    clean_env.setenv(workspace_policy.WRITE_ROOTS_ENV, str(evidence))
    assert "write_root_inside_read_root" in workspace_policy.validate_security_configuration()


def test_secure_mode_read_fails_closed_without_read_roots(clean_env, tmp_path):
    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    with pytest.raises(ValueError, match="read_roots_unconfigured"):
        workspace_policy.check_read_path(tmp_path / "anything.csv")


def test_secure_mode_write_fails_closed_without_write_roots(clean_env, tmp_path):
    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    with pytest.raises(ValueError, match="write_roots_unconfigured"):
        workspace_policy.check_write_path(tmp_path / "out.jsonld")


def test_development_mode_stays_backward_compatible(clean_env, tmp_path):
    assert workspace_policy.secure_mode_active() is False
    assert workspace_policy.validate_security_configuration() == []
    # No roots configured: reads and writes remain unrestricted.
    workspace_policy.check_read_path(tmp_path / "anything.csv")
    workspace_policy.check_write_path(tmp_path / "out.jsonld")


def test_production_profiles_imply_secure_mode(clean_env):
    for profile in ("offline-investigation", "production-authoring", "production-review"):
        clean_env.setenv(workspace_policy.PROFILE_ENV, profile)
        assert workspace_policy.secure_mode_active() is True
    clean_env.setenv(workspace_policy.PROFILE_ENV, "development")
    assert workspace_policy.secure_mode_active() is False


def test_unknown_profile_fails_closed(clean_env):
    clean_env.setenv(workspace_policy.PROFILE_ENV, "yolo-mode")
    assert workspace_policy.secure_mode_active() is True
    assert workspace_policy.validate_security_configuration() == ["unknown_deployment_profile"]
    assert workspace_policy.promotion_allowed() == (False, "")


def test_promotion_authority_by_profile(clean_env):
    assert workspace_policy.promotion_allowed() == (True, "")
    clean_env.setenv(workspace_policy.PROFILE_ENV, "offline-investigation")
    assert workspace_policy.promotion_allowed() == (False, "")
    clean_env.setenv(workspace_policy.PROFILE_ENV, "production-authoring")
    assert workspace_policy.promotion_allowed() == (False, "")
    clean_env.setenv(workspace_policy.PROFILE_ENV, "production-review")
    assert workspace_policy.promotion_allowed() == (True, "reviewer_identity")


def test_security_profile_is_bounded(clean_env, tmp_path):
    evidence = tmp_path / "evidence"
    work = tmp_path / "work"
    evidence.mkdir()
    work.mkdir()
    clean_env.setenv(workspace_policy.PROFILE_ENV, "production-review")
    clean_env.setenv(workspace_policy.READ_ROOTS_ENV, str(evidence))
    clean_env.setenv(workspace_policy.WRITE_ROOTS_ENV, str(work))
    profile = workspace_policy.security_profile()
    assert profile["profile"] == "production-review"
    assert profile["secure_mode"] is True
    assert profile["read_root_count"] == 1
    assert profile["write_root_count"] == 1
    assert profile["promotion_allowed"] is True
    assert profile["promotion_requirement"] == "reviewer_identity"
    assert profile["configuration_errors"] == []
    # Bounded: no full paths anywhere in the payload.
    assert str(tmp_path) not in json.dumps(profile)


def test_secure_startup_refused_on_invalid_configuration(clean_env):
    pytest.importorskip("fastmcp")
    import server  # import first (development env), then flip to secure

    clean_env.setenv(workspace_policy.SECURE_MODE_ENV, "1")
    with pytest.raises(SystemExit):
        server.enforce_secure_startup()
