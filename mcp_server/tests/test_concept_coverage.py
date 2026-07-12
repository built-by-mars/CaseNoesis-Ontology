"""Tests for closed-world concept coverage checking.

All fixtures are Tier T0 public-safe synthetic data. The checker itself is
pure rdflib and runs without the case_validate CLI; integration tests through
validate_graph_file skip when the CLI is unavailable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import concept_coverage
import graph_validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

CONTEXT = {
    "kb": "http://example.org/kb/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
}


def write_graph(tmp_path: Path, graph_nodes: list[dict], name: str = "graph.jsonld") -> Path:
    target = tmp_path / name
    target.write_text(
        json.dumps({"@context": CONTEXT, "@graph": graph_nodes}, indent=2),
        encoding="utf-8",
    )
    return target


def _core_ontologies_available() -> bool:
    return bool(concept_coverage._core_ontology_paths(PROJECT_ROOT))


def _cac_available() -> bool:
    return (
        PROJECT_ROOT / "ontology/cac/ontology/ontology/cacontology-core.ttl"
    ).is_file()


pytestmark = pytest.mark.skipif(
    not _core_ontologies_available(), reason="core ontology submodules not present"
)


def test_declared_core_terms_pass(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:observable-11111111-1111-4111-8111-111111111111",
                "@type": "uco-observable:ObservableObject",
                "uco-core:description": "Tier T0 synthetic observable.",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is True
    assert report.undeclared_total == 0
    assert report.checked_class_count == 1


def test_invented_term_fails_with_change_proposal_guidance(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:thing-22222222-2222-4222-8222-222222222222",
                "@type": "uco-core:InventedNonexistentClass",
                "uco-core:completelyMadeUpProperty": "value",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is False
    assert any("InventedNonexistentClass" in iri for iri in report.undeclared_classes)
    assert any(
        "completelyMadeUpProperty" in iri for iri in report.undeclared_properties
    )
    assert "change proposal" in report.guidance
    assert "extension ontology" in report.guidance


@pytest.mark.skipif(not _cac_available(), reason="CAC extension not present")
def test_undeclared_cac_term_fails_without_extension_loaded(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:charge-33333333-3333-4333-8333-333333333333",
                "@type": "uco-core:UcoObject",
                "cacontology-legal-outcomes:chargedWith": {
                    "@id": "kb:charge-44444444-4444-4444-8444-444444444444"
                },
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(
        graph, project_root=PROJECT_ROOT, extensions=None
    )
    assert report.ok is False
    assert any("chargedWith" in iri for iri in report.undeclared_properties)


@pytest.mark.skipif(not _cac_available(), reason="CAC extension not present")
def test_pending_extension_declares_proposed_terms(tmp_path):
    """Terms backed by filed change proposals are declared via the local
    pending extension file, so graphs using them pass with extensions=['cac']."""
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:investigation-55555555-5555-4555-8555-555555555555",
                "@type": "uco-core:UcoObject",
                "cacontology:caseNumber": "3:20-cr-00029-SLG-MMS",
                "cacontology:jurisdiction": "District of Alaska",
                "cacontology-legal-outcomes:chargedWith": {
                    "@id": "kb:charge-66666666-6666-4666-8666-666666666666"
                },
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(
        graph, project_root=PROJECT_ROOT, extensions=["cac"]
    )
    assert report.ok is True, report.undeclared_properties


def _cryptoinv_available() -> bool:
    return (PROJECT_ROOT / "extensions/cryptoinv/cryptoinv.ttl").is_file()


@pytest.mark.skipif(not _cryptoinv_available(), reason="cryptoinv extension not present")
def test_cryptoinv_extension_declares_crypto_terms(tmp_path):
    """Cryptocurrency facets pass with extensions=['cryptoinv'] and fail without."""
    nodes = [
        {
            "@id": "kb:addr-aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "@type": "uco-observable:ObservableObject",
            "uco-core:hasFacet": {
                "@id": "kb:addr-facet-aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                "@type": "http://example.org/ontology/cryptoinv/CryptocurrencyAddressFacet",
                "http://example.org/ontology/cryptoinv/addressValue": "bc1qsynthetic",
            },
        }
    ]
    graph = write_graph(tmp_path, nodes)
    without = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert without.ok is False
    assert any("CryptocurrencyAddressFacet" in iri for iri in without.undeclared_classes)
    with_ext = concept_coverage.check_graph_concepts(
        graph, project_root=PROJECT_ROOT, extensions=["cryptoinv"]
    )
    assert with_ext.ok is True, (with_ext.undeclared_classes, with_ext.undeclared_properties)


def test_standard_namespaces_are_never_flagged(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:thing-77777777-7777-4777-8777-777777777777",
                "@type": "uco-core:UcoObject",
                "http://www.w3.org/2000/01/rdf-schema#label": "labelled",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is True


def test_uco_profile_namespaces_are_never_flagged(tmp_path):
    """Terms from upper/external ontologies with UCO profiles (CDO-Shapes-*,
    https://github.com/Cyber-Domain-Ontology) are usable without an extension:
    PROV-O, OWL-Time, GeoSPARQL/Simple Features, FOAF, ORG, BFO, gUFO."""
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:action-aaaabbbb-1111-4111-8111-111111111111",
                "@type": "uco-core:UcoObject",
                "http://www.w3.org/ns/prov#used": {
                    "@id": "kb:entity-aaaabbbb-2222-4222-8222-222222222222"
                },
                "http://xmlns.com/foaf/0.1/knows": {
                    "@id": "kb:person-aaaabbbb-3333-4333-8333-333333333333"
                },
                "http://www.w3.org/2006/time#hasBeginning": {
                    "@id": "kb:instant-aaaabbbb-4444-4444-8444-444444444444"
                },
            },
            {
                "@id": "kb:geometry-aaaabbbb-5555-4555-8555-555555555555",
                "@type": "http://www.opengis.net/ont/sf#Point",
                "http://www.opengis.net/ont/geosparql#asWKT": "POINT(-149.9 61.2)",
            },
            {
                "@id": "kb:org-aaaabbbb-6666-4666-8666-666666666666",
                "@type": "http://www.w3.org/ns/org#Organization",
            },
            {
                "@id": "kb:continuant-aaaabbbb-7777-4777-8777-777777777777",
                "@type": "http://purl.obolibrary.org/obo/BFO_0000002",
            },
            {
                "@id": "kb:relator-aaaabbbb-8888-4888-8888-888888888888",
                "@type": "http://purl.org/nemo/gufo#Relator",
            },
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is True, (report.undeclared_classes, report.undeclared_properties)


@pytest.mark.skipif(
    not graph_validator.validator_available(), reason="case_validate CLI not installed"
)
def test_validate_graph_file_rejects_undeclared_concepts(tmp_path):
    # case_validate itself flags fabricated CDO-namespace terms; the concept
    # coverage check exists for terms in namespaces case_validate ignores.
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:bundle-88888888-8888-4888-8888-888888888888",
                "@type": "uco-core:Bundle",
                "uco-core:description": "Tier T0 synthetic bundle.",
                "http://example.org/madeup#madeUpBundleProperty": "not declared anywhere",
            }
        ],
    )
    report = graph_validator.validate_graph_file(graph, project_root=PROJECT_ROOT)
    assert report.conforms is False
    assert any("madeUpBundleProperty" in iri for iri in report.undeclared_concepts)
    assert "change proposal" in report.concept_guidance
    payload = graph_validator.report_to_dict(report)
    assert payload["undeclared_concepts"]
    assert "concept_guidance" in payload


# ---------------------------------------------------------------------------
# Exact-term validation for profiled upper ontologies (issue #47)
# ---------------------------------------------------------------------------

UPPER_REGISTRY_AVAILABLE = concept_coverage.UPPER_ONTOLOGY_REGISTRY_PATH.is_file()


@pytest.mark.skipif(not UPPER_REGISTRY_AVAILABLE, reason="upper ontology registry missing")
def test_upper_registry_has_pinned_provenance():
    registry = json.loads(
        concept_coverage.UPPER_ONTOLOGY_REGISTRY_PATH.read_text(encoding="utf-8")
    )
    assert registry["ontologies"], "registry must not be empty"
    for key, entry in registry["ontologies"].items():
        assert entry["source_url"], key
        assert entry["namespace_prefixes"], key
        assert entry["classes"] or entry["properties"], key


@pytest.mark.skipif(not UPPER_REGISTRY_AVAILABLE, reason="upper ontology registry missing")
@pytest.mark.parametrize(
    "iri,position",
    [
        ("http://www.w3.org/ns/prov#used", "property"),
        ("http://www.w3.org/2006/time#hasBeginning", "property"),
        ("http://www.opengis.net/ont/geosparql#asWKT", "property"),
        ("http://xmlns.com/foaf/0.1/knows", "property"),
        ("http://www.w3.org/ns/org#Organization", "class"),
        ("http://www.opengis.net/ont/sf#Point", "class"),
        ("http://purl.obolibrary.org/obo/BFO_0000002", "class"),
        ("http://purl.org/nemo/gufo#Relator", "class"),
        ("http://www.w3.org/ns/dx/prof/Profile", "class"),
    ],
)
def test_known_upper_ontology_terms_pass(tmp_path, iri, position):
    if position == "class":
        node = {"@id": "kb:u-11111111-1111-4111-8111-111111111111", "@type": iri}
    else:
        node = {
            "@id": "kb:u-11111111-1111-4111-8111-111111111111",
            "@type": "uco-core:UcoObject",
            iri: {"@id": "kb:u-22222222-2222-4222-8222-222222222222"},
        }
    graph = write_graph(tmp_path, [node])
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is True, (
        report.unknown_upper_ontology_terms,
        report.role_mismatches,
    )


@pytest.mark.skipif(not UPPER_REGISTRY_AVAILABLE, reason="upper ontology registry missing")
@pytest.mark.parametrize(
    "iri,position",
    [
        ("http://www.w3.org/ns/prov#CompletelyImaginaryClass", "class"),
        ("http://www.w3.org/ns/prov#completelyImaginaryProperty", "property"),
        ("http://www.w3.org/2006/time#InventedInstant", "class"),
        ("http://www.w3.org/2006/time#hasInventedEnding", "property"),
        ("http://www.opengis.net/ont/geosparql#FabricatedGeometry", "class"),
        ("http://www.opengis.net/ont/geosparql#asFabricatedText", "property"),
        ("http://xmlns.com/foaf/0.1/InventedAgent", "class"),
        ("http://xmlns.com/foaf/0.1/inventedKnows", "property"),
        ("http://www.w3.org/ns/org#InventedUnit", "class"),
        ("http://www.w3.org/ns/org#inventedMemberOf", "property"),
        ("http://purl.obolibrary.org/obo/BFO_9999999", "class"),
        ("http://purl.org/nemo/gufo#InventedRelator", "class"),
        ("http://purl.org/nemo/gufo#inventedMediates", "property"),
        ("http://www.w3.org/ns/dx/prof/InventedProfile", "class"),
        ("http://www.w3.org/ns/dx/prof/inventedIsProfileOf", "property"),
    ],
)
def test_fabricated_upper_ontology_terms_fail(tmp_path, iri, position):
    if position == "class":
        node = {"@id": "kb:f-11111111-1111-4111-8111-111111111111", "@type": iri}
    else:
        node = {
            "@id": "kb:f-11111111-1111-4111-8111-111111111111",
            "@type": "uco-core:UcoObject",
            iri: "value",
        }
    graph = write_graph(tmp_path, [node])
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is False
    assert iri in report.unknown_upper_ontology_terms
    # Unknown upper-ontology terms are reported distinctly from unknown
    # CASE/UCO or extension terms.
    assert iri not in report.undeclared_classes
    assert iri not in report.undeclared_properties
    assert "upper-ontology" in report.guidance


# ---------------------------------------------------------------------------
# RDF role awareness (issue #48)
# ---------------------------------------------------------------------------


def test_declared_class_used_as_predicate_is_role_mismatch(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:r-11111111-1111-4111-8111-111111111111",
                "@type": "uco-core:UcoObject",
                "uco-core:Relationship": "class in predicate position",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is False
    mismatched = {iri for iri, _, _ in report.role_mismatches}
    assert any("Relationship" in iri for iri in mismatched)
    # Reported as a role mismatch, not as an undeclared term.
    assert not any("Relationship" in iri for iri in report.undeclared_properties)
    assert "wrong RDF position" in report.guidance


def test_declared_property_used_as_class_is_role_mismatch(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:r-22222222-2222-4222-8222-222222222222",
                "@type": "uco-core:description",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is False
    mismatched = {iri for iri, _, _ in report.role_mismatches}
    assert any("description" in iri for iri in mismatched)
    assert not any("description" in iri for iri in report.undeclared_classes)


@pytest.mark.skipif(not UPPER_REGISTRY_AVAILABLE, reason="upper ontology registry missing")
def test_upper_ontology_class_used_as_predicate_is_role_mismatch(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:r-33333333-3333-4333-8333-333333333333",
                "@type": "uco-core:UcoObject",
                "http://www.w3.org/ns/prov#Activity": "class in predicate position",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    assert report.ok is False
    assert (
        "http://www.w3.org/ns/prov#Activity",
        "upper-ontology class",
        "property (predicate)",
    ) in report.role_mismatches


def _attack_technique_available() -> bool:
    return (
        PROJECT_ROOT / "extensions/attack-technique/mitre-attack-catalog.ttl"
    ).is_file()


@pytest.mark.skipif(
    not _attack_technique_available(), reason="attack-technique extension not present"
)
def test_attack_technique_punning_accepted_as_class(tmp_path):
    """ATT&CK techniques are punned (owl:Class + instance of the
    uco-action:Technique metaclass, per UCO PR #676); typing a concrete
    action with the technique class must pass role-aware coverage."""
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:action-44444444-4444-4444-8444-444444444444",
                "@type": "https://attack.mitre.org/techniques/T1112",
                "uco-core:description": "Registry modification observed.",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(
        graph, project_root=PROJECT_ROOT, extensions=["attack-technique"]
    )
    assert report.ok is True, (
        report.undeclared_classes,
        report.role_mismatches,
    )


def test_coverage_report_dict_distinguishes_categories(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:r-55555555-5555-4555-8555-555555555555",
                "@type": "uco-core:description",
                "http://www.w3.org/ns/prov#fabricatedTerm": "x",
                "uco-core:inventedProperty": "y",
            }
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    payload = concept_coverage.coverage_report_to_dict(report)
    assert payload["ok"] is False
    if UPPER_REGISTRY_AVAILABLE:
        assert payload["unknown_upper_ontology_terms"] == [
            "http://www.w3.org/ns/prov#fabricatedTerm"
        ]
    assert payload["role_mismatches"][0]["declared_role"] == "property"
    assert any("inventedProperty" in iri for iri in payload["undeclared_properties"])


# ---------------------------------------------------------------------------
# Declaration cache invalidation (issue #49)
# ---------------------------------------------------------------------------


def _write_extension(ext_dir: Path, ttl_body: str) -> None:
    ext_dir.mkdir(parents=True, exist_ok=True)
    (ext_dir / "testext.ttl").write_text(ttl_body, encoding="utf-8")
    (ext_dir / "manifest.json").write_text(
        json.dumps(
            {
                "name": "testext",
                "display_name": "Cache Test Extension",
                "version": "0.0.1",
                "owl_files": ["testext.ttl"],
                "shacl_files": [],
                "bridge_files": [],
            }
        ),
        encoding="utf-8",
    )


TESTEXT_TTL_V1 = """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix testext: <http://example.org/ontology/testext/> .

testext:FirstClass
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "FirstClass"@en .
"""

TESTEXT_TTL_V2 = TESTEXT_TTL_V1 + """
testext:SecondClass
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "SecondClass"@en .
"""


def test_cache_refreshes_after_extension_ontology_change(tmp_path):
    """A term added to an extension during the same process is recognized
    on the next check, without restarting the MCP server (issue #49)."""

    project_root = tmp_path / "project"
    # Provide a minimal core ontology so declared terms are non-empty.
    core_dir = project_root / "ontology/UCO/ontology/uco/core"
    core_dir.mkdir(parents=True)
    (core_dir / "core.ttl").write_text(
        """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
uco-core:UcoObject a owl:Class .
""",
        encoding="utf-8",
    )
    ext_dir = project_root / "extensions/testext"
    _write_extension(ext_dir, TESTEXT_TTL_V1)

    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:c-11111111-1111-4111-8111-111111111111",
                "@type": "http://example.org/ontology/testext/SecondClass",
            }
        ],
    )

    before = concept_coverage.check_graph_concepts(
        graph, project_root=project_root, extensions=["testext"]
    )
    assert before.ok is False

    # Simulate the self-improvement workflow: declare the term mid-process.
    ttl_path = ext_dir / "testext.ttl"
    ttl_path.write_text(TESTEXT_TTL_V2, encoding="utf-8")
    # Guarantee an mtime change even on coarse-resolution filesystems.
    import os

    stat = ttl_path.stat()
    os.utime(ttl_path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000))

    after = concept_coverage.check_graph_concepts(
        graph, project_root=project_root, extensions=["testext"]
    )
    assert after.ok is True, (after.undeclared_classes, after.role_mismatches)


