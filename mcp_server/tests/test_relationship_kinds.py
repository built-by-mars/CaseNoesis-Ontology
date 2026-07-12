"""Tests for relationship-kind registry lint (CQ-40)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from relationship_kinds import lint_relationship_kinds, known_relationship_kinds


def _relationship_graph(kind: str) -> dict:
    return {
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [
            {
                "@id": "kb:rel-1",
                "@type": "uco-core:Relationship",
                "uco-core:kindOfRelationship": kind,
            }
        ],
    }


def test_known_kind_ok_no_findings():
    known = next(iter(known_relationship_kinds()))
    report = lint_relationship_kinds(_relationship_graph(known))
    assert report["ok"] is True
    assert report["findings"] == []
    assert report["checked"] == 1


def test_unknown_kind_open_vocabulary_warning():
    report = lint_relationship_kinds(
        _relationship_graph("not-in-vocab-kind"),
        allow_open_vocabulary=True,
    )
    assert report["ok"] is True
    assert len(report["findings"]) == 1
    finding = report["findings"][0]
    assert finding["severity"] == "warning"
    assert finding["kind"] == "not-in-vocab-kind"
    assert finding["node_id"] == "kb:rel-1"


def test_unknown_kind_strict_mode_error():
    report = lint_relationship_kinds(
        _relationship_graph("not-in-vocab-kind"),
        allow_open_vocabulary=False,
    )
    assert report["ok"] is False
    assert len(report["findings"]) == 1
    assert report["findings"][0]["severity"] == "error"
