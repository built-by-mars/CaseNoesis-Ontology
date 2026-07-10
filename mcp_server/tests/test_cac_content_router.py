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
    assert "docs/recipes/cac-grooming-chat-modeling.md" in files
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


FEDERAL_ENTERPRISE_NARRATIVE = (
    "U.S. v. Defendant-1 et al. in the U.S. District Court. A multi-defendant "
    "indictment filed November 2025 charges six co-conspirators in a child "
    "exploitation enterprise under 18 U.S.C. 2252A(g). Count 1 alleges the "
    "enterprise; counts 2 through 10 include conspiracy to produce CSAM, "
    "production of CSAM, and conspiracy to transmit interstate threats. "
    "Federal prosecution is in pre-trial phase."
)


FEDERAL_PRODUCTION_NARRATIVE = (
    "U.S. v. Defendant-1 in U.S. District Court, District of Alaska, case "
    "3:24-cr-00091. Parallel federal prosecution in Western District of Texas. "
    "Indictment filed 2024-08-22 with five federal counts: transportation of "
    "CSAM, receipt of CSAM, possession of CSAM, attempted sexual exploitation "
    "of a minor, and receipt under 18 U.S.C. 2252. Alleged CSAM production "
    "and possession from 2021 to 2024. Asset forfeiture under 18 U.S.C. 2253 "
    "of Samsung Galaxy smartphones seized as evidence."
)


def test_detect_federal_prosecution_relationships_domain() -> None:
    matches = detect_cac_domains(FEDERAL_ENTERPRISE_NARRATIVE)
    domain_ids = {item["domain_id"] for item in matches}
    assert "federal-prosecution-relationships" in domain_ids
    assert "legal-sentencing-outcomes" in domain_ids


def test_detect_federal_production_multi_district_domain() -> None:
    matches = detect_cac_domains(FEDERAL_PRODUCTION_NARRATIVE)
    domain_ids = {item["domain_id"] for item in matches}
    assert "federal-prosecution-relationships" in domain_ids
    assert "production-case" in domain_ids


def test_route_federal_prosecution_includes_relationship_checklist() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=FEDERAL_ENTERPRISE_NARRATIVE,
        include_recipe_content=False,
        max_recipes=8,
    )
    assert result["ok"] is True
    domain_ids = {item["domain_id"] for item in result["matched_domains"]}
    assert "federal-prosecution-relationships" in domain_ids
    checklist_ids = {item["id"] for item in result["modeling_checklist"]}
    assert "defendant-charge-matrix" in checklist_ids
    assert "indictment-charge-links" in checklist_ids
    assert "enterprise-indictment-bridge" in checklist_ids
    assert "investigation-legal-scope" in checklist_ids
    recipe_files = {item["recipe_file"] for item in result["matched_domains"]}
    assert "docs/recipes/cac-federal-prosecution-relationships.md" in recipe_files


def test_route_federal_production_includes_multi_district_checklist() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=FEDERAL_PRODUCTION_NARRATIVE,
        include_recipe_content=False,
        max_recipes=8,
    )
    assert result["ok"] is True
    checklist_ids = {item["id"] for item in result["modeling_checklist"]}
    assert "multi-district-charge-jurisdiction" in checklist_ids
    assert "forfeiture-device-linkage" in checklist_ids
    assert "indictment-charge-links" in checklist_ids
    assert "prosecution-indictment-link" in checklist_ids


FEDERAL_ENTERPRISE_OVERT_ACT_NARRATIVE = (
    "U.S. v. Defendant-1 et al. Multi-defendant indictment under 18 U.S.C. "
    "2252A(g). Count 1 alleges a child exploitation enterprise with Violation "
    "One in the District of New Mexico and Violation Three in the Southern "
    "District of California. Asset forfeiture schedule lists serial numbers "
    "for seized SanDisk SSD and desktop tower devices."
)


SEXTORTION_FEDERAL_NARRATIVE = (
    "Sextortion indictment in U.S. District Court, District of Alaska. Defendant "
    "a citizen abroad extradited for prosecution. Counts include cyberstalking "
    "under 18 U.S.C. 2261A, aggravated identity theft under 1028A, and wire "
    "fraud under 1343. Coercion via Instagram and Snapchat with ban evasion "
    "and impersonation of a teen influencer."
)


