#!/usr/bin/env bash
# Synthetic Java benchmark harness (#73) — catalog serialize timing.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER="${1:-small}"
if [[ "${1:-}" == "--tier" ]]; then
  TIER="${2:-small}"
fi
OUT_DIR="${ROOT}/artifacts/bench"
mkdir -p "${OUT_DIR}"
RESULT="${OUT_DIR}/java-${TIER}.json"
cd "${ROOT}/java"
mvn -q -DskipTests compile
# Bypass pom exec.mainClass (SmokeTest) — run CatalogBench on the compile classpath.
java -cp target/classes org.caseontology.bench.CatalogBench --tier "${TIER}" | tee "${RESULT}"
grep -q '"language": "java"' "${RESULT}"
test -s "${RESULT}"
echo "Wrote ${RESULT}"
