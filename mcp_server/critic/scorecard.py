"""Nullable / evidence-backed scorecard semantics (Round 2)."""

from __future__ import annotations

from critic.models import CriticFinding, CriticScorecard, ScoreDimension, ValidationSummary


def build_deterministic_scorecard(
    validation: ValidationSummary,
    findings: list[CriticFinding],
    *,
    has_sources: bool,
    has_serializer: bool,
    has_coverage_contract: bool,
) -> CriticScorecard:
    score = CriticScorecard()

    # Schema/concept conformance — assessed from validation
    if validation.verification_status != "complete" or validation.conforms is not True:
        score.schema_concept_conformance = ScoreDimension(
            score=0,
            assessed=True,
            evidence=[
                f"conforms={validation.conforms}",
                f"verification_status={validation.verification_status}",
            ],
            hard_cap=0,
            cap_reason="validation_incomplete_or_nonconforming",
        )
        score.caps_applied.append("validation_incomplete_or_nonconforming")
    else:
        score.schema_concept_conformance = ScoreDimension(
            score=5,
            assessed=True,
            evidence=["validation_complete_conforming"],
        )

    # Source fidelity
    if has_sources or has_coverage_contract:
        src_findings = [f for f in findings if f.category in {"source_fidelity", "coverage"}]
        if src_findings:
            score.source_fidelity = ScoreDimension(
                score=2,
                assessed=True,
                evidence=[f.finding_id for f in src_findings[:5]],
                hard_cap=2,
                cap_reason="source_or_coverage_findings",
            )
        else:
            score.source_fidelity = ScoreDimension(
                score=4,
                assessed=True,
                evidence=["no_source_coverage_findings"],
            )
        score.coverage_completeness = score.source_fidelity
    else:
        score.source_fidelity = ScoreDimension(assessed=False)
        score.coverage_completeness = ScoreDimension(assessed=False)

    # Semantic precision — only when modeling heuristics ran findings of that class
    semantic_cats = {
        "relationship_direction",
        "action_grammar",
        "investigation_structure",
        "facet_placement",
        "generic_relationship",
        "dictionary_collision",
        "identity_conflation",
    }
    semantic = [f for f in findings if f.category in semantic_cats]
    if semantic:
        worst = min({"critical": 1, "high": 2, "medium": 3, "low": 4, "info": 5}[f.severity] for f in semantic)
        score.semantic_precision = ScoreDimension(
            score=worst,
            assessed=True,
            evidence=[f.finding_id for f in semantic[:5]],
            hard_cap=worst,
            cap_reason="semantic_modeling_findings",
        )
    else:
        # Assessed only lightly when graph heuristics evaluated with no hits
        score.semantic_precision = ScoreDimension(
            score=4,
            assessed=True,
            evidence=["no_semantic_heuristic_findings"],
        )

    # Markings / authorization
    auth = [f for f in findings if f.category in {"authorization", "markings"}]
    if auth:
        score.markings_authorization = ScoreDimension(
            score=2,
            assessed=True,
            evidence=[f.finding_id for f in auth[:5]],
            hard_cap=2,
            cap_reason="authorization_or_marking_findings",
        )
    else:
        score.markings_authorization = ScoreDimension(assessed=False)

    # Provenance / custody
    prov = [f for f in findings if f.category in {"provenance", "custody"}]
    if prov:
        score.provenance_custody = ScoreDimension(
            score=2,
            assessed=True,
            evidence=[f.finding_id for f in prov[:5]],
            hard_cap=2,
            cap_reason="provenance_or_custody_findings",
        )
    else:
        score.provenance_custody = ScoreDimension(assessed=False)

    # Serializer quality
    if has_serializer:
        ser = [f for f in findings if f.category.startswith("serializer_")]
        if any(f.category == "serializer_validation" for f in ser):
            score.serializer_quality = ScoreDimension(
                score=1,
                assessed=True,
                evidence=[f.finding_id for f in ser[:5]],
                hard_cap=1,
                cap_reason="serializer_validation_findings",
            )
        elif ser:
            score.serializer_quality = ScoreDimension(
                score=2,
                assessed=True,
                evidence=[f.finding_id for f in ser[:5]],
                hard_cap=2,
                cap_reason="serializer_findings",
            )
        else:
            score.serializer_quality = ScoreDimension(
                score=4,
                assessed=True,
                evidence=["no_serializer_findings"],
            )
        score.maintainability_reproducibility = ScoreDimension(
            score=3 if ser else 4,
            assessed=True,
            evidence=["serializer_present"],
        )
    else:
        score.serializer_quality = ScoreDimension(assessed=False)
        score.maintainability_reproducibility = ScoreDimension(assessed=False)

    return score


def merge_scorecards(
    deterministic: CriticScorecard,
    model: CriticScorecard | None,
) -> CriticScorecard:
    """Apply model scores only where assessed; never exceed deterministic hard caps."""

    if model is None:
        return deterministic

    def merge_dim(det: ScoreDimension, mod: ScoreDimension) -> ScoreDimension:
        if not mod.assessed or mod.score is None:
            return det
        if not det.assessed:
            # Model may assess; still honor det hard_cap if any
            score = mod.score
            if det.hard_cap is not None:
                score = min(score, det.hard_cap)
            return ScoreDimension(
                score=score,
                assessed=True,
                evidence=list(mod.evidence),
                hard_cap=det.hard_cap,
                cap_reason=det.cap_reason,
            )
        score = mod.score
        if det.hard_cap is not None:
            score = min(score, det.hard_cap)
        if det.score is not None:
            score = min(score, det.score)
        return ScoreDimension(
            score=score,
            assessed=True,
            evidence=list(dict.fromkeys(det.evidence + mod.evidence)),
            hard_cap=det.hard_cap,
            cap_reason=det.cap_reason,
        )

    return CriticScorecard(
        schema_concept_conformance=merge_dim(
            deterministic.schema_concept_conformance, model.schema_concept_conformance
        ),
        source_fidelity=merge_dim(deterministic.source_fidelity, model.source_fidelity),
        semantic_precision=merge_dim(
            deterministic.semantic_precision, model.semantic_precision
        ),
        provenance_custody=merge_dim(
            deterministic.provenance_custody, model.provenance_custody
        ),
        markings_authorization=merge_dim(
            deterministic.markings_authorization, model.markings_authorization
        ),
        coverage_completeness=merge_dim(
            deterministic.coverage_completeness, model.coverage_completeness
        ),
        serializer_quality=merge_dim(
            deterministic.serializer_quality, model.serializer_quality
        ),
        maintainability_reproducibility=merge_dim(
            deterministic.maintainability_reproducibility,
            model.maintainability_reproducibility,
        ),
        caps_applied=list(
            dict.fromkeys(deterministic.caps_applied + ["model_scores_merged"])
        ),
    )
