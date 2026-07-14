"""Operator-approved critic → self-improvement handoff preview (issue #78)."""

from __future__ import annotations

import hashlib
import json
import os
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
        "case_specific",
        "false_positive",
        "known_limitation",
        "generalizable",
    }
)

CANDIDATES_SUBDIR = Path("critic-handoffs") / "candidates"
HANDOFF_APPROVAL_ENV = "CASE_UCO_CRITIC_HANDOFF_TOKEN"


def prepare_critic_handoff(
    session_id: str,
    finding_ids: list[str],
    *,
    requested_handoff_type: str | None = None,
    operator_rationale: str = "",
    operator_id: str = "",
    output_path: str | None = None,
    approve_write: bool = False,
    approval_token: str | None = None,
) -> dict[str, Any]:
    """Build a preview handoff package from a finalized critic session.

    Persistent write requires:
    - explicit operator-selected handoff type (no auto category promotion)
    - approve_write=True
    - matching CASE_UCO_CRITIC_HANDOFF_TOKEN (never session extend challenge)
    - dedicated candidates directory under a write root
    - atomic O_EXCL create of the exact validated package
    """

    if not finding_ids:
        raise CriticSessionError("critic_handoff_no_findings")
    if not operator_id.strip():
        raise CriticSessionError("critic_handoff_operator_required")
    if not requested_handoff_type:
        raise CriticSessionError(
            "critic_handoff_type_required",
            "operator must explicitly select handoff type",
        )
    if requested_handoff_type not in HANDOFF_TYPES:
        raise CriticSessionError("critic_handoff_invalid_type", requested_handoff_type)

    profile = workspace_policy.deployment_profile()
    offline = profile == workspace_policy.PROFILE_OFFLINE_INVESTIGATION

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
        status = str(finding.get("status") or "")
        if status == "resolved":
            raise CriticSessionError("critic_handoff_finding_resolved", fid)
        selected.append(
            {
                "finding_id": fid,
                "handoff_type": requested_handoff_type,
                "severity": finding.get("severity"),
                "category": finding.get("category"),
                "rule_id": finding.get("rule_id"),
                "evidence_kind": finding.get("evidence_kind"),
                "confidence": finding.get("confidence"),
                "status": status,
                "rationale": str(finding.get("rationale") or "")[:500],
                "recommended_change": str(finding.get("recommended_change") or "")[:500],
                "related_recipe": finding.get("related_recipe"),
            }
        )

    package: dict[str, Any] = {
        "schema_version": "1.1.0",
        "handoff_kind": "critic_self_improvement_preview",
        "session_id": session_id,
        "session_schema_version": session.get("schema_version"),
        "artifact_hashes": review.get("artifact_hashes")
        or session.get("latest_reviewed_artifacts"),
        "validation": (session.get("latest_review_summary") or {}).get("validation"),
        "operator_id": operator_id.strip()[:128],
        "operator_rationale": operator_rationale.strip()[:2000],
        "requires_operator_approval": True,
        "suggestion_only": True,
        "unverified_generalization": True,
        "persistent_write": False,
        "handoff_type": requested_handoff_type,
        "selected_findings": selected,
        "next_tools": [
            "knowledge_lifecycle_preview",
            "draft_change_proposal",
        ],
        "created_at": time.time(),
        "notes": (
            "Preview only. Does not promote recipes, create issues, call GitHub, "
            "or write extension ontologies. Operator must use next_tools manually."
        ),
        "deployment_profile": profile,
    }

    schema = load_json_schema("critic-handoff.schema.json")
    _validate_handoff(schema, package)

    written = None
    package_sha256 = None
    if approve_write:
        # Offline profile: preview is allowed; persistent writes are not.
        if offline:
            raise CriticSessionError(
                "critic_handoff_profile_denied",
                "offline-investigation profile forbids persistent handoffs",
            )
        # NEVER accept extend_approval_challenge — dedicated out-of-band token only.
        expected = os.environ.get(HANDOFF_APPROVAL_ENV)
        if not expected or not approval_token or approval_token != expected:
            raise CriticSessionError("critic_handoff_approval_denied")
        # Reject tokens that match session extend challenge even if env is unset
        # (defense: never treat extend challenge as handoff approval).
        extend_challenge = session.get("extend_approval_challenge")
        if extend_challenge and approval_token == extend_challenge:
            raise CriticSessionError("critic_handoff_approval_denied")

        write_roots = workspace_policy.write_roots()
        if not write_roots:
            raise CriticSessionError("critic_handoff_write_denied", "no write root")
        candidates = (write_roots[0] / CANDIDATES_SUBDIR).resolve()
        try:
            workspace_policy.check_write_path(
                str(candidates), enforce_no_overwrite=False
            )
        except ValueError as exc:
            raise CriticSessionError("critic_handoff_write_denied", "candidates") from exc
        candidates.mkdir(parents=True, exist_ok=True)
        if output_path:
            dest = Path(output_path).expanduser()
            if not dest.is_absolute():
                dest = (candidates / dest.name).resolve()
            else:
                dest = dest.resolve()
        else:
            dest = (candidates / f"{session_id}-{int(time.time())}.json").resolve()

        try:
            dest.relative_to(candidates)
        except ValueError as exc:
            raise CriticSessionError(
                "critic_handoff_write_denied",
                "destination outside critic-handoffs/candidates",
            ) from exc

        final_package = dict(package)
        final_package["persistent_write"] = True
        final_package["written_at"] = time.time()
        final_package.pop("package_sha256", None)
        _validate_handoff(schema, final_package)
        # Hash covers canonical JSON of the package without package_sha256.
        body_raw = json.dumps(final_package, indent=2, sort_keys=True) + "\n"
        package_sha256 = hashlib.sha256(body_raw.encode("utf-8")).hexdigest()
        final_package["package_sha256"] = package_sha256
        _validate_handoff(schema, final_package)
        raw = json.dumps(final_package, indent=2, sort_keys=True) + "\n"

        try:
            fd = os.open(
                str(dest),
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                0o600,
            )
        except FileExistsError as exc:
            raise CriticSessionError(
                "critic_handoff_write_denied", "destination exists"
            ) from exc
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            try:
                os.unlink(dest)
            except OSError:
                # Best-effort cleanup of a partial handoff write.
                pass
            raise
        written = str(dest)
        package = final_package

    return {
        "session_id": session_id,
        "preview": package,
        "written_path": written,
        "package_sha256": package_sha256,
        "requires_operator_approval": True,
    }


def _validate_handoff(schema: dict[str, Any], package: dict[str, Any]) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(package),
        key=lambda e: list(e.path),
    )
    if errors:
        raise CriticSessionError(
            "critic_handoff_schema_mismatch", errors[0].message
        )
