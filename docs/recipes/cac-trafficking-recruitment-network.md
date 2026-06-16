# Child Sex Trafficking and Recruitment Networks

> See [Recipe Index](INDEX.md) for all recipes.

Model child sex trafficking enterprises, recruitment networks, and digital-to-physical escalation using [CAC Ontology](https://cacontology.projectvic.org/) classes on top of core CASE/UCO investigation containers. For institutional task-force response, see [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md). For victim extraction after identification, see [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md).

## Scope

**Layer 2 — Behavioral / enterprise structure** plus supporting **Layer 1 evidence** (locations, accounts, transport artifacts).

## Key classes

| Class | Role |
|---|---|
| `CACInvestigation` | Investigation container (multi-typed on `case-investigation:Investigation`) |
| `TraffickingEnterprise` / `TraffickingRing` / `TraffickingCell` | Structural anchor for the criminal network |
| `TraffickingVictimRole` / `MinorTraffickingVictimRole` | Victim role borne by Identity via `has-role` |
| `PeerRecruitmentNetwork` / `ClassmateRecruitmentNetwork` | School-based recruitment structures |
| `SchoolBasedRecruitment` / `StreetBasedRecruitment` | Recruitment context |
| `HelpOfferApproach` / `FoodOfferApproach` / `TransportationOfferApproach` | Pretext approach subclasses |
| `DigitalToPhysicalBridge` | Online contact → in-person meet transition |
| `VictimRotation` / `InterstateVictimTransport` | Movement patterns across victims or jurisdictions |
| `Identity` / `Location` / `Relationship` | Core CASE/UCO anchors |

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

## Modeling rules

- Use **specific approach subclasses** (`TransportationOfferApproach`, not generic `InvestigativeAction`) so analysts can query pretext patterns.
- Split **online recruitment** and **in-person meet** into separate events linked by `DigitalToPhysicalBridge`.
- Model the ring as `TraffickingEnterprise`, not a single `Identity`.
- Physical items (condoms, hotel keys) → `uco-core:UcoObject`; digital artifacts (DMs, ads) → `uco-observable:ObservableObject`.

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={"cacontology": "https://cacontology.projectvic.org#"})
inv = graph.add_node("kb:inv-1", "case-investigation:Investigation", {
    "case-investigation:name": "Trafficking Ring 2026-014",
})
ring = graph.add_node("kb:ring-1", "cacontology-sex-trafficking:TraffickingRing", {
    "uco-core:name": "Brooklyn cell",
})
graph.write("trafficking-ring.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=trafficking-ring.jsonld
```

Or via MCP: `validate_graph("trafficking-ring.jsonld", extensions=["cac"])`.

## Related recipes

- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) — when recruitment starts in chat/DM
- [cac-multi-jurisdiction-task-force.md](cac-multi-jurisdiction-task-force.md) — joint enforcement response
- [cross-domain-extensions.md](cross-domain-extensions.md) — extension setup
