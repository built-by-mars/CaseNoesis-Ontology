# Hotline Intake and Referral Lifecycle

> See [Recipe Index](INDEX.md) for all recipes.

Model hotline intake, triage, referral, and escalation from first report through law-enforcement handoff using CAC hotline module classes.

## Scope

**Layer 3 — Institutional workflow** for report intake organizations and referral chains.

## Key classes

| Class | Role |
|---|---|
| `HotlineIntake` | Initial report receipt |
| `IntakeAssessment` | Triage and urgency classification |
| `ReferralAction` | Referral to agency or service provider |
| `MandatoryReportingActivation` | Mandated reporter trigger when applicable |
| `CACInvestigation` | Investigation opened from referral |
| `InvestigativeAction` | Each intake workflow step |

## Canonical pattern

```
HotlineIntake
  └── result ──▶ IntakeAssessment
        └── result ──▶ ReferralAction
              ├── MandatoryReportingActivation (if triggered)
              └── resultedInInvestigation ──▶ CACInvestigation
```

## Modeling rules

- Model **each intake stage** as its own `InvestigativeAction` with explicit `uco-action:result` links.
- Do not collapse triage and referral into one node — urgency and routing are queryable only when separated.
- When the intake leads to NCMEC, chain into [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md).

## Python skeleton

```python
from case_uco import CASEGraph

graph = CASEGraph(extra_context={
    "cacontology-hotlines": "https://cacontology.projectvic.org/hotlines#",
})
intake = graph.add_node("kb:intake-1", "cacontology-hotlines:HotlineIntake", {
    "uco-core:name": "CyberTipline intake call",
})
graph.write("hotline-intake.jsonld")
```

## Validation

```bash
make validate-extension EXT=cac DATA=hotline-intake.jsonld
```

## Related recipes

- [cybertip-ncmec-workflow.md](cybertip-ncmec-workflow.md)
- [cac-victim-rescue-extraction.md](cac-victim-rescue-extraction.md)
