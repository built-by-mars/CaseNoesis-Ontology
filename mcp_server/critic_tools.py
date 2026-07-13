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
        kwargs.setdefault("model_policy", "client_sampling")
        started = start_critic_review(**kwargs)
        if started.get("model_policy") != "client_sampling":
            return {"ok": True, **started, "sampling": {"status": "skipped_policy"}}
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
        submitted = submit_manual_critic_response(
            started["session_id"], sample.response
        )
        return {
            "ok": True,
            **submitted,
            "sampling": sample.to_dict(),
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
        revised = submit_critic_revision(**kwargs)
        if revised.get("state") != "awaiting_critic_response":
            return {"ok": True, **revised, "sampling": {"status": "skipped_policy"}}
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
        submitted = submit_manual_critic_response(
            revised["session_id"], sample.response
        )
        return {"ok": True, **submitted, "sampling": sample.to_dict()}
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
