"""Resumable critic-session state machine (issue #76)."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import tempfile
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterator, Literal

import workspace_policy
from critic.deterministic import CriticError, analyze_artifact
from critic.file_lock import FileLock, ensure_lock_file
from critic.graph_integrity import sha256_file
from critic.models import CriticArtifactRequest, CriticFinding, CriticReview, CriticScorecard
from critic.pass_merge import finalize_outcome_from_summary, merge_completed_pass_review
from critic.response_parser import (
    CriticResponseError,
    build_assessment_ledger,
    parse_critic_model_response,
)
from critic.schema_util import compute_review_config_sha256

REQUIRED_PASSES = 2
MAX_TOTAL_PASSES = 8
SESSION_DIR_NAME = "critic-sessions"
CRITIC_SESSION_SCHEMA = "1.1.0"
HANDOFF_CANDIDATES_DIR = "critic-handoffs/candidates"

ModelPolicy = Literal["disabled", "manual", "client_sampling"]
SessionState = Literal[
    "awaiting_critic_response",
    "awaiting_revision",
    "finalized",
    "cancelled",
    "failed",
]

POLICY_ENV = "CASE_UCO_CRITIC_MODEL_POLICY"
SESSION_ROOT_ENV = "CASE_UCO_CRITIC_SESSION_ROOT"
EXTEND_TOKEN_ENV = "CASE_UCO_CRITIC_EXTEND_TOKEN"
PERSIST_PROMPTS_ENV = "CASE_UCO_CRITIC_PERSIST_PROMPTS"
DEPLOYMENT_MODE_ENV = "CASE_UCO_MCP_CRITIC_MODE"

# Fields retained on disk for review-pass-N.json (prompt body never persisted by default).
_REVIEW_PASS_KEEP = (
    "artifact_hashes",
    "validation",
    "merged_findings",
    "scorecard",
    "analysis_status",
    "status",
    "rule_executions",
    "errors",
    "elapsed_ms",
)


class CriticSessionError(Exception):
    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code


@dataclass
class SessionConfig:
    graph_path: str
    serializer_path: str | None = None
    source_paths: list[str] = field(default_factory=list)
    coverage_contract_path: str | None = None
    extensions: list[str] = field(default_factory=list)
    profiles: list[str] = field(default_factory=list)
    critic_scope: str = "both"
    additional_iterations: int = 0
    model_policy: ModelPolicy = "manual"
    report_output: str | None = None
    project_root: str | None = None
    serializer_mode: str = "auto"
    extra_ontology_graphs: list[str] = field(default_factory=list)
    force_rdfs_inference: bool = False


def normalize_model_policy(raw: str | None) -> ModelPolicy | None:
    """Normalize hyphen/underscore policy strings to ModelPolicy values."""

    if raw is None:
        return None
    cleaned = str(raw).strip().lower().replace("-", "_")
    if cleaned in {"disabled", "manual", "client_sampling"}:
        return cleaned  # type: ignore[return-value]
    return None


def default_model_policy() -> ModelPolicy:
    return normalize_model_policy(os.environ.get(POLICY_ENV)) or "manual"


def deployment_critic_mode() -> ModelPolicy:
    """Non-bypassable deployment gate for sampling.

    Explicit ``CASE_UCO_MCP_CRITIC_MODE`` always wins. When unset, profile
    defaults apply:

    - ``offline-investigation`` → ``manual``
    - production-like (``secure`` / ``production`` / ``prod`` /
      ``production-authoring`` / ``production-review``) → ``disabled``
    - otherwise (local/dev) → ``client_sampling``
    """

    explicit = normalize_model_policy(os.environ.get(DEPLOYMENT_MODE_ENV))
    if explicit is not None:
        return explicit
    profile = (os.environ.get("CASE_UCO_MCP_PROFILE") or "").strip().lower()
    if profile == "offline-investigation":
        return "manual"
    if profile in {
        "secure",
        "production",
        "prod",
        "production-authoring",
        "production-review",
    }:
        return "disabled"
    return "client_sampling"


def effective_model_policy(requested: str | ModelPolicy | None) -> ModelPolicy:
    """Clamp requested session policy by deployment mode ceiling."""

    requested_norm = normalize_model_policy(requested) or default_model_policy()
    deployment = deployment_critic_mode()
    rank = {"disabled": 0, "manual": 1, "client_sampling": 2}
    if rank[requested_norm] > rank[deployment]:
        return deployment
    return requested_norm


def _persist_prompts_enabled() -> bool:
    raw = (os.environ.get(PERSIST_PROMPTS_ENV) or "").strip().lower()
    return raw in {"1", "true", "yes"}


def session_root() -> Path:
    """Resolve session root under an approved write root (fail closed)."""

    override = os.environ.get(SESSION_ROOT_ENV)
    write_roots = workspace_policy.write_roots()
    if override:
        candidate = Path(override).expanduser().resolve()
        try:
            checked = workspace_policy.check_write_path(
                str(candidate), enforce_no_overwrite=False
            )
        except ValueError as exc:
            raise CriticSessionError(
                "critic_session_root_denied", "session root outside write roots"
            ) from exc
        checked.mkdir(parents=True, exist_ok=True)
        return checked
    if write_roots:
        path = (write_roots[0] / SESSION_DIR_NAME).resolve()
        try:
            checked = workspace_policy.check_write_path(
                str(path), enforce_no_overwrite=False
            )
        except ValueError as exc:
            raise CriticSessionError(
                "critic_session_root_denied", "session root outside write roots"
            ) from exc
        checked.mkdir(parents=True, exist_ok=True)
        return checked
    raise CriticSessionError(
        "critic_session_root_unavailable",
        "no write root configured for critic sessions",
    )


def _session_dir(session_id: str) -> Path:
    if not session_id.startswith("critsess-") or "/" in session_id or ".." in session_id:
        raise CriticSessionError("critic_session_invalid_id")
    return session_root() / session_id


@contextmanager
def _locked(session_id: str) -> Iterator[Path]:
    directory = _session_dir(session_id)
    if not directory.is_dir():
        raise CriticSessionError("critic_session_not_found")
    lock_path = directory / "lock"
    ensure_lock_file(lock_path)
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        with FileLock(lock_file):
            yield directory


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name, dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def _append_audit(
    directory: Path,
    event: str,
    payload: dict[str, Any],
    *,
    prior_state: str | None = None,
    new_state: str | None = None,
    artifact_set_sha256: str | None = None,
) -> None:
    audit_path = directory / "audit.jsonl"
    previous_event_sha256 = "0" * 64
    sequence = 0
    if audit_path.is_file():
        lines = [ln for ln in audit_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if lines:
            try:
                last = json.loads(lines[-1])
                previous_event_sha256 = str(last.get("event_sha256") or previous_event_sha256)
                sequence = int(last.get("sequence") or 0)
            except (json.JSONDecodeError, TypeError, ValueError):
                # Corrupt trailing audit line: start a new chain segment.
                pass
    sequence += 1
    body = {
        "ts": time.time(),
        "event": event,
        "sequence": sequence,
        "previous_event_sha256": previous_event_sha256,
        "prior_state": prior_state,
        "new_state": new_state,
        "artifact_set_sha256": artifact_set_sha256,
        **payload,
    }
    # Hash without event_sha256 field.
    event_sha256 = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    body["event_sha256"] = event_sha256
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(body, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _artifact_set_from_hashes(hashes: dict[str, Any]) -> dict[str, Any]:
    result = {
        "graph_sha256": hashes.get("graph_sha256"),
        "serializer_sha256": hashes.get("serializer_sha256"),
        "source_sha256": dict(hashes.get("source_sha256") or {}),
        "coverage_contract_sha256": hashes.get("coverage_contract_sha256"),
        "extra_ontology_sha256": dict(hashes.get("extra_ontology_sha256") or {}),
    }
    if hashes.get("review_config_sha256"):
        result["review_config_sha256"] = hashes["review_config_sha256"]
    return result


def _artifact_set_sha256(artifact_set: dict[str, Any]) -> str:
    payload = {
        "graph_sha256": artifact_set.get("graph_sha256"),
        "serializer_sha256": artifact_set.get("serializer_sha256"),
        "source_sha256": dict(sorted((artifact_set.get("source_sha256") or {}).items())),
        "coverage_contract_sha256": artifact_set.get("coverage_contract_sha256"),
        "extra_ontology_sha256": dict(
            sorted((artifact_set.get("extra_ontology_sha256") or {}).items())
        ),
    }
    if artifact_set.get("review_config_sha256"):
        payload["review_config_sha256"] = artifact_set["review_config_sha256"]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _extra_ontology_hashes(paths: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for idx, raw in enumerate(paths or [], start=1):
        path = _resolve_artifact_path(
            raw, allow_write_roots=True, label=f"extra_ontology:{idx}"
        )
        result[f"extra-{idx}:{path.name}"] = sha256_file(path)
    return result


def _artifact_set_for_config(
    hashes: dict[str, Any], cfg: dict[str, Any]
) -> dict[str, Any]:
    merged = dict(hashes)
    merged["extra_ontology_sha256"] = _extra_ontology_hashes(
        cfg.get("extra_ontology_graphs")
    )
    if hashes.get("review_config_sha256"):
        merged["review_config_sha256"] = hashes["review_config_sha256"]
    return _artifact_set_from_hashes(merged)


def _review_config_sha256_for(
    cfg: dict[str, Any],
    *,
    bundle_fingerprint: str | None = None,
    bundle_resource_hashes: dict[str, str] | None = None,
    extra_ontology_sha256: dict[str, str] | None = None,
) -> str:
    return compute_review_config_sha256(
        critic_scope=str(cfg.get("critic_scope") or "both"),
        serializer_mode=str(cfg.get("serializer_mode") or "auto"),
        extensions=list(cfg.get("extensions") or []),
        profiles=list(cfg.get("profiles") or []),
        force_rdfs_inference=bool(cfg.get("force_rdfs_inference")),
        extra_ontology_sha256=(
            dict(extra_ontology_sha256)
            if extra_ontology_sha256 is not None
            else _extra_ontology_hashes(cfg.get("extra_ontology_graphs"))
        ),
        bundle_fingerprint=bundle_fingerprint,
        bundle_resource_hashes=bundle_resource_hashes,
    )


def _bundle_resource_hashes_from_validation(
    validation: dict[str, Any] | None,
) -> dict[str, str]:
    if not validation:
        return {}
    raw = validation.get("bundle_resource_hashes")
    if isinstance(raw, dict):
        return {str(k): str(v) for k, v in raw.items()}
    return {}


_SESSION_REQUIRED_KEYS = frozenset(
    {
        "schema_version",
        "session_id",
        "state",
        "model_policy",
        "config",
        "current_pass",
        "latest_artifact_hash",
    }
)
_REVIEW_PASS_REQUIRED_KEYS = frozenset(
    {
        "artifact_hashes",
        "validation",
        "prompt_package_hash",
    }
)
_COMPLETED_PASS_REQUIRED_KEYS = frozenset(
    {
        "merged_findings",
        "artifact_hashes",
        "status",
    }
)
_CRITIC_PASS_REQUIRED_KEYS = frozenset({"findings"})


def _require_keys(
    data: dict[str, Any],
    required: frozenset[str],
    *,
    code: str,
    label: str,
) -> None:
    missing = sorted(required - set(data))
    if missing:
        raise CriticSessionError(code, f"{label} missing keys: {missing}")


def _load_json_object(path: Path, *, code: str, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise CriticSessionError(code, f"missing {label}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CriticSessionError(code, f"corrupt {label}") from exc
    if not isinstance(data, dict):
        raise CriticSessionError(code, f"{label} must be object")
    return data


def _load_review_pass(directory: Path, pass_number: int) -> dict[str, Any]:
    data = _load_json_object(
        directory / f"review-pass-{pass_number}.json",
        code="critic_session_corrupt",
        label=f"review-pass-{pass_number}.json",
    )
    _require_keys(
        data,
        _REVIEW_PASS_REQUIRED_KEYS,
        code="critic_session_corrupt",
        label=f"review-pass-{pass_number}.json",
    )
    return data


def _load_completed_pass(directory: Path, pass_number: int) -> dict[str, Any]:
    data = _load_json_object(
        directory / f"completed-pass-{pass_number}.json",
        code="critic_session_corrupt",
        label=f"completed-pass-{pass_number}.json",
    )
    _require_keys(
        data,
        _COMPLETED_PASS_REQUIRED_KEYS,
        code="critic_session_corrupt",
        label=f"completed-pass-{pass_number}.json",
    )
    return data


def _load_critic_pass(directory: Path, pass_number: int) -> dict[str, Any]:
    data = _load_json_object(
        directory / f"critic-pass-{pass_number}.json",
        code="critic_session_corrupt",
        label=f"critic-pass-{pass_number}.json",
    )
    _require_keys(
        data,
        _CRITIC_PASS_REQUIRED_KEYS,
        code="critic_session_corrupt",
        label=f"critic-pass-{pass_number}.json",
    )
    return data


def _verify_prompt_package_against_stored(
    package: dict[str, Any],
    *,
    stored_review: dict[str, Any],
    session: dict[str, Any],
) -> None:
    """Ensure rebuilt/loaded prompt package matches immutable review-pass metadata."""

    checks = (
        ("prompt_package_hash", "latest_prompt_package_hash"),
        ("prompt_content_sha256", "latest_prompt_content_sha256"),
        ("review_request_sha256", "latest_review_request_sha256"),
        ("response_schema_sha256", None),
        ("review_config_sha256", "latest_review_config_sha256"),
    )
    for package_field, session_field in checks:
        got = package.get(package_field)
        expected = stored_review.get(package_field)
        if expected is not None and got != expected:
            raise CriticSessionError(
                "critic_session_prompt_rebuild_mismatch", package_field
            )
        if session_field:
            session_expected = session.get(session_field)
            if session_expected is not None and got != session_expected:
                raise CriticSessionError(
                    "critic_session_prompt_rebuild_mismatch", package_field
                )


def _resolve_artifact_path(
    path: str,
    *,
    allow_write_roots: bool,
    label: str,
) -> Path:
    """Resolve artifact paths: generated graph/serializer may live under write roots.

    Evidence/source paths stay read-root-only when ``allow_write_roots`` is False,
    matching ``analyze_artifact`` for graphs/serializers.
    """

    try:
        if allow_write_roots:
            return workspace_policy.check_read_path(
                path, include_write_roots=True
            )
        return workspace_policy.check_read_path(path)
    except ValueError as exc:
        raise CriticSessionError(
            "critic_session_artifact_path_denied", label
        ) from exc


def _rehash_config_artifacts(cfg: dict[str, Any]) -> dict[str, Any]:
    """Resolve current config paths through workspace policy and rehash.

    Graph/serializer/coverage (generated) may sit under approved write roots.
    Source evidence paths remain read-root-only.
    """

    graph_path = _resolve_artifact_path(
        cfg["graph_path"], allow_write_roots=True, label="graph"
    )
    serializer_sha = None
    if cfg.get("serializer_path"):
        ser_path = _resolve_artifact_path(
            cfg["serializer_path"], allow_write_roots=True, label="serializer"
        )
        serializer_sha = sha256_file(ser_path)
    source_sha: dict[str, str] = {}
    for idx, raw in enumerate(cfg.get("source_paths") or [], start=1):
        path = _resolve_artifact_path(
            raw, allow_write_roots=False, label=f"source:{idx}"
        )
        source_sha[f"source-{idx}:{path.name}"] = sha256_file(path)
    coverage_sha = None
    if cfg.get("coverage_contract_path"):
        cov = _resolve_artifact_path(
            cfg["coverage_contract_path"],
            allow_write_roots=True,
            label="coverage",
        )
        coverage_sha = sha256_file(cov)
    return _artifact_set_from_hashes(
        {
            "graph_sha256": sha256_file(graph_path),
            "serializer_sha256": serializer_sha,
            "source_sha256": source_sha,
            "coverage_contract_sha256": coverage_sha,
            "extra_ontology_sha256": _extra_ontology_hashes(
                cfg.get("extra_ontology_graphs")
            ),
        }
    )


def _load(directory: Path) -> dict[str, Any]:
    path = directory / "session.json"
    if not path.is_file():
        raise CriticSessionError("critic_session_corrupt", "missing session.json")
    try:
        session = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CriticSessionError(
            "critic_session_corrupt", "corrupt session.json"
        ) from exc
    if not isinstance(session, dict) or not session.get("schema_version"):
        raise CriticSessionError(
            "critic_session_corrupt", "missing schema_version"
        )
    _require_keys(
        session,
        _SESSION_REQUIRED_KEYS,
        code="critic_session_corrupt",
        label="session.json",
    )
    if not isinstance(session.get("config"), dict):
        raise CriticSessionError("critic_session_corrupt", "config must be object")
    return session


def _save(directory: Path, session: dict[str, Any]) -> None:
    _atomic_write_json(directory / "session.json", session)


def _verify_audit_chain(directory: Path) -> None:
    """Walk audit.jsonl and verify sequence + previous_event_sha256 linkage."""

    audit_path = directory / "audit.jsonl"
    if not audit_path.is_file():
        raise CriticSessionError(
            "critic_session_audit_corrupt", "missing audit.jsonl"
        )
    previous_event_sha256 = "0" * 64
    expected_sequence = 0
    for line_no, line in enumerate(
        audit_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CriticSessionError(
                "critic_session_audit_corrupt", f"invalid json at line {line_no}"
            ) from exc
        expected_sequence += 1
        if int(event.get("sequence") or 0) != expected_sequence:
            raise CriticSessionError(
                "critic_session_audit_corrupt",
                f"sequence mismatch at line {line_no}",
            )
        if str(event.get("previous_event_sha256") or "") != previous_event_sha256:
            raise CriticSessionError(
                "critic_session_audit_corrupt",
                f"previous_event_sha256 mismatch at line {line_no}",
            )
        stored_hash = str(event.get("event_sha256") or "")
        body = {k: v for k, v in event.items() if k != "event_sha256"}
        computed = hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if stored_hash != computed:
            raise CriticSessionError(
                "critic_session_audit_corrupt",
                f"event_sha256 mismatch at line {line_no}",
            )
        previous_event_sha256 = stored_hash


def _write_config_pass(
    directory: Path,
    pass_number: int,
    *,
    config: dict[str, Any],
    package: dict[str, Any],
    validation: dict[str, Any] | None,
) -> None:
    extra_ontology_sha256 = _extra_ontology_hashes(config.get("extra_ontology_graphs"))
    snapshot = {
        "config": dict(config),
        "review_config_sha256": package.get("review_config_sha256"),
        "bundle_fingerprint": (validation or {}).get("bundle_fingerprint"),
        "bundle_resource_hashes": _bundle_resource_hashes_from_validation(validation),
        "extra_ontology_sha256": extra_ontology_sha256,
    }
    _atomic_write_json(directory / f"config-pass-{pass_number}.json", snapshot)


def _write_review_pass(
    directory: Path, pass_number: int, review: CriticReview
) -> dict[str, Any]:
    """Persist review metadata without raw prompt_package body by default."""

    full = review.to_dict()
    package = full.get("prompt_package") or review.prompt_package or {}
    stored: dict[str, Any] = {
        key: full[key] for key in _REVIEW_PASS_KEEP if key in full
    }
    if "schema_version" in full:
        stored["schema_version"] = full["schema_version"]
    stored["prompt_package_hash"] = package.get("prompt_package_hash")
    stored["prompt_content_sha256"] = package.get("prompt_content_sha256")
    stored["review_request_sha256"] = package.get("review_request_sha256")
    stored["review_config_sha256"] = package.get("review_config_sha256")
    stored["response_schema_sha256"] = package.get("response_schema_sha256")
    _atomic_write_json(directory / f"review-pass-{pass_number}.json", stored)
    if _persist_prompts_enabled():
        _atomic_write_json(
            directory / f"prompt-pass-{pass_number}.json", package
        )
    return stored


def _target_passes(additional_passes_approved: int) -> int:
    return REQUIRED_PASSES + int(additional_passes_approved)


def _open_actionable_blockers(session: dict[str, Any]) -> bool:
    """True when critical/high remain open, or actionable medium findings remain."""

    summary = session.get("latest_review_summary") or {}
    counts = summary.get("finding_counts") or {}
    if int(counts.get("critical_high_open") or 0) > 0:
        return True
    for finding in session.get("prior_findings") or []:
        if finding.get("status") in {"resolved"}:
            continue
        severity = finding.get("severity")
        if severity in {"critical", "high"}:
            return True
        # Actionable medium: explicitly non-suppressible open medium findings.
        if severity == "medium" and finding.get("suppressible") is False:
            return True
    return False


def rebuild_prompt_package_for_pass(
    session: dict[str, Any],
    directory: Path,
    pass_number: int,
) -> dict[str, Any]:
    """Rebuild the prompt package for schema binding when prompt-pass file is absent."""

    cfg = session["config"]
    prior: list[CriticFinding] = []
    if pass_number > 1:
        completed_path = directory / f"completed-pass-{pass_number - 1}.json"
        if completed_path.is_file():
            completed = _load_completed_pass(directory, pass_number - 1)
            prior = _findings_from_review_dict(completed)
    request = CriticArtifactRequest(
        graph_path=cfg["graph_path"],
        serializer_path=cfg.get("serializer_path"),
        source_paths=list(cfg.get("source_paths") or []),
        coverage_contract_path=cfg.get("coverage_contract_path"),
        extensions=list(cfg.get("extensions") or []),
        profiles=list(cfg.get("profiles") or []),
        critic_scope=cfg.get("critic_scope") or "both",
        project_root=cfg.get("project_root"),
        serializer_mode=cfg.get("serializer_mode") or "auto",  # type: ignore[arg-type]
        extra_ontology_graphs=list(cfg.get("extra_ontology_graphs") or []),
        force_rdfs_inference=bool(cfg.get("force_rdfs_inference")),
        prior_findings=prior,
        session_id=session["session_id"],
        pass_number=pass_number,
    )
    try:
        review = analyze_artifact(request)
    except CriticError as exc:
        raise CriticSessionError(exc.code, str(exc)) from exc
    if review.artifact_hashes.graph_sha256 != session.get("latest_artifact_hash"):
        raise CriticSessionError(
            "critic_session_hash_mismatch",
            "rebuilt prompt package artifact hash mismatch",
        )
    package = review.prompt_package
    review_config_sha = package.get("review_config_sha256")
    rebuilt_set = _artifact_set_for_config(
        {
            **review.artifact_hashes.to_dict(),
            "review_config_sha256": review_config_sha,
        },
        cfg,
    )
    latest_set = session.get("latest_artifact_set") or {}
    if latest_set and rebuilt_set != latest_set:
        raise CriticSessionError(
            "critic_session_hash_mismatch",
            "rebuilt prompt package artifact set mismatch",
        )
    stored_review = _load_review_pass(directory, pass_number)
    _verify_prompt_package_against_stored(
        package, stored_review=stored_review, session=session
    )
    # Config drift: recompute review_config_sha256 from session config + stored bundle.
    validation = stored_review.get("validation") or {}
    recomputed = _review_config_sha256_for(
        cfg,
        bundle_fingerprint=validation.get("bundle_fingerprint"),
        bundle_resource_hashes=_bundle_resource_hashes_from_validation(validation),
    )
    if review_config_sha != recomputed:
        raise CriticSessionError(
            "critic_session_prompt_rebuild_mismatch", "review_config_sha256"
        )
    return package


def _new_session_id() -> str:
    return f"critsess-{uuid.uuid4().hex}"


def _review_summary(review: CriticReview) -> dict[str, Any]:
    open_findings = [
        f
        for f in review.merged_findings
        if f.status not in {"resolved"}
    ]
    return {
        "status": review.status,
        "analysis_status": review.analysis_status,
        "artifact_hashes": review.artifact_hashes.to_dict(),
        "validation": {
            "conforms": review.validation.conforms,
            "verification_status": review.validation.verification_status,
            "error_code": review.validation.error_code,
            "bundle_fingerprint": review.validation.bundle_fingerprint,
        },
        "finding_counts": {
            "merged": len(review.merged_findings),
            "open": len(open_findings),
            "critical_high_open": len(
                [f for f in open_findings if f.severity in {"critical", "high"}]
            ),
        },
        "open_finding_ids": [f.finding_id for f in open_findings],
        "rule_execution_count": len(review.rule_executions),
        "scorecard": review.scorecard.to_dict(),
        "errors": list(review.errors),
        "elapsed_ms": review.elapsed_ms,
    }


def _open_critical_high(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        f
        for f in findings
        if f.get("status") not in {"resolved"}
        and f.get("severity") in {"critical", "high"}
    ]


def _findings_from_review_dict(review_dict: dict[str, Any]) -> list[CriticFinding]:
    return [
        CriticFinding.from_dict(item)
        for item in review_dict.get("merged_findings") or []
    ]


def build_sampling_messages(prompt_package: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": str(prompt_package.get("system_role") or ""),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "instruction": (
                        "Return ONLY a JSON object matching response_schema. "
                        "No markdown fences."
                    ),
                    "prompt_package": prompt_package,
                },
                sort_keys=True,
            ),
        },
    ]


def start_critic_review(
    graph_path: str,
    serializer_path: str | None = None,
    source_paths: list[str] | None = None,
    coverage_contract_path: str | None = None,
    extensions: list[str] | None = None,
    profiles: list[str] | None = None,
    critic_scope: str = "both",
    additional_iterations: int = 0,
    model_policy: str | None = None,
    report_output: str | None = None,
    project_root: str | None = None,
    serializer_mode: str = "auto",
    extra_ontology_graphs: list[str] | None = None,
    force_rdfs_inference: bool = False,
) -> dict[str, Any]:
    if additional_iterations < 0:
        raise CriticSessionError("critic_session_invalid_additional_iterations")
    if additional_iterations > MAX_TOTAL_PASSES - REQUIRED_PASSES:
        raise CriticSessionError(
            "critic_session_pass_cap",
            f"additional_iterations exceeds cap of {MAX_TOTAL_PASSES - REQUIRED_PASSES}",
        )
    policy = effective_model_policy(
        model_policy
        if normalize_model_policy(model_policy) is not None
        else default_model_policy()
    )
    approved_additional = int(additional_iterations)
    target_passes = _target_passes(approved_additional)
    max_passes = target_passes

    session_id = _new_session_id()
    directory = session_root() / session_id
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "lock").touch()

    request = CriticArtifactRequest(
        graph_path=graph_path,
        serializer_path=serializer_path,
        source_paths=list(source_paths or []),
        coverage_contract_path=coverage_contract_path,
        extensions=list(extensions or []),
        profiles=list(profiles or []),
        critic_scope=critic_scope,  # type: ignore[arg-type]
        project_root=project_root,
        serializer_mode=serializer_mode or "auto",  # type: ignore[arg-type]
        extra_ontology_graphs=list(extra_ontology_graphs or []),
        force_rdfs_inference=bool(force_rdfs_inference),
        session_id=session_id,
        pass_number=1,
    )
    try:
        review = analyze_artifact(request)
    except CriticError as exc:
        raise CriticSessionError(exc.code, str(exc)) from exc

    config = asdict(
        SessionConfig(
            graph_path=graph_path,
            serializer_path=serializer_path,
            source_paths=list(source_paths or []),
            coverage_contract_path=coverage_contract_path,
            extensions=list(extensions or []),
            profiles=list(profiles or []),
            critic_scope=critic_scope,
            additional_iterations=approved_additional,
            model_policy=policy,
            report_output=report_output,
            project_root=project_root,
            serializer_mode=serializer_mode or "auto",
            extra_ontology_graphs=list(extra_ontology_graphs or []),
            force_rdfs_inference=bool(force_rdfs_inference),
        )
    )
    _write_review_pass(directory, 1, review)
    _write_config_pass(
        directory,
        1,
        config=config,
        package=review.prompt_package,
        validation=review.validation.to_dict(),
    )

    extend_token = secrets.token_urlsafe(24)
    extend_challenge = secrets.token_urlsafe(18)
    review_config_sha = review.prompt_package.get("review_config_sha256")
    artifact_set = _artifact_set_for_config(
        {
            **review.artifact_hashes.to_dict(),
            "review_config_sha256": review_config_sha,
        },
        config,
    )
    session = {
        "schema_version": CRITIC_SESSION_SCHEMA,
        "session_id": session_id,
        "state": "awaiting_critic_response" if policy != "disabled" else "awaiting_revision",
        "model_policy": policy,
        "required_passes": REQUIRED_PASSES,
        "additional_passes_approved": approved_additional,
        "target_passes": target_passes,
        "max_total_passes": max_passes,
        "current_pass": 1,
        "completed_critic_responses": 0,
        "completed_deterministic_passes": 1,
        "config": config,
        "artifact_hash_history": [review.artifact_hashes.graph_sha256],
        "latest_artifact_hash": review.artifact_hashes.graph_sha256,
        "latest_reviewed_hash": None,
        "latest_artifact_set": artifact_set,
        "latest_reviewed_artifacts": None,
        "latest_prompt_package_hash": review.prompt_package.get("prompt_package_hash"),
        "latest_prompt_content_sha256": review.prompt_package.get("prompt_content_sha256"),
        "latest_review_request_sha256": review.prompt_package.get("review_request_sha256"),
        "latest_review_config_sha256": review_config_sha,
        "latest_serializer_sha256": review.artifact_hashes.serializer_sha256,
        "latest_bundle_fingerprint": (review.validation.bundle_fingerprint
                                      if hasattr(review.validation, "bundle_fingerprint")
                                      else None),
        "latest_review_summary": _review_summary(review),
        "prior_finding_ids": [f.finding_id for f in review.merged_findings],
        "prior_findings": [f.to_dict() for f in review.merged_findings],
        "extend_approval_token": extend_token,
        "extend_approval_challenge": extend_challenge,
        "passes": [
            {
                "pass_number": 1,
                "deterministic": _review_summary(review),
                "critic": None,
                "completed_pass": None,
            }
        ],
    }
    if policy == "disabled":
        session["state"] = "awaiting_revision"
        session["latest_reviewed_hash"] = review.artifact_hashes.graph_sha256
        session["latest_reviewed_artifacts"] = artifact_set

    _save(directory, session)
    _append_audit(
        directory,
        "start",
        {"pass": 1, "model_policy": policy},
        prior_state=None,
        new_state=session["state"],
        artifact_set_sha256=_artifact_set_sha256(artifact_set),
    )

    result = {
        "session_id": session_id,
        "state": session["state"],
        "pass_number": 1,
        "model_policy": policy,
        "required_passes": REQUIRED_PASSES,
        "target_passes": target_passes,
        "max_total_passes": max_passes,
        "additional_passes_approved": approved_additional,
        "review": _review_summary(review),
        "prompt_package": review.prompt_package if policy != "disabled" else None,
        "assessment_ledger": build_assessment_ledger(review.merged_findings),
        "next_action": (
            "submit_manual_critic_response"
            if policy == "manual"
            else (
                "start_critic_review_with_sampling"
                if policy == "client_sampling"
                else "submit_critic_revision_or_finalize"
            )
        ),
        "extend_approval_challenge": extend_challenge,
    }
    return result


def get_critic_review_status(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        _verify_audit_chain(directory)
    return {
        "session_id": session_id,
        "state": session["state"],
        "model_policy": session["model_policy"],
        "current_pass": session["current_pass"],
        "completed_critic_responses": session["completed_critic_responses"],
        "completed_deterministic_passes": session["completed_deterministic_passes"],
        "required_passes": session["required_passes"],
        "target_passes": session.get("target_passes")
        or _target_passes(session.get("additional_passes_approved") or 0),
        "additional_passes_approved": session["additional_passes_approved"],
        "max_total_passes": session["max_total_passes"],
        "latest_artifact_hash": session["latest_artifact_hash"],
        "latest_reviewed_hash": session["latest_reviewed_hash"],
        "latest_reviewed_artifacts": session.get("latest_reviewed_artifacts"),
        "latest_review_summary": session.get("latest_review_summary"),
        "final_outcome": session.get("final_outcome"),
        "extend_approval_challenge": session.get("extend_approval_challenge"),
        "passes": [
            {
                "pass_number": p["pass_number"],
                "has_critic": p.get("critic") is not None,
                "deterministic_status": (p.get("deterministic") or {}).get("status"),
                "completed_status": (p.get("completed_pass") or {}).get("status"),
            }
            for p in session.get("passes") or []
        ],
    }


def submit_manual_critic_response(
    session_id: str,
    response: dict[str, Any] | str,
    *,
    sampling: dict[str, Any] | None = None,
) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["model_policy"] == "disabled":
            raise CriticSessionError("critic_session_manual_disabled")
        if session["state"] != "awaiting_critic_response":
            raise CriticSessionError(
                "critic_session_invalid_state", session["state"]
            )
        prior_state = session["state"]
        pass_number = int(session["current_pass"])
        prompt_path = directory / f"prompt-pass-{pass_number}.json"
        if prompt_path.is_file():
            prompt = _load_json_object(
                prompt_path,
                code="critic_session_corrupt",
                label=f"prompt-pass-{pass_number}.json",
            )
        else:
            prompt = rebuild_prompt_package_for_pass(session, directory, pass_number)
        review_dict = _load_review_pass(directory, pass_number)
        _verify_prompt_package_against_stored(
            prompt, stored_review=review_dict, session=session
        )
        hashes = review_dict["artifact_hashes"]
        det_findings = _findings_from_review_dict(review_dict)
        ledger = build_assessment_ledger(det_findings)
        try:
            parsed = parse_critic_model_response(
                response,
                expected_graph_sha256=hashes["graph_sha256"],
                expected_prompt_package_hash=prompt["prompt_package_hash"],
                expected_serializer_sha256=hashes.get("serializer_sha256"),
                session_id=session_id,
                pass_number=pass_number,
                expected_review_request_sha256=prompt.get("review_request_sha256"),
                expected_review_config_sha256=prompt.get("review_config_sha256"),
                bound_schema=prompt.get("response_schema"),
                allowed_assessments=ledger,
            )
        except CriticResponseError as exc:
            raise CriticSessionError(exc.code, str(exc)) from exc

        model_scorecard = parsed["scorecard"]
        if not isinstance(model_scorecard, CriticScorecard):
            model_scorecard = CriticScorecard.from_dict(model_scorecard or {})
        det_scorecard = CriticScorecard.from_dict(
            (review_dict.get("scorecard") or {})
        )
        assessments = list(parsed.get("finding_assessments") or [])
        critic_findings = list(parsed["findings"])
        completed = merge_completed_pass_review(
            deterministic_findings=det_findings,
            assessments=assessments,
            new_critic_findings=critic_findings,
            det_scorecard=det_scorecard,
            model_scorecard=model_scorecard,
            validation=dict(review_dict.get("validation") or {}),
            analysis_status=str(review_dict.get("analysis_status") or "complete"),
            artifact_hashes=hashes,
            status=None,
        )
        _atomic_write_json(
            directory / f"completed-pass-{pass_number}.json", completed
        )
        _atomic_write_json(
            directory / f"critic-pass-{pass_number}.json",
            {
                "findings": [f.to_dict() for f in critic_findings],
                "finding_assessments": assessments,
                "scorecard": completed["scorecard"],
            },
        )

        critic_record: dict[str, Any] = {
            "finding_ids": [f.finding_id for f in critic_findings],
            "finding_count": len(critic_findings),
            "assessment_count": len(assessments),
            "notes": parsed.get("notes") or "",
            "scorecard": completed["scorecard"],
            "completed_status": completed["status"],
            "finding_counts": completed["finding_counts"],
        }
        if sampling:
            # Persist sampling metadata (model, tokens, status, fallback reason).
            critic_record["sampling"] = {
                "status": sampling.get("status"),
                "model": sampling.get("model"),
                "input_tokens": sampling.get("input_tokens"),
                "output_tokens": sampling.get("output_tokens"),
                "fallback": sampling.get("fallback"),
                "error": sampling.get("error"),
                "metadata": sampling.get("metadata") or {},
            }
        for item in session["passes"]:
            if item["pass_number"] == pass_number:
                item["critic"] = critic_record
                item["completed_pass"] = {
                    "status": completed["status"],
                    "finding_counts": completed["finding_counts"],
                    "open_finding_ids": completed["open_finding_ids"],
                }
                break

        artifact_set = _artifact_set_for_config(
            {
                **hashes,
                "review_config_sha256": prompt.get("review_config_sha256")
                or review_dict.get("review_config_sha256"),
            },
            session["config"],
        )
        session["completed_critic_responses"] = int(session["completed_critic_responses"]) + 1
        session["latest_reviewed_hash"] = hashes["graph_sha256"]
        session["latest_reviewed_artifacts"] = artifact_set
        session["latest_artifact_set"] = artifact_set
        session["latest_review_summary"] = {
            "status": completed["status"],
            "analysis_status": completed["analysis_status"],
            "artifact_hashes": hashes,
            "validation": completed["validation"],
            "finding_counts": completed["finding_counts"],
            "open_finding_ids": completed["open_finding_ids"],
            "scorecard": completed["scorecard"],
            "errors": list(review_dict.get("errors") or []),
            "elapsed_ms": review_dict.get("elapsed_ms"),
        }
        session["state"] = "awaiting_revision"
        session["prior_findings"] = completed["merged_findings"]
        session["prior_finding_ids"] = [
            f["finding_id"] for f in completed["merged_findings"]
        ]
        _save(directory, session)
        _append_audit(
            directory,
            "manual_critic_response",
            {
                "pass": pass_number,
                "finding_count": len(critic_findings),
                "assessment_count": len(assessments),
                "completed_status": completed["status"],
                "sampling_status": (sampling or {}).get("status"),
            },
            prior_state=prior_state,
            new_state=session["state"],
            artifact_set_sha256=_artifact_set_sha256(artifact_set),
        )
        return {
            "session_id": session_id,
            "state": session["state"],
            "pass_number": pass_number,
            "completed_critic_responses": session["completed_critic_responses"],
            "critic": critic_record,
            "completed_pass": session["latest_review_summary"],
            "next_action": "submit_critic_revision",
        }


def apply_sampled_critic_response(
    session_id: str,
    raw_text_or_dict: dict[str, Any] | str,
    *,
    sampling: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return submit_manual_critic_response(
        session_id, raw_text_or_dict, sampling=sampling
    )


def submit_critic_revision(
    session_id: str,
    graph_path: str,
    serializer_path: str | None = None,
    source_paths: list[str] | None = None,
    coverage_contract_path: str | None = None,
    change_summary: str | None = None,
    addressed_finding_ids: list[str] | None = None,
    extensions: list[str] | None = None,
    profiles: list[str] | None = None,
    serializer_mode: str | None = None,
    extra_ontology_graphs: list[str] | None = None,
    force_rdfs_inference: bool | None = None,
) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] != "awaiting_revision":
            raise CriticSessionError(
                "critic_session_invalid_state", session["state"]
            )
        target_passes = int(
            session.get("target_passes")
            or _target_passes(session.get("additional_passes_approved") or 0)
        )
        if session["current_pass"] >= session["max_total_passes"] and (
            session["completed_critic_responses"] >= target_passes
            or session["model_policy"] == "disabled"
        ):
            # Allow final confirmation analysis only if under cap for next pass.
            pass

        next_pass = int(session["current_pass"]) + 1
        if next_pass > session["max_total_passes"]:
            raise CriticSessionError("critic_session_pass_cap")

        cfg = session["config"]
        prior_raw = session.get("prior_findings") or []
        prior = [CriticFinding.from_dict(item) for item in prior_raw]

        if serializer_mode is not None:
            cfg["serializer_mode"] = serializer_mode
        if extra_ontology_graphs is not None:
            cfg["extra_ontology_graphs"] = list(extra_ontology_graphs)
        if force_rdfs_inference is not None:
            cfg["force_rdfs_inference"] = bool(force_rdfs_inference)

        request = CriticArtifactRequest(
            graph_path=graph_path,
            serializer_path=serializer_path
            if serializer_path is not None
            else cfg.get("serializer_path"),
            source_paths=list(
                source_paths
                if source_paths is not None
                else cfg.get("source_paths") or []
            ),
            coverage_contract_path=(
                coverage_contract_path
                if coverage_contract_path is not None
                else cfg.get("coverage_contract_path")
            ),
            extensions=list(
                extensions if extensions is not None else cfg.get("extensions") or []
            ),
            profiles=list(
                profiles if profiles is not None else cfg.get("profiles") or []
            ),
            critic_scope=cfg.get("critic_scope") or "both",
            project_root=cfg.get("project_root"),
            serializer_mode=cfg.get("serializer_mode") or "auto",  # type: ignore[arg-type]
            extra_ontology_graphs=list(cfg.get("extra_ontology_graphs") or []),
            force_rdfs_inference=bool(cfg.get("force_rdfs_inference")),
            prior_findings=prior,
            session_id=session_id,
            pass_number=next_pass,
        )
        try:
            review = analyze_artifact(request)
        except CriticError as exc:
            raise CriticSessionError(exc.code, str(exc)) from exc

        # Update config paths before building artifact set so extras/paths match.
        session["config"]["graph_path"] = graph_path
        if serializer_path is not None:
            session["config"]["serializer_path"] = serializer_path
        if source_paths is not None:
            session["config"]["source_paths"] = list(source_paths)
        if coverage_contract_path is not None:
            session["config"]["coverage_contract_path"] = coverage_contract_path
        if extensions is not None:
            session["config"]["extensions"] = list(extensions)
        if profiles is not None:
            session["config"]["profiles"] = list(profiles)

        new_hash = review.artifact_hashes.graph_sha256
        review_config_sha = review.prompt_package.get("review_config_sha256")
        new_set = _artifact_set_for_config(
            {
                **review.artifact_hashes.to_dict(),
                "review_config_sha256": review_config_sha,
            },
            session["config"],
        )
        old_set = session.get("latest_artifact_set") or {}
        if new_set == old_set and _open_actionable_blockers(session):
            raise CriticSessionError(
                "critic_session_revision_unchanged",
                "artifact set unchanged while blockers remain",
            )

        # Drift check: package review_config must match recomputed config+bundle.
        expected_cfg = _review_config_sha256_for(
            session["config"],
            bundle_fingerprint=review.validation.bundle_fingerprint,
            bundle_resource_hashes=dict(review.validation.bundle_resource_hashes or {}),
        )
        if review_config_sha != expected_cfg:
            raise CriticSessionError(
                "critic_session_hash_mismatch", "review_config_sha256"
            )

        _write_review_pass(directory, next_pass, review)
        _write_config_pass(
            directory,
            next_pass,
            config=session["config"],
            package=review.prompt_package,
            validation=review.validation.to_dict(),
        )

        session["current_pass"] = next_pass
        session["completed_deterministic_passes"] = (
            int(session["completed_deterministic_passes"]) + 1
        )
        session["artifact_hash_history"].append(new_hash)
        session["latest_artifact_hash"] = new_hash
        session["latest_prompt_package_hash"] = review.prompt_package.get(
            "prompt_package_hash"
        )
        session["latest_prompt_content_sha256"] = review.prompt_package.get(
            "prompt_content_sha256"
        )
        session["latest_review_request_sha256"] = review.prompt_package.get(
            "review_request_sha256"
        )
        session["latest_review_config_sha256"] = review_config_sha
        session["latest_serializer_sha256"] = review.artifact_hashes.serializer_sha256
        session["latest_review_summary"] = _review_summary(review)
        session["latest_artifact_set"] = new_set
        session["latest_bundle_fingerprint"] = review.validation.bundle_fingerprint
        if change_summary:
            session["last_change_summary"] = change_summary[:2000]
        if addressed_finding_ids:
            session["last_addressed_finding_ids"] = list(addressed_finding_ids)[:200]

        session["passes"].append(
            {
                "pass_number": next_pass,
                "deterministic": _review_summary(review),
                "critic": None,
                "completed_pass": None,
            }
        )

        if session["model_policy"] == "disabled":
            session["latest_reviewed_hash"] = new_hash
            session["latest_reviewed_artifacts"] = session["latest_artifact_set"]
            session["state"] = "awaiting_revision"
            next_action = (
                "finalize_critic_review"
                if session["completed_deterministic_passes"] >= target_passes
                else "submit_critic_revision"
            )
        else:
            session["state"] = "awaiting_critic_response"
            next_action = "submit_manual_critic_response"

        session["prior_findings"] = [f.to_dict() for f in review.merged_findings]
        session["prior_finding_ids"] = [f.finding_id for f in review.merged_findings]
        _save(directory, session)
        _append_audit(
            directory,
            "revision",
            {
                "pass": next_pass,
                "graph_sha256": new_hash,
                "addressed": list(addressed_finding_ids or [])[:50],
            },
            prior_state="awaiting_revision",
            new_state=session["state"],
            artifact_set_sha256=_artifact_set_sha256(session["latest_artifact_set"]),
        )
        return {
            "session_id": session_id,
            "state": session["state"],
            "pass_number": next_pass,
            "review": _review_summary(review),
            "assessment_ledger": build_assessment_ledger(review.merged_findings),
            "prompt_package": (
                None
                if session["model_policy"] == "disabled"
                else review.prompt_package
            ),
            "next_action": next_action,
        }


def extend_critic_review(
    session_id: str,
    additional_iterations: int,
    *,
    approval_token: str,
) -> dict[str, Any]:
    if not isinstance(additional_iterations, int) or additional_iterations <= 0:
        raise CriticSessionError("critic_session_invalid_additional_iterations")
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] in {"finalized", "cancelled"}:
            raise CriticSessionError("critic_session_invalid_state", session["state"])
        env_token = os.environ.get(EXTEND_TOKEN_ENV)
        expected_tokens = {
            t
            for t in (
                env_token,
                session.get("extend_approval_token"),
                session.get("extend_approval_challenge"),
            )
            if t
        }
        if not approval_token or approval_token not in expected_tokens:
            raise CriticSessionError("critic_session_extend_denied")
        new_additional = int(session["additional_passes_approved"]) + additional_iterations
        new_target = _target_passes(new_additional)
        if new_target > MAX_TOTAL_PASSES:
            raise CriticSessionError("critic_session_pass_cap")
        # One-time challenge: rotate after successful use when challenge matched.
        if approval_token == session.get("extend_approval_challenge"):
            session["extend_approval_challenge"] = secrets.token_urlsafe(18)
        session["additional_passes_approved"] = new_additional
        session["target_passes"] = new_target
        session["max_total_passes"] = new_target
        _save(directory, session)
        _append_audit(
            directory,
            "extend",
            {
                "additional_iterations": additional_iterations,
                "max": new_target,
                "target_passes": new_target,
            },
            prior_state=session["state"],
            new_state=session["state"],
        )
        return {
            "session_id": session_id,
            "additional_passes_approved": new_additional,
            "target_passes": new_target,
            "max_total_passes": new_target,
            "state": session["state"],
            "extend_approval_challenge": session.get("extend_approval_challenge"),
        }


def finalize_critic_review(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] in {"cancelled", "finalized"}:
            raise CriticSessionError("critic_session_invalid_state", session["state"])

        _verify_audit_chain(directory)

        target_passes = int(
            session.get("target_passes")
            or _target_passes(session.get("additional_passes_approved") or 0)
        )
        policy = session["model_policy"]
        if policy == "disabled":
            if int(session["completed_deterministic_passes"]) < target_passes:
                raise CriticSessionError("critic_session_passes_incomplete")
        else:
            if int(session["completed_critic_responses"]) < target_passes:
                raise CriticSessionError("critic_session_passes_incomplete")
            if session["state"] != "awaiting_revision":
                raise CriticSessionError(
                    "critic_session_invalid_state", session["state"]
                )

        # Rehash complete artifact set from disk and compare to last reviewed set.
        current_set = _rehash_config_artifacts(session["config"])
        reviewed_set = session.get("latest_reviewed_artifacts") or {}
        if not reviewed_set:
            raise CriticSessionError("critic_session_hash_mismatch", "no reviewed artifacts")
        # Compare artifact fields excluding optional review_config binding.
        current_core = {
            k: v for k, v in current_set.items() if k != "review_config_sha256"
        }
        reviewed_core = {
            k: v for k, v in reviewed_set.items() if k != "review_config_sha256"
        }
        if current_core != reviewed_core:
            raise CriticSessionError(
                "critic_session_hash_mismatch",
                "artifact set changed after last review",
            )
        if session["latest_artifact_hash"] != session["latest_reviewed_hash"]:
            raise CriticSessionError("critic_session_hash_mismatch")

        # review_config_sha256 drift: recompute from config + stored review validation.
        pass_number = int(session["current_pass"])
        review_pass = _load_review_pass(directory, pass_number)
        validation = review_pass.get("validation") or {}
        recomputed_cfg = _review_config_sha256_for(
            session["config"],
            bundle_fingerprint=validation.get("bundle_fingerprint"),
            bundle_resource_hashes=_bundle_resource_hashes_from_validation(validation),
        )
        stored_cfg = (
            session.get("latest_review_config_sha256")
            or review_pass.get("review_config_sha256")
            or reviewed_set.get("review_config_sha256")
        )
        if stored_cfg and stored_cfg != recomputed_cfg:
            raise CriticSessionError(
                "critic_session_hash_mismatch", "review_config_sha256"
            )

        summary = session.get("latest_review_summary") or {}
        # Prefer completed-pass file for the latest critic pass when present.
        completed_path = directory / f"completed-pass-{pass_number}.json"
        if completed_path.is_file():
            completed = _load_completed_pass(directory, pass_number)
            summary = {
                "status": completed.get("status"),
                "analysis_status": completed.get("analysis_status"),
                "artifact_hashes": completed.get("artifact_hashes"),
                "validation": completed.get("validation"),
                "finding_counts": completed.get("finding_counts"),
                "open_finding_ids": completed.get("open_finding_ids"),
                "scorecard": completed.get("scorecard"),
            }

        outcome = finalize_outcome_from_summary(summary)
        if outcome == "validation_incomplete":
            raise CriticSessionError("critic_session_validation_incomplete")
        if outcome == "needs_revision":
            raise CriticSessionError("critic_session_nonconforming")
        if outcome == "analysis_incomplete":
            raise CriticSessionError("critic_session_analysis_incomplete")
        if outcome == "blocked_with_findings":
            raise CriticSessionError("critic_session_blockers_remain")

        # accepted and completed_with_findings are successful finalizations
        session["state"] = "finalized"
        session["finalized_at"] = time.time()
        session["final_outcome"] = outcome
        session["accepted"] = outcome == "accepted"
        _save(directory, session)
        _append_audit(
            directory,
            "finalize",
            {
                "hash": session["latest_artifact_hash"],
                "outcome": outcome,
                "artifact_set": current_set,
            },
            prior_state="awaiting_revision",
            new_state="finalized",
            artifact_set_sha256=_artifact_set_sha256(current_set),
        )

        if session["config"].get("report_output"):
            try:
                out = workspace_policy.check_write_path(
                    session["config"]["report_output"]
                )
                _atomic_write_json(
                    out,
                    {
                        "session_id": session_id,
                        "finalized": True,
                        "outcome": outcome,
                        "accepted": session["accepted"],
                        "latest_artifact_hash": session["latest_artifact_hash"],
                        "latest_reviewed_artifacts": reviewed_set,
                        "summary": summary,
                    },
                )
            except ValueError as exc:
                raise CriticSessionError(
                    "critic_session_report_write_denied", "report path denied"
                ) from exc

        return {
            "session_id": session_id,
            "state": "finalized",
            "outcome": outcome,
            "accepted": session["accepted"],
            "latest_artifact_hash": session["latest_artifact_hash"],
            "latest_reviewed_hash": session["latest_reviewed_hash"],
            "latest_reviewed_artifacts": reviewed_set,
            "summary": summary,
        }


def cancel_critic_review(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] == "finalized":
            raise CriticSessionError("critic_session_invalid_state", "finalized")
        prior_state = session["state"]
        session["state"] = "cancelled"
        _save(directory, session)
        _append_audit(
            directory,
            "cancel",
            {},
            prior_state=prior_state,
            new_state="cancelled",
        )
        return {"session_id": session_id, "state": "cancelled"}


def load_session_for_handoff(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] != "finalized":
            raise CriticSessionError("critic_session_not_finalized")
        pass_number = int(session["current_pass"])
        review = json.loads(
            (directory / f"review-pass-{pass_number}.json").read_text(encoding="utf-8")
        )
        completed_path = directory / f"completed-pass-{pass_number}.json"
        if completed_path.is_file():
            completed = json.loads(completed_path.read_text(encoding="utf-8"))
            review = {
                **review,
                "merged_findings": completed.get("merged_findings")
                or review.get("merged_findings"),
                "artifact_hashes": completed.get("artifact_hashes")
                or review.get("artifact_hashes"),
            }
        critic_path = directory / f"critic-pass-{pass_number}.json"
        critic = (
            json.loads(critic_path.read_text(encoding="utf-8"))
            if critic_path.is_file()
            else {"findings": []}
        )
        return {
            "session": session,
            "review": review,
            "critic": critic,
            "directory": str(directory),
        }


def replay_manual_session(
    *,
    case_dir: Path | str,
    pass1_response_path: Path | str,
    pass2_response_path: Path | str,
    session_id: str | None = None,
    project_root: Path | str | None = None,
    pass1_graph_path: Path | str | None = None,
    pass2_graph_path: Path | str | None = None,
) -> dict[str, Any]:
    """Real two-pass session state-machine replay for evaluation harnesses."""

    case_dir = Path(case_dir)
    manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
    if pass1_graph_path:
        graph_path = Path(pass1_graph_path).resolve()
    else:
        graph_path = (case_dir / manifest["graph_path"]).resolve()
    if pass2_graph_path:
        pass2_graph = Path(pass2_graph_path).resolve()
    elif manifest.get("pass2_graph_path"):
        pass2_graph = (case_dir / manifest["pass2_graph_path"]).resolve()
    else:
        pass2_graph = graph_path
    started = start_critic_review(
        graph_path=str(graph_path),
        critic_scope=manifest.get("critic_scope", "graph"),
        model_policy="manual",
        extensions=list(manifest.get("extensions") or []),
        profiles=list(manifest.get("profiles") or []),
        coverage_contract_path=(
            str((case_dir / manifest["coverage_contract_path"]).resolve())
            if manifest.get("coverage_contract_path")
            else None
        ),
        source_paths=[
            str((case_dir / p).resolve()) for p in (manifest.get("source_paths") or [])
        ],
        project_root=str(project_root) if project_root else None,
        serializer_mode=manifest.get("serializer_mode", "auto"),
        extra_ontology_graphs=[
            str((case_dir / p).resolve())
            if not Path(p).is_absolute()
            else str(Path(p).resolve())
            for p in (manifest.get("extra_ontology_graphs") or [])
        ],
        force_rdfs_inference=bool(manifest.get("force_rdfs_inference")),
    )
    sid = started["session_id"]
    if session_id:
        # Keep generated id; external ids are not injectable into store path.
        pass

    def _bind(template: dict[str, Any], package: dict[str, Any], pass_number: int) -> dict[str, Any]:
        bound = dict(template)
        bound["schema_version"] = template.get("schema_version", "1.2.0")
        bound["graph_sha256"] = package["artifact_hashes"]["graph_sha256"]
        bound["serializer_sha256"] = package["artifact_hashes"].get("serializer_sha256")
        bound["prompt_package_hash"] = package["prompt_package_hash"]
        bound["session_id"] = sid
        bound["pass_number"] = pass_number
        bound["review_request_sha256"] = package.get("review_request_sha256")
        bound["review_config_sha256"] = package.get("review_config_sha256")
        bound.setdefault("findings", [])
        bound.setdefault("finding_assessments", [])
        bound.setdefault("scorecard", {})
        return bound

    def _finding_snapshot(pass_number: int) -> dict[str, Any]:
        review_path = session_root() / sid / f"review-pass-{pass_number}.json"
        if not review_path.is_file():
            return {
                "open": 0,
                "resolved": 0,
                "regressions": 0,
                "open_rule_ids": [],
                "resolved_rule_ids": [],
                "validation_conforms": None,
                "scorecard": None,
            }
        review = json.loads(review_path.read_text(encoding="utf-8"))
        open_ids: list[str] = []
        resolved_ids: list[str] = []
        regressions = 0
        for finding in review.get("merged_findings") or []:
            rule_id = finding.get("rule_id")
            status = finding.get("status")
            if status == "resolved" and rule_id:
                resolved_ids.append(str(rule_id))
            elif status == "regression":
                regressions += 1
                if rule_id:
                    open_ids.append(str(rule_id))
            elif status != "resolved" and rule_id:
                open_ids.append(str(rule_id))
        validation = review.get("validation") or {}
        return {
            "open": len(open_ids),
            "resolved": len(resolved_ids),
            "regressions": regressions,
            "open_rule_ids": sorted(set(open_ids)),
            "resolved_rule_ids": sorted(set(resolved_ids)),
            "validation_conforms": validation.get("conforms"),
            "scorecard": review.get("scorecard"),
        }

    pass1_template = json.loads(Path(pass1_response_path).read_text(encoding="utf-8"))
    pass1 = submit_manual_critic_response(
        sid, _bind(pass1_template, started["prompt_package"], 1)
    )
    snap1 = _finding_snapshot(1)
    revised = submit_critic_revision(
        sid,
        graph_path=str(pass2_graph),
        change_summary="evaluation replay pass-2 artifact",
    )
    pass2_template = json.loads(Path(pass2_response_path).read_text(encoding="utf-8"))
    package2 = revised.get("prompt_package") or {}
    pass2 = submit_manual_critic_response(
        sid, _bind(pass2_template, package2, 2)
    )
    snap2 = _finding_snapshot(2)
    final_error = None
    final: dict[str, Any] | None = None
    try:
        final = finalize_critic_review(sid)
    except CriticSessionError as exc:
        final_error = {"code": exc.code, "message": str(exc)}

    return {
        "case_id": manifest.get("case_id"),
        "session_id": sid,
        "pass1_graph": str(graph_path),
        "pass2_graph": str(pass2_graph),
        "passes": [
            {
                "pass_number": 1,
                "parsed_ok": True,
                "model_finding_count": pass1.get("critic", {}).get("finding_count"),
                "completed_status": (pass1.get("completed_pass") or {}).get("status"),
                "findings": snap1,
            },
            {
                "pass_number": 2,
                "parsed_ok": True,
                "model_finding_count": pass2.get("critic", {}).get("finding_count"),
                "completed_status": (pass2.get("completed_pass") or {}).get("status"),
                "findings": snap2,
            },
        ],
        "converged": bool(
            final
            and final.get("outcome") in {"accepted", "completed_with_findings"}
        ),
        "finalized": final is not None,
        "final": final,
        "final_error": final_error,
        "final_status": (pass2.get("completed_pass") or {}).get("status"),
        "final_outcome": (final or {}).get("outcome"),
        "accepted": bool((final or {}).get("accepted")),
    }
