"""MCP-facing wrappers for critic session tools (issues #76 / #78)."""

from __future__ import annotations

from typing import Any

from critic.deterministic import CriticError
from critic.handoff import prepare_critic_handoff
from critic.response_parser import CriticResponseError
from critic.sampling import maybe_sample_critic
from critic.sessions import (
    CriticSessionError,
    cancel_critic_review,
    deployment_critic_mode,
    effective_model_policy,
    extend_critic_review,
    finalize_critic_review,
    get_critic_review_status,
    start_critic_review,
    submit_critic_revision,
    submit_manual_critic_response,
)


def _fail(exc: Exception) -> dict[str, Any]:
    code = getattr(exc, "code", type(exc).__name__)
    # Never echo raw filesystem paths from ValueError.
    message = str(exc) or code
    if "outside" in message or "unconfigured" in message or "/" in message:
        message = code
    return {"ok": False, "error": message, "code": code}


def _deployment_sampling_gate() -> dict[str, Any] | None:
    """Return a typed sampling fallback when deployment mode forbids sampling."""

    mode = deployment_critic_mode()
    if mode == "client_sampling":
        return None
    status = (
        "skipped_policy" if mode == "disabled" else "critic_manual_response_required"
    )
    return {
        "status": status,
        "fallback": True,
        "reason": "deployment_mode",
        "error": "deployment_mode",
        "metadata": {"reason": "deployment_mode", "deployment_mode": mode},
    }


def tool_start_critic_review(**kwargs: Any) -> dict[str, Any]:
    try:
        result = start_critic_review(**kwargs)
        return {"ok": True, **result}
    except (CriticSessionError, CriticError, ValueError) as exc:
        return _fail(exc)


async def tool_start_critic_review_with_sampling(
    ctx: Any, **kwargs: Any
) -> dict[str, Any]:
    """Start a session and attempt client sampling when policy allows."""

    try:
        gate = _deployment_sampling_gate()
        requested = kwargs.get("model_policy")
        # Prefer client_sampling for with_sampling tools, but clamp by deployment.
        if requested is None:
            requested = "client_sampling"
        kwargs["model_policy"] = effective_model_policy(requested)
        started = start_critic_review(**kwargs)
        if gate is not None:
            return {"ok": True, **started, "sampling": gate}
        if started.get("model_policy") != "client_sampling":
            return {
                "ok": True,
                **started,
                "sampling": {
                    "status": "skipped_policy",
                    "fallback": True,
                    "reason": "deployment_mode",
                },
            }
        package = started.get("prompt_package")
        if not package:
            return {
                "ok": True,
                **started,
                "sampling": {
                    "status": "critic_manual_response_required",
                    "fallback": True,
                },
            }
        sample = await maybe_sample_critic(
            ctx, package, model_policy="client_sampling"
        )
        if sample.status != "ok" or not sample.response:
            return {
                "ok": True,
                **started,
                "sampling": sample.to_dict(),
                "next_action": "submit_manual_critic_response",
            }
        sampling_meta = sample.to_dict()
        submitted = submit_manual_critic_response(
            started["session_id"],
            sample.response,
            sampling=sampling_meta,
        )
        return {
            "ok": True,
            **submitted,
            "sampling": sampling_meta,
            "prompt_package": None,
        }
    except (CriticSessionError, CriticResponseError, CriticError, ValueError) as exc:
        return _fail(exc)


def tool_submit_manual_critic_response(
    session_id: str, response: dict[str, Any] | str
) -> dict[str, Any]:
    try:
        result = submit_manual_critic_response(session_id, response)
        return {"ok": True, **result}
    except (CriticSessionError, CriticResponseError, CriticError, ValueError) as exc:
        return _fail(exc)


def tool_submit_critic_revision(**kwargs: Any) -> dict[str, Any]:
    try:
        result = submit_critic_revision(**kwargs)
        return {"ok": True, **result}
    except (CriticSessionError, CriticError, ValueError) as exc:
        return _fail(exc)


async def tool_submit_critic_revision_with_sampling(
    ctx: Any, **kwargs: Any
) -> dict[str, Any]:
    try:
        gate = _deployment_sampling_gate()
        revised = submit_critic_revision(**kwargs)
        if gate is not None:
            return {"ok": True, **revised, "sampling": gate}
        if revised.get("state") != "awaiting_critic_response":
            return {"ok": True, **revised, "sampling": {"status": "skipped_policy"}}
        if revised.get("model_policy") not in {None, "client_sampling"}:
            # Session may not echo model_policy; fall through to maybe_sample gate.
            pass
        package = revised.get("prompt_package")
        if not package:
            return {
                "ok": True,
                **revised,
                "sampling": {
                    "status": "critic_manual_response_required",
                    "fallback": True,
                },
            }
        sample = await maybe_sample_critic(
            ctx, package, model_policy="client_sampling"
        )
        if sample.status != "ok" or not sample.response:
            return {
                "ok": True,
                **revised,
                "sampling": sample.to_dict(),
                "next_action": "submit_manual_critic_response",
            }
        sampling_meta = sample.to_dict()
        submitted = submit_manual_critic_response(
            revised["session_id"], sample.response, sampling=sampling_meta
        )
        return {"ok": True, **submitted, "sampling": sampling_meta}
    except (CriticSessionError, CriticResponseError, CriticError, ValueError) as exc:
        return _fail(exc)


def tool_extend_critic_review(
    session_id: str, additional_iterations: int, approval_token: str
) -> dict[str, Any]:
    try:
        result = extend_critic_review(
            session_id,
            additional_iterations,
            approval_token=approval_token,
        )
        return {"ok": True, **result}
    except (CriticSessionError, ValueError) as exc:
        return _fail(exc)


def tool_get_critic_review_status(session_id: str) -> dict[str, Any]:
    try:
        result = get_critic_review_status(session_id)
        return {"ok": True, **result}
    except (CriticSessionError, ValueError) as exc:
        return _fail(exc)


def tool_finalize_critic_review(session_id: str) -> dict[str, Any]:
    try:
        result = finalize_critic_review(session_id)
        return {"ok": True, **result}
    except (CriticSessionError, ValueError) as exc:
        return _fail(exc)


def tool_cancel_critic_review(session_id: str) -> dict[str, Any]:
    try:
        result = cancel_critic_review(session_id)
        return {"ok": True, **result}
    except (CriticSessionError, ValueError) as exc:
        return _fail(exc)


def tool_prepare_critic_handoff(**kwargs: Any) -> dict[str, Any]:
    try:
        result = prepare_critic_handoff(**kwargs)
        return {"ok": True, **result}
    except (CriticSessionError, ValueError) as exc:
        return _fail(exc)