def test_cache_invalidates_when_term_removed(tmp_path):
    project_root = tmp_path / "project"
    core_dir = project_root / "ontology/UCO/ontology/uco/core"
    core_dir.mkdir(parents=True)
    (core_dir / "core.ttl").write_text(
        """\
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
uco-core:UcoObject a owl:Class .
""",
        encoding="utf-8",
    )
    ext_dir = project_root / "extensions/testext"
    _write_extension(ext_dir, TESTEXT_TTL_V2)

    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:c-22222222-2222-4222-8222-222222222222",
                "@type": "http://example.org/ontology/testext/SecondClass",
            }
        ],
    )
    before = concept_coverage.check_graph_concepts(
        graph, project_root=project_root, extensions=["testext"]
    )
    assert before.ok is True

    ttl_path = ext_dir / "testext.ttl"
    ttl_path.write_text(TESTEXT_TTL_V1, encoding="utf-8")
    import os

    stat = ttl_path.stat()
    os.utime(ttl_path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000))

    after = concept_coverage.check_graph_concepts(
        graph, project_root=project_root, extensions=["testext"]
    )
    assert after.ok is False


def test_clear_declared_term_cache():
    concept_coverage.load_declared_terms(project_root=PROJECT_ROOT)
    assert concept_coverage._DECLARED_CACHE
    concept_coverage.clear_declared_term_cache()
    assert not concept_coverage._DECLARED_CACHE


