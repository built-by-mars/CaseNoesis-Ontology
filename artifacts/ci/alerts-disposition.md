# Code-scanning alerts disposition

**Date:** 2026-07-12  
**Source:** `artifacts/ci/alerts-table.tsv` / `artifacts/ci/code-scanning-alerts.json` (40 open alerts on `ed0c7f9`)  
**Do not tag / do not push** (per directive).

Commit note for all rows: **pending** (local fixes; no commit requested in this pass).

## Summary counts

| Disposition | Count |
|-------------|------:|
| fixed | 40 |
| false_positive | 0 |
| accepted_debt | 0 |
| **Total** | **40** |

## Disposition table

| alert# | rule | path | disposition | rationale | commit note |
|-------:|------|------|-------------|-----------|-------------|
| 393 | py/syntax-error | packages/case-uco-solveit/python/case_uco_solveit/solveit_data.py:9 | fixed | Hyphenated OWL local names (`techniqueDFT-1001`) were emitted as invalid Python class identifiers. Renamed to underscores in generated bindings; generator `safe_identifier` now sanitizes hyphens for all backends. | pending |
| 394 | py/unused-import | mcp_server/tests/test_extension_paths.py:8 | fixed | Removed unused `pytest` import. | pending |
| 395 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:40 | fixed | Prefixed unused ctx binding (`_leo_marking`). | pending |
| 396 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:46 | fixed | Prefixed unused ctx binding (`_corp_marking`). | pending |
| 397 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:52 | fixed | Prefixed unused ctx binding (`_art_002_source_macbook`). | pending |
| 398 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:59 | fixed | Prefixed unused ctx binding (`_ai_001`). | pending |
| 399 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:60 | fixed | Prefixed unused ctx binding (`_ai_002`). | pending |
| 400 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:63 | fixed | Prefixed unused ctx binding (`_msg_003`). | pending |
| 401 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:66 | fixed | Prefixed unused ctx binding (`_msg_006_facet` at current line; alert line tracked `msg_006`/`facet` unused local). | pending |
| 402 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:84 | fixed | Prefixed unused ctx binding (`_victor_lam`). | pending |
| 403 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:85 | fixed | Prefixed unused ctx binding (`_victim_7`). | pending |
| 404 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:94 | fixed | Prefixed unused ctx binding (`_loc_004`). | pending |
| 405 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:96 | fixed | Prefixed unused ctx binding (`_loc_009`). | pending |
| 406 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:102 | fixed | Prefixed unused ctx binding (`_examiner_keel`). | pending |
| 407 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:108 | fixed | Prefixed unused ctx binding (`_streamvault`). | pending |
| 408 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:111 | fixed | Prefixed unused ctx binding (`_coc_action_ids`). | pending |
| 409 | py/unused-local-variable | examples/scenarios/phantom_gate_longtail.py:114 | fixed | Prefixed unused ctx binding (`_solveit_v7_acquire`). | pending |
| 410 | py/empty-except | python/case_uco/graph.py:527 | fixed | Documented intentional `DuplicateNodeError` swallow under `merge_compatible` partition ingest. | pending |
| 413 | py/unused-import | mcp_server/validation_bundle.py:12 | fixed | Alert targeted pre-rewrite `asdict`/`field` imports; current module no longer imports them (CQ-27–36 rewrite). Verified clean. | pending |
| 414 | py/unused-import | mcp_server/validation_bundle.py:16 | fixed | Alert targeted unused `_extension_dir` import; removed in current tree. | pending |
| 417 | cs/linq/missed-where | csharp/CaseUco/CaseGraph.cs:665 | fixed | `IngestRawNode` property merge uses `.Where(...)` to skip `@id`/`@type`. | pending |
| 418 | cs/linq/missed-where | csharp/CaseUco/CaseGraph.cs:697 | fixed | `MergeTypes` adds only novel IRIs via `.Where(...)`. | pending |
| 419 | cs/inefficient-containskey | csharp/CaseUco/CaseGraph.cs:132 | fixed | `UpsertNode` uses `TryGetValue` for `@type`. | pending |
| 420 | cs/inefficient-containskey | csharp/CaseUco/CaseGraph.cs:145 | fixed | `AddType` uses `TryGetValue` for `@type`. | pending |
| 421 | cs/inefficient-containskey | csharp/CaseUco/CaseGraph.cs:660 | fixed | `IngestRawNode` uses `TryGetValue` for `@type` on raw/existing. | pending |
| 422 | cs/inefficient-containskey | csharp/CaseUco/CaseGraph.cs:663 | fixed | Same `TryGetValue` path for existing `@type`. | pending |
| 423 | cs/inefficient-containskey | csharp/CaseUco/CaseGraph.cs:707 | fixed | `SetProperty` uses `TryGetValue` instead of `ContainsKey` + indexer. | pending |
| 424 | cs/nested-if-statements | csharp/CaseUco/CaseGraph.cs:612 | fixed | `FindObject` index hit flattened to single condition with early return. | pending |
| 425 | cs/nested-if-statements | csharp/CaseUco/CaseGraph.cs:719 | fixed | `SetProperty` list/`@id` dedupe flattened into one guard. | pending |
| 426 | cs/linq/missed-select | csharp/CaseUco/CaseGraph.cs:282 | fixed | Type matching uses `.Select(...).Where(...).Distinct()`. | pending |
| 427 | py/empty-except | python/case_uco/graph.py:537 | fixed | Documented intentional `DuplicateNodeError` swallow when copying shared partition nodes. | pending |
| 428 | py/empty-except | mcp_server/validation_bundle.py:230 | fixed | Alert line shifted; added explanatory comments on `OSError` staging cleanup and `KeyError` cache-shape rebuild paths. | pending |
| 429 | py/import-and-import-from | mcp_server/knowledge_lifecycle.py:279 | fixed | Consolidated on module-level `import graph_validator` (removed mixed `from` imports). | pending |
| 430 | py/import-and-import-from | mcp_server/knowledge_lifecycle.py:324 | fixed | Same consolidation for negative-fixture gate. | pending |
| 431 | py/import-and-import-from | mcp_server/tests/test_validation_bundle.py:112 | fixed | Tests now use only `import validation_bundle as vb`. | pending |
| 432 | py/import-and-import-from | mcp_server/tests/test_validation_bundle.py:148 | fixed | Same single-style import throughout the test module. | pending |
| 433 | py/unused-import | python/case_uco/graph.py:11 | fixed | Removed unused `Iterator` import. | pending |
| 434 | py/unused-local-variable | examples/upper-ontology/solveit-plan-execution/build_exemplar.py:46 | fixed | Renamed unused create result to `_examiner`. | pending |
| 435 | py/unused-local-variable | examples/upper-ontology/foaf-org/build_exemplar.py:91 | fixed | Renamed unused create result to `_contractor`. | pending |
| 436 | py/unused-local-variable | examples/upper-ontology/geosparql/build_exemplar.py:115 | fixed | Renamed unused create result to `_derive_action`. | pending |

## Related CQ-37–CQ-40 (same pass)

| CQ | Status | Notes |
|----|--------|-------|
| CQ-37 | Done | `promote_recipe` uses `fcntl` lock + `.promotion-staging/<slug>/` + `os.replace` with backup rollback (`_commit_recipe_promotion`). |
| CQ-38 | Done | `entries_for_promotion_gate(slug)` expands to shared extension/profile exemplars; `include_full_manifest=True` for full catalog. Structure-only candidates keep an empty gate. |
| CQ-39 | Done | `PROFILE_DISPLAY_TO_ID` derived from `PROFILE_REGISTRY` (+ UCO_PROFILES labels); missing required extensions mark `validation_bundle_preview` unavailable instead of resolving a partial bundle. |
| CQ-40 | Done | `mcp_server/relationship_kinds.json` + `lint_relationship_kinds()`; typed `OrderedRoutingRecommendations` model behind the router. |

## Verification (local)

```text
python3 -c "ast.parse(solveit_data.py)" → OK
pytest test_validation_bundle.py test_knowledge_lifecycle.py (promote/deprecate) → passed
relationship_kinds lint smoke → OK
```
