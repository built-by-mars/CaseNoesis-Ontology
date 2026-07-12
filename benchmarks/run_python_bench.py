#!/usr/bin/env python3
"""Synthetic cross-language benchmark harness — small CI tier (#73).

Generates deterministic catalog-style graphs and measures create/serialize/
lookup/enrichment timing. Medium/large tiers are reserved for nightly runs.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from case_uco import CASEGraph  # noqa: E402
from case_uco.uco.tool import Tool  # noqa: E402


def build_catalog(n: int) -> CASEGraph:
    g = CASEGraph(kb_prefix="https://example.org/bench/")
    for i in range(n):
        g.create(Tool, id=f"kb:tool-{i}", name=f"Tool-{i}", version="1.0")
    return g


def run_tier(n: int) -> dict:
    t0 = time.perf_counter()
    g = build_catalog(n)
    t_build = time.perf_counter() - t0

    t0 = time.perf_counter()
    for i in range(0, n, max(1, n // 100)):
        assert g.contains(f"kb:tool-{i}")
        g.add_property(f"kb:tool-{i}", "uco-core:description", f"bench-{i}")
    t_lookup = time.perf_counter() - t0

    t0 = time.perf_counter()
    payload = g.serialize()
    t_ser = time.perf_counter() - t0

    return {
        "nodes": n,
        "build_seconds": round(t_build, 6),
        "lookup_enrich_seconds": round(t_lookup, 6),
        "serialize_seconds": round(t_ser, 6),
        "serialize_bytes": len(payload.encode("utf-8")),
        "estimate_triples": g.estimate_triples(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=["small", "medium", "large"], default="small")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    sizes = {"small": 1000, "medium": 10000, "large": 100000}
    result = {
        "suite": "case-uco-synthetic-benchmark",
        "tier": args.tier,
        "language": "python",
        "result": run_tier(sizes[args.tier]),
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
