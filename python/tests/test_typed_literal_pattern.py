"""Custom RDF datatype serialization for pattern:PatternExpression."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from case_uco import CASEGraph, TypedLiteral
from case_uco.uco.pattern import LogicalPattern

ROOT = Path(__file__).resolve().parents[2]
PATTERN_DT = (
    "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression"
)


def test_logical_pattern_emits_pattern_expression_datatype():
    graph = CASEGraph()
    expr = "process.name = 'wscript.exe'"
    graph.create(
        LogicalPattern,
        id="kb:lp-1",
        pattern_expression=TypedLiteral(expr, PATTERN_DT),
    )
    doc = json.loads(graph.serialize())
    node = next(n for n in doc["@graph"] if n["@id"] == "kb:lp-1")
    pe = node["uco-pattern:patternExpression"]
    assert isinstance(pe, dict)
    assert pe["@value"] == expr
    assert "PatternExpression" in pe["@type"]


def test_logical_pattern_string_uses_range_iri_datatype():
    graph = CASEGraph()
    graph.create(
        LogicalPattern,
        id="kb:lp-2",
        pattern_expression="file.name = 'invoice.exe'",
    )
    doc = json.loads(graph.serialize())
    node = next(n for n in doc["@graph"] if n["@id"] == "kb:lp-2")
    pe = node["uco-pattern:patternExpression"]
    assert pe["@value"] == "file.name = 'invoice.exe'"
    assert pe["@type"] in {
        "uco-pattern:PatternExpression",
        PATTERN_DT,
    }


@pytest.mark.skipif(
    __import__("case_uco.validation", fromlist=["validator_available"]).validator_available()
    is False,
    reason="case_validate not installed",
)
def test_logical_pattern_validates_against_uco(tmp_path):
    from case_uco.validation import validate_graph_file

    graph = CASEGraph()
    graph.create(
        LogicalPattern,
        id="kb:lp-3",
        pattern_expression=TypedLiteral(
            "registry.key = 'HKCU\\\\Software'",
            PATTERN_DT,
        ),
    )
    out = tmp_path / "pattern.jsonld"
    graph.write_streaming(str(out), atomic=True)
    report = validate_graph_file(out, project_root=ROOT)
    assert report.conforms is True
    assert report.verification_status == "complete"
