"""Resumable critic-session state machine (issue #76)."""

from __future__ import annotations

import fcntl
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
from critic.models import CriticArtifactRequest, CriticFinding, CriticReview
from critic.response_parser import CriticResponseError, parse_critic_model_response
from critic.scorecard import merge_scorecards

REQUIRED_PASSES = 2
MAX_TOTAL_PASSES = 8
SESSION_DIR_NAME = "critic-sessions"
CRITIC_SESSION_SCHEMA = "1.0.0"

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


def default_model_policy() -> ModelPolicy:
    raw = (os.environ.get(POLICY_ENV) or "manual").strip().lower()
    if raw in {"disabled", "manual", "client_sampling"}:
        return raw  # type: ignore[return-value]
    return "manual"


def session_root() -> Path:
    override = os.environ.get(SESSION_ROOT_ENV)
    if override:
        path = Path(override).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path
    write_roots = workspace_policy.write_roots()
    if write_roots:
        path = (write_roots[0] / SESSION_DIR_NAME).resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path
    path = (Path.cwd() / ".critic-sessions").resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


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
    lock_path.touch(exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield directory
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


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


def _append_audit(directory: Path, event: str, payload: dict[str, Any]) -> None:
    entry = {
        "ts": time.time(),
        "event": event,
        **payload,
    }
    with (directory / "audit.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def _load(directory: Path) -> dict[str, Any]:
    path = directory / "session.json"
    if not path.is_file():
        raise CriticSessionError("critic_session_corrupt", "missing session.json")
    return json.loads(path.read_text(encoding="utf-8"))


def _save(directory: Path, session: dict[str, Any]) -> None:
    _atomic_write_json(directory / "session.json", session)


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
) -> dict[str, Any]:
    if additional_iterations < 0:
        raise CriticSessionError("critic_session_invalid_additional_iterations")
    policy: ModelPolicy = (  # type: ignore[assignment]
        model_policy if model_policy in {"disabled", "manual", "client_sampling"} else default_model_policy()
    )
    approved_additional = min(int(additional_iterations), MAX_TOTAL_PASSES - REQUIRED_PASSES)
    max_passes = REQUIRED_PASSES + approved_additional
    if max_passes > MAX_TOTAL_PASSES:
        raise CriticSessionError("critic_session_pass_cap")

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
        session_id=session_id,
        pass_number=1,
    )
    try:
        review = analyze_artifact(request)
    except CriticError as exc:
        raise CriticSessionError(exc.code, str(exc)) from exc

    review_dict = review.to_dict()
    _atomic_write_json(directory / "review-pass-1.json", review_dict)
    _atomic_write_json(directory / "prompt-pass-1.json", review.prompt_package)

    extend_token = secrets.token_urlsafe(24)
    session = {
        "schema_version": CRITIC_SESSION_SCHEMA,
        "session_id": session_id,
        "state": "awaiting_critic_response" if policy != "disabled" else "awaiting_revision",
        "model_policy": policy,
        "required_passes": REQUIRED_PASSES,
        "additional_passes_approved": approved_additional,
        "max_total_passes": max_passes,
        "current_pass": 1,
        "completed_critic_responses": 0,
        "completed_deterministic_passes": 1,
        "config": asdict(
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
            )
        ),
        "artifact_hash_history": [review.artifact_hashes.graph_sha256],
        "latest_artifact_hash": review.artifact_hashes.graph_sha256,
        "latest_reviewed_hash": None,
        "latest_prompt_package_hash": review.prompt_package.get("prompt_package_hash"),
        "latest_review_request_sha256": review.prompt_package.get("review_request_sha256"),
        "latest_serializer_sha256": review.artifact_hashes.serializer_sha256,
        "latest_review_summary": _review_summary(review),
        "prior_finding_ids": [f.finding_id for f in review.merged_findings],
        "extend_approval_token": extend_token,
        "passes": [
            {
                "pass_number": 1,
                "deterministic": _review_summary(review),
                "critic": None,
            }
        ],
    }
    if policy == "disabled":
        # Deterministic-only: pass 1 analysis done; await revision or finalize path.
        session["state"] = "awaiting_revision"
        session["latest_reviewed_hash"] = review.artifact_hashes.graph_sha256

    _save(directory, session)
    _append_audit(directory, "start", {"pass": 1, "model_policy": policy})

    result = {
        "session_id": session_id,
        "state": session["state"],
        "pass_number": 1,
        "model_policy": policy,
        "required_passes": REQUIRED_PASSES,
        "max_total_passes": max_passes,
        "additional_passes_approved": approved_additional,
        "review": _review_summary(review),
        "prompt_package": review.prompt_package if policy != "disabled" else None,
        "next_action": (
            "submit_manual_critic_response"
            if policy == "manual"
            else (
                "sample_or_submit_manual_critic_response"
                if policy == "client_sampling"
                else "submit_critic_revision_or_finalize"
            )
        ),
        "extend_approval_token_hint": "set CASE_UCO_CRITIC_EXTEND_TOKEN or use session token via get status (redacted)",
    }
    return result


