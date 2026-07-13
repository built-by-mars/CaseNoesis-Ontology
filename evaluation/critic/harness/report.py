"""Convergence and detection metrics for critic evaluation harnesses."""

from __future__ import annotations

from typing import Any

SEVERITY_RANK = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

VALIDATION_RULE_PREFIX = "CRIT-V-"


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
    }


def aggregate_oracle_metrics(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Roll up per-case oracle metrics for a harness report."""

    recalls = [
        item["metrics"]["detection_recall"]["recall"]
        for item in case_results
        if item.get("metrics", {}).get("detection_recall", {}).get("recall") is not None
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
        "gold_false_positive_critical_high_total": sum(
            fp.get("count", 0) for fp in gold_fp
        ),
    }
