"""Public CASE/UCO graph validation (SHACL + concept coverage + bundles).

This package is the canonical home for the rich validator previously kept
under ``mcp_server``. MCP tools and repo examples should import from here::

    from case_uco.validation import validate_graph_file, GraphValidationReport

    report = validate_graph_file(
        "graph.jsonld",
        extensions=["attack-technique:full"],
        profiles=[],
        strict_concepts=True,
    )
    assert report.conforms
"""

from case_uco.validation.graph import (
    GraphValidationReport,
    report_to_dict,
    validate_graph_file,
    validator_available,
)

__all__ = [
    "GraphValidationReport",
    "report_to_dict",
    "validate_graph_file",
    "validator_available",
]
