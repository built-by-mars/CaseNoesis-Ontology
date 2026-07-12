# PROF metadata exemplar — validator warning disposition (v1.21.0)

**Graph:** `examples/upper-ontology/prof-metadata/prof-metadata.jsonld`  
**Profiles:** `prof`, `prov-o`  
**Validated:** 2026-07-12 via `graph_validator.validate_graph_file(...)` / `case_validate`  
**Outcome:** `Conforms: True`, `verification_status: complete`, **0 SHACL violations**, **2 validator warnings**

## Summary

| Status | Count | Action |
|--------|------:|--------|
| Fixed in exemplar | 2 | UcoThing UUID-suffix `sh:Info` results removed |
| Expected / harmless | 2 | Documented below (strict concept coverage) |

After the UUID-suffix fix, **no SHACL constraint results remain**. The two remaining warnings are Python-level strict concept-coverage notices from `case-utils`, not conformance failures.

---

## Fixed — UcoThing identifier regex (`sh:Info`)

**Identifier:** `core:UcoThing-identifier-regex-shape`  
**Severity:** `sh:Info` (informational)  
**Message:** `UcoThings are suggested to end with a UUID.`

**Affected nodes (before fix):**

- `kb:validation-report-1`
- `kb:validation-report-2`

**Fix applied:** Renamed validation-report nodes (and the linked validator activity) to UUID-suffixed IRIs in `build_exemplar.py` and regenerated `prof-metadata.jsonld`:

- `kb:validation-report-11111111-1111-4111-8111-111111111111`
- `kb:validation-report-22222222-2222-4222-8222-222222222222`
- `kb:action-validate-33333333-3333-4333-8333-333333333333`

**Verification:** Re-validation produces zero SHACL results; these informational shapes no longer appear.

---

## Expected / harmless — ontology root IRI not in loaded graph

**Warning identifiers (verbatim from `case-utils`):**

1. `NonExistentCDOConceptWarning: https://ontology.unifiedcyberontology.org/uco/`
2. `UserWarning: There were 1 concepts with CDO IRIs in the data graph that are not in the ontology graph.`

**Source in data graph:**

```json
"prof:isProfileOf": {
  "@id": "https://ontology.unifiedcyberontology.org/uco/"
}
```

**Why this is expected for v1.21:**

- The exemplar intentionally declares a **PROF Profile** whose `prof:isProfileOf` target is the **UCO ontology namespace IRI**, not a specific `owl:Ontology` individual bundled in the validation subset.
- Profile-aware validation loads PROF + PROV-O + CASE/UCO SHACL bundles; it does **not** ingest every referenced namespace root as a declared class/property in the strict concept-coverage pass.
- SHACL conformance still passes (`Conforms: True`); these are **coverage warnings**, not shape violations.
- Replacing the IRI with a synthetic ontology individual would misrepresent PROF semantics; omitting `isProfileOf` would weaken the recipe’s teaching goal.

**Disposition:** **Accept for v1.21** — document and monitor. Revisit only if `case-utils` adds first-class support for ontology-namespace references in profile metadata or if a canonical `owl:Ontology` individual IRI is published for CASE/UCO 1.4.0.

---

## Reproduction

```bash
PYTHONPATH=python:mcp_server python3 -c "
from graph_validator import validate_graph_file
r = validate_graph_file(
    'examples/upper-ontology/prof-metadata/prof-metadata.jsonld',
    profiles=['prof', 'prov-o'],
)
print(r.conforms, r.warning_count, r.safe_summary)
print(r.validator_diagnostics or 'no diag')
"
```

Or via the recipe gate:

```bash
PYTHONPATH=python:mcp_server python3 mcp_server/tools/run_recipe_examples.py --id prof-metadata --validate
```
