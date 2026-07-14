#!/usr/bin/env python3
"""Offline critic oracle harness (issue #77).

Discovers evaluation cases via manifest.json, runs deterministic
``analyze_artifact``, and compares open findings against per-case oracles.

Usage:
    python -m harness.run_oracles
    python evaluation/critic/harness/run_oracles.py
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVAL_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = EVAL_ROOT.parents[1]
sys.path.insert(0, str(EVAL_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_server"))

from harness.report import (  # noqa: E402
    aggregate_oracle_metrics,
    detection_recall,
    false_positive_critical_high_on_gold,
    open_findings_by_rule,
    open_rule_ids,
    oracle_detection_precision,
    report_environment_metadata,
    severity_at_least,
)


def discover_cases(cases_root: Path) -> list[Path]:
    return sorted(cases_root.glob("**/manifest.json"))


def resolve_path(case_dir: Path, raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    if "/" in raw and not raw.startswith("."):
        repo_candidate = PROJECT_ROOT / raw
        if repo_candidate.exists():
            return repo_candidate
    return (case_dir / raw).resolve()


def build_request(case_dir: Path, manifest: dict[str, Any], oracle: dict[str, Any]):
    from critic import CriticArtifactRequest

    graph_raw = oracle.get("graph_path") or manifest["graph_path"]
    graph_path = resolve_path(case_dir, str(graph_raw))

    serializer_path = None
    if manifest.get("serializer_path"):
        serializer_path = str(resolve_path(case_dir, str(manifest["serializer_path"])))

    coverage_path = None
    cov_raw = oracle.get("coverage_contract_path") or manifest.get(
        "coverage_contract_path"
    )
    if cov_raw:
        coverage_path = str(resolve_path(case_dir, str(cov_raw)))

    source_paths: list[str] = []
    for raw in manifest.get("source_paths") or []:
        source_paths.append(str(resolve_path(case_dir, str(raw))))
    source_raw = oracle.get("source_path")
    if source_raw:
        source_paths.append(str(resolve_path(case_dir, str(source_raw))))

    return CriticArtifactRequest(
        graph_path=str(graph_path),
        serializer_path=serializer_path,
        source_paths=source_paths,
        coverage_contract_path=coverage_path,
        extensions=list(manifest.get("extensions") or []),
        profiles=list(manifest.get("profiles") or []),
        critic_scope=manifest["critic_scope"],
        project_root=str(PROJECT_ROOT),
        serializer_mode=manifest.get("serializer_mode", "auto"),
        extra_ontology_graphs=[
            str(resolve_path(case_dir, p))
            for p in (manifest.get("extra_ontology_graphs") or [])
        ],
        force_rdfs_inference=bool(manifest.get("force_rdfs_inference")),
    )


def evaluate_oracle(
    oracle: dict[str, Any],
    review_dict: dict[str, Any],
) -> tuple[bool, list[str], dict[str, Any]]:
    violations: list[str] = []
    findings = list(review_dict.get("merged_findings") or [])
    detected = open_rule_ids(findings)
    by_rule = open_findings_by_rule(findings)

    for rule_id in oracle.get("expected_rule_ids") or []:
        if rule_id not in detected:
            violations.append(f"missing_expected_rule:{rule_id}")

    for rule_id, minimum in (oracle.get("expected_severities_min") or {}).items():
        finding = by_rule.get(rule_id)
        if not finding:
            violations.append(f"missing_severity_target:{rule_id}")
            continue
        if not severity_at_least(str(finding.get("severity")), str(minimum)):
            violations.append(
                f"severity_below_minimum:{rule_id}:{finding.get('severity')}<{minimum}"
            )

    for rule_id in oracle.get("forbidden_rule_ids_on_gold") or []:
        if rule_id in detected:
            violations.append(f"forbidden_rule_present:{rule_id}")

    allowed_ch = set(oracle.get("allowed_critical_high_rule_ids") or [])
    if oracle.get("forbidden_unexpected_critical_high"):
        fp = false_positive_critical_high_on_gold(
            findings,
            allowed_rule_ids=allowed_ch,
            include_validation=False,
        )
        if fp["count"]:
            violations.append(
                "unexpected_critical_high_deterministic:"
                + ",".join(fp["rule_ids"])
            )

    if oracle.get("expect_zero_unexpected_critical_high"):
        fp = false_positive_critical_high_on_gold(
            findings,
            allowed_rule_ids=set(oracle.get("expected_rule_ids") or []),
            include_validation=False,
        )
        if fp["count"]:
            violations.append(
                "zero_unexpected_critical_high_violated:"
                + ",".join(fp["rule_ids"])
            )

    validation = dict(review_dict.get("validation") or {})
    expect_validation = dict(oracle.get("expect_validation") or {})
    if expect_validation.get("allow_unavailable"):
        if validation.get("error_code") == "critic_validation_unavailable":
            pass
        elif validation.get("verification_status") == "could_not_verify":
            pass
    if expect_validation.get("require_conforming") and validation.get("conforms") is not True:
        violations.append(
            f"validation_not_conforming:conforms={validation.get('conforms')}"
        )
    if (
        expect_validation.get("require_conforming_when_complete")
        and validation.get("verification_status") == "complete"
        and validation.get("conforms") is not True
    ):
        violations.append(
            f"validation_complete_but_nonconforming:conforms={validation.get('conforms')}"
        )
    max_viol = oracle.get("expect_shacl_violation_count_max")
    if max_viol is not None:
        actual_viol = int(validation.get("violation_count") or 0)
        if actual_viol > int(max_viol):
            violations.append(
                f"shacl_violation_count:{actual_viol}>{max_viol}"
            )

    if oracle.get("expect_analysis_success") and review_dict.get("analysis_status") == "failed":
        violations.append("analysis_failed")

    prompt_package = review_dict.get("prompt_package") or {}
    if oracle.get("expect_prompt_trust_boundary"):
        trust = prompt_package.get("trust_boundary") or {}
        if trust.get("content_trust") != "untrusted-source-content":
            violations.append("missing_prompt_trust_boundary")
        if not trust.get("forbidden_actions"):
            violations.append("missing_forbidden_actions")

    expected_ids = list(oracle.get("expected_rule_ids") or [])
    metrics = {
        "detection_recall": detection_recall(expected_ids, detected),
        "oracle_detection_precision": oracle_detection_precision(
            expected_ids, detected
        ),
    }
    if oracle.get("forbidden_unexpected_critical_high") or oracle.get(
        "expect_zero_unexpected_critical_high"
    ):
        metrics["false_positive_critical_high"] = false_positive_critical_high_on_gold(
            findings,
            allowed_rule_ids=allowed_ch
            | set(oracle.get("expected_rule_ids") or [])
            | set(oracle.get("forbidden_rule_ids_on_gold") or []),
            include_validation=False,
        )

    return not violations, violations, metrics


def run_case(case_dir: Path) -> dict[str, Any]:
    from critic import analyze_artifact

    manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
    oracle = json.loads((case_dir / "oracle.json").read_text(encoding="utf-8"))
    if manifest["case_id"] != oracle["case_id"]:
        return {
            "case_id": manifest["case_id"],
            "passed": False,
            "violations": [
                f"case_id_mismatch:manifest={manifest['case_id']} oracle={oracle['case_id']}"
            ],
        }

    request = build_request(case_dir, manifest, oracle)
    review = analyze_artifact(request)
    review_dict = review.to_dict()
    passed, violations, metrics = evaluate_oracle(oracle, review_dict)
    return {
        "case_id": manifest["case_id"],
        "passed": passed,
        "violations": violations,
        "detected_rule_ids": sorted(open_rule_ids(review_dict.get("merged_findings") or [])),
        "validation": review_dict.get("validation"),
        "status": review_dict.get("status"),
        "analysis_status": review_dict.get("analysis_status"),
        "metrics": metrics,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases-root",
        type=Path,
        default=EVAL_ROOT / "cases",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=EVAL_ROOT / "reports" / "oracle-latest.json",
    )
    args = parser.parse_args(argv)

    manifests = discover_cases(args.cases_root)
    case_results = [run_case(path.parent) for path in manifests]
    passed = all(item.get("passed") for item in case_results)

    report = {
        "harness": "run_oracles",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "metrics": aggregate_oracle_metrics(case_results),
        "metadata": report_environment_metadata(root=PROJECT_ROOT),
        "case_results": case_results,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        f"critic oracle harness — {report['metrics']['case_count']} cases, "
        f"{report['metrics']['passed_cases']} passed"
    )
    for item in case_results:
        state = "PASS" if item.get("passed") else "FAIL"
        print(f"  [{state}] {item['case_id']}")
        for violation in item.get("violations") or []:
            print(f"         - {violation}")
        validation = item.get("validation") or {}
        if validation:
            print(
                f"         validation: conforms={validation.get('conforms')} "
                f"status={validation.get('verification_status')}"
            )

    if not passed:
        return 1
    print("all oracles satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
