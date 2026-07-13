"""Deterministic scorecard caps from validation + findings."""

from __future__ import annotations

from critic.models import CriticFinding, CriticScorecard, ValidationSummary


def build_deterministic_scorecard(
    validation: ValidationSummary,
    findings: list[CriticFinding],
) -> CriticScorecard:
    """Compute baseline scores; validation failures hard-cap conformance."""

    score = CriticScorecard(
        schema_concept_conformance=5,
        source_fidelity=3,
        semantic_precision=4,
        provenance_custody=4,
        markings_authorization=4,
        coverage_completeness=4,
        serializer_quality=4,
        maintainability_reproducibility=4,
    )

    if validation.verification_status != "complete" or validation.conforms is not True:
        score.schema_concept_conformance = 0
        score.caps_applied.append("validation_incomplete_or_nonconforming")
    elif validation.violation_count > 0:
        score.schema_concept_conformance = 0
        score.caps_applied.append("shacl_violations")

    critical = sum(1 for f in findings if f.severity == "critical")
    high = sum(1 for f in findings if f.severity == "high")
    if critical:
        score.semantic_precision = min(score.semantic_precision, 1)
        score.caps_applied.append("critical_deterministic_findings")
    elif high:
        score.semantic_precision = min(score.semantic_precision, 2)
        score.caps_applied.append("high_deterministic_findings")

    if any(f.category == "serializer_validation" for f in findings):
        score.serializer_quality = min(score.serializer_quality, 1)
        score.caps_applied.append("serializer_validation_findings")
    elif any(f.category.startswith("serializer_") for f in findings):
        score.serializer_quality = min(score.serializer_quality, 2)
        score.caps_applied.append("serializer_findings")

    if any(f.category in {"authorization", "markings"} for f in findings):
        score.markings_authorization = min(score.markings_authorization, 2)
    if any(f.category in {"provenance", "custody"} for f in findings):
        score.provenance_custody = min(score.provenance_custody, 2)
    if any(f.category in {"source_fidelity", "coverage"} for f in findings):
        score.source_fidelity = min(score.source_fidelity, 2)
        score.coverage_completeness = min(score.coverage_completeness, 2)

    return score


def merge_scorecards(
    deterministic: CriticScorecard,
    model: CriticScorecard | None,
) -> CriticScorecard:
    """Model scores cannot exceed deterministic caps on conformance dimensions."""

    if model is None:
        return deterministic
    merged = CriticScorecard(
        schema_concept_conformance=min(
            deterministic.schema_concept_conformance, model.schema_concept_conformance
        ),
        source_fidelity=min(deterministic.source_fidelity, model.source_fidelity),
        semantic_precision=min(
            deterministic.semantic_precision, model.semantic_precision
        ),
        provenance_custody=min(
            deterministic.provenance_custody, model.provenance_custody
        ),
        markings_authorization=min(
            deterministic.markings_authorization, model.markings_authorization
        ),
        coverage_completeness=min(
            deterministic.coverage_completeness, model.coverage_completeness
        ),
        serializer_quality=min(
            deterministic.serializer_quality, model.serializer_quality
        ),
        maintainability_reproducibility=min(
            deterministic.maintainability_reproducibility,
            model.maintainability_reproducibility,
        ),
        caps_applied=list(
            dict.fromkeys(deterministic.caps_applied + ["model_scores_capped"])
        ),
    )
    return merged
