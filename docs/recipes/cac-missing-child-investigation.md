# Missing Child Investigations

> See [Recipe Index](INDEX.md) for all recipes.

Model missing-child cases including AMBER alerts, stranger abduction investigations, runaway tracking, and recovery operations using CAC abduction and investigation-coordination classes.

## Scope

**Layer 3 — Institutional workflow** with location and communications evidence support.

## Key classes

| Class | Role |
|---|---|
| `MissingChildReport` | Initial missing-person report |
| `StrangerAbductionInvestigation` | Stranger-abduction case type |
| `AMBERAlertActivation` | Alert issuance |
| `LocationTrackingAction` | Cell-site / GPS tracking steps |
| `ChildRecovery` | Successful recovery event |
| `CACInvestigation` | Investigation container |
| `CellSiteFacet` / `LatLongCoordinatesFacet` | Location evidence |

## Canonical pattern

```
MissingChildReport
  └── triggers ──▶ CACInvestigation
        ├── AMBERAlertActivation (when criteria met)
        ├── LocationTrackingAction (CDR / cell-site / GPS)
        └── ChildRecovery (when located)
```

## Modeling rules

- Separate **report**, **alert**, **tracking**, and **recovery** into distinct actions.
- Link location evidence via `CellSiteFacet` or `LatLongCoordinatesFacet` — see [cell-site.md](cell-site.md).
- When rescue involves extraction from ongoing danger, chain to [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-stranger-abduction": "https://cacontology.projectvic.org/abduction#",
})
report = graph.add_node("kb:missing-1", "cacontology-stranger-abduction:MissingChildReport", {
    "uco-core:name": "Missing 14-year-old report",
})
graph.write("missing-child.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=missing-child.jsonld
```

## Related recipes

- [cell-site.md](cell-site.md)
- [location.md](location.md)
- [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md)
