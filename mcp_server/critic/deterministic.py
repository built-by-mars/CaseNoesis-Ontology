"""Deterministic critic analysis entrypoint (issue #75).

Runs parse/integrity, reused validation + relationship lint, structural
heuristics, optional coverage/source checks, and Python serializer AST checks.
Produces a ``CriticReview`` with a bounded prompt package for sampling/manual
critics (#76). Does **not** call an LLM or mutate artifacts.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import graph_validator
import relationship_kinds
import workspace_policy
from critic.context_builder import build_prompt_package, excerpt_serializer
from critic.coverage import check_embedded_source_hash, compare_coverage_contract
from critic.finding_diff import assign_sequential_ids, diff_findings
from critic.graph_heuristics import run_graph_heuristics
from critic.graph_integrity import (
    check_integrity,
    load_jsonld_graph,
    sha256_file,
)
from critic.models import (
    CRITIC_SCHEMA_VERSION,
    ArtifactHashes,
    CriticArtifactRequest,
    CriticFinding,
    CriticReview,
    CriticTarget,
    ValidationSummary,
)
from critic.scorecard import build_deterministic_scorecard, merge_scorecards
from critic.serializer_python import analyze_python_serializer


class CriticError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def analyze_artifact(request: CriticArtifactRequest) -> CriticReview:
    """Run a full deterministic critic pass and build a bounded prompt package."""

    started = time.perf_counter()
    errors: list[str] = []

    try:
        graph_path = workspace_policy.check_read_path(
            request.graph_path, include_write_roots=True
        )
    except ValueError as exc:
        raise CriticError("critic_path_outside_workspace", str(exc)) from exc

    if not graph_path.is_file():
        raise CriticError("critic_graph_missing")

    serializer_path: Path | None = None
    if request.serializer_path and request.critic_scope in {"serializer", "both"}:
        try:
            serializer_path = workspace_policy.check_read_path(
                request.serializer_path, include_write_roots=True
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if not serializer_path.is_file():
            raise CriticError("critic_serializer_missing")

    source_paths: list[Path] = []
    for raw in request.source_paths:
        try:
            source_paths.append(
                workspace_policy.check_read_path(raw, include_write_roots=True)
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc

    coverage_path: Path | None = None
    if request.coverage_contract_path:
        try:
            coverage_path = workspace_policy.check_read_path(
                request.coverage_contract_path, include_write_roots=True
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc

    project_root = (
        Path(request.project_root).resolve()
        if request.project_root
        else Path(__file__).resolve().parents[2]
    )

    hashes = ArtifactHashes(
        graph_sha256=sha256_file(graph_path),
        serializer_sha256=sha256_file(serializer_path) if serializer_path else None,
        source_sha256={p.name: sha256_file(p) for p in source_paths if p.is_file()},
        coverage_contract_sha256=(
            sha256_file(coverage_path) if coverage_path and coverage_path.is_file() else None
        ),
    )

    findings: list[CriticFinding] = []
    document: dict[str, Any] | None = None

    if request.critic_scope in {"graph", "both"}:
        document, parse_findings = load_jsonld_graph(graph_path)
        findings.extend(parse_findings)
        if document is not None:
            findings.extend(check_integrity(document))
            findings.extend(run_graph_heuristics(document))
            if coverage_path and coverage_path.is_file():
                findings.extend(compare_coverage_contract(document, coverage_path))
            findings.extend(
                check_embedded_source_hash(document, hashes.source_sha256)
            )

            # Relationship lint on parsed JSON-LD
            lint = relationship_kinds.lint_relationship_kinds(document)
            for item in lint.get("findings") or []:
                node_id = item.get("node_id")
                findings.append(
                    CriticFinding(
                        finding_id="CRIT-PENDING",
                        severity="medium" if item.get("severity") == "warning" else "high",
                        category="relationship_vocabulary",
                        confidence=1.0,
                        status="new",
                        target=CriticTarget(
                            node_id=node_id if isinstance(node_id, str) else None,
                            predicate="uco-core:kindOfRelationship",
                        ),
                        evidence_kind="deterministic",
                        evidence=[str(item.get("kind") or "")],
                        rationale=str(item.get("message") or "relationship kind lint"),
                        recommended_change=(
                            "Use a vocabulary member or justify open-vocabulary kind."
                        ),
                        verification_method="relationship_kinds.lint_relationship_kinds",
                        rule_id="CRIT-G-REL-KIND-LINT",
                    )
                )

    validation = _run_validation(
        graph_path,
        extensions=request.extensions,
        profiles=request.profiles,
        project_root=project_root,
        errors=errors,
    )

    # Map validation issues into findings
    findings.extend(_validation_findings(validation))

    serializer_excerpts: list[dict[str, Any]] = []
    if serializer_path and request.critic_scope in {"serializer", "both"}:
        source_text = serializer_path.read_text(encoding="utf-8", errors="replace")
        if serializer_path.suffix.lower() == ".py":
            ser_findings = analyze_python_serializer(serializer_path, source_text)
            findings.extend(ser_findings)
            serializer_excerpts = excerpt_serializer(
                source_text, ser_findings, path_name=serializer_path.name
            )
        else:
            findings.append(
                CriticFinding(
                    finding_id="CRIT-PENDING",
                    severity="info",
                    category="serializer_api",
                    confidence=1.0,
                    status="new",
                    target=CriticTarget(path=serializer_path.name),
                    evidence_kind="deterministic",
                    evidence=[f"language={serializer_path.suffix}"],
                    rationale=(
                        "Non-Python serializers receive bounded text review in #76; "
                        "deep AST analysis is Python-first in v1.22."
                    ),
                    recommended_change="Optional: provide a Python builder or await language analyzers.",
                    verification_method="Check serializer_path suffix.",
                    rule_id="CRIT-S-NON-PYTHON",
                )
            )
            serializer_excerpts = [
                {
                    "path": serializer_path.name,
                    "start_line": 1,
                    "end_line": min(40, source_text.count("\n") + 1),
                    "text": "\n".join(source_text.splitlines()[:40]),
                }
            ]

    # Re-running deterministic rules is explicit verification: a prior
    # deterministic finding whose identity_key is absent from the new scan
    # is treated as resolved.
    prior = list(request.prior_findings)
    current_keys = {f.ensure_identity_key() for f in findings}
    resolved_keys = {
        old.ensure_identity_key()
        for old in prior
        if old.evidence_kind == "deterministic"
        and old.rule_id
        and old.ensure_identity_key() not in current_keys
    }

    diff = diff_findings(
        prior,
        findings,
        disputed_identity_keys=request.disputed_identity_keys,
        resolved_identity_keys=resolved_keys,
    )
    merged = [f for f in diff.apply_statuses() if f.status != "resolved"]
    assign_sequential_ids(merged)

    scorecard = build_deterministic_scorecard(validation, merged)
    # Model score unused in deterministic-only pass
    scorecard = merge_scorecards(scorecard, None)

    try:
        prompt_package = build_prompt_package(
            artifact_hashes=hashes,
            validation=validation,
            deterministic_findings=merged,
            graph_document=document,
            serializer_excerpts=serializer_excerpts,
            source_excerpts=_source_excerpts(source_paths),
            prior_findings=prior,
            extensions=request.extensions,
            profiles=request.profiles,
        )
    except ValueError as exc:
        if str(exc) == "critic_prompt_package_too_large":
            raise CriticError("critic_prompt_package_too_large") from exc
        raise

    status = _status_from(validation, merged, errors)

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    return CriticReview(
        schema_version=CRITIC_SCHEMA_VERSION,
        artifact_hashes=hashes,
        validation=validation,
        deterministic_findings=list(merged),
        critic_findings=[],
        merged_findings=list(merged),
        scorecard=scorecard,
        prompt_package=prompt_package,
        status=status,
        elapsed_ms=elapsed_ms,
        handoff_candidates=_classify_handoffs(merged),
        errors=errors,
    )


def _run_validation(
    graph_path: Path,
    *,
    extensions: list[str],
    profiles: list[str],
    project_root: Path,
    errors: list[str],
) -> ValidationSummary:
    if not graph_validator.validator_available():
        errors.append("critic_validation_unavailable")
        return ValidationSummary(
            conforms=None,
            verification_status="could_not_verify",
            error_code="critic_validation_unavailable",
            safe_summary="case_validate CLI is not available",
            selected_extensions=list(extensions),
            selected_profiles=list(profiles),
        )

    try:
        report = graph_validator.validate_graph_file(
            graph_path,
            extensions=extensions or None,
            profiles=profiles or None,
            project_root=project_root,
        )
    except Exception as exc:  # noqa: BLE001 — typed surface for critic
        errors.append("critic_validation_incomplete")
        return ValidationSummary(
            conforms=None,
            verification_status="could_not_verify",
            error_code="critic_validation_incomplete",
            safe_summary=type(exc).__name__,
            selected_extensions=list(extensions),
            selected_profiles=list(profiles),
        )

    stage = dict(report.stage_status)
    return ValidationSummary(
        conforms=report.conforms,
        verification_status=report.verification_status,
        violation_count=report.violation_count,
        warning_count=report.warning_count,
        bundle_fingerprint=report.bundle_fingerprint,
        selected_profiles=list(report.selected_profiles),
        selected_extensions=list(report.selected_extensions),
        stage_status={k: v for k, v in stage.items()} if stage else {},
        profile_not_selected=list(report.profile_not_selected),
        role_mismatches=[list(t) for t in report.role_mismatches],
        safe_summary=report.safe_summary,
        error_code=(
            None
            if report.verification_status == "complete"
            else "critic_validation_incomplete"
        ),
    )


def _validation_findings(validation: ValidationSummary) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    if validation.error_code == "critic_validation_unavailable":
        findings.append(
            CriticFinding(
                finding_id="CRIT-PENDING",
                severity="critical",
                category="validation",
                confidence=1.0,
                status="new",
                target=CriticTarget(),
                evidence_kind="deterministic",
                evidence=["validator_unavailable"],
                rationale="Required validation stage could not run (case_validate missing).",
                recommended_change="Install case-utils and re-run the critic.",
                verification_method="shutil.which('case_validate')",
                rule_id="CRIT-V-UNAVAILABLE",
                related_validation_result="could_not_verify",
            )
        )
    elif validation.verification_status != "complete" or validation.conforms is not True:
        findings.append(
            CriticFinding(
                finding_id="CRIT-PENDING",
                severity="critical",
                category="validation",
                confidence=1.0,
                status="new",
                target=CriticTarget(),
                evidence_kind="deterministic",
                evidence=[
                    f"conforms={validation.conforms}",
                    f"verification_status={validation.verification_status}",
                    f"violations={validation.violation_count}",
                ],
                rationale="Graph validation is incomplete or non-conforming.",
                recommended_change="Resolve SHACL/coverage failures before acceptance.",
                verification_method="graph_validator.validate_graph_file",
                rule_id="CRIT-V-NONCONFORMING",
                related_validation_result=validation.verification_status,
            )
        )
    for item in validation.profile_not_selected:
        findings.append(
            CriticFinding(
                finding_id="CRIT-PENDING",
                severity="high",
                category="validation",
                confidence=1.0,
                status="new",
                target=CriticTarget(
                    node_id=(
                        str(item.get("term"))
                        if isinstance(item, dict) and item.get("term")
                        else None
                    )
                ),
                evidence_kind="deterministic",
                evidence=[str(item)],
                rationale="Upper-ontology term used without selecting its profile.",
                recommended_change="Pass the required profile in the validation bundle.",
                verification_method="validation.profile_not_selected",
                rule_id="CRIT-V-PROFILE-NOT-SELECTED",
            )
        )
    for finding in findings:
        finding.ensure_identity_key()
    return findings


def _status_from(
    validation: ValidationSummary,
    findings: list[CriticFinding],
    errors: list[str],
) -> str:
    if "critic_validation_unavailable" in errors:
        return "validation_incomplete"
    if validation.verification_status != "complete":
        return "validation_incomplete"
    actionable = [f for f in findings if f.severity in {"critical", "high"}]
    if actionable:
        return "needs_revision"
    medium = [f for f in findings if f.severity == "medium"]
    if medium:
        return "completed_with_findings"
    if validation.conforms is True:
        return "deterministic_clean"
    return "needs_revision"


def _source_excerpts(paths: list[Path], max_chars: int = 800) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in paths[:5]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        out.append(
            {
                "path": path.name,
                "sha256": sha256_file(path),
                "text": text[:max_chars] + ("…" if len(text) > max_chars else ""),
            }
        )
    return out


def _classify_handoffs(findings: list[CriticFinding]):
    from critic.models import SelfImprovementHandoffCandidate

    candidates: list[SelfImprovementHandoffCandidate] = []
    by_cat: dict[str, list[CriticFinding]] = {}
    for finding in findings:
        by_cat.setdefault(finding.category, []).append(finding)

    mapping = {
        "relationship_direction": "recipe_improvement",
        "generic_relationship": "recipe_improvement",
        "facet_placement": "recipe_improvement",
        "investigation_structure": "recipe_improvement",
        "serializer_api": "sdk_bug",
        "serializer_validation": "sdk_bug",
        "serializer_safety": "sdk_bug",
    }
    for category, handoff_type in mapping.items():
        group = by_cat.get(category) or []
        if not group:
            continue
        candidates.append(
            SelfImprovementHandoffCandidate(
                handoff_type=handoff_type,  # type: ignore[arg-type]
                finding_ids=[f.finding_id for f in group],
                summary=f"{len(group)} {category} finding(s) may indicate reusable SDK gap",
                recurrence_key=f"{handoff_type}:{category}",
                validation_evidence=[f.rule_id or "" for f in group if f.rule_id],
                requires_operator_approval=True,
            )
        )
    return candidates
