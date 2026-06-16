# Sextortion and Online Coercion

> See [Recipe Index](INDEX.md) for all recipes.

Model sextortion schemes where offenders coerce minors through threats to share explicit images, financial demands, or compliance pressure. Combines **Layer 1 evidence** (messages, images) with **Layer 2 CAC interpretation** and **Layer 3 federal prosecution** when indictments stack CSEA counts with cyberstalking, identity theft, and wire fraud.

## Scope

**Layer 2 — Behavioral interpretation** for coercion dynamics; link to [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md) when grooming precedes sextortion.

**Layer 3 — Federal prosecution** when the source is an indictment or complaint: compose with [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) for `chargedWith`, indictment bridges, and charge stacking. Use [cac-international-coordination.md](cac-international-coordination.md) when the defendant is abroad and extradition is alleged.

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
| `FederalCharge` | Numbered counts (CSEA, cyberstalking, fraud) |
| `FederalProsecution` / `MultiDefendantIndictment` | Court filing structure |
| `ChildExploitationEnterprise` | When § 2252A(g) alleged alongside sextortion |
| `ExtraditionProcess` | Defendant abroad → U.S. prosecution |
| `InternationalJurisdiction` / `Location` | Foreign residence and filing court |

## Canonical pattern (Layer 2 conduct)

```
MessageThread (evidence)
  └── interpreted as ──▶ SextortionScheme
        ├── ThreatToDisclose
        ├── CoercionDemand
        ├── CompliancePressure
        ├── Impersonation (posed as peer/influencer)
        └── used_platform ──▶ Instagram / Snapchat / Dropbox
              └── targets ──▶ ChildVictim (Identity + VictimRole)
```

## Federal prosecution bridge (Layer 3)

Sextortion indictments often **stack** non-CSEA counts on top of exploitation charges. Agents must wire both behavioral and legal layers:

```
uco-core:Bundle
  ├── SextortionScheme
  │     ├── Relates_To ◀── FederalCharge (cyberstalking § 2261A)
  │     ├── Relates_To ◀── FederalCharge (wire fraud § 1343)
  │     └── used_platform ──▶ platform nodes
  │
  ├── FederalProsecution
  │     └── Relates_To ──▶ MultiDefendantIndictment
  │
  ├── FederalCharge (Count 1 — conspiracy to produce)
  │     └── Relates_To ──▶ SextortionScheme / CSAMIncident
  │
  ├── FederalCharge (Count 3 — enterprise § 2252A(g))
  │     └── Relates_To ──▶ ChildExploitationEnterprise
  │
  ├── FederalCharge (Count 6 — cyberstalking)
  │     └── Relates_To ──▶ SextortionScheme
  │
  ├── FederalCharge (Counts 7–8 — aggravated identity theft § 1028A)
  │     └── Relates_To ──▶ SextortionScheme (impersonation conduct)
  │
  ├── FederalCharge (Counts 9–13 — wire fraud § 1343)
  │     └── Relates_To ──▶ SextortionScheme / FinancialExtortionDemand
  │
  ├── Person (defendant)
  │     └── chargedWith ──▶ all applicable FederalCharge nodes
  │
  └── ExtraditionProcess (when defendant abroad)
        ├── Relates_To ──▶ Person (defendant)
        └── Relates_To ──▶ FederalProsecution
```

### Relationship checklist (sextortion + federal)

| # | Edge | When | Pattern |
|---|---|---|---|
| S1 | Scheme → charges | Indictment sourced | `Relates_To` from each `FederalCharge` to `SextortionScheme`, `CSAMIncident`, or enterprise |
| S2 | `chargedWith` | Always | Single-defendant cases still need `chargedWith` on the defendant `Person` |
| S3 | Cyberstalking count | § 2261A alleged | Dedicated `FederalCharge` linked to `SextortionScheme` (not only description text) |
| S4 | Identity theft counts | § 1028A alleged | Link to impersonation conduct node or scheme |
| S5 | Wire fraud counts | § 1343 alleged | Link to `FinancialExtortionDemand` or scheme; grouped counts (`9_13`) acceptable when indictment groups them |
| S6 | Enterprise count | § 2252A(g) in same case | Compose enterprise addendum from federal prosecution recipe |
| S7 | Co-conspirator narrative | Paragraphs name co-conspirators | `hasMember` on enterprise + `participatesInEvent` on conspiracy |
| S8 | Extradition chain | Defendant abroad | `ExtraditionProcess` → defendant + prosecution; foreign `Location` |
| S9 | Platform affordance abuse | Ban evasion / account recreation | `used_platform` edges + ban-evasion detail in `uco-core:description` on platform or scheme |
| S10 | Impersonation → scheme | Posed-as-peer alleged | `Relates_To` from impersonation node to `SextortionScheme` |

