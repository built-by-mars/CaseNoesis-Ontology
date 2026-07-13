#!/usr/bin/env bash
# Synthetic C# benchmark harness (#73) — catalog serialize timing.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER="${1:-small}"
if [[ "${1:-}" == "--tier" ]]; then
  TIER="${2:-small}"
fi
OUT_DIR="${ROOT}/artifacts/bench"
mkdir -p "${OUT_DIR}"
RESULT="${OUT_DIR}/csharp-${TIER}.json"
dotnet run --project "${ROOT}/csharp/CaseUco.Bench/CaseUco.Bench.csproj" -c Release -v q -- --tier "${TIER}" | tee "${RESULT}"
test -s "${RESULT}"
echo "Wrote ${RESULT}"
