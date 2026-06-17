# Child Sex Trafficking and Recruitment Networks

> See [Recipe Index](INDEX.md) for all recipes.

Model child sex trafficking enterprises, **solo-operator federal § 1591 prosecutions**, recruitment networks, and digital-to-physical escalation using [CAC Ontology](https://cacontology.projectvic.org/) classes on top of core CASE/UCO investigation containers. For institutional task-force response, see [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md). For victim extraction after identification, see [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md). For indictment charge wiring and superseding instruments, see [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) and [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md).

## Scope

**Layer 2 — Behavioral / enterprise structure** plus supporting **Layer 1 evidence** (locations, accounts, transport artifacts) and **Layer 3 — Federal prosecution** when § 1591 counts appear in indictments.

## Key classes

| Class | Role |
|---|---|
| `CACInvestigation` | Investigation container (multi-typed on `case-investigation:Investigation`) |
| `TraffickingEnterprise` / `TraffickingRing` / `TraffickingCell` | Structural anchor for multi-trafficker networks |
| `CommercialSexualExploitation` | In-person commercial sex acts (solo or ring) |
| `SexTraffickingOfMinors` | Federal conduct type aligned with 18 U.S.C. § 1591 |
| `MinorTraffickingVictimRole` | Per-victim role when indictment names Minor Victim 1–N |
| `VictimTransportation` | Rideshare/taxi/hotel transport to exploitation locations |
| `DigitalToPhysicalBridge` | Online contact → in-person meet transition |
| `PeerRecruitmentNetwork` / `ClassmateRecruitmentNetwork` | School-based recruitment structures |
| `TransportationOfferApproach` | Rides, hotels, money as commercial inducements |
| `FederalCharge` | § 1591, § 2422, § 2251 stacked counts per victim |
| `Location` | Hotels, apartments, vehicles, beaches |
| `ApplicationAccount` / platform nodes | Grindr, Snapchat, text messaging |

## Canonical pattern

```
CACInvestigation
  └── TraffickingRing (or TraffickingCell)
        ├── employs / controls ──▶ Identity (trafficker)
        ├── targets ──▶ MinorTraffickingVictimRole ──▶ Identity (victim)
        └── uses ──▶ PeerRecruitmentNetwork

SchoolBasedRecruitment
  └── approach ──▶ TransportationOfferApproach
        └── DigitalToPhysicalBridge (IG DM → motel meet)
```

## Solo-operator federal child sex trafficking (§ 1591)

Many federal **child sex trafficking** cases involve a **single defendant** recruiting multiple minor victims through dating/social apps — not a multi-trafficker ring. Do **not** force a `TraffickingRing` when the source describes one operator and enumerated minor victims.

```
Person (defendant / Primary Trafficker Role)
  ├── chargedWith ──▶ FederalCharge (Count 4 — § 1591) … per victim
  └── participatesInEvent ──▶ CommercialSexualExploitation (per victim)

MinorTraffickingVictimRole (MV2)
  ├── exploitedIn ──▶ CommercialSexualExploitation
  └── linked counts ──▶ FederalCharge 3, 4, 5

DigitalToPhysicalBridge (Grindr → in-person)
  ├── used_platform ──▶ Grindr
  └── resultsIn ──▶ CommercialSexualExploitation at Location (hotel/apartment)

VictimTransportation
  ├── transportationMethod: Uber / Lyft / taxi
  └── destinationLocation ──▶ hotel or defendant residence
```

Modeling rules:

1. Create one **`MinorTraffickingVictimRole`** (or anonymized victim node) per **Minor Victim N** in the indictment or trial brief.
2. Link each victim to **their specific counts** via `Relates_To` from `FederalCharge` — counts often stack production (§ 2251), trafficking (§ 1591), enticement (§ 2422), and distribution/receipt (§ 2252) for the **same victim**.
3. Model **commercial inducements** (money offers, phones, hotel payment) on `CommercialSexualExploitation` or `TransportationOfferApproach` — these support the commercial sex act element of § 1591.
4. Model **Grindr → text → in-person** as `DigitalToPhysicalBridge` linked to [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) message evidence when available.
5. Model **rideshare/taxi transport** as `VictimTransportation` with origin/destination `Location` nodes when the trial brief or indictment describes arranged transport.
6. Document **substance facilitation** (drugs provided during encounters) in conduct `uco-core:description` when alleged — link to the same exploitation event.
7. For **multiple victims across years**, use separate exploitation nodes with temporal bounds rather than one aggregate CSAM incident.

### Per-victim charge bundle matrix

Indictments often assign **different count groups per minor victim**:

```text
VICTIM_COUNTS:
  MV1: 1,2,12        # production x2 + aggregate possession
  MV2: 3,4,5          # production + trafficking + distribution
  MV3: 6,7,8          # trafficking + enticement + receipt
  MV4: 9,10           # trafficking + enticement
  MV5: 11             # trafficking only
```

Each row drives:
- `Relates_To` from each `FederalCharge` → victim role node
- `Relates_To` from each charge → conduct type (`CSAMIncident`, `CommercialSexualExploitation`, enticement event)
- Trial brief sections → same victim IRIs for anticipated testimony

### Stacked statutes per encounter

When one encounter supports multiple counts (production video + trafficking + distribution to same victim):

```
CommercialSexualExploitation (MV2 — Aug 2019, Waikiki apartment)
  ├── Relates_To ◀── FederalCharge Count 4 (§ 1591)
  ├── Relates_To ◀── FederalCharge Count 3 (§ 2251 production)
  └── Relates_To ◀── FederalCharge Count 5 (§ 2252 distribution)
```

## Modeling rules (network cases)

- Use **specific approach subclasses** (`TransportationOfferApproach`, not generic `InvestigativeAction`) so analysts can query pretext patterns.
- Split **online recruitment** and **in-person meet** into separate events linked by `DigitalToPhysicalBridge`.
- Model the ring as `TraffickingEnterprise`, not a single `Identity`.
- Physical items (condoms, hotel keys) → `uco-core:UcoObject`; digital artifacts (DMs, ads) → `uco-observable:ObservableObject`.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-trafficking": "https://cacontology.projectvic.org/trafficking#",
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
})

