#!/usr/bin/env python3
"""Held-out routing evaluation harness (issue #58).

Runs the hybrid investigation router against a versioned, held-out corpus
and produces a machine-readable report with:

- per-family precision / recall / F1 (macro-averaged)
- multi-label exact match and partial (Jaccard) match on positive cases
- family false-positive rate on hard negatives
- abstention accuracy on unseen-domain / negative cases
- confidence calibration by band (does "high" mean right?)
- regression against the deterministic keyword baseline (the hybrid stage
  must never recall fewer expected families than keywords alone)

Runs entirely offline and without any LLM in the loop, so results are
identical whether the MCP server is driven by a small local model or a
frontier model. Exits non-zero when any threshold documented in the corpus
file fails. Only case ids (never case text) are printed, so a hidden split
can be enforced in CI without exposing its content.

Usage:
    python evaluation/routing/run_evaluation.py \
        --corpus evaluation/routing/heldout-corpus-v1.json \
        --report evaluation/routing/report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _path in (PROJECT_ROOT / "mcp_server", PROJECT_ROOT / "python"):
    _path_str = str(_path)
    if _path_str not in sys.path:
        sys.path.insert(0, _path_str)


def evaluate(corpus: dict) -> dict:
    from investigation_router import route_investigation_content

    cases = corpus["cases"]
    per_family_tp: dict[str, int] = defaultdict(int)
    per_family_fp: dict[str, int] = defaultdict(int)
    per_family_fn: dict[str, int] = defaultdict(int)

    positives = 0
    exact_matches = 0
    jaccard_sum = 0.0
    paraphrase_total = 0
    paraphrase_recalled = 0
    multi_total = 0
    multi_partial = 0

    negatives = 0
    negative_family_hits = 0
    abstain_expected = 0
    abstain_correct = 0

    baseline_recall_hits = 0
    hybrid_recall_hits = 0
    recall_total = 0

    bands: dict[str, dict[str, int]] = {
        "high": {"cases": 0, "correct": 0},
        "low": {"cases": 0, "correct": 0},
        "abstain": {"cases": 0, "correct": 0},
    }
    failures: list[dict] = []

    for case in cases:
        result = route_investigation_content(
            PROJECT_ROOT, content_text=case["text"]
        )
        matched = [m["family_id"] for m in result["matched_families"]]
        baseline = [b["family_id"] for b in result.get("deterministic_baseline", [])]
        level = result["routing_confidence"]["level"]

        expected = set(case["expected_families"])
        acceptable = expected | set(case.get("acceptable_extra_families", []))
        matched_set = set(matched)

        for family in matched_set:
            if family in expected:
                per_family_tp[family] += 1
            elif family not in acceptable:
                per_family_fp[family] += 1
        for family in expected - matched_set:
            per_family_fn[family] += 1

        if expected:
            positives += 1
            recall_total += len(expected)
            hybrid_recall_hits += len(expected & matched_set)
            baseline_recall_hits += len(expected & set(baseline))
            strict_extras = matched_set - acceptable
            if matched_set >= expected and not strict_extras:
                exact_matches += 1
            union = expected | (matched_set - (acceptable - expected))
            jaccard_sum += len(expected & matched_set) / len(union) if union else 0.0
            if case["category"] == "paraphrase":
                paraphrase_total += 1
                if expected & matched_set:
                    paraphrase_recalled += 1
            if case["category"] == "multi_domain":
                multi_total += 1
                if len(expected & matched_set) >= 2:
                    multi_partial += 1
            correct = bool(expected & matched_set)
        else:
            negatives += 1
            unacceptable = matched_set - acceptable
            if unacceptable:
                negative_family_hits += 1
            correct = not unacceptable
        if case.get("should_abstain"):
            abstain_expected += 1
            if not (matched_set - acceptable):
                abstain_correct += 1

        band = bands.setdefault(level, {"cases": 0, "correct": 0})
        band["cases"] += 1
        band["correct"] += 1 if correct else 0

        if not correct:
            failures.append({
                "id": case["id"],
                "category": case["category"],
                "expected": sorted(expected),
                "matched": sorted(matched_set),
                "confidence_level": level,
            })

    families = sorted(set(per_family_tp) | set(per_family_fp) | set(per_family_fn))
    per_family = {}
    f1_values = []
    for family in families:
        tp, fp, fn = per_family_tp[family], per_family_fp[family], per_family_fn[family]
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_family[family] = {
            "tp": tp, "fp": fp, "fn": fn,
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
        }
        f1_values.append(f1)

    calibration = {
        level: {
            "cases": stats["cases"],
            "precision": round(stats["correct"] / stats["cases"], 3) if stats["cases"] else None,
        }
        for level, stats in bands.items()
    }

    return {
        "corpus_version": corpus["corpus_version"],
        "case_count": len(cases),
        "metrics": {
            "macro_f1": round(sum(f1_values) / len(f1_values), 3) if f1_values else 0.0,
            "multi_label_exact_match": round(exact_matches / positives, 3) if positives else None,
            "multi_label_mean_jaccard": round(jaccard_sum / positives, 3) if positives else None,
            "paraphrase_recall": round(paraphrase_recalled / paraphrase_total, 3) if paraphrase_total else None,
            "multi_domain_partial_match": round(multi_partial / multi_total, 3) if multi_total else None,
            "negative_family_rate": round(negative_family_hits / negatives, 3) if negatives else None,
            "abstention_accuracy": round(abstain_correct / abstain_expected, 3) if abstain_expected else None,
            "hybrid_expected_family_recall": round(hybrid_recall_hits / recall_total, 3) if recall_total else None,
            "baseline_expected_family_recall": round(baseline_recall_hits / recall_total, 3) if recall_total else None,
        },
        "calibration_by_confidence_band": calibration,
        "per_family": per_family,
        "failures": failures,
    }


def check_thresholds(report: dict, thresholds: dict) -> list[str]:
    metrics = report["metrics"]
    violations: list[str] = []

    def _fail(name: str, actual, bound) -> None:
        violations.append(f"{name}: {actual} (required {bound})")

    if metrics["macro_f1"] < thresholds["min_macro_f1"]:
        _fail("macro_f1", metrics["macro_f1"], f">= {thresholds['min_macro_f1']}")
    if metrics["paraphrase_recall"] is not None and \
            metrics["paraphrase_recall"] < thresholds["min_paraphrase_recall"]:
        _fail("paraphrase_recall", metrics["paraphrase_recall"],
              f">= {thresholds['min_paraphrase_recall']}")
    if metrics["negative_family_rate"] is not None and \
            metrics["negative_family_rate"] > thresholds["max_negative_family_rate"]:
        _fail("negative_family_rate", metrics["negative_family_rate"],
              f"<= {thresholds['max_negative_family_rate']}")
    if metrics["abstention_accuracy"] is not None and \
            metrics["abstention_accuracy"] < thresholds["min_abstention_accuracy"]:
        _fail("abstention_accuracy", metrics["abstention_accuracy"],
              f">= {thresholds['min_abstention_accuracy']}")
    if metrics["multi_domain_partial_match"] is not None and \
            metrics["multi_domain_partial_match"] < thresholds["min_multi_domain_partial_match"]:
        _fail("multi_domain_partial_match", metrics["multi_domain_partial_match"],
              f">= {thresholds['min_multi_domain_partial_match']}")
    if thresholds.get("hybrid_recall_must_not_trail_baseline") and \
            metrics["hybrid_expected_family_recall"] is not None and \
            metrics["baseline_expected_family_recall"] is not None and \
            metrics["hybrid_expected_family_recall"] < metrics["baseline_expected_family_recall"]:
        _fail("hybrid_expected_family_recall",
              metrics["hybrid_expected_family_recall"],
              f">= baseline {metrics['baseline_expected_family_recall']}")
    high = report["calibration_by_confidence_band"].get("high", {})
    if high.get("cases") and high["precision"] is not None and \
            high["precision"] < thresholds["calibration_high_band_min_precision"]:
        _fail("calibration high-band precision", high["precision"],
              f">= {thresholds['calibration_high_band_min_precision']}")
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(__file__).parent / "heldout-corpus-v1.json",
    )
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args(argv)

    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    report = evaluate(corpus)
    violations = check_thresholds(report, corpus["thresholds"])
    report["threshold_violations"] = violations
    report["passed"] = not violations

    rendered = json.dumps(report, indent=2)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")

    metrics = report["metrics"]
    print(f"held-out routing evaluation — corpus v{report['corpus_version']}, "
          f"{report['case_count']} cases")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    if report["failures"]:
        print("  failed case ids: "
              + ", ".join(f["id"] for f in report["failures"]))
    if violations:
        print("THRESHOLD FAILURES:")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print("all thresholds met")
    return 0


if __name__ == "__main__":
    sys.exit(main())
