#!/usr/bin/env python3
"""Check Operation PHANTOM GATE graph against phantom_gate_coverage.json."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "phantom_gate_coverage.json"
GRAPH = HERE / "operation-phantom-gate.jsonld"
SCENARIO = HERE / "operation-phantom-gate.md"
NS_SUFFIX = "operation-phantom-gate-2026/"

sys.path.insert(0, str(HERE))
from phantom_gate_acceptance import (  # noqa: E402
    assert_no_action_authorizations,
    assert_unique_top_level_ids,
    verify_embedded_scenario_hash,
)


def node_matches_label(node: dict, label: str) -> bool:
    node_id = node.get("@id", "")
    if node_id.endswith(f"/{label}") or node_id.endswith(label):
        return True
    name = node.get("uco-core:name", "")
    return label in name


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    graph_doc = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = graph_doc.get("@graph", [])

    missing: list[str] = []
    for _group, labels in contract["required_artifact_labels"].items():
        for label in labels:
            if not any(node_matches_label(n, label) for n in nodes):
                missing.append(label)

    for phrase in contract["required_authorizations"]:
        if not any(phrase in n.get("uco-core:name", "") for n in nodes):
            missing.append(f"auth:{phrase}")

    for docket in contract["required_charging_dockets"]:
        if not any(n.get("legalproc:caseIdentifier") == docket for n in nodes):
            missing.append(f"docket:{docket}")

    grouping = contract["required_grouping"]
    if not any(grouping in n.get("uco-core:name", "") for n in nodes):
        missing.append(f"grouping:{grouping}")

    sub_inv = [
        n for n in nodes
        if n.get("@type") == "case-investigation:Investigation"
        and n.get("legalproc:caseIdentifier")
        and n.get("legalproc:caseIdentifier") != contract["case_identifier"]
    ]
    cti_name = contract.get("required_sub_investigation_without_docket")
    if cti_name and not any(cti_name in n.get("uco-core:name", "") for n in nodes):
        missing.append(f"sub_investigation:{cti_name}")

    if len(sub_inv) < contract["required_sub_investigation_count"]:
        missing.append(
            f"sub_investigations:{len(sub_inv)}/{contract['required_sub_investigation_count']}"
        )

    node_count = len(nodes)
    if node_count < contract["min_nodes"]:
        missing.append(f"min_nodes:{node_count}/{contract['min_nodes']}")

    try:
        assert_unique_top_level_ids(nodes)
        assert_no_action_authorizations(nodes)
        verify_embedded_scenario_hash(nodes, hashlib.sha256(SCENARIO.read_bytes()).hexdigest())
    except RuntimeError as exc:
        missing.append(str(exc))

    if missing:
        print(f"Coverage FAIL — {len(missing)} gap(s):", file=sys.stderr)
        for item in missing:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(
        f"Coverage OK — {node_count} nodes; "
        f"{sum(len(v) for v in contract['required_artifact_labels'].values())} artifact labels; "
        f"{len(sub_inv)} docketed sub-investigations + CTI wing"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