def test_route_enterprise_overt_act_includes_violation_checklist() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=FEDERAL_ENTERPRISE_OVERT_ACT_NARRATIVE,
        include_recipe_content=False,
        max_recipes=8,
    )
    assert result["ok"] is True
    checklist_ids = {item["id"] for item in result["modeling_checklist"]}
    assert "enterprise-overt-act-violations" in checklist_ids
    assert "charge-venue-locations" in checklist_ids
    assert "forfeiture-device-linkage" in checklist_ids


def test_route_sextortion_federal_includes_stacking_checklist() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=SEXTORTION_FEDERAL_NARRATIVE,
        include_recipe_content=False,
        max_recipes=8,
    )
    assert result["ok"] is True
    domain_ids = {item["domain_id"] for item in result["matched_domains"]}
    assert "sextortion-coercion" in domain_ids
    checklist_ids = {item["id"] for item in result["modeling_checklist"]}
    assert "sextortion-federal-prosecution-bridge" in checklist_ids
    assert "financial-charge-stacking" in checklist_ids
    assert "transnational-extradition-chain" in checklist_ids
    assert "platform-affordance-abuse" in checklist_ids


HAWAII_TRAFFICKING_NARRATIVE = (
    "U.S. v. Riley in U.S. District Court, District of Hawaii, case "
    "1:23-cr-00071-JMS. Superseding indictment filed July 2024 with twelve "
    "federal counts: sex trafficking a minor under 18 U.S.C. 1591, production "
    "of child pornography, coercion and enticement under 2422(b), and possession "
    "of CSAM. Five minor victims. Defendant met victims on Grindr, offered money "
    "and hotel rooms, arranged Uber and taxi transportation. Government trial brief "
    "Doc 188 describes anticipated testimony per minor victim. PACER docket shows "
    "competency hearing under 4241 and jury trial scheduled."
)


PACER_BUNDLE_NARRATIVE = (
    "PACER PDF bundle for Case 3:20-cr-00029-SLG-MMS. Document 2 Filed 02/21/20: "
    "INDICTMENT — the Grand Jury charges production of child pornography (18 U.S.C. 2251), "
    "possession, sex trafficking of a minor, and Criminal Forfeiture Allegation 1. "
    "Document 251: AO 245B Judgment in a Criminal Case, USM Number 15966-006, "
    "240 months imprisonment, supervised release for a term of 20 years with Sheet 3D "
    "special conditions, restitution, special assessment, and a schedule of payments."
)


def test_detect_pacer_document_ingestion_domain() -> None:
    matches = detect_cac_domains(PACER_BUNDLE_NARRATIVE)
    domain_ids = {item["domain_id"] for item in matches}
    assert "pacer-document-ingestion" in domain_ids


def test_route_pacer_bundle_includes_ingestion_checklist() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=PACER_BUNDLE_NARRATIVE,
        include_recipe_content=False,
        max_recipes=10,
    )
    assert result["ok"] is True
    domain_ids = {item["domain_id"] for item in result["matched_domains"]}
    assert "pacer-document-ingestion" in domain_ids
    checklist_ids = {item["id"] for item in result["modeling_checklist"]}
    assert "pacer-single-investigation-per-docket" in checklist_ids
    assert "pacer-no-fabricated-timestamps" in checklist_ids
    assert "pacer-judgment-supervision-conditions" in checklist_ids
    assert "pacer-assertion-status-tags" in checklist_ids
    recipe_files = {item["recipe_file"] for item in result["matched_domains"]}
    assert "docs/recipes/cac-pacer-document-ingestion.md" in recipe_files


def test_route_hawaii_trafficking_includes_victim_bundle_checklist() -> None:
    result = route_cac_content(
        project_root=PROJECT_ROOT,
        content_text=HAWAII_TRAFFICKING_NARRATIVE,
        include_recipe_content=False,
        max_recipes=10,
    )
    assert result["ok"] is True
    domain_ids = {item["domain_id"] for item in result["matched_domains"]}
    assert "trafficking-recruitment" in domain_ids
    assert "federal-prosecution-relationships" in domain_ids
    assert "federal-trial-proceedings" in domain_ids
    checklist_ids = {item["id"] for item in result["modeling_checklist"]}
    assert "per-victim-charge-bundles" in checklist_ids
    assert "trafficking-conduct-charge-bridge" in checklist_ids
    assert "superseding-indictment-chain" in checklist_ids
    assert "trial-brief-anticipated-evidence" in checklist_ids
    recipe_files = {item["recipe_file"] for item in result["matched_domains"]}
    assert "docs/recipes/cac-federal-trial-proceedings.md" in recipe_files
