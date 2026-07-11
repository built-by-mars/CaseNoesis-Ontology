#!/usr/bin/env python3
"""CASEGraph load/serialize round-trip smoke test for Operation PHANTOM GATE."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "mcp_server"))

from case_uco.graph import CASEGraph  # noqa: E402
from graph_validator import validate_graph_file, validator_available  # noqa: E402

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "operation-phantom-gate.jsonld"
ROUNDTRIP = HERE / "operation-phantom-gate-roundtrip.jsonld"

EXTENSIONS = [
    "legalproc",
    "rico",
    "cryptoinv",
    "attack-technique:full",
    "solveit",
    "weapons",
    "drugs",
    "cac",
]


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing source graph: {SOURCE}", file=sys.stderr)
        return 1

    original = json.loads(SOURCE.read_text(encoding="utf-8"))
    original_count = len(original.get("@graph", []))

    graph = CASEGraph()
    graph.load_file(str(SOURCE))
    loaded_count = len(graph._objects)

    graph.write(str(ROUNDTRIP))
    try:
        roundtrip = json.loads(ROUNDTRIP.read_text(encoding="utf-8"))
        roundtrip_count = len(roundtrip.get("@graph", []))

        if loaded_count != original_count or roundtrip_count != original_count:
            print(
                f"round-trip node count mismatch: "
                f"source={original_count} loaded={loaded_count} written={roundtrip_count}",
                file=sys.stderr,
            )
            return 1

        if not validator_available():
            print("case_validate unavailable — skipping post-roundtrip validation", file=sys.stderr)
            print(f"Round-trip OK — {roundtrip_count} nodes preserved")
            return 0

        report = validate_graph_file(
            ROUNDTRIP,
            project_root=ROOT,
            extensions=EXTENSIONS,
            extra_ontology_graphs=[ROOT / "ontology/solveit/solve-it-kb.ttl"],
            force_rdfs_inference=True,
        )
        if report.conforms is not True:
            print(report.safe_summary, file=sys.stderr)
            return 1

        print(f"Round-trip OK — {roundtrip_count} nodes; Conforms: True")
        return 0
    finally:
        ROUNDTRIP.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
