#!/usr/bin/env python3
"""Compare a synthetic benchmark result against a committed baseline (#73).

Fails (exit 1) if any compared timing key exceeds baseline by more than
``--threshold`` (default +100%, i.e. 2×). Lenient for CI host variance.

v1.22 advisory median policy: the CI ``bench-python`` job runs this step with
``continue-on-error: true`` so median timing noise does not fail ``test-python``.
Treat a non-zero exit as an advisory signal until a harder gate lands in a
later release.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TIMING_SUFFIXES = ("_seconds",)
SKIP_KEYS = frozenset({"nodes", "partition_count", "serialize_bytes", "bytes_written", "estimate_triples"})
# Absolute floor: sub-50ms timings are too noisy for a 2× CI gate on shared runners.
MIN_BASELINE_SECONDS = 0.05


def _timing_keys(obj: dict[str, Any], prefix: str = "") -> list[tuple[str, float]]:
    found: list[tuple[str, float]] = []
    for key, value in obj.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            found.extend(_timing_keys(value, path))
        elif isinstance(value, (int, float)) and key.endswith(TIMING_SUFFIXES) and key not in SKIP_KEYS:
            found.append((path, float(value)))
    return found


def compare(baseline: dict[str, Any], current: dict[str, Any], threshold: float) -> list[str]:
    base_timings = dict(_timing_keys(baseline.get("result", baseline)))
    curr_timings = dict(_timing_keys(current.get("result", current)))
    failures: list[str] = []
    for path, base_val in sorted(base_timings.items()):
        if path not in curr_timings:
            continue
        if base_val < MIN_BASELINE_SECONDS:
            continue
        curr_val = curr_timings[path]
        ratio = curr_val / base_val
        if ratio > (1.0 + threshold):
            failures.append(
                f"{path}: {curr_val:.6f}s is {ratio:.2f}× baseline {base_val:.6f}s "
                f"(limit {1.0 + threshold:.2f}×)"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path(__file__).resolve().parent / "baselines" / "python-small.json",
    )
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument(
        "--threshold",
        type=float,
        default=1.0,
        help="Max allowed relative increase (1.0 = +100%%)",
    )
    args = parser.parse_args()

    if not args.baseline.is_file():
        print(f"No baseline at {args.baseline}; skipping compare.", file=sys.stderr)
        return 0
    if not args.result.is_file():
        print(f"Missing result file: {args.result}", file=sys.stderr)
        return 2

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    current = json.loads(args.result.read_text(encoding="utf-8"))
    failures = compare(baseline, current, args.threshold)
    if failures:
        print("Benchmark regression vs baseline:", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(
        f"OK: all timing keys within +{args.threshold * 100:.0f}% of {args.baseline}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
