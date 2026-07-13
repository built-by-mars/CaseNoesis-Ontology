#!/usr/bin/env bash
# Synthetic Rust benchmark harness (#73) — wraps `cargo run --example bench`.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER="${1:-small}"
if [[ "${1:-}" == "--tier" ]]; then
  TIER="${2:-small}"
fi
exec cargo run --example bench --manifest-path "${ROOT}/rust/Cargo.toml" -- --tier "${TIER}"
