# Critic deterministic rules

Developer guide for adding graph/serializer critic rules (issue #75).

## Layout

| Module | Role |
|--------|------|
| `mcp_server/critic/models.py` | Typed request/review/finding contracts |
| `mcp_server/critic/deterministic.py` | Offline analysis entrypoint `analyze_artifact` |
| `mcp_server/critic/graph_integrity.py` | Parse, duplicate IDs, dangling refs |
| `mcp_server/critic/graph_heuristics.py` | Structural modeling heuristics |
| `mcp_server/critic/serializer_python.py` | Python AST serializer checks |
| `mcp_server/critic/coverage.py` | Coverage-contract / source-hash checks |
| `mcp_server/critic/context_builder.py` | Bounded prompt package |
| `mcp_server/critic/finding_diff.py` | Stable IDs and pass-to-pass state |
| `mcp_server/critic/response_parser.py` | Model/manual response normalization |
| `mcp_server/critic/schemas/` | JSON Schemas |
| `mcp_server/critic/vocabularies.json` | Severities, categories, error codes |

Orchestration (MCP sampling, sessions, additional passes) is **issue #76**.

## Adding a graph heuristic

1. Add a function in `graph_heuristics.py` that returns `list[CriticFinding]`.
2. Use a stable `rule_id` prefixed `CRIT-H-…`.
3. Set `evidence_kind="deterministic"`, exact `target` (node IRI / predicate), rationale, recommended change, and verification method.
4. Document the false-positive boundary in the table below.
5. Call it from `run_graph_heuristics`.
6. Add a seeded fixture under `mcp_server/tests/fixtures/critic/` and assert the `rule_id` in `test_critic.py`.

## Adding a Python serializer check

1. Prefer `ast` over regex.
2. Use `rule_id` prefix `CRIT-S-PY-…`.
3. Attach `target.path` and `target.line` when possible.
4. Cover the rule in `bad_serializer.py` or a dedicated fixture.

## Finding identity

`identity_key` is `CRIT-` + SHA-256 prefix of `category|rule_id|target|evidence`.
Pass-to-pass resolution requires re-running deterministic verification (or an explicit assessment). Omitting a finding in a model response does **not** resolve it.

## Score caps

If validation is incomplete or non-conforming, `schema_concept_conformance` is capped at **0**. Model scorecards cannot raise that cap (`merge_scorecards`).

## Current heuristic false-positive boundaries

| Rule ID | False-positive boundary |
|---------|-------------------------|
| `CRIT-H-INV-NO-OBJECT` | Draft graphs mid-construction; empty investigations used as stubs |
| `CRIT-H-AUTH-NON-INVESTIGATION` | Extension patterns that legitimately hang authorizations on other nodes |
| `CRIT-H-ACQ-INPUT-RESULT-INVERSION` | Actions named with “image” that are not acquisitions |
| `CRIT-H-CHARGED-WITH-REVERSED` | Non-CASE jurisdictions using inverted charge edges |
| `CRIT-H-RELATED-TO-OVERUSE` | Early exploratory graphs before specific kinds are chosen |
| `CRIT-H-DICT-ENTRY-COLLISION` | Intentionally shared controlled-vocabulary entries |
| `CRIT-H-FACET-PROPS-ON-OBSERVABLE` | Compact examples that inline facet props for brevity |

## Trust boundary

Graph literals, serializer comments, and source excerpts are **untrusted**. Prompt packages always include a trust-boundary block forbidding egress, extra iterations, writes, and promotion.
