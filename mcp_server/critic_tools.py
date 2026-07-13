"""MCP-facing wrappers for critic session tools (issues #76 / #78)."""

from __future__ import annotations

from typing import Any

from critic.deterministic import CriticError
from critic.handoff import prepare_critic_handoff
from critic.response_parser import CriticResponseError
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
    return {"ok": False, "error": str(exc) or code, "code": code}


def tool_start_critic_review(**kwargs: Any) -> dict[str, Any]:
    try:
        result = start_critic_review(**kwargs)
        return {"ok": True, **result}
    except (CriticSessionError, CriticError, ValueError) as exc:
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
