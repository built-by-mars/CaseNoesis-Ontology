"""Tests for CAC content routing and multi-recipe selection."""

from __future__ import annotations

from pathlib import Path

import pytest

from cac_content_router import (
    assess_extraction_quality,
    cac_content_detected,
    detect_cac_domains,
    graph_contains_cac_signals,
    route_cac_content,
    search_recipes,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
HOTLINE_EXAMPLE = (
    PROJECT_ROOT
    / "extensions/cac/ontology/examples_knowledge_graphs/hotline-lifecycle.ttl"
)


def test_detect_trafficking_and_task_force_domains() -> None:
    text = (
        "A regional ICAC task force conducted a joint investigation into a "
        "child sex trafficking ring using peer recruitment and interstate transport."
    )
    matches = detect_cac_domains(text)
    domain_ids = {item["domain_id"] for item in matches}
    assert "trafficking-recruitment" in domain_ids
    assert "multi-jurisdiction-task-force" in domain_ids


def test_route_cac_content_returns_multiple_recipes() -> None:
    text = (
        "After grooming on Snapchat, the ESP filed a CyberTip with NCMEC. "
        "An ICAC task force opened a trafficking investigation and executed "
        "a high-risk arrest with asset forfeiture."
    )
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=text,
        include_recipe_content=False,
        max_recipes=6,
    )
    assert result["ok"] is True
    assert result["cac_detected"] is True
    assert len(result["matched_domains"]) >= 3
    assert result["output_format"] == "json-ld"
    assert "validation" in result
    assert result["validation"]["extension"] == "cac"
    assert "recommended_workflow" in result


def test_route_cac_content_ttl_output_format() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text="International Europol operation with cross-border evidence sharing.",
        output_format="ttl",
        include_recipe_content=False,
    )
    assert result["output_format"] == "ttl"
    assert "ttl" in result["validation"]["output_formats"]


def test_route_cac_content_from_graph_path() -> None:
    if not HOTLINE_EXAMPLE.exists():
        pytest.skip("CAC hotline example graph not present in submodule")
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        source_path=str(HOTLINE_EXAMPLE),
        include_recipe_content=False,
    )
    assert result["ok"] is True
    assert result["cac_detected"] is True
    assert result.get("graph_has_cac_signals") is True
    assert result["input_type"] == "graph_partial"


def test_route_cac_content_no_cac_signals() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text="Routine disk imaging with Autopsy on a workstation image.",
        include_recipe_content=False,
    )
    assert result["cac_detected"] is False
    assert result["matched_domains"] == []


def test_route_cac_content_requires_submission() -> None:
    with pytest.raises(ValueError, match="empty_submission"):
        route_cac_content(project_root=PROJECT_ROOT)


def test_search_recipes_returns_multiple_cac_matches() -> None:
    matches = search_recipes("grooming cybertip trafficking", limit=5)
    assert len(matches) >= 3
    files = {item["file"] for item in matches}
    assert "docs/recipes/grooming-chat-modeling.md" in files
    assert "docs/recipes/cybertip-ncmec-workflow.md" in files


def test_graph_contains_cac_signals() -> None:
    if not HOTLINE_EXAMPLE.exists():
        pytest.skip("CAC hotline example graph not present in submodule")
    assert graph_contains_cac_signals(HOTLINE_EXAMPLE) is True


def test_cac_content_detected_generic_keywords() -> None:
    assert cac_content_detected("Internet Crimes Against Children task force case") is True


MARYLAND_CLEAN_NARRATIVE = (
    "Maryland State Police Computer Crimes Unit and Maryland ICAC Task Force "
    "investigated online child sex abuse material purchasing and sexual "
    "solicitation of a minor. Investigators executed a search warrant at a "
    "residence in Annapolis. A 38-year-old Annapolis man was taken into custody "
    "without incident and transported to a detention center, where he was held "
    "without bond. He was charged with sexual solicitation of a minor and "
    "knowingly permitting solicitation. Anne Arundel County Police assisted."
)


def test_maryland_icac_narrative_matches_five_domains() -> None:
    matches = detect_cac_domains(MARYLAND_CLEAN_NARRATIVE)
    domain_ids = {item["domain_id"] for item in matches}
    assert "multi-jurisdiction-task-force" in domain_ids
    assert "icac-search-warrant-arrest" in domain_ids
    assert "grooming-chat" in domain_ids
    assert "legal-sentencing-outcomes" in domain_ids
    assert "csam-forensic-provenance" in domain_ids
    assert len(domain_ids) >= 5


def test_route_maryland_narrative_includes_extraction_quality() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=MARYLAND_CLEAN_NARRATIVE,
        include_recipe_content=False,
        max_recipes=8,
    )
    assert result["ok"] is True
    assert result["extraction_quality"]["noisy_extraction"] is False
    domain_ids = {item["domain_id"] for item in result["matched_domains"]}
    assert "icac-search-warrant-arrest" in domain_ids
    assert result["validation"]["validation_mode"] == "subset"
    checklist = result["modeling_checklist"]
    assert len(checklist) >= 5
    assert any(item["id"] == "perpetrator-crime-links" for item in checklist)


def test_assess_extraction_quality_flags_noisy_pdf_text() -> None:
    noisy = (
        "https://www.eyeonannapolis.net/2025/12/article "
        "https://www.eyeonannapolis.net/subscribe "
        "https://www.eyeonannapolis.net/latest-posts "
        "https://www.eyeonannapolis.net/buy-tickets "
        "https://www.eyeonannapolis.net/latest-posts-again "
        "= menu powered by advertisement buy tickets "
        "you might be interested latest posts "
        "icac task force charged with arrest"
    )
    quality = assess_extraction_quality(noisy)
    assert quality["noisy_extraction"] is True
    assert quality["noise_marker_hits"] >= 3
    assert "recommendation" in quality
