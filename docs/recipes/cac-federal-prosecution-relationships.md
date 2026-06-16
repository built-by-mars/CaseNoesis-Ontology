# Federal Prosecution Relationship Completeness

> See [Recipe Index](INDEX.md) for all recipes.

Model **federal court prosecution graphs** from indictments, criminal complaints, superseding indictments, or hand-extracted fact files — covering single- and multi-defendant cases, **multi-district parallel prosecutions**, child exploitation **enterprise** prosecutions, and **CSAM production/possession/transport** cases.

This recipe focuses on **relationship completeness**: agents often populate typed nodes correctly but omit edges that connect defendants to counts, indictments to charges, prosecutions to districts, conduct to equipment, and forfeiture to enumerated devices. Use this recipe for **any** federal CAC prosecution graph, not only enterprise cases.

Based on validated patterns in `brooklyn-trafficking-april-2025-example.ttl`, `ceos-federal-law-example.ttl`, `rhode-island-production-case.ttl`, and community federal prosecution graphs.

## When to use this recipe

Use when the source describes:

- **Federal charges** (`FederalCharge`, `FederalProsecution`, `PreTrialPhase`)
- **Indictment or criminal complaint** with numbered counts
- **Single or multiple defendants** facing federal CAC counts
- **Multi-district parallel prosecution** (same defendant, charges in more than one federal district)
- **CSAM production, possession, transport, or receipt** under Title 18
- **Child exploitation enterprise** (18 U.S.C. § 2252A(g)) with co-conspirators
- **Forfeiture** of devices or proceeds alleged in the charging instrument

Pair with [cac-production-case.md](cac-production-case.md) for production-environment and equipment typing, and [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) for plea/sentencing follow-on.

## Scope

**Layer 2 — Conduct / offense structure** composed with **Layer 3 — Federal legal workflow**:

- [cac-production-case.md](cac-production-case.md) — production equipment and produced media
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — charge nodes and sentencing
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) — forensic acquisition context
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) — ring structure when applicable
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) — enticement conduct

## Key classes

| Class | Role |
|---|---|
| `uco-core:Bundle` | Top-level case container |
| `CACInvestigation` | Investigation with `case-investigation:focus` |
| `FederalProsecution` / `PreTrialPhase` | Federal legal process (one per lead district) |
| `MultiDefendantIndictment` / charging instrument | Formal indictment or complaint node |
| `FederalCharge` | Individual numbered counts |
| `Person` / `Subject` / `OffenderRole` | Defendant and principal subject |
| `CSAMIncident` | Alleged exploitation conduct |
| `MobileRecordingDevice` | Production/forfeiture smartphones and cameras |
| `AssetForfeitureAction` | Forfeiture allegations |
| `Location` | Court and parallel-district jurisdictions |
| `ChildExploitationEnterprise` | Enterprise cases only (§ 2252A(g)) |
| `ConspiracyToCommitCSA` | Conspiracy anchor when alleged |
| `gufo:Relator` | Enterprise leadership/exploitation mediators |
| `uco-core:Relationship` | Cross-layer bridges (SHACL: UcoObject endpoints) |

## Universal relationship pattern

Agents should produce a **connected** graph, not a flat list of typed nodes inside a Bundle:

```
uco-core:Bundle
  ├── CACInvestigation
  │     ├── Relates_To ──▶ charging instrument (indictment/complaint)
  │     ├── Relates_To ──▶ FederalCharge set and/or CSAMIncident
  │     ├── located_at ──▶ primary court Location
  │     └── parallel_jurisdiction ──▶ parallel district Location(s)
  │
  ├── FederalProsecution (per lead district)
  │     ├── prosecutedBy ──▶ FederalProsecutorRole
  │     ├── hasLegalPhase ──▶ PreTrialPhase
  │     └── Relates_To ──▶ charging instrument
  │
  ├── charging instrument
  │     ├── indictmentCounts (literal)
  │     └── Relates_To ──▶ each FederalCharge
  │
  ├── FederalCharge (one per count; prefix by district when multi-district)
  │     ├── chargeCount (literal)
  │     ├── Relates_To ──▶ CSAMIncident or conduct event
  │     └── Relates_To ──▶ district Location (multi-district cases)
  │
  ├── Person (each defendant)
  │     ├── chargedWith ──▶ FederalCharge (subset per defendant)
  │     └── has_role ──▶ Subject / OffenderRole (principal)
  │
  ├── CSAMIncident
  │     ├── participatesInEvent ◀── Subject
  │     └── used_equipment / usesEquipment ──▶ MobileRecordingDevice(s)
  │
  └── AssetForfeitureAction
        ├── targetedAsset ──▶ each enumerated device (not only aggregate stub)
        └── relatedCriminalCharges ──▶ supporting FederalCharge nodes
```

