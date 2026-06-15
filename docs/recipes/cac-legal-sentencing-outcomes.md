# Legal Charges, Sentencing, and Case Outcomes

> See [Recipe Index](INDEX.md) for all recipes.

Model indictments, charges, plea agreements, sentencing, supervised release, and sex-offender registry outcomes using CAC legal-outcomes module classes.

## Scope

**Layer 3 — Institutional workflow** for post-investigation legal disposition.

## Key classes

| Class | Role |
|---|---|
| `CriminalCharge` / `ChargeSet` | Formal charges |
| `StateCharge` / `FloridaStateCharge` / `GeorgiaStateCharge` | Jurisdiction-specific charges |
| `PleaAgreement` | Plea disposition |
| `SentencingOutcome` / `PrisonSentence` / `SupervisedRelease` | Sentencing results |
| `SexOffenderRegistryEntry` | Registry integration when applicable |
| `StatuteReference` | Statutory basis |
| `CACInvestigation` | Source investigation linkage |
| `Identity` | Defendant / subject |

## Maryland press-release pattern

Maryland ICAC arrest articles often report charges before sentencing. Until `MarylandStateCharge` subclasses are added to the CAC ontology (like Florida and Georgia), model Maryland counts as generic `StateCharge`:

| Press language | Modeling |
|---|---|
| Sexual solicitation of a minor | `StateCharge` + `uco-core:name` + `skos:altLabel` "Sexual Solicitation of a Minor" |
| Knowingly permitting sexual solicitation of a minor | separate `StateCharge` node |
| Held without bond | document on `BookingAction` / `CorrectionalFacility` description |
| Transported to detention center | `BookingAction` → `CorrectionalFacility` |

```python
charge = graph.add_node("kb:charge-1", "cacontology-legal-outcomes:StateCharge", {
    "uco-core:name": "Sexual Solicitation of a Minor",
    "uco-core:description": "Maryland state charge reported in press release.",
    "cacontology-legal-outcomes:chargeLevel": "felony",
    "cacontology-legal-outcomes:chargeCount": {
        "@type": "xsd:nonNegativeInteger", "@value": "1",
    },
})
graph.add_node("kb:suspect", "uco-identity:Person", {
    "cacontology-legal-outcomes:chargedWith": [{"@id": "kb:charge-1"}],
})
```

**Ontology gap:** Consider a change proposal for `MarylandStateCharge` subclasses mirroring `ComputerSeduceSolicitLure` patterns in Florida exemplars.

## Canonical pattern

```
CACInvestigation
  └── resultsIn ──▶ ChargeSet
        └── PleaAgreement (optional)
              └── SentencingOutcome
                    └── SexOffenderRegistryEntry (when ordered)
```

## Modeling rules

- Link charges back to the **source investigation** and relevant **exploitation events** via `uco-core:Relationship` (`Relates_To`), not only `chargedWith` on the suspect.
- Use **statute references** as structured nodes when statute numbers are known.
- Registry outcomes are separate auditable events — do not bury them in sentencing description text.
- Use typed literals for `chargeCount` (`xsd:nonNegativeInteger`).

## Validation

```bash
validate_graph("sentencing-outcome.jsonld", extensions=["cac"])
```

## Related recipes

- [cac-icac-search-warrant-arrest.md](cac-icac-search-warrant-arrest.md)
- [cac-tactical-undercover-operation.md](cac-tactical-undercover-operation.md)
- [event.md](event.md)