Grouped multi-count nodes (e.g., `charge-7_8`, `charge-9_13`) are acceptable when the indictment treats counts as a group **if** `chargedWith` and `Relates_To` to conduct are still present.

## Modeling rules

- Keep **raw messages** in Layer 1; add CAC coercion types in Layer 2 as multi-typed interpretations.
- Document **financial vs. image-disclosure** coercion paths with the appropriate demand subclass.
- Link platform accounts and IP addresses when CyberTip reporting is in scope — see [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md).
- When platform sections in an indictment define **affordances** (DMs, stories, account recreation after ban), model platforms as nodes and link `used_platform` from scheme or enterprise — do not bury affordance detail only in indictment description on the Bundle.
- For **ban evasion** (dozens of recreated accounts), record counts in enterprise or scheme `uco-core:description` and link each primary platform node via `used_platform`.
- Always run the [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) checklist when building from an indictment.

## Fact-file template

```text
CASE_ID: 3:22-cr-00055-SLG-KFR
PRIMARY_COURT: U.S. District Court, District of Alaska
DEFENDANTS: 1
DEFENDANT_COUNTS:
  AMIN: 1,2,3,4,5,6,7,8,9,10,11,12,13

CHARGE_STACK:
  1-5: CSEA (conspiracy, enterprise, production, receipt/distribution)
  6: Cyberstalking — 18 U.S.C. 2261A
  7-8: Aggravated identity theft — 18 U.S.C. 1028A
  9-13: Wire fraud — 18 U.S.C. 1343

PLATFORMS: Instagram, Snapchat, Dropbox
TRANSNATIONAL: defendant citizen of Bangladesh, residing Malaysia
EXTRADITION: alleged extradition to U.S. for prosecution
```

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-sextortion": "https://cacontology.projectvic.org/sextortion#",
    "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
    "cacontology-usa-federal-law": "https://cacontology.projectvic.org/usa-federal-law#",
})

scheme = graph.add_node("kb:sextort-1", "cacontology-sextortion:SextortionScheme", {
    "uco-core:name": "Snapchat sextortion scheme",
})

charge_cyber = graph.add_node("kb:charge-6", "cacontology-legal-outcomes:FederalCharge", {
    "uco-core:name": "Count 6 — Cyberstalking (18 U.S.C. 2261A)",
    "cacontology-legal-outcomes:chargeCount": {"@type": "xsd:nonNegativeInteger", "@value": "6"},
})

defendant = graph.add_node("kb:defendant-1", "uco-identity:Person", {
    "uco-core:name": "Defendant-1",
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-6"}],
})

graph.add_node("kb:rel-charge-scheme", "uco-core:Relationship", {
    "uco-core:source": {"@id": "kb:charge-6"},
    "uco-core:target": {"@id": "kb:sextort-1"},
    "uco-core:kindOfRelationship": "Relates_To",
    "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
})

graph.write("sextortion-case.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=sextortion-case.jsonld
```

## Related recipes

- [cac-federal-prosecution-relationships.md](cac-federal-prosecution-relationships.md) — indictment edges and charge stacking
- [cac-international-coordination.md](cac-international-coordination.md) — extradition and cross-border prosecution
- [cac-grooming-chat-modeling.md](cac-grooming-chat-modeling.md)
- [cac-production-case.md](cac-production-case.md) — production counts in sextortion indictments
- [threaded-messaging.md](threaded-messaging.md)
- [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md)
