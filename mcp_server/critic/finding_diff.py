"""Stable finding identity and pass-to-pass diffing (issue #75)."""

from __future__ import annotations

from dataclasses import dataclass

from critic.models import CriticFinding, FindingStatus


@dataclass
class FindingDiffResult:
    new: list[CriticFinding]
    persisting: list[CriticFinding]
    resolved: list[CriticFinding]
    regressions: list[CriticFinding]
    disputed: list[CriticFinding]

    def apply_statuses(self) -> list[CriticFinding]:
        """Return a merged list with statuses set for the current pass."""

        out: list[CriticFinding] = []
        for finding in self.new:
            finding.status = "new"
            out.append(finding)
        for finding in self.persisting:
            finding.status = "persisting"
            out.append(finding)
        for finding in self.regressions:
            finding.status = "regression"
            out.append(finding)
        for finding in self.disputed:
            finding.status = "disputed"
            out.append(finding)
        # Resolved findings are reported for the session ledger; keep status.
        for finding in self.resolved:
            finding.status = "resolved"
            out.append(finding)
        return out


def _index(findings: list[CriticFinding]) -> dict[str, CriticFinding]:
    indexed: dict[str, CriticFinding] = {}
    for finding in findings:
        key = finding.ensure_identity_key()
        indexed[key] = finding
    return indexed


def diff_findings(
    previous: list[CriticFinding],
    current: list[CriticFinding],
    *,
    disputed_identity_keys: dict[str, str] | None = None,
    resolved_identity_keys: set[str] | None = None,
) -> FindingDiffResult:
    """Diff prior-pass findings against the current deterministic/critic set.

    A finding is **not** considered resolved merely because it is absent from
    ``current``. Callers must supply ``resolved_identity_keys`` after
    deterministic verification (or an explicit critic assessment) confirms the
    defect is gone. Absent that, previously open findings that disappear are
    treated as *persisting* (carry-forward) unless disputed.
    """

    disputed_identity_keys = disputed_identity_keys or {}
    resolved_identity_keys = resolved_identity_keys or set()

    prev = _index(previous)
    curr = _index(current)

    new: list[CriticFinding] = []
    persisting: list[CriticFinding] = []
    resolved: list[CriticFinding] = []
    regressions: list[CriticFinding] = []
    disputed: list[CriticFinding] = []

    for key, finding in curr.items():
        if key in disputed_identity_keys:
            finding.disputed_rationale = disputed_identity_keys[key]
            disputed.append(finding)
            continue
        if key in prev:
            prior = prev[key]
            if prior.status == "resolved" and finding.severity in {
                "critical",
                "high",
                "medium",
            }:
                regressions.append(finding)
            else:
                persisting.append(finding)
        else:
            new.append(finding)

    for key, finding in prev.items():
        if key in curr or key in disputed_identity_keys:
            continue
        if key in resolved_identity_keys:
            resolved.append(finding)
            continue
        # Carry forward: omission alone does not resolve.
        carried = CriticFinding.from_dict(finding.to_dict())
        carried.status = "persisting"
        persisting.append(carried)

    return FindingDiffResult(
        new=new,
        persisting=persisting,
        resolved=resolved,
        regressions=regressions,
        disputed=disputed,
    )


def assign_sequential_ids(
    findings: list[CriticFinding],
    *,
    start: int = 1,
) -> list[CriticFinding]:
    """Assign human-readable CRIT-NNNN finding_id values; preserve identity_key."""

    for index, finding in enumerate(findings, start=start):
        finding.ensure_identity_key()
        finding.finding_id = f"CRIT-{index:04d}"
    return findings


def status_counts(findings: list[CriticFinding]) -> dict[FindingStatus, int]:
    counts: dict[str, int] = {
        "new": 0,
        "persisting": 0,
        "resolved": 0,
        "regression": 0,
        "disputed": 0,
    }
    for finding in findings:
        counts[finding.status] = counts.get(finding.status, 0) + 1
    return counts  # type: ignore[return-value]
