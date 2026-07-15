"""Release-gating DarkWatchman: rebuild → manifest → critic → validate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DW_DIR = ROOT / "examples/cti/darkwatchman_2021"
COMMITTED = DW_DIR / "darkwatchman-prevailion.jsonld"
MANIFEST = DW_DIR / "build-manifest.json"
BUILDER = DW_DIR / "build_darkwatchman.py"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_darkwatchman", BUILDER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not COMMITTED.is_file(), reason="DarkWatchman exemplar missing")
def test_builder_output_matches_committed_graph(tmp_path):
    mod = _load_builder()
    assert hasattr(mod, "build_graph")
    out = tmp_path / "darkwatchman.jsonld"
    graph = mod.build_graph()
    graph.write_streaming(str(out), atomic=True)

    committed_sha = _sha(COMMITTED)
    built_sha = _sha(out)
    assert built_sha == committed_sha, (
        "Rebuilt DarkWatchman graph diverges from committed JSON-LD"
    )

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifacts = payload.get("artifacts") or []
    by_role = {
        str(a.get("role")): a for a in artifacts if isinstance(a, dict) and a.get("role")
    }
    output = by_role.get("output_artifact") or payload.get("output") or {}
    assert str(output.get("sha256", "")).lower() == committed_sha.lower()
    assert _sha(MANIFEST)  # sidecar present for critic binding


@pytest.mark.skipif(
    not __import__("case_uco.validation", fromlist=["validator_available"]).validator_available(),
    reason="case_validate not installed",
)
def test_darkwatchman_validate_complete():
    from case_uco.validation import validate_graph_file

    report = validate_graph_file(
        COMMITTED,
        extensions=["attack-technique:full"],
        project_root=ROOT,
    )
    assert report.conforms is True
    assert report.verification_status == "complete"


@pytest.mark.skipif(not MANIFEST.is_file(), reason="build-manifest missing")
def test_darkwatchman_critic_casegraph_raw_with_manifest(tmp_path, monkeypatch):
    mcp = ROOT / "mcp_server"
    if str(mcp) not in sys.path:
        sys.path.insert(0, str(mcp))
    if str(ROOT / "python") not in sys.path:
        sys.path.insert(0, str(ROOT / "python"))

    import workspace_policy  # noqa: F401
    from critic.deterministic import analyze_artifact
    from critic.models import CriticArtifactRequest

    read = tmp_path / "read"
    write = tmp_path / "write"
    read.mkdir()
    write.mkdir()
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", f"{read}:{ROOT}")
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(write))
    monkeypatch.setenv("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")

    review = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(COMMITTED),
            serializer_path=str(BUILDER),
            provenance_manifest_path=str(MANIFEST),
            extensions=["attack-technique:full"],
            project_root=str(ROOT),
            critic_scope="both",
            serializer_mode="casegraph_raw",
            # Critic-only token for heuristic policy (filtered from SHACL profiles).
            profiles=["cti-report"],
            force_rdfs_inference=True,
        )
    )
    open_high = [
        f
        for f in review.merged_findings
        if f.status != "resolved" and f.severity in {"critical", "high"}
    ]
    assert open_high == [], [f.rule_id for f in open_high]
    missing = [
        f
        for f in review.merged_findings
        if f.rule_id == "CRIT-H-DERIVED-NO-HASH" and f.severity == "medium"
    ]
    assert len(missing) == 1
    assert review.artifact_hashes.provenance_manifest_sha256 == _sha(MANIFEST)
    if review.validation.conforms is not None:
        assert review.validation.conforms is True
        assert review.validation.verification_status == "complete"
