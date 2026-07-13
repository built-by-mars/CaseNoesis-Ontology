"""Merge deterministic review + critic assessments into a completed pass review."""

from __future__ import annotations

from typing import Any

from critic.models import CriticFinding, CriticScorecard
from critic.scorecard import merge_scorecards


def merge_completed_pass_review(
    *,
    deterministic_findings: list[CriticFinding],
    assessments: list[dict[str, Any]],
    new_critic_findings: list[CriticFinding],
    det_scorecard: CriticScorecard,
    model_scorecard: CriticScorecard,
    validation: dict[str, Any],
    analysis_status: str,
    artifact_hashes: dict[str, Any],
    status: str | None = None,
) -> dict[str, Any]:
    """Build the completed per-pass review used for blockers and finalization.

    Rules:
    - Deterministic/source findings stay open unless their own verifier resolved them
      (model may only dispute / mark persists — never resolve).
    - Model-originated findings may be resolved by an explicit assessment.
    - Findings omitted from assessments remain open.
    - New critic findings are appended as open.
    """

    by_id: dict[str, CriticFinding] = {
        f.finding_id: CriticFinding.from_dict(f.to_dict()) for f in deterministic_findings
    }
    assessment_by_id = {
        str(a["assesses_finding_id"]): a for a in assessments if a.get("assesses_finding_id")
    }

    for finding_id, finding in list(by_id.items()):
        assessment = assessment_by_id.get(finding_id)
        if assessment is None:
            if finding.status not in {"resolved"}:
                # Omitted → remains open (unevaluated for prior model findings).
                if finding.evidence_kind == "critic_inference" and finding.status == "new":
                    finding.status = "unevaluated"
            continue
        verdict = assessment["assessment"]
        if finding.evidence_kind in {"deterministic", "source"}:
            if verdict == "disputed":
                finding.status = "disputed"
                finding.disputed_rationale = str(assessment.get("rationale") or "")[:2000]
            elif verdict == "persists":
                if finding.status != "resolved":
                    finding.status = "persisting"
            # resolved is rejected at parse time for deterministic/source
        else:
            if verdict == "resolved":
                finding.status = "resolved"
            elif verdict == "disputed":
                finding.status = "disputed"
                finding.disputed_rationale = str(assessment.get("rationale") or "")[:2000]
            elif verdict == "persists":
                finding.status = "persisting"

    for finding in new_critic_findings:
        clone = CriticFinding.from_dict(finding.to_dict())
        clone.status = "new"
        by_id[clone.finding_id] = clone

    merged = list(by_id.values())
    open_findings = [f for f in merged if f.status not in {"resolved"}]
    critical_high_open = [
        f for f in open_findings if f.severity in {"critical", "high"}
    ]
    medium_low_open = [
        f for f in open_findings if f.severity in {"medium", "low"}
    ]
    merged_score = merge_scorecards(det_scorecard, model_scorecard)

    derived_status = status or _derive_status(
        validation=validation,
        analysis_status=analysis_status,
        critical_high_open=critical_high_open,
        medium_low_open=medium_low_open,
    )

    return {
        "status": derived_status,
        "analysis_status": analysis_status,
        "artifact_hashes": artifact_hashes,
        "validation": validation,
        "merged_findings": [f.to_dict() for f in merged],
        "finding_assessments": list(assessments),
        "new_critic_finding_ids": [f.finding_id for f in new_critic_findings],
        "finding_counts": {
            "merged": len(merged),
            "open": len(open_findings),
            "critical_high_open": len(critical_high_open),
            "medium_low_open": len(medium_low_open),
        },
        "open_finding_ids": [f.finding_id for f in open_findings],
        "scorecard": merged_score.to_dict(),
    }


def _derive_status(
    *,
    validation: dict[str, Any],
    analysis_status: str,
    critical_high_open: list[CriticFinding],
    medium_low_open: list[CriticFinding],
) -> str:
    if analysis_status != "complete":
        return "analysis_incomplete"
    if validation.get("verification_status") != "complete":
        return "validation_incomplete"
    if validation.get("conforms") is not True:
        return "needs_revision"
    if critical_high_open:
        return "blocked_with_findings"
    if medium_low_open:
        return "completed_with_findings"
    return "accepted"


def finalize_outcome_from_summary(summary: dict[str, Any]) -> str:
    """Map a completed-pass summary to a final session outcome string."""

    status = str(summary.get("status") or "")
    if status in {
        "accepted",
        "completed_with_findings",
        "blocked_with_findings",
        "needs_revision",
        "validation_incomplete",
        "analysis_incomplete",
    }:
        return status
    validation = summary.get("validation") or {}
    analysis_status = str(summary.get("analysis_status") or "incomplete")
    counts = summary.get("finding_counts") or {}
    if analysis_status != "complete":
        return "analysis_incomplete"
    if validation.get("verification_status") != "complete":
        return "validation_incomplete"
    if validation.get("conforms") is not True:
        return "needs_revision"
    if int(counts.get("critical_high_open") or 0):
        return "blocked_with_findings"
    if int(counts.get("medium_low_open") or 0) or int(counts.get("open") or 0):
        return "completed_with_findings"
    return "accepted"