@pytest.mark.skipif(
    not graph_validator.validator_available(), reason="case_validate CLI not installed"
)
def test_validate_graph_file_strict_concepts_can_be_disabled(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:bundle-99999999-9999-4999-8999-999999999999",
                "@type": "uco-core:Bundle",
                "uco-core:description": "Tier T0 synthetic bundle.",
                "uco-core:madeUpBundleProperty": "not declared anywhere",
            }
        ],
    )
    report = graph_validator.validate_graph_file(
        graph, project_root=PROJECT_ROOT, strict_concepts=False
    )
    assert report.undeclared_concepts == ()


# ---------------------------------------------------------------------------
# Fail-closed verification (issue #55)
# ---------------------------------------------------------------------------


def _upper_term_graph(tmp_path):
    return write_graph(
        tmp_path,
        [
            {
                "@id": "kb:relator-aaaabbbb-8888-4888-8888-888888888888",
                "@type": "http://purl.org/nemo/gufo#Relator",
            },
        ],
    )


def test_missing_registry_fails_closed_for_upper_terms(tmp_path, monkeypatch):
    graph = _upper_term_graph(tmp_path)
    monkeypatch.setattr(
        concept_coverage,
        "UPPER_ONTOLOGY_REGISTRY_PATH",
        tmp_path / "no-such-registry.json",
    )
    concept_coverage.clear_declared_term_cache()
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    concept_coverage.clear_declared_term_cache()
    assert report.ok is False
    assert report.verification_status == "could_not_verify"
    assert "upper_ontology_registry_missing" in report.verification_errors
    assert "never reported as conformant" in report.guidance