victim2 = graph.add_node("kb:mv2", "cacontology-trafficking:MinorTraffickingVictimRole", {
    "uco-core:name": "Minor Victim 2",
})

exploitation = graph.add_node("kb:cse-mv2", "cacontology-trafficking:CommercialSexualExploitation", {
    "uco-core:name": "Alleged commercial sexual exploitation — MV2",
})

charge_trafficking = graph.add_node("kb:charge-4", "cacontology-legal-outcomes:FederalCharge", {
    "uco-core:name": "Count 4 — Sex trafficking a minor (18 U.S.C. 1591)",
    "cacontology-legal-outcomes:chargeCount": {"@type": "xsd:nonNegativeInteger", "@value": "4"},
})

defendant = graph.add_node("kb:defendant-1", "uco-identity:Person", {
    "uco-core:name": "Defendant-1",
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-4"}],
})

for rel_id, src, tgt in [
    ("rel-charge-victim", "kb:charge-4", "kb:mv2"),
    ("rel-charge-conduct", "kb:charge-4", "kb:cse-mv2"),
]:
    graph.add_node(f"kb:{rel_id}", "uco-core:Relationship", {
        "uco-core:source": {"@id": src},
        "uco-core:target": {"@id": tgt},
        "uco-core:kindOfRelationship": "Relates_To",
        "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
    })

graph.write("trafficking-solo-operator.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=trafficking-ring.jsonld
```

Or via MCP: `validate_graph("trafficking-ring.jsonld", extensions=["cac"])`.

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — defendant→counts, forfeiture, indictment bridges
- [cac-federal-trial-proceedings.md](cac-federal-trial-proceedings.md) — superseding indictment, docket, trial brief
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) — Grindr/messaging evidence layer
- [cac-production-case.md](cac-production-case.md) — production counts stacked with trafficking
- [cac-csam-forensic-provenance.md](cac-csam-forensic-provenance.md) — multi-device CSAM exhibits
- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md) — joint enforcement response
- [cross-domain-extensions.md](cross-domain-extensions.md) — extension setup
