#!/usr/bin/env python3
"""Public synthetic CASE/UCO benchmark harness (#73).

Tiers:
  small  — PR/CI (1_000 nodes)
  medium — nightly (10_000 nodes)
  large  — release (100_000 nodes)

Workloads:
  catalog            — independent Tool nodes
  relationship_rich  — devices/files/relationships (dependency partition target)
  deserialize_roundtrip — serialize + cold/warm from_jsonld
  streaming_write    — write_streaming metrics
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from case_uco import CASEGraph, clear_class_registry_cache  # noqa: E402
from case_uco.uco.tool import Tool  # noqa: E402


SIZES = {"small": 1_000, "medium": 10_000, "large": 100_000}


def build_catalog(n: int) -> CASEGraph:
    g = CASEGraph(kb_prefix="https://example.org/bench/")
    for i in range(n):
        g.create(Tool, id=f"kb:tool-{i}", name=f"Tool-{i}", version="1.0")
    return g


def build_relationship_rich(n: int) -> CASEGraph:
    """n device roots, each with one file + Related_To edge."""
    g = CASEGraph(kb_prefix="https://example.org/bench/")
    for i in range(n):
        device = f"kb:device-{i}"
        file_id = f"kb:file-{i}"
        g.upsert_node(device, types="uco-core:UcoObject", properties={"uco-core:name": f"D{i}"})
        g.upsert_node(
            file_id,
            types="uco-core:UcoObject",
            properties={
                "uco-core:name": f"F{i}",
                "uco-core:object": {"@id": device},
            },
        )
        g.create_relationship(file_id, device, "Contained_Within")
    return g


def run_catalog(n: int) -> dict:
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
        "workload": "catalog",
        "nodes": n,
        "build_seconds": round(t_build, 6),
        "lookup_enrich_seconds": round(t_lookup, 6),
        "serialize_seconds": round(t_ser, 6),
        "serialize_bytes": len(payload.encode("utf-8")),
        "estimate_triples": g.estimate_triples(),
    }


def run_relationship_rich(n: int) -> dict:
    t0 = time.perf_counter()
    g = build_relationship_rich(n)
    t_build = time.perf_counter() - t0
    roots = [f"kb:file-{i}" for i in range(0, n, max(1, n // 10))]
    t0 = time.perf_counter()
    parts = g.partition(strategy="roots", roots=roots[:5])
    t_part = time.perf_counter() - t0
    return {
        "workload": "relationship_rich",
        "nodes": len(g),
        "build_seconds": round(t_build, 6),
        "partition_seconds": round(t_part, 6),
        "partition_count": len(parts),
        "estimate_triples": g.estimate_triples(),
    }


def run_deserialize_roundtrip(n: int) -> dict:
    g = build_catalog(n)
    payload = g.serialize()
    clear_class_registry_cache()
    t0 = time.perf_counter()
    cold, _ = CASEGraph.from_jsonld(
        payload, kb_prefix="https://example.org/bench/"
    )
    t_cold = time.perf_counter() - t0
    t0 = time.perf_counter()
    warm, _ = CASEGraph.from_jsonld(
        payload, kb_prefix="https://example.org/bench/"
    )
    t_warm = time.perf_counter() - t0
    assert len(cold) == n and len(warm) == n
    return {
        "workload": "deserialize_roundtrip",
        "nodes": n,
        "from_jsonld_cold_seconds": round(t_cold, 6),
        "from_jsonld_warm_seconds": round(t_warm, 6),
        "serialize_bytes": len(payload.encode("utf-8")),
    }


def run_streaming_write(n: int, tmp: Path) -> dict:
    g = build_catalog(n)
    out = tmp / "stream.jsonld"
    t0 = time.perf_counter()
    metrics = g.write_streaming(str(out), atomic=True)
    t_stream = time.perf_counter() - t0
    t0 = time.perf_counter()
    g.write(str(tmp / "full.jsonld"))
    t_full = time.perf_counter() - t0
    return {
        "workload": "streaming_write",
        "nodes": n,
        "write_streaming_seconds": round(t_stream, 6),
        "write_full_seconds": round(t_full, 6),
        "bytes_written": metrics["bytes_written"],
    }


def run_tier(n: int, tmp: Path) -> dict:
    return {
        "catalog": run_catalog(n),
        "relationship_rich": run_relationship_rich(max(10, n // 10)),
        "deserialize_roundtrip": run_deserialize_roundtrip(n),
        "streaming_write": run_streaming_write(n, tmp),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=["small", "medium", "large"], default="small")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--workdir", type=Path, default=None)
    args = parser.parse_args()
    workdir = args.workdir or Path("/tmp/case-uco-bench")
    workdir.mkdir(parents=True, exist_ok=True)
    result = {
        "suite": "case-uco-synthetic-benchmark",
        "schema_version": "1.1.0",
        "tier": args.tier,
        "language": "python",
        "result": run_tier(SIZES[args.tier], workdir),
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