def test_corrupt_registry_fails_closed_for_upper_terms(tmp_path, monkeypatch):
    graph = _upper_term_graph(tmp_path)
    bad_registry = tmp_path / "registry.json"
    bad_registry.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(
        concept_coverage, "UPPER_ONTOLOGY_REGISTRY_PATH", bad_registry
    )
    concept_coverage.clear_declared_term_cache()
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    concept_coverage.clear_declared_term_cache()
    assert report.ok is False
    assert report.verification_status == "could_not_verify"
    assert "upper_ontology_registry_malformed" in report.verification_errors


def test_provenance_invalid_registry_fails_closed(tmp_path, monkeypatch):
    graph = _upper_term_graph(tmp_path)
    bad_registry = tmp_path / "registry.json"
    bad_registry.write_text(
        json.dumps({
            "ontologies": {
                "gufo": {
                    "classes": ["http://purl.org/nemo/gufo#Relator"],
                    "properties": [], "individuals": [], "datatypes": [],
                }
            }
        }),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        concept_coverage, "UPPER_ONTOLOGY_REGISTRY_PATH", bad_registry
    )
    concept_coverage.clear_declared_term_cache()
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    concept_coverage.clear_declared_term_cache()
    assert report.ok is False
    assert "upper_ontology_registry_provenance_invalid" in report.verification_errors


