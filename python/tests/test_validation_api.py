"""Public case_uco.validation API smoke tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from case_uco.validation import (
    GraphValidationReport,
    validate_graph_file,
    validator_available,
)

ROOT = Path(__file__).resolve().parents[2]
DW_GRAPH = ROOT / "examples/cti/darkwatchman_2021/darkwatchman-prevailion.jsonld"


@pytest.mark.skipif(not validator_available(), reason="case_validate not installed")
def test_validate_graph_file_darkwatchman():
    report = validate_graph_file(
        DW_GRAPH,
        extensions=["attack-technique:full"],
        project_root=ROOT,
    )
    assert isinstance(report, GraphValidationReport)
    assert report.conforms is True
    assert report.verification_status == "complete"


@pytest.mark.skipif(not validator_available(), reason="case_validate not installed")
def test_casegraph_validate_report_roundtrip(tmp_path):
    from case_uco import CASEGraph
    from case_uco.uco.identity import Organization

    graph = CASEGraph()
    graph.create(Organization, id="kb:org-1", name="Synthetic Org")
    out = tmp_path / "org.jsonld"
    graph.write_streaming(str(out), atomic=True)
    report = graph.validate_report(project_root=ROOT)
    assert isinstance(report, GraphValidationReport)
    assert report.conforms is True