## Relationship completeness checklist

Before calling `validate_graph`, verify every applicable row:

| # | Edge | Required when | Property / pattern |
|---|---|---|---|
| 1 | **Defendant → counts** | Always | `cacontology-legal-outcomes:chargedWith` on **each** `Person` defendant → specific `FederalCharge` nodes. Never leave orphan charges. |
| 2 | **Indictment → charges** | Charges exist | `uco-core:Relationship` (`Relates_To`) from charging instrument to **each** `FederalCharge`; set `indictmentCounts` and per-charge `chargeCount` literals. |
| 3 | **Prosecution → indictment** | Both exist | `uco-core:Relationship` (`Relates_To`) from `FederalProsecution` to charging instrument. |
| 4 | **Investigation → legal scope** | Always | `Relates_To` from `CACInvestigation` to indictment, prosecution, charges, and/or `CSAMIncident`. Focus-area text alone is insufficient. |
| 5 | **Charge → conduct** | Conduct nodes exist | `Relates_To` or charge `uco-core:description` IRI references to `CSAMIncident`, conspiracy, or platform abuse. |
| 6 | **Principal subject role** | Lead defendant | `uco-core:Relationship` (`has_role`) from principal `Person` to `Subject` / `OffenderRole`; `participatesInEvent` on conduct. |
| 7 | **Multi-district charges → court** | Parallel districts | Each district-prefixed charge (`AK_1`, `TX_1`) gets `Relates_To` → that district's `Location`. Add `parallel_jurisdiction` from investigation to each non-primary district. |
| 8 | **Parallel prosecution** | Multiple district cases | One `FederalProsecution` per district (or document secondary district on parallel `Location` + link its charges). Do not collapse unrelated dockets into one prosecution node without edges. |
| 9 | **Conduct → equipment** | Devices alleged | Link `CSAMIncident` to `MobileRecordingDevice` via `uco-core:Relationship` (`used_equipment`) or `cacontology-production:usesEquipment` on production offense classes. |
| 10 | **Forfeiture → devices + charges** | Forfeiture alleged | `targetedAsset` → **each** enumerated device (not only a generic aggregate stub). Add `relatedCriminalCharges` on `AssetForfeitureAction` per CAC SHACL. |
| 11 | **Provenance** | Court document sourced | `ProvenanceRecord` + extraction `InvestigativeAction`; mark `ALLEGED` where appropriate. |

### Enterprise addendum (when § 2252A(g) alleged)

| # | Edge | Property / pattern |
|---|---|---|
| E1 | Enterprise → indictment | `Relates_To` from `ChildExploitationEnterprise` to charging instrument |
| E2 | Conspiracy → indictment | `cacontology:resultsInIndictment` from `ConspiracyToCommitCSA` |
| E3 | Enterprise members | `hasMember` on enterprise → each defendant `Person` |
| E4 | Relator participants | `gufo:hasParticipant` on every `gufo:Relator` (not label-only shells) |
| E5 | Platform usage | `used_platform` from enterprise or conduct to platform nodes |

## Multi-district parallel prosecution

When the same defendant faces charges in **more than one federal district** (e.g., D. Alaska `3:24-cr-00091` and W.D. Texas `3:25-cr-01046`):

