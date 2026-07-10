"""Tests for the staged promotion lifecycle of learned artifacts (issue #52).

All fixtures are Tier T0 public-safe synthetic data.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import investigation_router
import knowledge_lifecycle

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

VALID_TTL = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix candext: <http://example.org/ontology/candext/> .

candext:CandidateThing
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "CandidateThing"@en ;
    rdfs:comment "Synthetic candidate class for lifecycle tests."@en .
"""

ORPHAN_TTL = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix candext: <http://example.org/ontology/candext/> .

candext:OrphanThing
    a owl:Class ;
    rdfs:label "OrphanThing"@en .
"""

BROKEN_TTL = "@prefix broken this is not turtle at all {{{"


def make_extension(root: Path, name: str, ttl: str, status: str = "candidate") -> Path:
    ext_dir = root / "extensions" / name
    ext_dir.mkdir(parents=True)
    (ext_dir / f"{name}.ttl").write_text(ttl, encoding="utf-8")
    manifest = {
        "name": name,
        "display_name": f"Test {name}",
        "version": "0.0.1",
        "status": status,
        "owl_files": [f"{name}.ttl"],
        "shacl_files": [],
        "bridge_files": [],
    }
    (ext_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return ext_dir


def test_status_defaults_to_operational_for_bundled_manifests():
    assert knowledge_lifecycle.extension_status({}) == "operational"
    assert knowledge_lifecycle.is_routable({}) is True
    assert knowledge_lifecycle.is_routable({"status": "candidate"}) is False
    assert knowledge_lifecycle.is_routable({"status": "deprecated"}) is False


def test_candidate_extension_invisible_to_routing(tmp_path):
    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    make_extension(tmp_path, "opext", VALID_TTL, status="operational")
    installed = investigation_router._installed_extensions(tmp_path)
    assert "opext" in installed
    assert "candext" not in installed


def test_deprecated_extension_invisible_to_routing(tmp_path):
    make_extension(tmp_path, "oldext", VALID_TTL, status="deprecated")
    installed = investigation_router._installed_extensions(tmp_path)
    assert "oldext" not in installed


def test_candidate_extension_still_loadable_explicitly(tmp_path):
    """The authoring investigation can keep using a candidate by name."""

    import concept_coverage

    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    core_dir = tmp_path / "ontology/UCO/ontology/uco/core"
    core_dir.mkdir(parents=True)
    (core_dir / "core.ttl").write_text(
        """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
uco-core:UcoObject a owl:Class .
""",
        encoding="utf-8",
    )
    graph_path = tmp_path / "g.jsonld"
    graph_path.write_text(
        json.dumps({
            "@context": {"kb": "http://example.org/kb/"},
            "@graph": [{
                "@id": "kb:t-11111111-1111-4111-8111-111111111111",
                "@type": "http://example.org/ontology/candext/CandidateThing",
            }],
        }),
        encoding="utf-8",
    )
    report = concept_coverage.check_graph_concepts(
        graph_path, project_root=tmp_path, extensions=["candext"]
    )
    assert report.ok is True, report.undeclared_classes


def test_promotion_success_records_provenance(tmp_path):
    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "candext", project_root=tmp_path, reviewed_by="Synthetic Reviewer",
        require_validator=False,
    )
    assert result.ok is True, result.gates
    assert result.status == "operational"

    manifest = json.loads(
        (tmp_path / "extensions/candext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "operational"
    promo = manifest["promotion"]
    assert promo["reviewed_by"] == "Synthetic Reviewer"
    assert promo["previous_status"] == "candidate"
    assert promo["promoted_at"]
    assert all(g["ok"] for g in promo["gates"])

    # After promotion the extension is routable.
    installed = investigation_router._installed_extensions(tmp_path)
    assert "candext" in installed


def test_promotion_fails_on_unparseable_ontology(tmp_path):
    make_extension(tmp_path, "brokenext", BROKEN_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "brokenext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error.startswith("promotion_gate_failed:ontology_files_parse")
    manifest = json.loads(
        (tmp_path / "extensions/brokenext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "candidate", "failed promotion must not change status"
    assert "promotion" not in manifest


def test_promotion_fails_on_orphan_class(tmp_path):
    make_extension(tmp_path, "orphanext", ORPHAN_TTL, status="candidate")
    result = knowledge_lifecycle.promote_extension(
        "orphanext", project_root=tmp_path, require_validator=False
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:classes_anchored"


def test_promotion_fails_on_missing_exemplar(tmp_path):
    ext_dir = make_extension(tmp_path, "exemext", VALID_TTL, status="candidate")
    manifest = json.loads((ext_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest["exemplar_files"] = ["missing-exemplar.ttl"]
    (ext_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    import graph_validator

    if not graph_validator.validator_available():
        pytest.skip("case_validate CLI not installed")
    result = knowledge_lifecycle.promote_extension(
        "exemext", project_root=tmp_path, require_validator=True
    )
    assert result.ok is False
    assert result.error == "promotion_gate_failed:exemplars_validate"


def test_deprecation_records_reason_and_revokes_routing(tmp_path):
    make_extension(tmp_path, "badext", VALID_TTL, status="operational")
    assert "badext" in investigation_router._installed_extensions(tmp_path)

    result = knowledge_lifecycle.deprecate_extension(
        "badext", reason="synthetic modeling error", project_root=tmp_path,
        deprecated_by="Synthetic Reviewer",
    )
    assert result["status"] == "deprecated"
    manifest = json.loads(
        (tmp_path / "extensions/badext/manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["deprecation"]["reason"] == "synthetic modeling error"
    assert "badext" not in investigation_router._installed_extensions(tmp_path)


def test_bundled_extensions_remain_operational():
    """The nine bundled extensions (no status field) stay routable."""

    installed = investigation_router._installed_extensions(PROJECT_ROOT)
    for name in ("legalproc", "rico", "cryptoinv"):
        if (PROJECT_ROOT / "extensions" / name / "manifest.json").is_file():
            assert name in installed


def test_candidate_recipe_directory_is_outside_catalog():
    candidates = PROJECT_ROOT / "docs/recipes/candidates"
    assert candidates.is_dir()
    sys.path.insert(0, str(PROJECT_ROOT / "mcp_server"))
    from domain_index import RECIPE_INDEX

    for entry in RECIPE_INDEX:
        assert "candidates/" not in entry["file"], entry["file"]


def test_cli_status_and_promote(tmp_path, capsys):
    make_extension(tmp_path, "candext", VALID_TTL, status="candidate")
    rc = knowledge_lifecycle.main(
        ["status", "--project-root", str(tmp_path)]
    )
    assert rc == 0
    assert "candext: candidate" in capsys.readouterr().out
