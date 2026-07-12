# PROF Validation Profile Metadata

> See [Recipe Index](INDEX.md) for all recipes.

Describe **what profile** a graph conforms to (intent) separately from **whether it validated** (result). Use the [W3C Profiles Vocabulary (PROF)](https://www.w3.org/TR/dx-prof/) to serialize resolved bundle metadata alongside CASE/UCO investigation data.

Issue: [#64](https://github.com/vulnmaster/CASE-UCO-SDK/issues/64)

## Scope

- Profile intent (`prof:Profile`) vs validation outcome (separate resource)
- Serializing resolved bundle metadata (`prof:ResourceDescriptor`, `prof:hasResource`)
- Exemplar: `examples/upper-ontology/prof-metadata/build_exemplar.py`

## Concepts

| PROF class | Forensic use |
|---|---|
| `prof:Profile` | Declares the specification the graph was authored against (CASE 1.4.0 + extensions) |
| `prof:ResourceDescriptor` | One artifact in the bundle (SHACL shapes, JSON-LD context, extension TTL) |
| `prof:hasResource` | Links profile → descriptor |
| `prof:hasArtifact` | Links profile → concrete validation report or exported bundle file |
| `prof:isProfileOf` | Target specification IRI (e.g. UCO namespace) |

**Profile intent** answers: "What rules was this graph written to satisfy?"

**Validation result** answers: "Did it pass SHACL on date X?" — model as a separate `UcoObject` or external report IRI referenced via `prof:hasArtifact`. Do not overload `prof:Profile` with pass/fail booleans.

## Python pattern

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation

graph = CASEGraph(extra_context={
    "prof": "http://www.w3.org/ns/dx/prof/",
    "dcterms": "http://purl.org/dc/terms/",
})

profile_id = "kb:profile-case-1.4"
graph.upsert_node(profile_id, types="prof:Profile", properties={
    "dcterms:title": "CASE/UCO 1.4.0 investigation graph",
    "prof:isProfileOf": "https://ontology.unifiedcyberontology.org/uco/",
})

descriptor_id = "kb:descriptor-shacl"
graph.upsert_node(descriptor_id, types="prof:ResourceDescriptor", properties={
    "dcterms:format": "text/turtle",
    "dcterms:description": "CASE/UCO SHACL shapes bundle.",
})
graph.add_property(profile_id, "prof:hasResource", {"@id": descriptor_id})

report_id = "kb:validation-report-1"
graph.upsert_node(report_id, types="uco-core:UcoObject", properties={
    "uco-core:name": "Validation run ...",
    "uco-core:description": ["SHACL result — separate from profile intent."],
})
graph.add_property(profile_id, "prof:hasArtifact", {"@id": report_id})

graph.create(Investigation, name="...", description=["..."])
graph.write("prof-metadata.jsonld")
```

</details>

```bash
python examples/upper-ontology/prof-metadata/build_exemplar.py
```

## Validation

```bash
validate_graph("prof-metadata.jsonld", profiles=["prof"])

case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/upper/shapes/sh-prof.ttl \
  --allow-info prof-metadata.jsonld
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Conformance flag on `prof:Profile` | Separate validation report resource |
| Profile without `prof:isProfileOf` | Link to specification IRI |
| Missing descriptor for shapes bundle | `prof:ResourceDescriptor` per artifact |
| PROF replaces `case_validate` | PROF documents intent; validator produces result |
| Invented `prof:` properties | Use pinned PROF registry only |

## Related

- [extensions.md](extensions.md) — extension manifests and validation subsets
- [runtime-discovery.md](runtime-discovery.md) — registry and class discovery
- [cross-ontology-composition.md](cross-ontology-composition.md) — composing multiple profiles