1. Model **each district court** as a `Location` node with case number and filing date in `uco-core:description`.
2. Prefix charge IRIs by district (`charge-AK_1`, `charge-TX_1`) and link each charge to its district court.
3. Add `uco-core:Relationship` (`parallel_jurisdiction`) from `CACInvestigation` to each non-primary district.
4. Optionally add a **second `FederalProsecution`** node for the parallel district with its own `prosecutedBy` role.
5. Apply `chargedWith` on the defendant for **all** counts across districts in one `Person` node (same defendant, multiple dockets).

```
CACInvestigation
  ├── located_at ──▶ D. Alaska (primary)
  ├── parallel_jurisdiction ──▶ W.D. Texas (El Paso)
  └── Relates_To ──▶ all FederalCharge nodes

FederalCharge (AK_1)
  └── Relates_To ──▶ D. Alaska Location

FederalCharge (TX_1)
  └── Relates_To ──▶ W.D. Texas Location
```

## Production equipment and forfeiture

When indictments enumerate **specific devices** for seizure/forfeiture:

1. Type each device as `MobileRecordingDevice` + `ObservableObject` with `deviceBrand`, `deviceModel`, `equipmentType`.
2. Link conduct → device (this edge is often done correctly — preserve it).
3. Link **forfeiture → each device** via `targetedAsset` (multiple assertions allowed).
4. Link **forfeiture → charges** via `relatedCriminalCharges`.
5. Do not leave a generic `forfeiture-asset` stub disconnected from enumerated device nodes when the source names them.

Prefer `cacontology-production:usesEquipment` when the conduct node is a `ProductionOffense` subclass; use `uco-core:Relationship` (`used_equipment`) for `CSAMIncident` when no direct property exists.

## Fact-file template for agents

```text
CASE_ID: 3:24-cr-00091-SLG-KFR
PRIMARY_COURT: U.S. District Court, District of Alaska
FILING_DATE: 2024-08-22
DEFENDANTS: 1
EVIDENTIARY_BASIS: ALLEGED

DEFENDANT_COUNTS:
  Defendant-1: AK_1,AK_2,AK_3,TX_1,TX_2

COUNTS:
  AK_1: Transportation of CSAM — 18 U.S.C. 2252A(a)(1),(b)(1) — District of Alaska
  AK_2: Receipt of CSAM — 18 U.S.C. 2252A(a)(2),(b)(1) — District of Alaska
  AK_3: Possession of CSAM — 18 U.S.C. 2252A(a)(5)(B),(b)(2) — District of Alaska
  TX_1: Attempted sexual exploitation — 18 U.S.C. 2251(a),(e) — W.D. Texas
  TX_2: Receipt of CSAM — 18 U.S.C. 2252(a)(2),(b)(1) — W.D. Texas

PARALLEL_CASES:
  W.D. Texas: 3:25-cr-01046 — filed 2025-05-14 — counts TX_1, TX_2

FORFEITURE_DEVICES:
  Samsung Galaxy S21 Ultra
  Samsung Galaxy S23 Ultra
  Samsung Galaxy S8+

FORFEITURE_STATUTE: 18 U.S.C. 2253
CONDUCT_WINDOW: 2021-03-07 to 2024-05-14
FOCUS_AREAS: CSAM Production; CSAM Possession; Multi-District Prosecution
```

`DEFENDANT_COUNTS` and `PARALLEL_CASES` are the highest-value inputs for edge completeness.

## Python skeleton (multi-district production case)

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
    "cacontology-production": "https://cacontology.projectvic.org/production#",
    "cacontology-asset-forfeiture": "https://cacontology.projectvic.org/asset-forfeiture#",
})

inv = graph.add_node("kb:inv-1", [
    "case-investigation:Investigation", "cacontology:CACInvestigation",
], {
    "case-investigation:name": "U.S. v. Defendant-1 — 3:24-cr-00091",
    "case-investigation:focus": ["CSAM Production", "Multi-District Prosecution"],
})

court_ak = graph.add_node("kb:court-ak", "uco-location:Location", {
    "uco-core:name": "U.S. District Court, District of Alaska",
})
court_tx = graph.add_node("kb:court-tx", "uco-location:Location", {
    "uco-core:name": "U.S. District Court, Western District of Texas (El Paso)",
})

