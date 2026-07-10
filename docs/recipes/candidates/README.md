# Candidate recipes (not yet operational)

Recipes drafted during live investigations start here. Files in this
directory are **invisible to routing**: they are not registered in
`RECIPE_INDEX`, not listed in `docs/recipes/INDEX.md`, and not returned by
`get_recipe` / `get_recipes` / `route_investigation_content`.

## Promotion workflow

1. Draft the recipe here following `docs/recipes/recipe-authoring.md`
   (structure, Tier T0 synthetic data, validated JSON-LD snippets).
2. Validate every embedded graph snippet with `validate_graph` /
   `case_validate` until it conforms with zero undeclared concepts.
3. Move the file into `docs/recipes/` and register it in `RECIPE_INDEX`
   (`mcp_server/domain_index.py`) and `docs/recipes/INDEX.md`.
4. Run `make test-mcp` — the catalog integrity tests fail if the recipe is
   unregistered, cross-links are broken, or routing keywords are missing.
5. Commit with provenance: source investigation (Tier-classified), authoring
   agent/tool, and reviewer.

Rollback: recipes are plain files under git; restore a previous approved
generation with `git checkout <ref> -- docs/recipes/<file>.md`.

See `mcp_server/knowledge_lifecycle.py` for the extension-ontology
equivalent (candidate/operational/deprecated manifest statuses).
