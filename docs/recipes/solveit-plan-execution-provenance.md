# SOLVE-IT Plan and Execution Provenance

> See [Recipe Index](INDEX.md) for all recipes.

Separate **planned** forensic procedure (`prov:Plan`) from **executed** steps (`solveit-core:SolveitInvestigativeAction`), including deviation, partial completion, and re-execution. Requires the bundled `solveit` extension.

Issue: [#65](https://github.com/vulnmaster/CASE-UCO-SDK/issues/65)

## Scope

- `prov:Plan` vs `SolveitInvestigativeAction` execution
- Deviation, partial completion, re-execution (`prov:wasRevisionOf`)
- Exemplar: `examples/upper-ontology/solveit-plan-execution/build_exemplar.py`

Pair with [solve-it-investigation-planning.md](solve-it-investigation-planning.md) for technique/mitigation catalog usage.

## Concepts

| Node | Types | Role |
|---|---|---|
| Acquisition plan | `prov:Plan` | What was **intended** before execution |
| Planned step | `solveit-core:SolveitInvestigativeAction` | Method selection without timestamps |
| Executed step | `solveit-core:SolveitInvestigativeAction` + `prov:Activity` | What **happened** — with `usedTechnique`, `appliedMitigation`, times |
| Re-execution | `solveit-core:SolveitInvestigativeAction` | `prov:wasRevisionOf` prior partial execution |

## Decision rules

1. **One `prov:Plan` per procedure** — link actions with `prov:hadPlan`.
2. **Planned ≠ executed.** Do not copy plan steps into executed actions without recording deviations in `uco-core:description`.
3. **`usedTechnique` on execution only** when the technique was actually applied; planned actions may reference techniques prospectively.
4. **Partial completion** — document stop reason; link re-execution with `prov:wasRevisionOf`.
5. **SOLVE-IT KB IRIs** — use `solveit-data:techniqueDFT-*` / `mitigationDFM-*` from the vendored knowledge base.

## Python pattern

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "prov": "http://www.w3.org/ns/prov#",
    "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
    "solveit-data": "https://ontology.solveit-df.org/solveit/data/",
})

plan_id = "kb:plan-1"
graph.upsert_node(plan_id, types="prov:Plan", properties={
    "uco-core:name": "Acquisition plan",
    "uco-core:description": ["Planned: write-block, DFT-1002, DFT-1042."],
})

executed_id = "kb:action-executed"
graph.upsert_node(executed_id, types=[
    "case-investigation:InvestigativeAction",
    "solveit-core:SolveitInvestigativeAction",
    "prov:Activity",
], properties={
    "uco-core:name": "Acquire image (partial)",
    "solveit-core:usedTechnique": [{"@id": "solveit-data:techniqueDFT-1002"}],
    "solveit-core:appliedMitigation": [{"@id": "solveit-data:mitigationDFM-1003"}],
    "prov:hadPlan": {"@id": plan_id},
})

reexec_id = "kb:action-reexec"
graph.upsert_node(reexec_id, types=[
    "case-investigation:InvestigativeAction",
    "solveit-core:SolveitInvestigativeAction",
    "prov:Activity",
], properties={
    "uco-core:name": "Re-execute imaging",
    "solveit-core:usedTechnique": [{"@id": "solveit-data:techniqueDFT-1002"}],
    "prov:hadPlan": {"@id": plan_id},
})
graph.create_relationship(reexec_id, "prov:wasRevisionOf", executed_id)
graph.write("solveit-plan-execution.jsonld")
```

</details>

```bash
python examples/upper-ontology/solveit-plan-execution/build_exemplar.py
```

## Validation

```bash
validate_graph("solveit-plan-execution.jsonld", extensions=["solveit"], profiles=["prov-o"])

case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/solveit/solveit-core.ttl \
  --ontology-graph ontology/upper/shapes/sh-prov-o.ttl \
  --inference rdfs --allow-info solveit-plan-execution.jsonld
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Plan without linked executions | `prov:hadPlan` on each action |
| Executed action missing technique IRI | `solveit-core:usedTechnique` → KB individual |
| Re-run modeled as unrelated action | `prov:wasRevisionOf` |
| Plan typed as `InvestigativeAction` only | Add `prov:Plan` for intent |
| Mitigations listed but not applied | `appliedMitigation` = positive assertions only |

## Related

- [solve-it-investigation-planning.md](solve-it-investigation-planning.md) — objectives, weaknesses, mitigations
- [prov-o-evidence-lineage.md](prov-o-evidence-lineage.md) — activity/entity lineage
- [forensic-lifecycle.md](forensic-lifecycle.md) — phase ordering
- [starter-tool-run.md](starter-tool-run.md) — tool run provenance
