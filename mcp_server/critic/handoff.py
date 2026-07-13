"""Operator-approved critic → self-improvement handoff preview (issue #78)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import workspace_policy
from critic.sessions import CriticSessionError, load_session_for_handoff
from critic.schema_util import load_json_schema
from jsonschema import Draft202012Validator

HANDOFF_TYPES = frozenset(
    {
        "recipe_improvement",
        "routing_gap",
        "new_recipe_candidate",
        "ontology_gap",
        "extension_gap",
        "sdk_bug",
    }
)

_CATEGORY_DEFAULTS = {
    "serializer_api": "sdk_bug",
    "serializer_validation": "sdk_bug",
    "serializer_safety": "sdk_bug",
    "serializer_performance": "sdk_bug",
    "coverage": "recipe_improvement",
    "source_fidelity": "recipe_improvement",
    "relationship_direction": "recipe_improvement",
    "action_grammar": "recipe_improvement",
    "investigation_structure": "recipe_improvement",
    "authorization": "recipe_improvement",
    "markings": "recipe_improvement",
    "provenance": "recipe_improvement",
    "custody": "recipe_improvement",
    "facet_placement": "recipe_improvement",
    "dictionary_collision": "sdk_bug",
    "identity_conflation": "recipe_improvement",
    "generic_relationship": "recipe_improvement",
    "validation": "ontology_gap",
    "syntax_integrity": "sdk_bug",
    "relationship_vocabulary": "ontology_gap",
}


def _classify(category: str, requested: str | None) -> str:
    if requested:
        if requested not in HANDOFF_TYPES:
            raise CriticSessionError("critic_handoff_invalid_type", requested)
        return requested
    return _CATEGORY_DEFAULTS.get(category, "recipe_improvement")


def prepare_critic_handoff(
    session_id: str,
    finding_ids: list[str],
    *,
    requested_handoff_type: str | None = None,
    operator_rationale: str = "",
    operator_id: str = "",
    output_path: str | None = None,
    approve_write: bool = False,
) -> dict[str, Any]:
    """Build a preview handoff package from a finalized critic session."""

    if not finding_ids:
        raise CriticSessionError("critic_handoff_no_findings")
    if not operator_id.strip():
        raise CriticSessionError("critic_handoff_operator_required")

    loaded = load_session_for_handoff(session_id)
    session = loaded["session"]
    review = loaded["review"]
    critic = loaded["critic"]

    by_id: dict[str, dict[str, Any]] = {}
    for item in review.get("merged_findings") or []:
        by_id[str(item.get("finding_id"))] = item
    for item in critic.get("findings") or []:
        by_id[str(item.get("finding_id"))] = item

    missing = [fid for fid in finding_ids if fid not in by_id]
    if missing:
        raise CriticSessionError(
            "critic_handoff_unknown_finding", ",".join(missing[:10])
        )

    selected = []
    for fid in finding_ids:
        finding = by_id[fid]
        handoff_type = _classify(str(finding.get("category") or ""), requested_handoff_type)
        selected.append(
            {
                "finding_id": fid,
                "handoff_type": handoff_type,
                "severity": finding.get("severity"),
                "category": finding.get("category"),
                "rule_id": finding.get("rule_id"),
                "evidence_kind": finding.get("evidence_kind"),
                "confidence": finding.get("confidence"),
                "rationale": str(finding.get("rationale") or "")[:500],
                "recommended_change": str(finding.get("recommended_change") or "")[:500],
                "related_recipe": finding.get("related_recipe"),
            }
        )

    package = {
        "schema_version": "1.0.0",
        "handoff_kind": "critic_self_improvement_preview",
        "session_id": session_id,
        "session_schema_version": session.get("schema_version"),
        "artifact_hashes": review.get("artifact_hashes"),
        "validation": (session.get("latest_review_summary") or {}).get("validation"),
        "operator_id": operator_id.strip()[:128],
        "operator_rationale": operator_rationale.strip()[:2000],
        "requires_operator_approval": True,
        "suggestion_only": True,
        "unverified_generalization": True,
        "persistent_write": False,
        "selected_findings": selected,
        "created_at": time.time(),
        "notes": (
            "Preview only. Does not promote recipes, create issues, or write "
            "persistent SDK knowledge unless approve_write is explicitly set."
        ),
    }

    schema = load_json_schema("critic-handoff.schema.json")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(package),
        key=lambda e: list(e.path),
    )
    if errors:
        raise CriticSessionError(
            "critic_handoff_schema_mismatch", errors[0].message
        )

    written = None
    if approve_write:
        if not output_path:
            raise CriticSessionError("critic_handoff_output_required")
        try:
            dest = workspace_policy.check_write_path(output_path)
        except ValueError as exc:
            raise CriticSessionError(
                "critic_handoff_write_denied", str(exc)
            ) from exc
        dest.parent.mkdir(parents=True, exist_ok=True)
        package["persistent_write"] = True
        dest.write_text(
            json.dumps(package, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        written = str(dest)

    return {
        "preview": package,
        "written_path": written,
        "approve_write": bool(approve_write and written),
    }
