# Victim Rescue, Extraction, and Post-Rescue Services

> See [Recipe Index](INDEX.md) for all recipes.

Model emergency response, victim extraction, ongoing danger assessment, safety planning, and multi-agency victim services after a child is identified in danger.

## Scope

**Layer 3 — Institutional workflow** with victim-centered service linkage.

## Key classes

| Class | Role |
|---|---|
| `EmergencyResponse` | Initial crisis response activation |
| `VictimExtraction` | Physical removal from danger location |
| `OngoingDangerAssessment` | Continued threat evaluation |
| `SafetyPlanning` | Safety plan with CPS/DCFS or partner agencies |
| `MultiAgencyVictimResponse` | Coordinated service delivery |
| `TraumaIndicator` / `HelpSeekingBarrier` | Victim presentation factors |
| `RecantationAssessment` / `ReaffirmedDisclosureStatement` | Disclosure dynamics |
| `ChildVictim` | Victim identity anchor |

## Canonical pattern

```
EmergencyResponse
  └── result ──▶ VictimExtraction
        ├── OngoingDangerAssessment
        ├── SafetyPlanning
        └── MultiAgencyVictimResponse
              └── TraumaIndicator + HelpSeekingBarrier (as documented)
```

## Modeling rules

- Post-rescue services are **in scope** — model `SafetyPlanning` and `MultiAgencyVictimResponse`.
- **Recantation** is its own event; it does not automatically close the investigation.
- Link each extraction to a `ProvenanceRecord` when chain-of-custody for the victim contact is documented.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph()
extraction = graph.add_node("kb:extract-1", "cacontology:VictimExtraction", {
    "uco-core:name": "Victim extraction at motel",
})
graph.write("victim-rescue.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=victim-rescue.jsonld
```

## Related recipes

- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md)
- [cac-missing-child-investigation.md](cac-missing-child-investigation.md)
- [chain-of-custody.md](chain-of-custody.md)
