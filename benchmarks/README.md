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
# Python (all workloads)
python3 benchmarks/run_python_bench.py --tier small --out artifacts/bench/python-small.json

# Rust
./benchmarks/run_rust_bench.sh --tier small

# C# / Java — use language test projects' smoke paths or:
#   cd csharp && dotnet run --project CaseUco.Smoke -- --bench small
#   (add dedicated runners as needed)
```

## Workloads (Python)

- `catalog` — independent Tool nodes
- `relationship_rich` — device/file graphs + `partition(strategy="roots")`
- `deserialize_roundtrip` — cold/warm `from_jsonld` after registry clear
- `streaming_write` — `write_streaming` vs full `write`

## Correctness

Benchmarks assert containment / round-trip equality. They are not a language
competition; regressions are measured against prior committed JSON results.
