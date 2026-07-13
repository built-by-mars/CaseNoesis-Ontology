"""Stable finding identity and pass-to-pass diffing (issue #75 Round 2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from critic.models import CriticFinding, make_stable_finding_id

__all__ = [
    "FindingDiffResult",
    "FindingOccurrence",
    "assign_display_indexes",
    "diff_findings",
    "make_stable_finding_id",
    "status_counts",
]


@dataclass
class FindingOccurrence:
    finding_id: str
    artifact_hash: str
    first_seen_pass: int
    last_seen_pass: int
    source_location: dict[str, Any] = field(default_factory=dict)
    display_index: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "artifact_hash": self.artifact_hash,
            "first_seen_pass": self.first_seen_pass,
            "last_seen_pass": self.last_seen_pass,
            "source_location": dict(self.source_location),
            "display_index": self.display_index,
        }


@dataclass
class FindingDiffResult:
    new: list[CriticFinding]
    persisting: list[CriticFinding]
    resolved: list[CriticFinding]
    regressions: list[CriticFinding]
    disputed: list[CriticFinding]
    unevaluated: list[CriticFinding]

    def all_for_review(self) -> list[CriticFinding]:
        """Return findings including resolved/unevaluated for the review ledger."""

        out: list[CriticFinding] = []
        for group, status in (
            (self.new, "new"),
            (self.persisting, "persisting"),
            (self.regressions, "regression"),
            (self.disputed, "disputed"),
            (self.resolved, "resolved"),
            (self.unevaluated, "unevaluated"),
        ):
            for finding in group:
                finding.status = status  # type: ignore[assignment]
                out.append(finding)
        return out

    def to_dict(self) -> dict[str, Any]:
        return {
            "new": [f.to_dict() for f in self.new],
            "persisting": [f.to_dict() for f in self.persisting],
            "resolved": [f.to_dict() for f in self.resolved],
            "regressions": [f.to_dict() for f in self.regressions],
            "disputed": [f.to_dict() for f in self.disputed],
            "unevaluated": [f.to_dict() for f in self.unevaluated],
        }


def _index(findings: list[CriticFinding]) -> dict[str, CriticFinding]:
    indexed: dict[str, CriticFinding] = {}
    for finding in findings:
        key = finding.finding_id or finding.ensure_identity_key()
        indexed[key] = finding
    return indexed


def diff_findings(
    previous: list[CriticFinding],
    current: list[CriticFinding],
    *,
    disputed_identity_keys: dict[str, str] | None = None,
    resolved_finding_ids: set[str] | None = None,
    unevaluated_finding_ids: set[str] | None = None,
) -> FindingDiffResult:
    """Diff prior-pass findings against the current set.

    A finding is **resolved** only when its ID is listed in
    ``resolved_finding_ids`` (rule successfully re-evaluated the target and
    the defect was absent). Absence alone never resolves.

    IDs listed in ``unevaluated_finding_ids`` are carried forward as open
    (rule skipped/failed/not applicable) rather than resolved.
    """

    disputed_identity_keys = disputed_identity_keys or {}
    resolved_finding_ids = resolved_finding_ids or set()
    unevaluated_finding_ids = unevaluated_finding_ids or set()

    prev = _index(previous)
    curr = _index(current)

    new: list[CriticFinding] = []
    persisting: list[CriticFinding] = []
    resolved: list[CriticFinding] = []
    regressions: list[CriticFinding] = []
    disputed: list[CriticFinding] = []
    unevaluated: list[CriticFinding] = []

    for key, finding in curr.items():
        if key in disputed_identity_keys:
            finding.disputed_rationale = disputed_identity_keys[key]
            disputed.append(finding)
            continue
        if key in prev:
            prior = prev[key]
            if prior.status == "resolved":
                regressions.append(finding)
            else:
                persisting.append(finding)
        else:
            new.append(finding)

    for key, finding in prev.items():
        if key in curr or key in disputed_identity_keys:
            continue
        if key in resolved_finding_ids:
            carried = CriticFinding.from_dict(finding.to_dict())
            carried.status = "resolved"
            resolved.append(carried)
            continue
        if key in unevaluated_finding_ids or key not in resolved_finding_ids:
            carried = CriticFinding.from_dict(finding.to_dict())
            # Default: not verified this pass → unevaluated/persisting open
            if key in unevaluated_finding_ids:
                unevaluated.append(carried)
            else:
                # Still open unless explicitly resolved
                unevaluated.append(carried)

    return FindingDiffResult(
        new=new,
        persisting=persisting,
        resolved=resolved,
        regressions=regressions,
        disputed=disputed,
        unevaluated=unevaluated,
    )


def assign_display_indexes(findings: list[CriticFinding], *, start: int = 1) -> list[CriticFinding]:
    """Assign display_index only; never rewrite stable finding_id."""

    for index, finding in enumerate(findings, start=start):
        finding.display_index = index
    return findings


def status_counts(findings: list[CriticFinding]) -> dict[str, int]:
    counts: dict[str, int] = {
        "new": 0,
        "persisting": 0,
        "resolved": 0,
        "regression": 0,
        "disputed": 0,
        "unevaluated": 0,
    }
    for finding in findings:
        counts[finding.status] = counts.get(finding.status, 0) + 1
    return counts
