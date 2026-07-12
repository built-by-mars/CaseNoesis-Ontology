# Cross-Domain Extension Usage

> **This recipe has moved.** See **[cross-ontology-composition.md](cross-ontology-composition.md)** for the full composition policy matrix (CASE/UCO, extensions, BFO/gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF), ordered modeling plan, anti-patterns, and the composite exemplar.

## Quick start (unchanged)

Extension packages (CAC, AEO, SOLVE-IT, etc.) use the same `CASEGraph` API as core — with `extra_context` for extension namespaces and `graph.create()` for typed classes:

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation

graph = CASEGraph(extra_context={
    "cac-core": "https://cacontology.projectvic.org/core#",
})

investigation = graph.create(Investigation,
    name="ICAC Task Force Case 2024-1234",
    description=["Multi-jurisdictional investigation"],
)
graph.write("cac-investigation.jsonld")
```

Validate with extension manifests:

```bash
validate_graph("cac-investigation.jsonld", extensions=["cac"])
```

For CAC + gUFO composition rules, profile compatibility, and anti-patterns, read [cross-ontology-composition.md](cross-ontology-composition.md).

## Related

- [cross-ontology-composition.md](cross-ontology-composition.md) — **primary reference**
- [extensions.md](extensions.md) — extension authoring and UCO profiles
- [INDEX.md](INDEX.md) — full recipe catalog