def get_critic_review_status(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
    return {
        "session_id": session_id,
        "state": session["state"],
        "model_policy": session["model_policy"],
        "current_pass": session["current_pass"],
        "completed_critic_responses": session["completed_critic_responses"],
        "completed_deterministic_passes": session["completed_deterministic_passes"],
        "required_passes": session["required_passes"],
        "additional_passes_approved": session["additional_passes_approved"],
        "max_total_passes": session["max_total_passes"],
        "latest_artifact_hash": session["latest_artifact_hash"],
        "latest_reviewed_hash": session["latest_reviewed_hash"],
        "latest_review_summary": session.get("latest_review_summary"),
        "passes": [
            {
                "pass_number": p["pass_number"],
                "has_critic": p.get("critic") is not None,
                "deterministic_status": (p.get("deterministic") or {}).get("status"),
            }
            for p in session.get("passes") or []
        ],
    }


def submit_manual_critic_response(
    session_id: str,
    response: dict[str, Any] | str,
) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["model_policy"] == "disabled":
            raise CriticSessionError("critic_session_manual_disabled")
        if session["state"] != "awaiting_critic_response":
            raise CriticSessionError(
                "critic_session_invalid_state", session["state"]
            )
        pass_number = int(session["current_pass"])
        prompt = json.loads(
            (directory / f"prompt-pass-{pass_number}.json").read_text(encoding="utf-8")
        )
        review_path = directory / f"review-pass-{pass_number}.json"
        review_dict = json.loads(review_path.read_text(encoding="utf-8"))
        hashes = review_dict["artifact_hashes"]
        try:
            parsed = parse_critic_model_response(
                response,
                expected_graph_sha256=hashes["graph_sha256"],
                expected_prompt_package_hash=prompt["prompt_package_hash"],
                expected_serializer_sha256=hashes.get("serializer_sha256"),
                session_id=session_id,
                pass_number=pass_number,
                expected_review_request_sha256=prompt.get("review_request_sha256"),
                bound_schema=prompt.get("response_schema"),
            )
        except CriticResponseError as exc:
            raise CriticSessionError(exc.code, str(exc)) from exc

        from critic.models import CriticScorecard

        model_scorecard = parsed["scorecard"]
        if not isinstance(model_scorecard, CriticScorecard):
            model_scorecard = CriticScorecard.from_dict(model_scorecard or {})
        det_scorecard = CriticScorecard.from_dict(
            (review_dict.get("scorecard") or {})
        )
        merged_score = merge_scorecards(det_scorecard, model_scorecard)

        critic_findings = [f.to_dict() for f in parsed["findings"]]
        critic_record = {
            "finding_ids": [f["finding_id"] for f in critic_findings],
            "finding_count": len(critic_findings),
            "notes": parsed.get("notes") or "",
            "scorecard": merged_score.to_dict(),
        }
        # Persist critic findings separately (no raw evidence graph).
        _atomic_write_json(
            directory / f"critic-pass-{pass_number}.json",
            {"findings": critic_findings, "scorecard": merged_score.to_dict()},
        )

        for item in session["passes"]:
            if item["pass_number"] == pass_number:
                item["critic"] = critic_record
                break
        session["completed_critic_responses"] = int(session["completed_critic_responses"]) + 1
        session["latest_reviewed_hash"] = hashes["graph_sha256"]
        session["state"] = "awaiting_revision"
        # Merge critic findings into prior set for next deterministic pass.
        prior = _findings_from_review_dict(review_dict)
        prior.extend(parsed["findings"])
        session["prior_findings"] = [f.to_dict() for f in prior]
        session["prior_finding_ids"] = [f.finding_id for f in prior]
        _save(directory, session)
        _append_audit(
            directory,
            "manual_critic_response",
            {"pass": pass_number, "finding_count": len(critic_findings)},
        )
        return {
            "session_id": session_id,
            "state": session["state"],
            "pass_number": pass_number,
            "completed_critic_responses": session["completed_critic_responses"],
            "critic": critic_record,
            "next_action": "submit_critic_revision",
        }


def apply_sampled_critic_response(
    session_id: str,
    raw_text_or_dict: dict[str, Any] | str,
) -> dict[str, Any]:
    return submit_manual_critic_response(session_id, raw_text_or_dict)


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
) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] != "awaiting_revision":
            raise CriticSessionError(
                "critic_session_invalid_state", session["state"]
            )
        if session["current_pass"] >= session["max_total_passes"] and (
            session["completed_critic_responses"] >= session["required_passes"]
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
            prior_findings=prior,
            session_id=session_id,
            pass_number=next_pass,
        )
        try:
            review = analyze_artifact(request)
        except CriticError as exc:
            raise CriticSessionError(exc.code, str(exc)) from exc

        new_hash = review.artifact_hashes.graph_sha256
        old_hash = session["latest_artifact_hash"]
        prev_summary = session.get("latest_review_summary") or {}
        prev_blockers = int(
            (prev_summary.get("finding_counts") or {}).get("critical_high_open") or 0
        )
        if new_hash == old_hash and prev_blockers > 0:
            raise CriticSessionError(
                "critic_session_revision_unchanged",
                "artifact hash unchanged while blockers remain",
            )

        review_dict = review.to_dict()
        _atomic_write_json(directory / f"review-pass-{next_pass}.json", review_dict)
        _atomic_write_json(
            directory / f"prompt-pass-{next_pass}.json", review.prompt_package
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
        session["latest_review_request_sha256"] = review.prompt_package.get(
            "review_request_sha256"
        )
        session["latest_serializer_sha256"] = review.artifact_hashes.serializer_sha256
        session["latest_review_summary"] = _review_summary(review)
        session["config"]["graph_path"] = graph_path
        if serializer_path is not None:
            session["config"]["serializer_path"] = serializer_path
        if change_summary:
            session["last_change_summary"] = change_summary[:2000]
        if addressed_finding_ids:
            session["last_addressed_finding_ids"] = list(addressed_finding_ids)[:200]

        session["passes"].append(
            {
                "pass_number": next_pass,
                "deterministic": _review_summary(review),
                "critic": None,
            }
        )

        if session["model_policy"] == "disabled":
            session["latest_reviewed_hash"] = new_hash
            session["state"] = "awaiting_revision"
            next_action = (
                "finalize_critic_review"
                if session["completed_deterministic_passes"] >= REQUIRED_PASSES
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
        )
        return {
            "session_id": session_id,
            "state": session["state"],
            "pass_number": next_pass,
            "review": _review_summary(review),
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
        expected = os.environ.get(EXTEND_TOKEN_ENV) or session.get(
            "extend_approval_token"
        )
        if not approval_token or approval_token != expected:
            raise CriticSessionError("critic_session_extend_denied")
        new_additional = int(session["additional_passes_approved"]) + additional_iterations
        new_max = REQUIRED_PASSES + new_additional
        if new_max > MAX_TOTAL_PASSES:
            raise CriticSessionError("critic_session_pass_cap")
        session["additional_passes_approved"] = new_additional
        session["max_total_passes"] = new_max
        _save(directory, session)
        _append_audit(
            directory,
            "extend",
            {"additional_iterations": additional_iterations, "max": new_max},
        )
        return {
            "session_id": session_id,
            "additional_passes_approved": new_additional,
            "max_total_passes": new_max,
            "state": session["state"],
        }


def finalize_critic_review(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] in {"cancelled", "finalized"}:
            raise CriticSessionError("critic_session_invalid_state", session["state"])

        policy = session["model_policy"]
        if policy == "disabled":
            if int(session["completed_deterministic_passes"]) < REQUIRED_PASSES:
                raise CriticSessionError("critic_session_passes_incomplete")
        else:
            if int(session["completed_critic_responses"]) < REQUIRED_PASSES:
                raise CriticSessionError("critic_session_passes_incomplete")
            if session["state"] != "awaiting_revision":
                # Must have submitted the last critic response.
                raise CriticSessionError(
                    "critic_session_invalid_state", session["state"]
                )

        if session["latest_artifact_hash"] != session["latest_reviewed_hash"]:
            raise CriticSessionError("critic_session_hash_mismatch")

        summary = session.get("latest_review_summary") or {}
        validation = summary.get("validation") or {}
        if validation.get("verification_status") != "complete":
            raise CriticSessionError("critic_session_validation_incomplete")
        if validation.get("conforms") is not True:
            raise CriticSessionError("critic_session_nonconforming")
        if summary.get("analysis_status") != "complete":
            raise CriticSessionError("critic_session_analysis_incomplete")
        blockers = int(
            (summary.get("finding_counts") or {}).get("critical_high_open") or 0
        )
        if blockers:
            raise CriticSessionError("critic_session_blockers_remain")

        session["state"] = "finalized"
        session["finalized_at"] = time.time()
        _save(directory, session)
        _append_audit(directory, "finalize", {"hash": session["latest_artifact_hash"]})

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
                        "latest_artifact_hash": session["latest_artifact_hash"],
                        "summary": summary,
                    },
                )
            except ValueError as exc:
                raise CriticSessionError("critic_session_report_write_denied", str(exc)) from exc

        return {
            "session_id": session_id,
            "state": "finalized",
            "latest_artifact_hash": session["latest_artifact_hash"],
            "latest_reviewed_hash": session["latest_reviewed_hash"],
            "summary": summary,
            "accepted": True,
        }


def cancel_critic_review(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] == "finalized":
            raise CriticSessionError("critic_session_invalid_state", "finalized")
        session["state"] = "cancelled"
        _save(directory, session)
        _append_audit(directory, "cancel", {})
        return {"session_id": session_id, "state": "cancelled"}


def load_session_for_handoff(session_id: str) -> dict[str, Any]:
    with _locked(session_id) as directory:
        session = _load(directory)
        if session["state"] != "finalized":
            raise CriticSessionError("critic_session_not_finalized")
        # Load last critic + review findings for handoff selection.
        pass_number = int(session["current_pass"])
        review = json.loads(
            (directory / f"review-pass-{pass_number}.json").read_text(encoding="utf-8")
        )
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
