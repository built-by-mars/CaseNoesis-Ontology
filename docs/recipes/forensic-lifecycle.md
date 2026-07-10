# Forensic Investigation Lifecycle

> See [Recipe Index](INDEX.md) for all recipes.

Model a structured forensic investigation as an ordered lifecycle of phases — survey, preservation, examination, analysis, reporting. Based on [CASE-Examples/forensic_lifecycle](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/forensic_lifecycle).

## Key classes

| Class | Role |
|---|---|
| `Investigation` | The case container |
| `ActionLifecycle` | An ordered sequence of phases |
| `ArrayOfAction` | The ordered list container for phases |
| `Action` / `InvestigativeAction` | Individual phases and their sub-actions |
| `ProvenanceRecord` | Links phases to their outputs |
| `Relationship` | Maps specific actions to lifecycle phases (`Mapped_Into`) |
| `Annotation` | Notes and observations on actions |

## Pattern

```
Investigation
    │
    └── object ──▶ ActionLifecycle
                       │
                       └── phase ──▶ ArrayOfAction
                                        ├── action[0] ──▶ Action ("Survey")
                                        ├── action[1] ──▶ Action ("Preservation")
                                        ├── action[2] ──▶ Action ("Examination")
                                        ├── action[3] ──▶ Action ("Analysis")
                                        └── action[4] ──▶ Action ("Reporting")

InvestigativeAction (specific task)
    │
    └── Mapped_Into ──▶ Action (lifecycle phase)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity
from case_uco.uco.core import Relationship, Annotation
from case_uco.uco.action import Action, ActionLifecycle, ArrayOfAction
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=...))
graph = CASEGraph()

# Define lifecycle phases as Actions
survey = graph.create(Action, name="Survey")
preservation = graph.create(Action, name="Preservation")
examination = graph.create(Action, name="Examination")
analysis = graph.create(Action, name="Analysis")
reporting = graph.create(Action, name="Reporting")

# Ordered phase array
phase_array = ArrayOfAction(
    action=[survey, preservation, examination, analysis, reporting],
)

# The lifecycle
lifecycle = graph.create(ActionLifecycle,
    name="...",  # lifecycle name from source
    phase=phase_array,
)

# Investigation linked to the lifecycle
investigation = graph.create(Investigation,
    name="...",
    description=["..."],
    object=[lifecycle],
)

# Specific investigative actions mapped to phases
imaging = graph.create(InvestigativeAction,
    name="...",  # e.g. "Disk imaging" from source
    description=["..."],
    start_time=datetime(..., tzinfo=tz),
    end_time=datetime(..., tzinfo=tz),
)

# Map the imaging action to the Preservation phase
graph.create(Relationship,
    source=[imaging], target=preservation,
    kind_of_relationship="Mapped_Into",
    is_directional=True,
)

# Annotate an action
annotation = graph.create(Annotation,
    statement=["..."],  # observation text from source
    object=[imaging],
)

graph.write("forensic_lifecycle.jsonld")
```

</details>

## Notes

- `ActionLifecycle.phase` is required and takes an `ArrayOfAction`. The `ArrayOfAction.action` field is `list[Action]` (required, one or more).
- Phase names are not fixed by the ontology. Common forensic lifecycle phases include Survey, Preservation, Examination, Analysis, and Reporting, but adapt to the source.
- Use `Relationship` with `kind_of_relationship="Mapped_Into"` to link specific `InvestigativeAction`s to their lifecycle phase.
- `Annotation.object` is `list[UcoObject]` (required) — it points to the objects being annotated. `statement` is `list[str]`.

## Related

- [chain-of-custody.md](chain-of-custody.md) — custody events within the phases
- [forensic-tool.md](forensic-tool.md) — the tool runs each phase contains
- [event.md](event.md) — structured events inside phases
- [starter-tool-run.md](starter-tool-run.md) — tool-run provenance starter kit
