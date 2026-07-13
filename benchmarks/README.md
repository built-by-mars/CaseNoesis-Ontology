# Public synthetic CASE/UCO benchmarks (#73)

Fully synthetic, deterministic workloads for Python / C# / Java / Rust.

## Tiers

| Tier | Nodes | When |
|------|------:|------|
| `small` | 1_000 | PR / CI |
| `medium` | 10_000 | Nightly |
| `large` | 100_000 | Release |

## Run

```bash
# Python (all workloads) + baseline compare
python3 benchmarks/run_python_bench.py --tier small --out artifacts/bench/python-small.json
python3 benchmarks/compare_baseline.py \
  --baseline benchmarks/baselines/python-small.json \
  --result artifacts/bench/python-small.json

# Rust / C# / Java (catalog serialize)
./benchmarks/run_rust_bench.sh --tier small
./benchmarks/run_csharp_bench.sh --tier small
./benchmarks/run_java_bench.sh --tier small
```

Committed baseline: `benchmarks/baselines/python-small.json`. Compare fails if
any `*_seconds` timing with baseline ≥ 50ms exceeds that baseline by more than
+100% (sub-50ms keys are skipped as too noisy for CI).

## Workloads (Python)

- `catalog` — independent Tool nodes
- `relationship_rich` — device/file graphs + `partition(strategy="roots")`
- `deserialize_roundtrip` — cold/warm `from_jsonld` after registry clear
- `streaming_write` — `write_streaming` vs full `write`

## Correctness

Benchmarks assert containment / round-trip equality. They are not a language
competition; regressions are measured against prior committed JSON results.