def test_missing_registry_irrelevant_without_upper_terms(tmp_path, monkeypatch):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:obj-11111111-1111-4111-8111-111111111111",
                "@type": "uco-core:UcoObject",
            },
        ],
    )
    monkeypatch.setattr(
        concept_coverage,
        "UPPER_ONTOLOGY_REGISTRY_PATH",
        tmp_path / "no-such-registry.json",
    )
    concept_coverage.clear_declared_term_cache()
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    concept_coverage.clear_declared_term_cache()
    assert report.ok is True
    assert report.verification_status == "complete"


def test_coverage_report_dict_includes_verification_status(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:obj-11111111-1111-4111-8111-111111111111",
                "@type": "uco-core:UcoObject",
            },
        ],
    )
    report = concept_coverage.check_graph_concepts(graph, project_root=PROJECT_ROOT)
    payload = concept_coverage.coverage_report_to_dict(report)
    assert payload["verification_status"] == "complete"


def test_selected_profiles_reject_unselected_upper_terms(tmp_path):
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:activity-1",
                "@type": "http://www.w3.org/ns/prov#Activity",
            },
            {
                "@id": "kb:geom-1",
                "@type": "http://www.opengis.net/ont/geosparql#Geometry",
            },
        ],
    )
    only_geo = concept_coverage.check_graph_concepts(
        graph, project_root=PROJECT_ROOT, selected_profiles=["geosparql"]
    )
    assert only_geo.ok is False
    assert any("profile_not_selected:prov-o" in t for t in only_geo.undeclared_classes)

    both = concept_coverage.check_graph_concepts(
        graph,
        project_root=PROJECT_ROOT,
        selected_profiles=["geosparql", "prov-o"],
    )
    assert both.ok is True
    assert both.undeclared_classes == ()


