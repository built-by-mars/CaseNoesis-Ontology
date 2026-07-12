# Upper-Ontology Exemplars

Runnable builders that produce JSON-LD graphs aligned with the upper-ontology recipe catalog. Each script uses the public `CASEGraph` API (`create`, `upsert_node`, `add_type`, `add_property`, `create_relationship`) and writes output next to the script.

Validate these graphs locally with vendored CDO-Shapes profiles under `ontology/upper/shapes/` (via `mcp_server/tools/run_recipe_examples.py --validate` or `validate_graph(..., profiles=[...])`). A dedicated CI recipe-validation job is forthcoming when `case-utils` is available in the workflow image.

## Index

| Recipe | Builder | Output |
|---|---|---|
| [foundational-typing-bfo-gufo.md](../../docs/recipes/foundational-typing-bfo-gufo.md) | `foundational-typing/build_bfo_variant.py` | `foundational-typing-bfo.jsonld` |
| [foundational-typing-bfo-gufo.md](../../docs/recipes/foundational-typing-bfo-gufo.md) | `foundational-typing/build_gufo_variant.py` | `foundational-typing-gufo.jsonld` |
| [foundational-typing-bfo-gufo.md](../../docs/recipes/foundational-typing-bfo-gufo.md) | *(static anti-pattern)* | `foundational-typing/invalid_category_mistake.jsonld` |
| [prov-o-evidence-lineage.md](../../docs/recipes/prov-o-evidence-lineage.md) | `prov-o-lineage/build_exemplar.py` | `prov-o-lineage.jsonld` |
| [owl-time-temporal-evidence.md](../../docs/recipes/owl-time-temporal-evidence.md) | `owl-time/build_exemplar.py` | `owl-time-temporal.jsonld` |
| [geosparql-geospatial-evidence.md](../../docs/recipes/geosparql-geospatial-evidence.md) | `geosparql/build_exemplar.py` | `geosparql-geospatial.jsonld` |
| [foaf-org-identity-roles.md](../../docs/recipes/foaf-org-identity-roles.md) | `foaf-org/build_exemplar.py` | `foaf-org-identity.jsonld` |
| [prof-validation-profile-metadata.md](../../docs/recipes/prof-validation-profile-metadata.md) | `prof-metadata/build_exemplar.py` | `prof-metadata.jsonld` |
| [solveit-plan-execution-provenance.md](../../docs/recipes/solveit-plan-execution-provenance.md) | `solveit-plan-execution/build_exemplar.py` | `solveit-plan-execution.jsonld` |
| [cross-ontology-composition.md](../../docs/recipes/cross-ontology-composition.md) | `composition/build_composite.py` | `cross-ontology-composite.jsonld` |

## Run all

```bash
for script in \
  foundational-typing/build_bfo_variant.py \
  foundational-typing/build_gufo_variant.py \
  prov-o-lineage/build_exemplar.py \
  owl-time/build_exemplar.py \
  geosparql/build_exemplar.py \
  foaf-org/build_exemplar.py \
  prof-metadata/build_exemplar.py \
  solveit-plan-execution/build_exemplar.py \
  composition/build_composite.py
do
  python "examples/upper-ontology/$script"
done
```

## Prerequisites

```bash
pip install -e python/   # CASEGraph from this repo
```

Builders do not invoke `case_validate` directly — validate outputs with profile shapes from `ontology/upper/shapes/` (CI job forthcoming / when `case-utils` is available in CI).

## Related

- [docs/recipes/INDEX.md](../../docs/recipes/INDEX.md) — full recipe catalog
- [docs/recipes/cross-ontology-composition.md](../../docs/recipes/cross-ontology-composition.md) — composition policy
- [ontology/upper/provenance.json](../../ontology/upper/provenance.json) — pinned upper-ontology sources