indictment = graph.add_node("kb:indictment-1", "cacontology:MultiDefendantIndictment", {
    "uco-core:name": "Federal indictment — D. Alaska and W.D. Texas",
    "cacontology:indictmentCounts": {"@type": "xsd:nonNegativeInteger", "@value": "5"},
})

prosecution = graph.add_node("kb:prosecution-1", "cacontology-usa-federal-law:FederalProsecution", {
    "uco-core:name": "Federal prosecution — D. Alaska",
})

charge_ak1 = graph.add_node("kb:charge-ak-1", "cacontology-legal-outcomes:FederalCharge", {
    "uco-core:name": "Count AK-1 — Transportation of CSAM",
    "cacontology-legal-outcomes:chargeCount": {"@type": "xsd:nonNegativeInteger", "@value": "1"},
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
    "uco-core:name": "Alleged CSAM production and possession",
})

defendant = graph.add_node("kb:defendant-1", "uco-identity:Person", {
    "uco-core:name": "Defendant-1",
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-ak-1"}],
})

forfeiture = graph.add_node("kb:forfeiture-1", "cacontology-asset-forfeiture:AssetForfeitureAction", {
    "uco-core:name": "Alleged asset forfeiture under 18 U.S.C. 2253",
    "cacontology-asset-forfeiture:targetedAsset": {"@id": "kb:device-1"},
    "cacontology-asset-forfeiture:relatedCriminalCharges": [{"@id": "kb:charge-ak-1"}],
})

# Relationship edges (representative set)
for rel_id, src, tgt, kind in [
    ("rel-inv-indictment", "kb:inv-1", "kb:indictment-1", "Relates_To"),
    ("rel-prosecution-indictment", "kb:prosecution-1", "kb:indictment-1", "Relates_To"),
    ("rel-indictment-charge", "kb:indictment-1", "kb:charge-ak-1", "Relates_To"),
    ("rel-charge-court", "kb:charge-ak-1", "kb:court-ak", "Relates_To"),
    ("rel-charge-conduct", "kb:charge-ak-1", "kb:csam-1", "Relates_To"),
    ("rel-inv-parallel", "kb:inv-1", "kb:court-tx", "parallel_jurisdiction"),
    ("rel-conduct-device", "kb:csam-1", "kb:device-1", "used_equipment"),
]:
    graph.add_node(f"kb:{rel_id}", "uco-core:Relationship", {
        "uco-core:source": {"@id": src},
        "uco-core:target": {"@id": tgt},
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
    })

graph.write("federal-prosecution-relationships.jsonld")
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| 5 `FederalCharge` nodes, 0 `chargedWith` | Add `chargedWith` from `DEFENDANT_COUNTS` |
| Charges and indictment in Bundle only | Add indictment `Relates_To` each charge |
| `FederalProsecution` disconnected from indictment | Add prosecution `Relates_To` indictment |
| Parallel district in description only | Add `parallel_jurisdiction` + per-charge district links |
| Generic forfeiture stub, enumerated devices elsewhere | `targetedAsset` → each device; add `relatedCriminalCharges` |
| Devices linked to conduct but not forfeiture | Bridge forfeiture to same device nodes |
| `MultiDefendantIndictment` for single defendant | Acceptable when instrument type is unknown; still wire all charge edges |
| Empty `gufo:Relator` (enterprise cases) | Add `gufo:hasParticipant` |

## Validation

```bash
validate_graph("federal-prosecution-relationships.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-production-case.md](cac-production-case.md) — production environments and produced media
- [cac-legal-sentencing-outcomes.md](cac-legal-sentencing-outcomes.md) — press-release and sentencing patterns
- [cac-trafficking-recruitment-network.md](cac-trafficking-recruitment-network.md) — recruitment ring structure
- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md) — pre-indictment ICAC pattern
- [forensic-lifecycle.md](forensic-lifecycle.md) — provenance and extraction actions
