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
        PROJECT_ROOT / "extensions/cac/ontology/ontology/cacontology-core.ttl"
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
