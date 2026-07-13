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

## Graph heuristics (`CRIT-H-*`, `graph_heuristics` v1.2.0)

| Rule ID | Intent |
|---------|--------|
| `CRIT-H-INV-NO-OBJECT` | Investigation missing `uco-core:object` |
| `CRIT-H-AUTH-NON-INVESTIGATION` | `relevantAuthorization` on non-Investigation |
| `CRIT-H-ACQ-INPUT-RESULT-INVERSION` | Acquisition-like action uses file only as input |
| `CRIT-H-RELATED-TO-OVERUSE` | Excessive generic `Related_To` |
| `CRIT-H-CHARGED-WITH-REVERSED` | `Charged_With` charge→person |
| `CRIT-H-DICT-ENTRY-COLLISION` | Dictionary entry IRI under multiple parents |
| `CRIT-H-FACET-PROPS-ON-OBSERVABLE` | Facet properties on ObservableObject |
| `CRIT-H-ACTION-COMPLETENESS` | Acquir/extract/analy/hash/image/export action missing performer\|instrument, object, or (acquisition) result |
| `CRIT-H-IDENTITY-CONFLATION` | Person also typed Account/`*Account`/Role |
| `CRIT-H-PROXY-DUPLICATE` | Same ContentDataFacet hashValue on distinct IRIs without link |
| `CRIT-H-DERIVED-NO-HASH` | Action result / Extracted_From target without hashValue |
| `CRIT-H-DERIVED-NO-PROVENANCE` | Derived node with no container membership or inbound provenance |
| `CRIT-H-MARKING-INHERITANCE` | Source has `objectMarking`, derived does not |
| `CRIT-H-CUSTODY-UNPAIRED` | Custody/transfer/release/receipt action without object+result or Transferred_To |
| `CRIT-H-IMAGE-CONTAINER-MISMATCH` | RasterPicture as forensic image, or File Contained_Within RasterPicture |
| `CRIT-H-CONTEXTUAL-COMPILATION-OMISSION` | Action-result File/Observable not in Investigation/ProvenanceRecord/ContextualCompilation |

## Python serializer AST (`CRIT-S-PY-*`)

| Rule ID | Intent |
|---------|--------|
| `CRIT-S-PY-PRIVATE-OBJECTS` | Mutate `CASEGraph._objects` |
| `CRIT-S-PY-JSON-DUMPS-ONLY` | `json.dumps` without graph write/serialize |
| `CRIT-S-PY-FAIL-OPEN-VALIDATION` | Success when validator unavailable |
| `CRIT-S-PY-SWALLOWED-EXCEPTION` | Broad `except` swallow |
| `CRIT-S-PY-UNSCOPED-UUID5` | uuid5 ID helper without parent scope |
| `CRIT-S-PY-GLOBAL-UUID-IDS` | uuid4 `make_*/new_*/build_*` without parent |
| `CRIT-S-PY-NONEXISTENT-API` | Unknown method on `graph`/`g`/`case_graph` |
| `CRIT-S-PY-REL-ID-COLLAPSE` | `create_relationship` in `for` without assertion_id |
| `CRIT-S-PY-SILENT-LOOKUP` | `.get(...)` then Return/Pass/Continue without Raise |
| `CRIT-S-PY-UNSAFE-OVERWRITE` | `open(...,"w")` / `Path.write_*` without `workspace_policy` |
| `CRIT-S-PY-SOURCE-HASH-DRIFT` | 64-hex `hash_value` literal without hashlib in function |
| `CRIT-S-PY-SYNTHETIC-HASH` | `synthetic_hash`/`fake_hash`/`placeholder_hash` feeds hash construction |
| `CRIT-S-PY-QUADRATIC-SCAN` | Nested `for` over `_objects` / `list(graph)` |
