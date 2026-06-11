"""Tests for the case_validate SHACL wrapper.

All fixtures are Tier T0 public-safe synthetic data. The live conformance
tests skip cleanly when the case_validate CLI is not installed; honest-failure
paths are always exercised.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import graph_validator
from graph_validator import (
    GraphValidationReport,
    validate_graph_file,
    validator_available,
)

T0_CONFORMANT_GRAPH = {
    "@context": {
        "kb": "http://example.org/kb/",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    },
    "@graph": [
        {
            "@id": "kb:bundle-11111111-1111-4111-8111-111111111111",
            "@type": "uco-core:Bundle",
            "uco-core:description": "Tier T0 synthetic bundle for validator wrapper tests.",
            "uco-core:object": {
                "@id": "kb:observable-22222222-2222-4222-8222-222222222222"
            },
        },
        {
            "@id": "kb:observable-22222222-2222-4222-8222-222222222222",
            "@type": "uco-observable:ObservableObject",
            "uco-core:description": "Tier T0 synthetic observable object.",
        },
    ],
}


def write_graph(tmp_path: Path, payload: dict, name: str = "graph.jsonld") -> Path:
    target = tmp_path / name
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target


def test_missing_validator_fails_honestly(tmp_path, monkeypatch):
    graph = write_graph(tmp_path, T0_CONFORMANT_GRAPH)
    monkeypatch.setattr(graph_validator.shutil, "which", lambda _name: None)
    with pytest.raises(ValueError, match="validator_unavailable"):
        validate_graph_file(graph)


def test_missing_graph_file_fails_honestly(tmp_path, monkeypatch):
    monkeypatch.setattr(
        graph_validator.shutil, "which", lambda _name: "/usr/bin/case_validate"
    )
    with pytest.raises(ValueError, match="graph_missing"):
        validate_graph_file(tmp_path / "does-not-exist.jsonld")


def test_unsupported_extension_fails_honestly(tmp_path, monkeypatch):
    monkeypatch.setattr(
        graph_validator.shutil, "which", lambda _name: "/usr/bin/case_validate"
    )
    target = tmp_path / "graph.csv"
    target.write_text("not,a,graph\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported_graph_extension"):
        validate_graph_file(target)


def test_oversized_graph_fails_honestly(tmp_path, monkeypatch):
    monkeypatch.setattr(
        graph_validator.shutil, "which", lambda _name: "/usr/bin/case_validate"
    )
    monkeypatch.setattr(graph_validator, "MAX_GRAPH_BYTES", 16)
    graph = write_graph(tmp_path, T0_CONFORMANT_GRAPH)
    with pytest.raises(ValueError, match="graph_oversized"):
        validate_graph_file(graph)


def test_parse_conforms_handles_report_lines():
    assert graph_validator._parse_conforms("Validation Report\nConforms: True\n") is True
    assert graph_validator._parse_conforms("Conforms: False\n") is False
    assert graph_validator._parse_conforms("no report here") is None


@pytest.mark.skipif(
    not validator_available(), reason="case_validate CLI not installed"
)
def test_live_conformant_graph_passes(tmp_path):
    graph = write_graph(tmp_path, T0_CONFORMANT_GRAPH)
    report = validate_graph_file(graph)
    assert isinstance(report, GraphValidationReport)
    assert report.conforms is True
    assert report.violation_count == 0
    assert "conforms" in report.safe_summary.lower()


@pytest.mark.skipif(
    not validator_available(), reason="case_validate CLI not installed"
)
def test_live_nonconformant_graph_reports_violations(tmp_path):
    bad_graph = {
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
        },
        "@graph": [
            {
                "@id": "kb:file-spec025-bad-1",
                "@type": "uco-observable:File",
                # Facets must be ObservableObject facets, not a bare string:
                "uco-observable:hasChanged": "not-a-boolean",
            }
        ],
    }
    graph = write_graph(tmp_path, bad_graph, name="bad.jsonld")
    report = validate_graph_file(graph)
    assert report.conforms is False or report.violation_count > 0
    assert "not conform" in report.safe_summary or report.violation_count > 0
