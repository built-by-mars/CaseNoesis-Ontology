# Critic deterministic rules (Round 2)

Developer guide for adding graph/serializer critic rules (issue #75).

## Layout

| Module | Role |
|--------|------|
| `canonical.py` | RDFLib-backed `CanonicalGraphView`, exact IRIs, scalar/list normalization |
| `models.py` | Typed contracts + `make_stable_finding_id` |
| `deterministic.py` | Offline `analyze_artifact` entrypoint |
| `graph_integrity.py` | Parse statuses, duplicate keys, dangling RDF object refs |
| `graph_heuristics.py` | Structural modeling heuristics (canonical API only) |
| `serializer_python.py` | Python AST serializer checks |
| `coverage.py` | Coverage contract + ContentDataFacet source-hash compare |
| `context_builder.py` | Bounded prompt package + hash + one-hop neighborhoods |
| `finding_diff.py` | Pass-to-pass ledger (resolved only after rule evaluation) |
| `response_parser.py` | Draft 2020-12 JSON Schema enforcement for model responses |
| `scorecard.py` | Nullable / evidence-backed dimensions + hard caps |
| `schemas/` | JSON Schemas |
| `vocabularies.json` | Severities, categories, error codes |

Orchestration (MCP sampling, sessions) is **issue #76**.

## Finding identity

`finding_id` is stable: `CRIT-` + SHA-256 of `rule_id|semantic target parts`.
Graph targets use expanded node/predicate/counterpart IRIs — **not** line, path, evidence prose, or artifact hash.
Serializer targets use path + qualified name — **not** line number.
`display_index` is report-only ordering.

## Rule-execution ledger

Every pass records `evaluated|not_applicable|skipped|failed` per rule.
A prior deterministic finding is **resolved** only when its rule ran successfully and the defect is absent. Otherwise it remains **unevaluated**/open.

## Adding a graph heuristic

1. Implement against `CanonicalGraphView` (exact IRIs, `node.refs(prop_iri)`).
2. Return `(findings, targets_examined)` and register in `run_graph_heuristics`.
3. Use stable `rule_id` `CRIT-H-…` and `make_stable_finding_id`.
4. Document false-positive boundary below.
5. Add production-shaped fixtures (list-valued UCO endpoints, CASE namespaces).

## Trust boundary

Graph literals, serializer comments, and source excerpts are **untrusted**.
Prompt packages include a trust-boundary block and a `prompt_package_hash` that model responses must echo.
