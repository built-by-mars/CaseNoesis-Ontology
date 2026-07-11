# Vendored Upper-Ontology Sources

Pinned source files for every upper/external ontology that UCO maintains a
[CDO-Shapes](https://github.com/ucoProject) conformance profile for. These
snapshots exist so the SDK works **fully offline**:

- `mcp_server/tools/build_upper_ontology_registry.py` rebuilds the strict
  concept-coverage registry (`mcp_server/upper_ontology_registry.json`)
  from these files by default — no network access required.
- Developers on air-gapped investigation networks can inspect the exact
  upper-ontology text the registry was derived from.

| File | Ontology | Upstream source |
| --- | --- | --- |
| `bfo.owl` | Basic Formal Ontology (BFO) 2.0 / ISO 21838-2 | <http://purl.obolibrary.org/obo/bfo.owl> |
| `gufo.ttl` | gentle Unified Foundational Ontology (gUFO) | <https://nemo-ufes.github.io/gufo/gufo.ttl> |
| `prov-o.ttl` | W3C Provenance Ontology (PROV-O) | <http://www.w3.org/ns/prov-o.ttl> |
| `time.ttl` | W3C OWL-Time | <https://www.w3.org/2006/time.ttl> |
| `geo.ttl` | OGC GeoSPARQL 1.1 (core) | <https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl> |
| `sf.ttl` | OGC Simple Features geometries | <https://opengeospatial.github.io/ogc-geosparql/geosparql11/sf_geometries.ttl> |
| `foaf.rdf` | Friend of a Friend (FOAF) 0.99 | <http://xmlns.com/foaf/spec/index.rdf> |
| `org.ttl` | W3C Organization Ontology (ORG) | <https://www.w3.org/ns/org.ttl> |
| `prof.ttl` | W3C Profiles Vocabulary (PROF) | <https://www.w3.org/ns/dx/prof/> |

`provenance.json` records the source URL, SHA-256, and fetch timestamp of
each file.

## CDO-Shapes conformance profiles (`shapes/`)

The `shapes/` subdirectory vendors the SHACL conformance profiles published
by the [Cyber Domain Ontology project](https://github.com/Cyber-Domain-Ontology)
for each profiled ontology (`sh-bfo.ttl`, `sh-gufo.ttl`, `sh-prov-o.ttl`,
`sh-time.ttl`, `sh-geo.ttl`, `sh-foaf.ttl`, `sh-org.ttl`, `sh-prof.ttl`),
pinned to a specific upstream commit recorded in `provenance.json`. They can
be passed to `case_validate` for offline profile conformance checks:

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph ontology/upper/shapes/sh-prov-o.ttl \
  --allow-info output.jsonld
```

The `get_uco_profiles` MCP tool reports these vendored paths as
`local_source` / `local_shapes` for each profile.

## Licensing

Each file remains under its upstream license and is vendored unmodified for
interoperability: BFO and gUFO are published under Creative Commons
Attribution 4.0; the W3C vocabularies (PROV-O, OWL-Time, ORG, PROF) under
the W3C Software and Document License; GeoSPARQL under the OGC document
license; FOAF under Creative Commons Attribution. Consult the ontology
headers inside each file for the authoritative license statement.

## Refreshing the snapshot

```bash
# Re-download all pinned sources and rebuild the registry (network required)
python3 mcp_server/tools/build_upper_ontology_registry.py --fetch

# Offline rebuild from this snapshot (default)
python3 mcp_server/tools/build_upper_ontology_registry.py
```

Review the resulting registry diff before committing — term additions or
removals change what strict concept coverage accepts.
