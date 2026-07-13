"""Deterministic critic analysis entrypoint (issue #75 Round 2)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import graph_validator
import relationship_kinds
import workspace_policy
from critic.context_builder import (
    build_prompt_package,
    build_serializer_overview,
    excerpt_serializer,
)
from critic.coverage import check_source_document_hash, compare_coverage_contract
from critic.finding_diff import assign_display_indexes, diff_findings
from critic.graph_heuristics import run_graph_heuristics
from critic.graph_integrity import analyze_graph_integrity, sha256_file
from critic.models import (
    CRITIC_SCHEMA_VERSION,
    ArtifactHashes,
    CriticArtifactRequest,
    CriticFinding,
    CriticReview,
    CriticTarget,
    SelfImprovementHandoffCandidate,
    ValidationSummary,
)
from critic.scorecard import build_deterministic_scorecard, merge_scorecards
from critic.serializer_python import analyze_python_serializer


class CriticError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


def analyze_artifact(request: CriticArtifactRequest) -> CriticReview:
    started = time.perf_counter()
    errors: list[str] = []
    rule_executions: list[dict[str, Any]] = []

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
            sp = workspace_policy.check_read_path(raw, include_write_roots=True)
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if not sp.is_file():
            raise CriticError("critic_graph_missing", f"source_missing:{sp.name}")
        source_paths.append(sp)

    coverage_path: Path | None = None
    if request.coverage_contract_path:
        try:
            coverage_path = workspace_policy.check_read_path(
                request.coverage_contract_path, include_write_roots=True
            )
        except ValueError as exc:
            raise CriticError("critic_path_outside_workspace", str(exc)) from exc
        if not coverage_path.is_file():
            raise CriticError("critic_graph_missing", "coverage_contract_missing")

    # project_root is internal — default to repository root; MCP tools must not
    # expose arbitrary caller selection without policy (Round 2 / #76).
    project_root = Path(__file__).resolve().parents[2]
    if request.project_root:
        candidate = Path(request.project_root).resolve()
        if candidate == project_root or project_root in candidate.parents:
            project_root = candidate

    hashes = ArtifactHashes(
        graph_sha256=sha256_file(graph_path),
        serializer_sha256=sha256_file(serializer_path) if serializer_path else None,
        source_sha256={
            # Preserve distinct keys when basenames collide
            f"{p.parent.name}/{p.name}" if True else p.name: sha256_file(p)
            for p in source_paths
        },
        coverage_contract_sha256=(
            sha256_file(coverage_path) if coverage_path else None
        ),
    )
    # Prefer plain basename when unique
    if len({p.name for p in source_paths}) == len(source_paths):
        hashes.source_sha256 = {p.name: sha256_file(p) for p in source_paths}

    findings: list[CriticFinding] = []
    view = None

    if request.critic_scope in {"graph", "both"}:
        view, integrity_findings, integrity_exec = analyze_graph_integrity(
            graph_path, artifact_hash=hashes.graph_sha256
        )
        findings.extend(integrity_findings)
        rule_executions.extend(e.to_dict() for e in integrity_exec)

        heur_findings, heur_exec = run_graph_heuristics(
            view, artifact_hash=hashes.graph_sha256
        )
        findings.extend(heur_findings)
        rule_executions.extend(e.to_dict() for e in heur_exec)

        if coverage_path:
            cov_findings, cov_exec = compare_coverage_contract(
                view, coverage_path, artifact_hash=hashes.graph_sha256
            )
            findings.extend(cov_findings)
            rule_executions.extend(e.to_dict() for e in cov_exec)

        for sp in source_paths:
            src_findings, src_exec = check_source_document_hash(
                view,
                source_name=sp.name,
                expected_sha256=sha256_file(sp),
                artifact_hash=hashes.graph_sha256,
            )
            findings.extend(src_findings)
            rule_executions.extend(e.to_dict() for e in src_exec)

        if view and view.raw_document is not None:
            lint = relationship_kinds.lint_relationship_kinds(view.raw_document)
            lint_findings: list[CriticFinding] = []
            for item in lint.get("findings") or []:
                node_id = item.get("node_id")
                f = CriticFinding(
                    finding_id="",
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
                f.ensure_identity_key()
                lint_findings.append(f)
            findings.extend(lint_findings)
            rule_executions.append(
                {
                    "rule_id": "CRIT-G-REL-KIND-LINT",
                    "rule_version": "1.1.0",
                    "status": "evaluated",
                    "input_artifact_hash": hashes.graph_sha256,
                    "targets_examined": lint.get("checked", 0),
                    "finding_ids": [f.finding_id for f in lint_findings],
                    "error_code": None,
                }
            )

    validation = _run_validation(
        graph_path,
        extensions=request.extensions,
        profiles=request.profiles,
        project_root=project_root,
        errors=errors,
    )
    findings.extend(_validation_findings(validation))

    serializer_excerpts: list[dict[str, Any]] = []
    serializer_overview: dict[str, Any] | None = None
    if serializer_path and request.critic_scope in {"serializer", "both"}:
        # Bound read: first 256 KiB for AST; overview from same buffer
        max_ser_bytes = 256 * 1024
        raw = serializer_path.read_bytes()[:max_ser_bytes]
        source_text = raw.decode("utf-8", errors="replace")
        if serializer_path.suffix.lower() == ".py":
            ser_findings = analyze_python_serializer(
                serializer_path,
                source_text,
                serializer_mode=request.serializer_mode,
            )
            findings.extend(ser_findings)
            serializer_excerpts = excerpt_serializer(
                source_text, ser_findings, path_name=serializer_path.name
            )
            serializer_overview = build_serializer_overview(
                source_text, path_name=serializer_path.name
            )
            rule_executions.append(
                {
                    "rule_id": "CRIT-S-PY-SUITE",
                    "rule_version": "1.1.0",
                    "status": "evaluated",
                    "input_artifact_hash": hashes.serializer_sha256,
                    "targets_examined": 1,
                    "finding_ids": [f.finding_id for f in ser_findings],
                    "error_code": None,
                }
            )
        else:
            serializer_overview = {
                "path": serializer_path.name,
                "note": "non-python overview only",
            }

    # Rule-execution ledger → resolve only when rule evaluated successfully
    evaluated_rules = {
        e["rule_id"]
        for e in rule_executions
        if e.get("status") == "evaluated"
    }
    skipped_rules = {
        e["rule_id"]
        for e in rule_executions
        if e.get("status") in {"skipped", "failed", "not_applicable"}
    }
    current_by_rule: dict[str, set[str]] = {}
    for f in findings:
        if f.rule_id:
            current_by_rule.setdefault(f.rule_id, set()).add(f.finding_id)

    resolved_ids: set[str] = set()
    unevaluated_ids: set[str] = set()
    for old in request.prior_findings:
        if old.evidence_kind != "deterministic" or not old.rule_id:
            unevaluated_ids.add(old.finding_id)
            continue
        if old.rule_id in skipped_rules or old.rule_id not in evaluated_rules:
            unevaluated_ids.add(old.finding_id)
            continue
        # Rule evaluated successfully and finding absent → resolved
        if old.finding_id not in {f.finding_id for f in findings}:
            resolved_ids.add(old.finding_id)
        # else persisting via diff

    diff = diff_findings(
        list(request.prior_findings),
        findings,
        disputed_identity_keys=request.disputed_identity_keys,
        resolved_finding_ids=resolved_ids,
        unevaluated_finding_ids=unevaluated_ids,
    )
    merged = diff.all_for_review()
    assign_display_indexes([f for f in merged if f.status != "resolved"])

    scorecard = build_deterministic_scorecard(
        validation,
        [f for f in merged if f.status != "resolved"],
        has_sources=bool(source_paths),
        has_serializer=bool(serializer_path),
        has_coverage_contract=bool(coverage_path),
    )
    scorecard = merge_scorecards(scorecard, None)

    source_excerpts = _bounded_source_excerpts(source_paths)
    try:
        prompt_package = build_prompt_package(
            artifact_hashes=hashes,
            validation=validation,
            deterministic_findings=[f for f in merged if f.status != "resolved"],
            graph_view=view,
            serializer_excerpts=serializer_excerpts,
            serializer_overview=serializer_overview,
            source_excerpts=source_excerpts,
            prior_findings=list(request.prior_findings),
            extensions=request.extensions,
            profiles=request.profiles,
            session_id=request.session_id,
            pass_number=request.pass_number,
        )
    except ValueError as exc:
        if str(exc) == "critic_prompt_package_too_large":
            raise CriticError("critic_prompt_package_too_large") from exc
        raise

    status = _status_from(validation, merged, errors)
    suggestions = _conservative_handoff_suggestions(
        merged, validation.bundle_fingerprint
    )

    return CriticReview(
        schema_version=CRITIC_SCHEMA_VERSION,
        artifact_hashes=hashes,
        validation=validation,
        deterministic_findings=[f for f in merged if f.evidence_kind == "deterministic"],
        critic_findings=[],
        merged_findings=merged,
        scorecard=scorecard,
        prompt_package=prompt_package,
        status=status,
        rule_executions=rule_executions,
        finding_diff=diff.to_dict(),
        elapsed_ms=int((time.perf_counter() - started) * 1000),
        handoff_suggestions=suggestions,
        handoff_candidates=suggestions,
        errors=errors,
        token_estimate=prompt_package.get("token_estimate"),
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
    except Exception as exc:  # noqa: BLE001
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
        f = CriticFinding(
            finding_id="",
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
        f.ensure_identity_key()
        findings.append(f)
    elif validation.verification_status != "complete" or validation.conforms is not True:
        f = CriticFinding(
            finding_id="",
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
        f.ensure_identity_key()
        findings.append(f)
    for item in validation.profile_not_selected:
        f = CriticFinding(
            finding_id="",
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
        f.ensure_identity_key()
        findings.append(f)
    return findings


def _status_from(
    validation: ValidationSummary,
    findings: list[CriticFinding],
    errors: list[str],
) -> str:
    open_findings = [f for f in findings if f.status != "resolved"]
    if "critic_validation_unavailable" in errors:
        return "validation_incomplete"
    if validation.verification_status != "complete":
        return "validation_incomplete"
    actionable = [f for f in open_findings if f.severity in {"critical", "high"}]
    if actionable:
        return "needs_revision"
    medium = [f for f in open_findings if f.severity == "medium"]
    if medium:
        return "completed_with_findings"
    if validation.conforms is True:
        return "deterministic_clean"
    return "needs_revision"


def _bounded_source_excerpts(
    paths: list[Path], *, max_chars: int = 800, max_read: int = 4096
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path in paths[:5]:
        raw = path.read_bytes()[:max_read]
        text = raw.decode("utf-8", errors="replace")
        if len(text) > max_chars:
            text = text[: max_chars - 1] + "…"
        out.append(
            {
                "path": path.name,
                "sha256": sha256_file(path),
                "text": text,
            }
        )
    return out


def _conservative_handoff_suggestions(
    findings: list[CriticFinding],
    bundle_fingerprint: str | None,
) -> list[SelfImprovementHandoffCandidate]:
    """Round 2: ordinary artifact defects are NOT persistent-learning suggestions."""

    # Only emit unverified suggestions when the same rule fires repeatedly-like
    # signal: multiple high findings of sdk_bug-ish serializer_api on private API
    # still stay as suggestion_only / unverified — and we default to empty for
    # single case defects.
    return []
