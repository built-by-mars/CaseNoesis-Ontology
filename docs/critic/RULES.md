# Critic deterministic rules and session loop

Developer guide for the CASE/UCO critic package (issues #75–#78).

## Layout

| Module | Role |
|--------|------|
| `canonical.py` | RDFLib-backed `CanonicalGraphView`, exact IRIs, offline remote-context policy |
| `models.py` | Typed contracts + `make_stable_finding_id` |
| `deterministic.py` | Offline `analyze_artifact` entrypoint |
| `sessions.py` | Resumable two-pass MCP session state machine (#76) |
| `sampling.py` | Optional `Context.sample` helper + fake sampler |
| `handoff.py` | Preview-only self-improvement handoff (#78) |
| `graph_integrity.py` | Parse statuses, duplicate keys, dangling RDF object refs |
| `graph_heuristics.py` | Structural modeling heuristics (canonical API only) |
| `serializer_python.py` | Python AST serializer checks (per-rule executions) |
| `coverage.py` | Coverage contract + ContentDataFacet source-hash compare |
| `context_builder.py` | Bounded prompt package + hash + one-hop neighborhoods |
| `finding_diff.py` | Pass-to-pass ledger (`unevaluated` vs `resolved`) |
| `response_parser.py` | Authoritative model-response schema enforcement |
| `scorecard.py` | Ledger-aware dimensions + hard-cap-only model merge |
| `schemas/` | JSON Schemas (prompt, response, review, handoff, …) |
| `vocabularies.json` | Severities, categories, error codes |

Evaluation corpus and offline oracles live under `evaluation/critic/` (#77).

## Session defaults (#76)

- Required critic passes: **2**
- Additional passes: operator-approved via `extend_critic_review` + token
- Hard maximum total passes: **8**
- Model policies: `disabled` | `manual` (default) | `client_sampling`
- Finalization requires: matching hashes, complete conforming validation,
  `analysis_status=complete`, no open critical/high findings, and two completed
  critic responses (or two deterministic passes when `disabled`)

## Finding identity

`finding_id` is stable: `CRIT-` + SHA-256 of `rule_id|semantic target parts`
(or `MODEL-category|target|claim_type` for critic inferences — **no array index**).
Graph targets use expanded node/predicate/counterpart IRIs — **not** line/path/
evidence prose. Serializer targets use path + qualified name — **not** line.

## Rule-execution ledger

Every pass records `evaluated|not_applicable|skipped|failed` per concrete rule.
Failed/skipped **required** rules yield `analysis_incomplete` and block
`deterministic_clean` / finalization. `not_applicable` does not block.

Prior deterministic/source findings resolve only when a matching `rule_id` or
`verifier_rule_id` evaluated successfully and the defect is absent.

## Trust boundary

Graph literals, serializer comments, and source excerpts are **untrusted**.
Prompt packages include a trust-boundary block. Self-improvement writes require
explicit operator approval (`prepare_critic_handoff(..., approve_write=True)`).
