"""Public critic API (issues #75–#78)."""

from __future__ import annotations

from critic.deterministic import CriticError, analyze_artifact
from critic.finding_diff import diff_findings
from critic.handoff import prepare_critic_handoff
from critic.models import (
    CRITIC_SCHEMA_VERSION,
    CriticArtifactRequest,
    CriticFinding,
    CriticReview,
    CriticScorecard,
    make_stable_finding_id,
)
from critic.response_parser import CriticResponseError, parse_critic_model_response
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

__all__ = [
    "CRITIC_SCHEMA_VERSION",
    "CriticArtifactRequest",
    "CriticError",
    "CriticFinding",
    "CriticResponseError",
    "CriticReview",
    "CriticScorecard",
    "CriticSessionError",
    "analyze_artifact",
    "cancel_critic_review",
    "diff_findings",
    "extend_critic_review",
    "finalize_critic_review",
    "get_critic_review_status",
    "make_stable_finding_id",
    "parse_critic_model_response",
    "prepare_critic_handoff",
    "start_critic_review",
    "submit_critic_revision",
    "submit_manual_critic_response",
]
