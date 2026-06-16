# CSAM Production and Manufacturing Cases

> See [Recipe Index](INDEX.md) for all recipes.

Model hands-on abuse and offender-produced CSAM cases including production environments, equipment, and produced-media artifacts using CAC production module classes.

When the source is a **federal court filing** (indictment, complaint) alleging production/possession/transport with enumerated devices and forfeiture, also follow [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) for legal relationship completeness.

## Scope

**Layer 2 — Behavioral / offense type** with strong **Layer 1 evidence** (images, video, devices, locations).

## Key classes

| Class | Role |
|---|---|
| `ProductionCase` | Overarching production offense container |
| `ProducedImage` / `ProducedVideo` | Offender-produced media (multi-typed observables) |
| `ProductionEnvironment` | Location/setup where production occurred |
| `MobileRecordingDevice` / `RecordingEquipment` | Cameras, phones used to produce material |
| `ChildVictim` | Victim identity |
| `ForensicAcquisitionAction` | Evidence collection from production site |
| `CSAMIncident` | Conduct event when modeled at incident level |
| `AssetForfeitureAction` | Device/proceeds forfeiture when alleged in filings |

## Canonical pattern

```
ProductionCase (or CSAMIncident)
  ├── involves ──▶ ChildVictim / VictimRole
  ├── occurredAt ──▶ ProductionEnvironment
  ├── usesEquipment ──▶ MobileRecordingDevice
  └── evidencedBy ──▶ ProducedImage / ProducedVideo
        └── ContentDataFacet (hashes required)

AssetForfeitureAction
  ├── targetedAsset ──▶ each enumerated MobileRecordingDevice
  └── relatedCriminalCharges ──▶ FederalCharge nodes
```

## Modeling rules

- Multi-type produced media as `ObservableObject` + `ProducedImage`/`ProducedVideo`.
- Physical equipment → `MobileRecordingDevice` with `deviceBrand` and `deviceModel` when known.
- Link conduct to equipment: `cacontology-production:usesEquipment` on production offense classes, or `uco-core:Relationship` (`used_equipment`) on `CSAMIncident`.
- When forfeiture is alleged, link **each named device** via `targetedAsset` — not only a generic aggregate asset stub.
- Add `relatedCriminalCharges` on `AssetForfeitureAction` linking to supporting `FederalCharge` nodes (CAC SHACL requires this).
- Always pair produced artifacts with forensic acquisition when post-seizure context exists — see [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md).
- For federal indictment graphs, apply the full checklist in [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-production": "https://cacontology.projectvic.org/production#",
    "cacontology-asset-forfeiture": "https://cacontology.projectvic.org/asset-forfeiture#",
})

device = graph.add_node("kb:device-1", [
    "uco-observable:ObservableObject",
    "cacontology-production:MobileRecordingDevice",
], {
    "uco-core:name": "Samsung Galaxy S21 Ultra",
    "cacontology-production:deviceBrand": "Samsung",
    "cacontology-production:deviceModel": "Galaxy S21 Ultra",
})

csam = graph.add_node("kb:csam-1", "cacontology:CSAMIncident", {
    "uco-core:name": "Alleged CSAM production",
})

graph.add_node("kb:rel-device", "uco-core:Relationship", {
    "uco-core:source": {"@id": "kb:csam-1"},
    "uco-core:target": {"@id": "kb:device-1"},
    "uco-core:kindOfRelationship": "used_equipment",
    "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
})

graph.write("production-case.jsonld")
```

## Validation

```bash
validate_graph("production-case.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — federal indictment relationship wiring
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md)
- [exif-data.md](exif-data.md)
- [device.md](device.md)
