"""Schema validation and normalization of critic model responses."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from critic.models import (
    CriticFinding,
    CriticScorecard,
    CriticTarget,
    load_vocabularies,
)

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


class CriticResponseError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def parse_critic_model_response(payload: dict[str, Any] | str) -> dict[str, Any]:
    """Validate and normalize a model/manual critic response.

    Returns ``{"findings": [...CriticFinding], "scorecard": CriticScorecard, "notes": str}``.
    """

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise CriticResponseError("critic_response_invalid", str(exc)) from exc

    if not isinstance(payload, dict):
        raise CriticResponseError("critic_response_invalid", "root must be object")

    vocab = load_vocabularies()
    severities = set(vocab["severities"])
    categories = set(vocab["categories"])
    evidence_kinds = set(vocab["evidence_kinds"])

    raw_findings = payload.get("findings")
    if not isinstance(raw_findings, list):
        raise CriticResponseError(
            "critic_response_schema_mismatch", "findings must be an array"
        )

    findings: list[CriticFinding] = []
    for index, item in enumerate(raw_findings):
        if not isinstance(item, dict):
            raise CriticResponseError(
                "critic_response_schema_mismatch", f"finding[{index}] not object"
            )
        try:
            severity = item["severity"]
            category = item["category"]
            confidence = float(item["confidence"])
            evidence_kind = item.get("evidence_kind", "critic_inference")
            target_raw = item.get("target") or {}
            if not isinstance(target_raw, dict):
                raise KeyError("target")
            if severity not in severities:
                raise CriticResponseError(
                    "critic_response_schema_mismatch", f"bad severity {severity}"
                )
            if category not in categories:
                raise CriticResponseError(
                    "critic_response_schema_mismatch", f"bad category {category}"
                )
            if evidence_kind not in evidence_kinds:
                raise CriticResponseError(
                    "critic_response_schema_mismatch",
                    f"bad evidence_kind {evidence_kind}",
                )
            if not 0.0 <= confidence <= 1.0:
                raise CriticResponseError(
                    "critic_response_schema_mismatch", "confidence out of range"
                )
            finding = CriticFinding(
                finding_id=str(item.get("finding_id") or f"MODEL-{index + 1:04d}"),
                severity=severity,
                category=category,
                confidence=confidence,
                status=item.get("status") or "new",
                target=CriticTarget(
                    path=target_raw.get("path"),
                    line=target_raw.get("line"),
                    node_id=target_raw.get("node_id"),
                    predicate=target_raw.get("predicate"),
                    json_pointer=target_raw.get("json_pointer"),
                ),
                evidence_kind=evidence_kind,
                evidence=[str(e) for e in (item.get("evidence") or [])],
                rationale=str(item.get("rationale") or ""),
                recommended_change=str(item.get("recommended_change") or ""),
                verification_method=str(item.get("verification_method") or ""),
                rule_id=item.get("rule_id"),
                related_recipe=item.get("related_recipe"),
            )
            finding.ensure_identity_key()
            findings.append(finding)
        except KeyError as exc:
            raise CriticResponseError(
                "critic_response_schema_mismatch", f"missing field {exc}"
            ) from exc

    score_raw = payload.get("scorecard") or {}
    if not isinstance(score_raw, dict):
        raise CriticResponseError(
            "critic_response_schema_mismatch", "scorecard must be object"
        )
    scorecard = CriticScorecard.from_dict(score_raw)
    _clamp_scorecard(scorecard)

    return {
        "findings": findings,
        "scorecard": scorecard,
        "notes": str(payload.get("notes") or ""),
    }


def _clamp_scorecard(scorecard: CriticScorecard) -> None:
    for name in (
        "schema_concept_conformance",
        "source_fidelity",
        "semantic_precision",
        "provenance_custody",
        "markings_authorization",
        "coverage_completeness",
        "serializer_quality",
        "maintainability_reproducibility",
    ):
        value = getattr(scorecard, name)
        setattr(scorecard, name, max(0, min(5, int(value))))
