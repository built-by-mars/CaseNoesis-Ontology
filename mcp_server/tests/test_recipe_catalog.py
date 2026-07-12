"""Guards for the recipe catalog: completeness, reachability, cross-links.

The MCP server routes agents to recipes via RECIPE_INDEX (get_recipe /
get_recipes), INVESTIGATION_FAMILIES (route_investigation_content), and the
CAC domain table (route_cac_content). A recipe missing from the indexes is
invisible to agents, and a recipe without cross-links breaks the "reason
through recipes" navigation chain. These tests fail when the catalog and
the routing layers drift apart.
"""

from __future__ import annotations

import re
from pathlib import Path

from domain_index import MAPPING_GUIDE_INDEX, RECIPE_INDEX
from investigation_router import INVESTIGATION_FAMILIES, build_extension_gap_guidance, route_investigation_content

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RECIPES_DIR = PROJECT_ROOT / "docs" / "recipes"


def _recipe_files() -> set[str]:
    return {p.name for p in RECIPES_DIR.glob("*.md")} - {"INDEX.md"}


def test_every_recipe_is_in_recipe_index() -> None:
    indexed = {entry["file"].removeprefix("docs/recipes/") for entry in RECIPE_INDEX}
    missing = _recipe_files() - indexed
    assert not missing, (
        f"Recipes not registered in RECIPE_INDEX (invisible to get_recipe/"
        f"get_recipes): {sorted(missing)} — see docs/recipes/recipe-authoring.md"
    )


def test_recipe_index_entries_point_at_existing_files() -> None:
    stale = [e["file"] for e in RECIPE_INDEX if not (PROJECT_ROOT / e["file"]).is_file()]
    assert not stale, f"RECIPE_INDEX entries with missing files: {stale}"


def test_every_recipe_is_in_index_md() -> None:
    index_text = (RECIPES_DIR / "INDEX.md").read_text(encoding="utf-8")
    missing = [r for r in sorted(_recipe_files()) if r not in index_text]
    assert not missing, f"Recipes missing from docs/recipes/INDEX.md: {missing}"


def test_family_and_gap_recipes_exist() -> None:
    referenced: set[str] = set(build_extension_gap_guidance()["recipes"])
    for family in INVESTIGATION_FAMILIES:
        referenced.update(family.recipes)
    for entry in MAPPING_GUIDE_INDEX:
        starter = entry.get("starter_kit")
        if starter:
            referenced.add(starter)
    missing = [r for r in sorted(referenced) if not (PROJECT_ROOT / r).is_file()]
    assert not missing, f"Routing layers reference nonexistent recipes: {missing}"


def test_recipe_cross_link_graph_has_no_orphans() -> None:
    """Every recipe links out to a neighbor and is reachable from one."""

    recipes = _recipe_files()
    inbound: dict[str, int] = {r: 0 for r in recipes}
    no_outgoing: list[str] = []
    for name in sorted(recipes):
        text = (RECIPES_DIR / name).read_text(encoding="utf-8")
        links = set(re.findall(r"([a-z0-9-]+\.md)", text)) - {name, "INDEX.md"}
        links &= recipes
        if not links:
            no_outgoing.append(name)
        for link in links:
            inbound[link] += 1
    no_inbound = sorted(r for r, count in inbound.items() if count == 0)
    assert not no_outgoing, (
        f"Recipes with no outgoing recipe links (add a Related section): {no_outgoing}"
    )
    assert not no_inbound, (
        f"Recipes no other recipe links to (add links from neighbors): {no_inbound}"
    )


def test_multi_domain_submission_routes_to_multiple_families() -> None:
    """One investigation spanning CAC + fraud + violent crime must surface
    all three families plus single-graph composition guidance."""

    text = (
        "The defendant groomed a minor victim through Instagram and produced "
        "CSAM; a NCMEC CyberTip identified the account. He was also charged "
        "with attempted murder and assault of a federal officer with a deadly "
        "or dangerous weapon after a shooting during the arrest, and with "
        "wire fraud and money laundering through a bitcoin wallet and "
        "cryptocurrency exchange accounts used to sell the material on a "
        "darknet market. The superseding indictment and plea agreement are "
        "on the PACER docket with forfeiture and restitution."
    )
    result = route_investigation_content(PROJECT_ROOT, content_text=text)
    family_ids = {m["family_id"] for m in result["matched_families"]}
    assert {"cac-child-exploitation", "violent-crime", "financial-crime-crypto", "legal-filings-docket"} <= family_ids
    workflow = " ".join(result["recommended_workflow"])
    assert "ONE investigation" in workflow
    assert "cross-ontology-composition.md" in workflow
    ordered = result["ordered_recommendations"]
    assert ordered["primary_composition_recipe"] == "docs/recipes/cross-ontology-composition.md"
    assert ordered["supporting_domain_recipes"]
    assert "cac" in ordered["required_extensions"]
    assert "gufo" in ordered["recommended_profiles"]
    assert "bfo" in ordered["not_recommended_profiles"]
    assert ordered["validation_bundle_preview"] is not None
    assert ordered["ontology_gap_workflow"] is None


def test_gap_guidance_points_to_recipe_authoring() -> None:
    guidance = build_extension_gap_guidance()
    assert "docs/recipes/recipe-authoring.md" in guidance["recipes"]
    assert "docs/recipes/cross-ontology-composition.md" in guidance["recipes"]
    assert any("recipe-authoring" in step for step in guidance["workflow"])


def test_gap_routing_exposes_ontology_gap_workflow() -> None:
    result = route_investigation_content(
        PROJECT_ROOT,
        content_text="Quarterly pump lubrication schedule for the water plant.",
    )
    assert result["matched_families"] == []
    ordered = result["ordered_recommendations"]
    assert ordered["ontology_gap_workflow"] is not None
    assert "docs/recipes/cross-ontology-composition.md" in ordered["ontology_gap_workflow"]["recipes"]
    assert result["extension_gap_guidance"] == ordered["ontology_gap_workflow"]