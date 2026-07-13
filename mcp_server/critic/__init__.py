"""Public critic API (issue #75) — deterministic analysis and review contracts.

Orchestration / MCP sampling lives in issue #76.
"""

from __future__ import annotations

from critic.deterministic import CriticError, analyze_artifact
from critic.finding_diff import diff_findings
from critic.models import (
    CRITIC_SCHEMA_VERSION,
    CriticArtifactRequest,
    CriticFinding,
    CriticReview,
    CriticScorecard,
)
from critic.response_parser import CriticResponseError, parse_critic_model_response

__all__ = [
    "CRITIC_SCHEMA_VERSION",
    "CriticArtifactRequest",
    "CriticError",
    "CriticFinding",
    "CriticResponseError",
    "CriticReview",
    "CriticScorecard",
    "analyze_artifact",
    "diff_findings",
    "parse_critic_model_response",
]
