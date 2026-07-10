"""Labeled routing benchmark for the hybrid retrieval pipeline (issue #53).

The corpus covers four case types:

- **keyword** — catalog vocabulary; the deterministic baseline must already
  route these (regression guard for the pre-hybrid behavior).
- **paraphrase** — investigator/colloquial phrasing with no (or too few)
  catalog keywords; the semantic stage must recover them. These are the
  recall wins that justify the hybrid pipeline.
- **multi-domain** — one investigation spanning several families; results
  must stay compositional.
- **negative** — content unrelated to any family; the router must abstain
  with extension-gap guidance rather than guess.

Confidence thresholds in ``semantic_retrieval`` are calibrated against this
corpus: change thresholds and corpus together.

All narratives are Tier T0 public-safe synthetic data.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import investigation_router
import semantic_retrieval

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def route(text: str) -> dict:
    return investigation_router.route_investigation_content(
        PROJECT_ROOT, content_text=text
    )


def matched_ids(payload: dict) -> set[str]:
    return {m["family_id"] for m in payload["matched_families"]}


# (narrative, expected family ids (any-of per tuple), case type)
BENCHMARK = [
    # --- keyword cases: deterministic baseline must already route these ---
    (
        "Ransomware intrusion with lateral movement, C2 beacon traffic in the "
        "pcap, and exfiltration of finance shares.",
        [("network-intrusion",)],
        "keyword",
    ),
    (
        "Cellebrite UFED physical extraction of the suspect's Android "
        "smartphone; review SMS and call log artifacts.",
        [("device-mobile-forensics",)],
        "keyword",
    ),
    (
        "Superseding indictment on the PACER docket charges wire fraud and "
        "money laundering through a darknet market bitcoin mixer.",
        [("legal-filings-docket",), ("financial-crime-crypto",)],
        "keyword",
    ),
    # --- paraphrase cases: no catalog keywords, semantic stage must route ---
    (
        "A stranger my daughter met online blackmailed her into sending "
        "photos and then demanded more images.",
        [("cac-child-exploitation",)],
        "paraphrase",
    ),
    (
        "Somebody hacked into our company network, encrypted our files, and "
        "is demanding payment in bitcoin.",
        [("network-intrusion", "financial-crime-crypto")],
        "paraphrase",
    ),
    (
        "The victim was stabbed to death outside a bar; a witness saw the "
        "suspect flee with a handgun.",
        [("violent-crime",)],
        "paraphrase",
    ),
    (
        "He was selling dope for the cartel and kept ledgers of every "
        "kilogram moved across the border.",
        [("drug-trafficking",)],
        "paraphrase",
    ),
    (
        "An investor lost her savings to a pig butchering romance scheme run "
        "through a fake exchange and USDT transfers.",
        [("financial-crime-crypto",)],
        "paraphrase",
    ),
    # --- multi-domain: compositional results ---
    (
        "Grand jury indictment charges the street crew with racketeering; "
        "predicate acts include murder, drug trafficking with "
        "methamphetamine and fentanyl, and money laundering through "
        "cryptocurrency wallets.",
        [
            ("racketeering-enterprise",),
            ("violent-crime",),
            ("drug-trafficking",),
            ("financial-crime-crypto",),
        ],
        "multi-domain",
    ),
    # --- negatives: must abstain ---
    (
        "Quarterly maintenance schedule for the municipal water treatment "
        "plant, including pump lubrication intervals.",
        [],
        "negative",
    ),
    (
        "Recipe collection for sourdough bread with hydration ratios and "
        "proofing times.",
        [],
        "negative",
    ),
    (
        "Veterinary vaccination records for the county livestock fair "
        "entrants.",
        [],
        "negative",
    ),
]


def test_keyword_cases_still_route_and_baseline_agrees():
    for text, expected, case_type in BENCHMARK:
        if case_type != "keyword":
            continue
        payload = route(text)
        ids = matched_ids(payload)
        for any_of in expected:
            assert ids & set(any_of), (text, ids)
        baseline_ids = {b["family_id"] for b in payload["deterministic_baseline"]}
        assert baseline_ids, f"keyword case must appear in deterministic baseline: {text}"


def test_paraphrase_cases_recovered_by_semantic_stage():
    for text, expected, case_type in BENCHMARK:
        if case_type != "paraphrase":
            continue
        payload = route(text)
        ids = matched_ids(payload)
        for any_of in expected:
            assert ids & set(any_of), (text, ids, payload.get("abstained_candidates"))


def test_hybrid_improves_recall_over_keyword_baseline():
    """The semantic stage must recover paraphrase cases the keyword stage
    misses, without breaking any keyword or negative case (precision)."""

    baseline_hits = 0
    hybrid_hits = 0
    paraphrase_total = 0
    for text, expected, case_type in BENCHMARK:
        if case_type != "paraphrase":
            continue
        paraphrase_total += 1
        payload = route(text)
        expected_any = {fid for any_of in expected for fid in any_of}
        baseline_ids = {b["family_id"] for b in payload["deterministic_baseline"]}
        if baseline_ids & expected_any:
            baseline_hits += 1
        if matched_ids(payload) & expected_any:
            hybrid_hits += 1
    assert hybrid_hits == paraphrase_total, "hybrid must route every paraphrase case"
    assert hybrid_hits > baseline_hits, (
        "benchmark must contain paraphrases the keyword baseline misses "
        f"(baseline={baseline_hits}, hybrid={hybrid_hits})"
    )


def test_negative_cases_abstain_with_gap_guidance():
    for text, _, case_type in BENCHMARK:
        if case_type != "negative":
            continue
        payload = route(text)
        assert payload["matched_families"] == [], (text, payload["matched_families"])
        assert payload["routing_confidence"]["level"] == "abstain", (
            text,
            payload["routing_confidence"],
        )
        assert "extension_gap_guidance" in payload


def test_multi_domain_results_are_compositional():
    for text, expected, case_type in BENCHMARK:
        if case_type != "multi-domain":
            continue
        payload = route(text)
        ids = matched_ids(payload)
        hit = sum(1 for any_of in expected if ids & set(any_of))
        assert hit >= 3, f"multi-domain case must match several families: {ids}"
        workflow = " ".join(payload["recommended_workflow"])
        assert "ONE" in workflow or "single graph" in workflow


def test_every_match_carries_explainable_evidence():
    payload = route(
        "Somebody hacked into our company network, encrypted our files, and "
        "is demanding payment in bitcoin."
    )
    assert payload["matched_families"]
    for match in payload["matched_families"]:
        assert match["match_stages"], match["family_id"]
        scoring = match["scoring"]
        assert 0.0 <= scoring["confidence"] <= 1.0
        # Every routed family shows *why*: keyword hits, semantic evidence,
        # or the explicit CAC-signal stage.
        assert (
            match["matched_keywords"]
            or match["semantic_evidence"]
            or match["match_stages"] == ["cac-signals"]
        ), match["family_id"]


def test_confidence_levels_are_ordered():
    assert semantic_retrieval.confidence_level(0.0) == "abstain"
    assert semantic_retrieval.confidence_level(
        semantic_retrieval.ABSTAIN_CONFIDENCE
    ) == "low"
    assert semantic_retrieval.confidence_level(
        semantic_retrieval.HIGH_CONFIDENCE
    ) == "high"


def test_semantic_retrieval_is_offline_and_deterministic():
    score1, ev1 = semantic_retrieval.semantic_score(
        "my kid was blackmailed for photos", "sextortion grooming minor victim"
    )
    score2, ev2 = semantic_retrieval.semantic_score(
        "my kid was blackmailed for photos", "sextortion grooming minor victim"
    )
    assert (score1, ev1) == (score2, ev2)
    assert score1 > 0
