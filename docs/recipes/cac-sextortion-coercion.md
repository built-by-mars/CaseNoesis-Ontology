# Sextortion and Online Coercion

> See [Recipe Index](INDEX.md) for all recipes.

Model sextortion schemes where offenders coerce minors through threats to share explicit images, financial demands, or compliance pressure. Combines **Layer 1 evidence** (messages, images) with **Layer 2 CAC interpretation**.

## Scope

**Layer 2 — Behavioral interpretation** for coercion dynamics; link to [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) when grooming precedes sextortion.

## Key classes

| Class | Role |
|---|---|
| `SextortionScheme` | Overarching coercion behavior |
| `CoercionDemand` / `FinancialExtortionDemand` | Demand events |
| `CompliancePressure` | Escalating pressure on the victim |
| `ThreatToDisclose` | Threat to publish explicit material |
| `ChildVictim` / `OnlinePredator` | Role-bearing identities |
| `Message` / `RasterPicture` | Digital evidence artifacts |
| `OffenderRole` / `VictimRole` | CAC role objects via `has-role` |

## Canonical pattern

```
MessageThread (evidence)
  └── interpreted as ──▶ SextortionScheme
        ├── ThreatToDisclose
        ├── CoercionDemand
        └── CompliancePressure
              └── targets ──▶ ChildVictim (Identity + VictimRole)
```

## Modeling rules

- Keep **raw messages** in Layer 1; add CAC coercion types in Layer 2 as multi-typed interpretations.
- Document **financial vs. image-disclosure** coercion paths with the appropriate demand subclass.
- Link platform accounts and IP addresses when CyberTip reporting is in scope — see [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-sextortion": "https://cacontology.projectvic.org/sextortion#",
})
scheme = graph.add_node("kb:sextort-1", "cacontology-sextortion:SextortionScheme", {
    "uco-core:name": "Snapchat sextortion scheme",
})
graph.write("sextortion-case.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=sextortion-case.jsonld
```

## Related recipes

- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md)
- [threaded-messaging.md](threaded-messaging.md)
- [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md)
