# CSAM Production and Manufacturing Cases

> See [Recipe Index](INDEX.md) for all recipes.

Model hands-on abuse and offender-produced CSAM cases including production environments, equipment, and produced-media artifacts using CAC production module classes.

## Scope

**Layer 2 — Behavioral / offense type** with strong **Layer 1 evidence** (images, video, devices, locations).

## Key classes

| Class | Role |
|---|---|
| `ProductionCase` | Overarching production offense container |
| `ProducedImage` / `ProducedVideo` | Offender-produced media (multi-typed observables) |
| `ProductionEnvironment` | Location/setup where production occurred |
| `RecordingEquipment` | Cameras, phones used to produce material |
| `ChildVictim` | Victim identity |
| `ForensicAcquisitionAction` | Evidence collection from production site |

## Canonical pattern

```
ProductionCase
  ├── involves ──▶ ChildVictim
  ├── occurredAt ──▶ ProductionEnvironment
  ├── usedEquipment ──▶ RecordingEquipment
  └── evidencedBy ──▶ ProducedImage / ProducedVideo
        └── ContentDataFacet (hashes required)
```

## Modeling rules

- Multi-type produced media as `ObservableObject` + `ProducedImage`/`ProducedVideo`.
- Physical equipment → `UcoObject` or device observables; produced files → `ObservableObject`.
- Always pair produced artifacts with forensic acquisition and verification — see [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-production": "https://cacontology.projectvic.org/production#",
})
case = graph.add_node("kb:prod-1", "cacontology-production:ProductionCase", {
    "uco-core:name": "Hands-on production case",
})
graph.write("production-case.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=production-case.jsonld
```

## Related recipes

- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md)
- [exif-data.md](exif-data.md)
- [device.md](device.md)
