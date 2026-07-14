"""Convergence and detection metrics for critic evaluation harnesses."""

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
from importlib import metadata
from pathlib import Path
from typing import Any

SEVERITY_RANK = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

VALIDATION_RULE_PREFIX = "CRIT-V-"


def _repo_relative(path: str | Path, root: Path) -> str:
    """Return a repo-relative path string; fall back to basename."""

    candidate = Path(path)
    try:
        return str(candidate.resolve().relative_to(root.resolve()))
    except (ValueError, OSError):
        return candidate.name


def open_rule_ids(findings: list[dict[str, Any]]) -> set[str]:
    """Rule IDs from open (non-resolved) findings."""

    out: set[str] = set()
    for finding in findings:
        if finding.get("status") == "resolved":
            continue
        rule_id = finding.get("rule_id")
        if rule_id:
            out.add(str(rule_id))
    return out


def open_findings_by_rule(findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_rule: dict[str, dict[str, Any]] = {}
    for finding in findings:
        if finding.get("status") == "resolved":
            continue
        rule_id = finding.get("rule_id")
        if rule_id and str(rule_id) not in by_rule:
            by_rule[str(rule_id)] = finding
    return by_rule


def severity_at_least(actual: str, minimum: str) -> bool:
    return SEVERITY_RANK.get(actual, -1) >= SEVERITY_RANK.get(minimum, 99)


def detection_recall(
    expected_rule_ids: list[str],
    detected_rule_ids: set[str],
) -> dict[str, Any]:
    """Fraction of seeded oracle rules observed in open findings."""

    expected = list(expected_rule_ids)
    if not expected:
        return {"expected": 0, "found": 0, "recall": None}
    found = sum(1 for rule_id in expected if rule_id in detected_rule_ids)
    return {
        "expected": len(expected),
        "found": found,
        "recall": round(found / len(expected), 3),
        "missing": [rule_id for rule_id in expected if rule_id not in detected_rule_ids],
    }


def oracle_detection_precision(
    expected_rule_ids: list[str],
    detected_rule_ids: set[str],
) -> dict[str, Any]:
    """Precision of detected open rule IDs against expected oracle rule IDs.

    ``true_positives / (true_positives + false_positives)`` where true positives
    are expected∩detected and false positives are detected − expected.
    """

    expected = set(expected_rule_ids)
    detected = set(detected_rule_ids)
    true_positives = sorted(expected & detected)
    false_positives = sorted(detected - expected)
    denom = len(true_positives) + len(false_positives)
    precision = round(len(true_positives) / denom, 3) if denom else None
    return {
        "true_positives": len(true_positives),
        "false_positives": len(false_positives),
        "precision": precision,
        "false_positive_rule_ids": false_positives,
    }


def false_positive_critical_high_on_gold(
    findings: list[dict[str, Any]],
    *,
    allowed_rule_ids: set[str] | None = None,
    include_validation: bool = False,
) -> dict[str, Any]:
    """Count unexpected open critical/high deterministic findings on gold graphs."""

    allowed = allowed_rule_ids or set()
    unexpected: list[str] = []
    for finding in findings:
        if finding.get("status") == "resolved":
            continue
        if finding.get("evidence_kind") != "deterministic":
            continue
        severity = finding.get("severity")
        if severity not in {"critical", "high"}:
            continue
        rule_id = str(finding.get("rule_id") or "")
        if not include_validation and rule_id.startswith(VALIDATION_RULE_PREFIX):
            continue
        if rule_id in allowed:
            continue
        unexpected.append(rule_id)

    return {
        "count": len(unexpected),
        "rule_ids": sorted(set(unexpected)),
    }


def pass_counts(session_report: dict[str, Any]) -> dict[str, Any]:
    """Summarize two-pass session replay completion."""

    passes = session_report.get("passes") or []
    completed = sum(1 for item in passes if item.get("parsed_ok"))
    return {
        "passes_attempted": len(passes),
        "passes_parsed_ok": completed,
        "converged": bool(session_report.get("converged")),
        "final_status": session_report.get("final_status"),
        "final_outcome": session_report.get("final_outcome"),
        "accepted": bool(session_report.get("accepted")),
    }


def _axis_score(scorecard: dict[str, Any] | None, axis: str) -> float | None:
    if not scorecard:
        return None
    block = scorecard.get(axis) or {}
    score = block.get("score")
    return float(score) if isinstance(score, (int, float)) else None


def session_repair_metrics(session_report: dict[str, Any]) -> dict[str, Any]:
    """Compute repair_rate / regressions / score_delta / validation_preservation."""

    passes = session_report.get("passes") or []
    snap1 = (passes[0].get("findings") if len(passes) > 0 else None) or {}
    snap2 = (passes[1].get("findings") if len(passes) > 1 else None) or {}
    open1 = set(snap1.get("open_rule_ids") or [])
    open2 = set(snap2.get("open_rule_ids") or [])
    resolved = set(snap2.get("resolved_rule_ids") or [])
    # Rules open at pass-1 that are resolved (or absent) at pass-2.
    repaired = sorted(rid for rid in open1 if rid in resolved or rid not in open2)
    still_open = sorted(open1 & open2)
    new_open = sorted(open2 - open1)
    repair_rate = (
        round(len(repaired) / len(open1), 3) if open1 else None
    )
    # Precision against pass-1 open set as the "relevant" defect population.
    repair_precision = (
        round(len(repaired) / max(len(repaired) + len(new_open), 1), 3)
        if open1 or new_open
        else None
    )
    recall = repair_rate
    regressions = int(snap2.get("regressions") or 0) + len(new_open)

    score1 = snap1.get("scorecard") or {}
    score2 = snap2.get("scorecard") or {}
    axes = (
        "schema_concept_conformance",
        "semantic_precision",
        "provenance_custody",
        "markings_authorization",
        "source_fidelity",
        "serializer_quality",
        "coverage_completeness",
        "maintainability_reproducibility",
    )
    score_delta: dict[str, Any] = {}
    for axis in axes:
        a = _axis_score(score1, axis)
        b = _axis_score(score2, axis)
        if a is None and b is None:
            continue
        score_delta[axis] = {
            "pass1": a,
            "pass2": b,
            "delta": None if a is None or b is None else round(b - a, 3),
        }

    conforms1 = snap1.get("validation_conforms")
    conforms2 = snap2.get("validation_conforms")
    validation_preservation = {
        "pass1_conforms": conforms1,
        "pass2_conforms": conforms2,
        "preserved": (
            conforms1 is True and conforms2 is True
            if conforms1 is not None and conforms2 is not None
            else None
        ),
        "improved": conforms1 is False and conforms2 is True,
        "regressed": conforms1 is True and conforms2 is False,
    }

    return {
        "open_pass1": len(open1),
        "open_pass2": len(open2),
        "resolved_pass2": len(resolved),
        "repaired_rule_ids": repaired,
        "still_open_rule_ids": still_open,
        "new_open_rule_ids": new_open,
        "recall": recall,
        "repair_precision": repair_precision,
        # Backward-compat alias for one release.
        "precision": repair_precision,
        "repair_rate": repair_rate,
        "regressions": regressions,
        "score_delta": score_delta,
        "validation_preservation": validation_preservation,
        "accepted": bool(session_report.get("accepted")),
    }


def aggregate_oracle_metrics(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Roll up per-case oracle metrics for a harness report."""

    recalls = [
        item["metrics"]["detection_recall"]["recall"]
        for item in case_results
        if item.get("metrics", {}).get("detection_recall", {}).get("recall") is not None
    ]
    precisions = [
        item["metrics"]["oracle_detection_precision"]["precision"]
        for item in case_results
        if item.get("metrics", {})
        .get("oracle_detection_precision", {})
        .get("precision")
        is not None
    ]
    gold_fp = [
        item["metrics"]["false_positive_critical_high"]
        for item in case_results
        if "false_positive_critical_high" in item.get("metrics", {})
    ]
    return {
        "case_count": len(case_results),
        "passed_cases": sum(1 for item in case_results if item.get("passed")),
        "mean_detection_recall": round(sum(recalls) / len(recalls), 3) if recalls else None,
        "mean_oracle_detection_precision": (
            round(sum(precisions) / len(precisions), 3) if precisions else None
        ),
        "gold_false_positive_critical_high_total": sum(
            fp.get("count", 0) for fp in gold_fp
        ),
    }


def _sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_sha(root: Path) -> str | None:
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        return env_sha.strip()
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if completed.returncode == 0:
            return completed.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None
    return None


def _pkg_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def report_environment_metadata(
    *,
    root: Path,
    fixture_paths: list[Path] | None = None,
    validation_bundle_fingerprint: str | None = None,
) -> dict[str, Any]:
    """Sanitized reproducibility metadata for harness JSON reports."""

    try:
        from critic.models import CRITIC_SCHEMA_VERSION
        from critic.schema_util import SUPPORTED_SCHEMA_VERSION
        from critic.deterministic import RULE_VERSION as DETERMINISTIC_RULE_VERSION
        from critic.graph_heuristics import RULE_VERSION as HEURISTIC_RULE_VERSION
    except Exception:  # noqa: BLE001
        CRITIC_SCHEMA_VERSION = None
        SUPPORTED_SCHEMA_VERSION = None
        DETERMINISTIC_RULE_VERSION = None
        HEURISTIC_RULE_VERSION = None

    fixture_hashes: dict[str, str] = {}
    for path in fixture_paths or []:
        digest = _sha256_file(Path(path))
        if digest:
            fixture_hashes[_repo_relative(path, root)] = digest

    return {
        "repository_sha": _git_sha(root),
        "fixture_hashes": fixture_hashes,
        "rule_schema_versions": {
            "CRITIC_SCHEMA_VERSION": CRITIC_SCHEMA_VERSION,
            "SUPPORTED_SCHEMA_VERSION": SUPPORTED_SCHEMA_VERSION,
            "deterministic_RULE_VERSION": DETERMINISTIC_RULE_VERSION,
            "heuristic_RULE_VERSION": HEURISTIC_RULE_VERSION,
        },
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "validation_bundle_fingerprint": validation_bundle_fingerprint,
        "dependency_versions": {
            "fastmcp": _pkg_version("fastmcp"),
        },
    }


def sanitize_session_paths(session_report: dict[str, Any], root: Path) -> dict[str, Any]:
    """Rewrite absolute graph paths in a session report to repo-relative form."""

    sanitized = dict(session_report)
    for key in ("pass1_graph", "pass2_graph"):
        if sanitized.get(key):
            sanitized[key] = _repo_relative(sanitized[key], root)
    return sanitized
