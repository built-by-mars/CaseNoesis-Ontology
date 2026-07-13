"""Schema validation and normalization of critic model responses (Round 2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from critic.models import (
    CriticFinding,
    CriticScorecard,
    CriticTarget,
    ScoreDimension,
    load_vocabularies,
    make_stable_finding_id,
)

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
MODEL_RESPONSE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "graph_sha256",
        "prompt_package_hash",
        "findings",
        "scorecard",
    ],
    "properties": {
        "schema_version": {"type": "string", "minLength": 1, "maxLength": 32},
        "session_id": {"type": ["string", "null"], "maxLength": 128},
        "pass_number": {"type": ["integer", "null"], "minimum": 1, "maximum": 32},
        "graph_sha256": {"type": "string", "minLength": 64, "maxLength": 64},
        "serializer_sha256": {"type": ["string", "null"], "minLength": 64, "maxLength": 64},
        "prompt_package_hash": {"type": "string", "minLength": 64, "maxLength": 64},
        "findings": {
            "type": "array",
            "maxItems": 200,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "severity",
                    "category",
                    "confidence",
                    "target",
                    "evidence",
                    "rationale",
                    "recommended_change",
                    "verification_method",
                ],
                "properties": {
                    "severity": {
                        "enum": ["critical", "high", "medium", "low", "info"]
                    },
                    "category": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 64,
                        "enum": [
                            "syntax_integrity",
                            "validation",
                            "relationship_direction",
                            "relationship_vocabulary",
                            "action_grammar",
                            "authorization",
                            "identity_conflation",
                            "provenance",
                            "markings",
                            "custody",
                            "facet_placement",
                            "dictionary_collision",
                            "source_fidelity",
                            "coverage",
                            "serializer_api",
                            "serializer_validation",
                            "serializer_safety",
                            "serializer_performance",
                            "generic_relationship",
                            "investigation_structure"
                        ]
                    },
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "target": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "path": {"type": ["string", "null"], "maxLength": 512},
                            "line": {"type": ["integer", "null"], "minimum": 1},
                            "node_id": {"type": ["string", "null"], "maxLength": 2048},
                            "predicate": {"type": ["string", "null"], "maxLength": 2048},
                            "counterpart_id": {
                                "type": ["string", "null"],
                                "maxLength": 2048,
                            },
                            "json_pointer": {
                                "type": ["string", "null"],
                                "maxLength": 1024,
                            },
                            "qualified_name": {
                                "type": ["string", "null"],
                                "maxLength": 512,
                            },
                        },
                    },
                    "evidence": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 20,
                        "items": {"type": "string", "minLength": 1, "maxLength": 2000},
                    },
                    "rationale": {"type": "string", "minLength": 1, "maxLength": 4000},
                    "recommended_change": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 4000,
                    },
                    "verification_method": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 2000,
                    },
                    "related_recipe": {"type": ["string", "null"], "maxLength": 256},
                },
            },
        },
        "scorecard": {"type": "object"},
        "notes": {"type": "string", "maxLength": 4000},
    },
}


class CriticResponseError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def parse_critic_model_response(
    payload: dict[str, Any] | str,
    *,
    expected_graph_sha256: str,
    expected_prompt_package_hash: str,
    expected_serializer_sha256: str | None = None,
    session_id: str | None = None,
    pass_number: int | None = None,
) -> dict[str, Any]:
    """Validate and normalize a model/manual critic response against JSON Schema."""

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise CriticResponseError("critic_response_invalid", str(exc)) from exc

    if not isinstance(payload, dict):
        raise CriticResponseError("critic_response_invalid", "root must be object")

    validator = Draft202012Validator(MODEL_RESPONSE_SCHEMA)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        raise CriticResponseError(
            "critic_response_schema_mismatch",
            errors[0].message,
        )

    if payload["graph_sha256"] != expected_graph_sha256:
        raise CriticResponseError("critic_artifact_hash_mismatch", "graph_sha256")
    if payload["prompt_package_hash"] != expected_prompt_package_hash:
        raise CriticResponseError("critic_artifact_hash_mismatch", "prompt_package_hash")

    # Serializer / session / pass bindings: when the caller declares expected
    # values, the response must echo them exactly (no silent omission).
    if expected_serializer_sha256 is not None:
        if payload.get("serializer_sha256") != expected_serializer_sha256:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "serializer_sha256"
            )
    if session_id is not None:
        if payload.get("session_id") != session_id:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "session_id"
            )
    if pass_number is not None:
        if payload.get("pass_number") != pass_number:
            raise CriticResponseError(
                "critic_artifact_hash_mismatch", "pass_number"
            )

    vocab = load_vocabularies()
    categories = set(vocab["categories"])

    findings: list[CriticFinding] = []
    for index, item in enumerate(payload["findings"]):
        category = item["category"]
        if category not in categories:
            raise CriticResponseError(
                "critic_response_schema_mismatch", f"bad category {category}"
            )
        # Reject model-supplied deterministic rule IDs / evidence kinds
        if item.get("rule_id"):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "model must not supply rule_id",
            )
        if item.get("evidence_kind") and item["evidence_kind"] != "critic_inference":
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "model evidence_kind must be critic_inference",
            )
        if item.get("finding_id"):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "model must not supply finding_id",
            )

        target_raw = item["target"]
        target = CriticTarget(
            path=target_raw.get("path"),
            line=target_raw.get("line"),
            node_id=target_raw.get("node_id"),
            predicate=target_raw.get("predicate"),
            counterpart_id=target_raw.get("counterpart_id"),
            json_pointer=target_raw.get("json_pointer"),
            qualified_name=target_raw.get("qualified_name"),
        )
        if not any(
            [
                target.path,
                target.node_id,
                target.predicate,
                target.json_pointer,
                target.qualified_name,
            ]
        ):
            raise CriticResponseError(
                "critic_response_schema_mismatch",
                "target must identify a location",
            )

        finding_id = make_stable_finding_id(
            f"MODEL-{category}",
            *target.semantic_parts(),
            str(index),
        )
        findings.append(
            CriticFinding(
                finding_id=finding_id,
                severity=item["severity"],
                category=category,
                confidence=float(item["confidence"]),
                status="new",
                target=target,
                evidence_kind="critic_inference",
                evidence=[str(e) for e in item["evidence"]],
                rationale=str(item["rationale"]),
                recommended_change=str(item["recommended_change"]),
                verification_method=str(item["verification_method"]),
                related_recipe=item.get("related_recipe"),
                identity_key=finding_id,
            )
        )

    scorecard = _parse_scorecard(payload.get("scorecard") or {})
    return {
        "findings": findings,
        "scorecard": scorecard,
        "notes": str(payload.get("notes") or ""),
        "session_id": payload.get("session_id", session_id),
        "pass_number": payload.get("pass_number", pass_number),
    }


def _parse_scorecard(raw: dict[str, Any]) -> CriticScorecard:
    def dim(key: str) -> ScoreDimension:
        value = raw.get(key)
        if value is None:
            return ScoreDimension(assessed=False)
        if isinstance(value, int):
            return ScoreDimension(score=max(0, min(5, value)), assessed=True)
        if isinstance(value, dict):
            score = value.get("score")
            if score is None:
                return ScoreDimension(
                    assessed=bool(value.get("assessed", False)),
                    evidence=list(value.get("evidence") or []),
                    hard_cap=value.get("hard_cap"),
                    cap_reason=value.get("cap_reason"),
                )
            return ScoreDimension(
                score=max(0, min(5, int(score))),
                assessed=True,
                evidence=list(value.get("evidence") or []),
                hard_cap=value.get("hard_cap"),
                cap_reason=value.get("cap_reason"),
            )
        raise CriticResponseError(
            "critic_response_schema_mismatch", f"bad scorecard.{key}"
        )

    return CriticScorecard(
        schema_concept_conformance=dim("schema_concept_conformance"),
        source_fidelity=dim("source_fidelity"),
        semantic_precision=dim("semantic_precision"),
        provenance_custody=dim("provenance_custody"),
        markings_authorization=dim("markings_authorization"),
        coverage_completeness=dim("coverage_completeness"),
        serializer_quality=dim("serializer_quality"),
        maintainability_reproducibility=dim("maintainability_reproducibility"),
    )


def load_review_schema() -> dict[str, Any]:
    return json.loads(
        (SCHEMA_DIR / "critic-review.schema.json").read_text(encoding="utf-8")
    )
