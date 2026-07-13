# CI triage and quality disposition (v1.21.0)

**Base commit reviewed:** `ed0c7f9e365d96c6751597d98a6e7490cd77534b`  
**Green verification SHA (CI + CodeQL):** `a269392bee7ffb777748c95f8bb72ad516e03b73`

## Green verification runs (`a269392`)

| Workflow | URL | Conclusion |
|----------|-----|------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29212444014 | success |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29212444012 | success |
| Rust Security (on `96c322d`) | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211198715 | success |

Rust Security was green on `96c322d` and was **not** re-triggered on `a269392` (path filters; Rust sources unchanged).

Code-scanning snapshot after `a269392`: **0** open alerts
(`artifacts/ci/code-scanning-open-after-a269392.json`, meta in
`code-scanning-snapshot-meta.json`). Historical open set before that SHA:
`code-scanning-open-before-a269392.json`.

**Quality summary:** **72** code-scanning findings across two passes
(**40** initial + **32** follow-up), all dispositioned as fixed.

Recipe validation: CI job `recipe-validation` uploads
`recipe-validation-report` as a workflow artifact. Do **not** commit
workstation-local reports (absolute `/home/...` paths). The gate covers the
**nine upper-ontology exemplars** in `docs/recipes/recipe-execution.json`
(#69); full operational catalog migration is **v1.22**.

## Failed Actions (authoritative — initial triage on `ed0c7f9`)

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

## Code-scanning alerts — pass 1 (40) and pass 2 (32)

See `artifacts/ci/alerts-disposition.md` (40) and
`artifacts/ci/alerts-disposition-32.md` (32). Summary: **72 fixed**,
0 false_positive, 0 accepted_debt.

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

Full operational recipe-catalog migration and original breadth for issues
#59–#73 (dependency-aware partition, multi-language performance harnesses)
remain open. Experimental foundations #70–#73 stay experimental v1.22 work.

## Intermediate green runs (superseded by `a269392`)

**Earlier RC HEAD:** `0e0b5cd32a3131af15770a05ac683b340620deed`

| Workflow | URL | Conclusion |
|----------|-----|------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211429925 | success |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211429931 | success |
| Rust Security (on `96c322d`) | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211198715 | success |


## Final RC SHA (tag not cut)

**HEAD:** `1b22f43818772684b3443165f7bdfc5df7da57bc`

| Workflow | URL | Conclusion |
|----------|-----|------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29214036412 | success |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29214036416 | success |
| Rust Security | unchanged since `96c322d` (path filters; Rust not modified in RC prep) — https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29211198715 | success |

Promotion fail-open fixed; #69 narrowed; issue disposition comments posted on #59–#73.


## Tag-ready release governance (post ChatGPT final checklist)

**Verified executable-code SHA:** `d5b6987bce18a2797fd0f53ebedfd438e03e2a9d`

| Workflow | URL | Conclusion |
|----------|-----|------------|
| CI | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29215329562 | success |
| CodeQL | https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29215329710 | success |
| Open code-scanning alerts | API `state=open` after CodeQL above | **0** |

Prior feature verification SHA `1b22f43` remains documented; `d5b6987` is a one-line test import hygiene fix re-verified green.

**Issue tracker:** #59–#69 closed as scoped-complete-v1.21; #70–#73 open on milestone **v1.22.0** with label `v1.22`.

**PUBLISH_PACKAGES:** leave false for GitHub Release with attached packages only unless credentials for PyPI/NuGet/Maven/crates.io are confirmed.

