# CI triage and quality disposition (v1.21.0 RC)

**Base commit reviewed:** `ed0c7f9e365d96c6751597d98a6e7490cd77534b`  
**Status:** v1.21.0 remains **untagged**. Issues #59–#73 stay open.

## Failed Actions (authoritative)

| Run | URL | Conclusion |
|-----|-----|------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29209600022 | failure |
| Rust Security | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29209599985 | failure |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29209599992 | success |

### First causal errors

| Job | Step / command | Causal error |
|-----|----------------|--------------|
| Test Doc Snippets | `python scripts/test_doc_snippets.py` | `docs/recipes/geosparql-geospatial-evidence.md`: `graph.create(..., name="...", ...)` — positional `...` after keyword args |
| Test Python | `pytest generator/tests python/tests` | `ImportError: cannot import name 'DuplicateNodeError'` — generator overwrite of `python/case_uco/__init__.py` dropped the export |
| Clippy security lints | `cargo clippy -D clippy::unwrap_used` | 7× `unwrap`/`expect` in `rust/src/graph.rs` |

Raw exports: `artifacts/ci/runs.json`, `failed-ci.log`, `failed-rust-security.log`, `check-runs.json`, `code-scanning-alerts.json`, `alerts-table.tsv`.

## Code-scanning alerts (40) — before → after

See `artifacts/ci/alerts-disposition.md` for the full table. Summary: **40 fixed**, 0 false_positive, 0 accepted_debt.

| # | Rule | Path | Disposition |
|---|------|------|-------------|
| 393 | py/syntax-error | packages/.../solveit_data.py:9 | fixed |
| 394 | py/unused-import | mcp_server/tests/test_extension_paths.py:8 | fixed |
| 395–409 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py | fixed |
| 410, 427 | py/empty-except | python/case_uco/graph.py | fixed |
| 413, 414 | py/unused-import | mcp_server/validation_bundle.py | fixed |
| 417–426 | cs/* | csharp/CaseUco/CaseGraph.cs | fixed |
| 428 | py/empty-except | mcp_server/validation_bundle.py | fixed |
| 429–432 | py/import-and-import-from | knowledge_lifecycle / tests | fixed |
| 433 | py/unused-import | python/case_uco/graph.py:11 | fixed |
| 434–436 | py/unused-local-variable | upper-ontology builders | fixed |

## CQ-01 … CQ-40 disposition

| CQ | Area | Disposition | Notes |
|----|------|-------------|-------|
| CQ-01–CQ-12 | Recipe gate | fixed | See `cq-01-12.md` |
| CQ-13–CQ-26 | Graph parity | fixed | See `cq-13-26.md`; multi-`@id` refs accumulate under merge_compatible |
| CQ-27–CQ-36 | Same-bundle coverage | fixed | See `cq-27-36.md`; coverage takes `ResolvedValidationBundle` |
| CQ-37–CQ-40 | Promotion / routing | fixed | See `cq-37-40.md` |

## Local verification (pre-push)

- Doc snippets: 111 passed
- Python composition tests: 29 passed
- MCP tests: 286 passed, 1 skipped
- Recipe gate: **9/9** with `verification_status=complete`
- Rust clippy (`unwrap_used`/`expect_used`): clean; graph_test 16 passed
- C# CaseUco build succeeded; Java CaseGraphTest run after push verification

## Deferred to v1.22.0 / keep open

Full original acceptance for issues #59–#73 (breadth of exemplars, dependency-aware partition, multi-language performance harnesses) remains open. Experimental foundations #70–#73 stay experimental.


## Green Actions on follow-up commit

**Release-candidate HEAD:** `0e0b5cd32a3131af15770a05ac683b340620deed`

| Workflow | URL | Conclusion |
|----------|-----|------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211429925 | success |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211429931 | success |
| Rust Security (on `96c322d`) | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211198715 | success |

Mypy follow-up (`0e0b5cd`) did not re-trigger Rust Security (path filters); Rust Security was green on the CQ commit `96c322d`.