def test_org_selected_profiles_include_dependency_namespaces(tmp_path):
    # Coverage itself does not expand depends_on; callers must pass the
    # resolved bundle profile list (org → foaf, prov-o).
    graph = write_graph(
        tmp_path,
        [
            {
                "@id": "kb:person-1",
                "@type": "http://xmlns.com/foaf/0.1/Person",
            },
            {
                "@id": "kb:org-1",
                "@type": "http://www.w3.org/ns/org#Organization",
            },
        ],
    )
    org_only = concept_coverage.check_graph_concepts(
        graph, project_root=PROJECT_ROOT, selected_profiles=["org"]
    )
    assert org_only.ok is False
    assert any("profile_not_selected:foaf" in t for t in org_only.undeclared_classes)

    with_deps = concept_coverage.check_graph_concepts(
        graph,
        project_root=PROJECT_ROOT,
        selected_profiles=["org", "foaf", "prov-o"],
    )
    assert with_deps.ok is True


# ---------------------------------------------------------------------------
# Typed extension dependency failures (issue #55)
# ---------------------------------------------------------------------------


def _make_ext(root: Path, name: str, depends_on=None, manifest_text=None):
    ext_dir = root / "extensions" / name
    ext_dir.mkdir(parents=True)
    if manifest_text is not None:
        (ext_dir / "manifest.json").write_text(manifest_text, encoding="utf-8")
        return
    manifest = {"name": name, "version": "0.0.1", "owl_files": []}
    if depends_on:
        manifest["depends_on"] = depends_on
    (ext_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def test_unknown_extension_is_typed_error(tmp_path):
    with pytest.raises(ValueError, match="extension_unknown"):
        graph_validator.resolve_extension_dependencies(["nope"], tmp_path)


def test_missing_dependency_is_typed_error(tmp_path):
    _make_ext(tmp_path, "a", depends_on=["ghost"])
    with pytest.raises(ValueError, match="extension_dependency_missing"):
        graph_validator.resolve_extension_dependencies(["a"], tmp_path)


def test_cyclic_dependency_is_typed_error(tmp_path):
    _make_ext(tmp_path, "a", depends_on=["b"])
    _make_ext(tmp_path, "b", depends_on=["a"])
    with pytest.raises(ValueError, match="extension_dependency_cycle"):
        graph_validator.resolve_extension_dependencies(["a"], tmp_path)


def test_malformed_manifest_is_typed_error(tmp_path):
    _make_ext(tmp_path, "bad", manifest_text="{not json")
    with pytest.raises(ValueError, match="extension_manifest_malformed"):
        graph_validator.resolve_extension_dependencies(["bad"], tmp_path)


def test_diamond_dependency_resolves_once(tmp_path):
    _make_ext(tmp_path, "d")
    _make_ext(tmp_path, "b", depends_on=["d"])
    _make_ext(tmp_path, "c", depends_on=["d"])
    _make_ext(tmp_path, "a", depends_on=["b", "c"])
    resolved = graph_validator.resolve_extension_dependencies(["a"], tmp_path)
    assert resolved == ["a", "b", "c", "d"]
