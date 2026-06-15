# International Coordination and Cross-Border Operations

> See [Recipe Index](INDEX.md) for all recipes.

Model transnational child exploitation investigations, Europol/Interpol coordination, extradition, and cross-border evidence sharing using CAC international module classes.

## Scope

**Layer 3 — Institutional workflow** extending multi-jurisdiction patterns to international boundaries.

## Key classes

| Class | Role |
|---|---|
| `InternationalJurisdiction` | Foreign jurisdiction node |
| `CrossBorderOperation` | Coordinated international operation |
| `ExtraditionProcess` | Extradition workflow |
| `InternationalEvidenceSharing` | Cross-border evidence transfer |
| `InterpolCoordination` / `EuropolCoordination` | Agency coordination nodes |
| `TaskForce` / `JointInvestigation` | Shared with domestic multi-jurisdiction pattern |

## Canonical pattern

```
JointInvestigation
  ├── FederalJurisdiction (domestic lead)
  ├── InternationalJurisdiction (foreign partner)
  └── CrossBorderOperation
        ├── InterpolCoordination / EuropolCoordination
        └── InternationalEvidenceSharing
```

## Modeling rules

- Use `InternationalJurisdiction` for foreign partners — do not overload domestic jurisdiction classes.
- Model **evidence sharing** as its own auditable action with `ProvenanceRecord`.
- Chain domestic task-force structure from [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-international": "https://cacontology.projectvic.org/international#",
})
op = graph.add_node("kb:op-1", "cacontology-international:CrossBorderOperation", {
    "uco-core:name": "Europol coordinated takedown",
})
graph.write("international-op.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=international-op.jsonld
```

## Related recipes

- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md)
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md)
