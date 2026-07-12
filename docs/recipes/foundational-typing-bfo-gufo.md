# Foundational Typing with BFO and gUFO

> See [Recipe Index](INDEX.md) for all recipes.

Enrich CASE/UCO domain objects with **foundational ontology types on the same IRI** — never as duplicate nodes. BFO and gUFO are **mutually exclusive** top-level choices; pick one per graph. The CAC Ontology aligns with **gUFO**; do not combine CAC graphs with BFO enrichment.

Issue: [#59](https://github.com/vulnmaster/CASE-UCO-SDK/issues/59)

## Scope

- When to choose BFO vs gUFO
- Domain-first typing: `uco-identity:Person`, `uco-observable:ObservableObject`, `case-investigation:InvestigativeAction` first; foundational type second on the **same** `@id`
- Six common mappings and anti-patterns
- Runnable exemplars under `examples/upper-ontology/foundational-typing/`

## Selection matrix: BFO vs gUFO

| Criterion | BFO (CDO-Shapes-BFO) | gUFO (CDO-Shapes-gufo) |
|---|---|---|
| **Stack** | Biomedical / ISO 21838-2 formal ontology | OntoUML-based gentle UFO |
| **CAC Ontology** | **Not recommended** — axioms conflict with CAC's gUFO spine | **Preferred** — CAC imports gUFO directly |
| **Continuants vs occurrents** | `obo:BFO_0000002` / `obo:BFO_0000003` distinction | `gufo:Object` / `gufo:Event` distinction |
| **Tooling** | OBO Foundry, scientific reasoning | CAC, OntoUML practitioners |
| **Coexistence** | **Never** on the same graph as gUFO | **Never** on the same graph as BFO |

**Rule:** one foundational profile per graph. Multiple *adopting* profiles (PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF) may coexist with either BFO or gUFO — see [cross-ontology-composition.md](cross-ontology-composition.md).

## Decision rules

1. **Domain type first.** Always `graph.create(Person, …)` / `graph.create(InvestigativeAction, …)` before enrichment.
2. **Same IRI.** Use `graph.add_type(node_id, "gufo:Object")` on the `id=` passed to `create()` — not a second node.
3. **CAC → gUFO only.** If the graph uses CAC classes, use gUFO enrichment or skip foundational typing entirely.
4. **Actions are occurrents.** Type `InvestigativeAction` as `gufo:Event` or `obo:BFO_0000011` (spatiotemporal/process), never the performer.
5. **Evidence is endurant.** Type `ObservableObject` as `gufo:Object` / `gufo:FunctionalComplex` or BFO material entity — not `gufo:Event`.
6. **Never both.** If you need BFO interop, do not add any `gufo:` types to the same graph.

## Mappings (domain → foundational)

| CASE/UCO class | gUFO enrichment (same IRI) | BFO enrichment (same IRI) |
|---|---|---|
| `uco-identity:Person` | `gufo:Object` | `obo:BFO_0000002` (Continuant) |
| `uco-observable:ObservableObject` (device/media) | `gufo:FunctionalComplex` | `obo:BFO_0000040` (Material entity) |
| `case-investigation:InvestigativeAction` | `gufo:Event` | `obo:BFO_0000011` (Spatiotemporal region) |
| `uco-identity:Identity` (organization) | `gufo:Collection` | `obo:BFO_0000027` (Object aggregate) |
| `uco-location:Location` | `gufo:Object` | `obo:BFO_0000006` (Spatial region) |
| Role held over a period | `gufo:Situation` (separate node) | BFO temporal region (separate node) |

For time-bounded roles, see [existence-intervals.md](existence-intervals.md) and [owl-time-temporal-evidence.md](owl-time-temporal-evidence.md).

## Python pattern

<details open><summary>Python (gUFO variant)</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.identity import Person
from case_uco.uco.observable import ObservableObject, FileFacet

graph = CASEGraph(extra_context={"gufo": "http://purl.org/nemo/gufo#"})

person_id = "kb:examiner-1"
person = graph.create(Person, id=person_id, name="...")
graph.add_type(person_id, "gufo:Object")

evidence_id = "kb:evidence-1"
evidence = graph.create(ObservableObject, id=evidence_id, name="...",
    has_facet=[FileFacet(file_name="...", size_in_bytes=...)],
)
graph.add_type(evidence_id, "gufo:FunctionalComplex")

action_id = "kb:action-1"
action = graph.create(InvestigativeAction, id=action_id, name="...",
    performer=person, object=[evidence],
)
graph.add_type(action_id, "gufo:Event")

graph.create(Investigation, name="...", object=[evidence, action])
graph.write("foundational-typing-gufo.jsonld")
```

</details>

Use `graph.upsert_node(...)` when the node has no SDK dataclass (e.g. a standalone `gufo:Situation`). Use `graph.get(node_id)` to inspect merged JSON-LD after enrichment.

**Exemplars:**

```bash
python examples/upper-ontology/foundational-typing/build_gufo_variant.py
python examples/upper-ontology/foundational-typing/build_bfo_variant.py
```

Anti-pattern reference: `examples/upper-ontology/foundational-typing/invalid_category_mistake.jsonld` (Person typed as `gufo:Event`).

## Validation

```bash
# MCP
validate_graph("foundational-typing-gufo.jsonld", profiles=["gufo"])

# CLI (vendored CDO-Shapes)
case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/upper/shapes/sh-gufo.ttl \
  --allow-info foundational-typing-gufo.jsonld
```

For BFO, swap `profiles=["bfo"]` and `sh-bfo.ttl`.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Person typed as `gufo:Event` / BFO occurrent | Category error — people are endurants | Type the **action**, not the person |
| Duplicate node for foundational type | Breaks identity and queries | `add_type` on same `@id` |
| BFO + gUFO on one graph | Inconsistent axioms | Pick one foundational profile |
| BFO with CAC extension | Conflicts with CAC gUFO spine | Use gUFO or omit foundational typing |
| Foundational type as only `@type` | Loses CASE/UCO semantics | Always keep domain `@type` first |
| `graph.add_node` / mutating `graph._objects` | Deprecated / unsupported | `create()` + `add_type` / `upsert_node` |

## Related

- [existence-intervals.md](existence-intervals.md) — temporal role patterns across foundational stacks
- [cross-ontology-composition.md](cross-ontology-composition.md) — combining profiles safely
- [extensions.md](extensions.md) — CAC gUFO alignment and strict concept coverage
- [owl-time-temporal-evidence.md](owl-time-temporal-evidence.md) — temporal enrichment alongside foundational typing
