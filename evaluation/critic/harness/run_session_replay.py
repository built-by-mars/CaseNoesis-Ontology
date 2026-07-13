#!/usr/bin/env python3
"""Two-pass manual session replay harness (issue #77).

Replays a bounded two-pass critic session against a micro evaluation case
using mock model responses from ``responses/mock/``. When
``critic.sessions`` is available (#76), delegates to it; otherwise uses a
local replay shim with the same contracts.

Usage:
    python -m harness.run_session_replay
    python evaluation/critic/harness/run_session_replay.py
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

from harness.report import pass_counts  # noqa: E402


DEFAULT_CASE = EVAL_ROOT / "cases" / "micro" / "gold-charged-with"
MOCK_DIR = EVAL_ROOT / "responses" / "mock"


def _bind_mock_response(
    template: dict[str, Any],
    *,
    review_dict: dict[str, Any],
    session_id: str,
    pass_number: int,
) -> dict[str, Any]:
    hashes = review_dict.get("artifact_hashes") or {}
    package = review_dict.get("prompt_package") or {}
    bound = dict(template)
    bound["schema_version"] = template.get("schema_version", "1.2.0")
    bound["graph_sha256"] = hashes.get("graph_sha256")
    bound["serializer_sha256"] = hashes.get("serializer_sha256")
    bound["prompt_package_hash"] = package.get("prompt_package_hash")
    bound["session_id"] = session_id
    bound["pass_number"] = pass_number
    bound["review_request_sha256"] = package.get("review_request_sha256")
    return bound


def _replay_with_shim(
    *,
    case_dir: Path,
    pass1_mock: Path,
    pass2_mock: Path,
    session_id: str,
) -> dict[str, Any]:
    from critic import CriticArtifactRequest, analyze_artifact
    from critic.response_parser import parse_critic_model_response
    from critic.scorecard import merge_scorecards
    from critic.models import CriticScorecard

    manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
    graph_path = (case_dir / manifest["graph_path"]).resolve()

    pass_reports: list[dict[str, Any]] = []
    prior_findings = []
    merged_scorecard = None
    final_review = None

    for pass_number, mock_path in ((1, pass1_mock), (2, pass2_mock)):
        request = CriticArtifactRequest(
            graph_path=str(graph_path),
            critic_scope=manifest.get("critic_scope", "graph"),
            project_root=str(PROJECT_ROOT),
            session_id=session_id,
            pass_number=pass_number,
            prior_findings=list(prior_findings),
        )
        review = analyze_artifact(request)
        review_dict = review.to_dict()
        template = json.loads(mock_path.read_text(encoding="utf-8"))
        payload = _bind_mock_response(
            template,
            review_dict=review_dict,
            session_id=session_id,
            pass_number=pass_number,
        )
        parsed_ok = True
        parse_error = None
        parsed_findings = []
        try:
            parsed = parse_critic_model_response(
                payload,
                expected_graph_sha256=review.artifact_hashes.graph_sha256,
                expected_prompt_package_hash=review.prompt_package["prompt_package_hash"],
                expected_serializer_sha256=review.artifact_hashes.serializer_sha256,
                session_id=session_id,
                pass_number=pass_number,
                expected_review_request_sha256=review.prompt_package.get(
                    "review_request_sha256"
                ),
                bound_schema=review.prompt_package.get("response_schema"),
            )
            parsed_findings = list(parsed.get("findings") or [])
            model_scorecard = parsed.get("scorecard")
            if not isinstance(model_scorecard, CriticScorecard):
                model_scorecard = CriticScorecard.from_dict(model_scorecard or {})
            merged_scorecard = merge_scorecards(review.scorecard, model_scorecard)
            prior_findings = list(review.merged_findings) + parsed_findings
        except Exception as exc:  # noqa: BLE001
            parsed_ok = False
            parse_error = type(exc).__name__
            prior_findings = list(review.merged_findings)

        pass_reports.append(
            {
                "pass_number": pass_number,
                "mock_path": str(mock_path.relative_to(EVAL_ROOT)),
                "parsed_ok": parsed_ok,
                "parse_error": parse_error,
                "model_finding_count": len(parsed_findings),
                "status": review.status,
                "analysis_status": review.analysis_status,
            }
        )
        final_review = review_dict

    converged = all(item["parsed_ok"] for item in pass_reports)
    return {
        "case_id": manifest["case_id"],
        "session_id": session_id,
        "passes": pass_reports,
        "converged": converged,
        "final_status": pass_reports[-1]["status"] if pass_reports else None,
        "final_analysis_status": pass_reports[-1]["analysis_status"]
        if pass_reports
        else None,
        "merged_scorecard": merged_scorecard.to_dict() if merged_scorecard else None,
        "final_review_status": final_review.get("status") if final_review else None,
    }


def replay_session(
    *,
    case_dir: Path,
    pass1_mock: Path,
    pass2_mock: Path,
    session_id: str,
) -> dict[str, Any]:
    try:
        from critic.sessions import replay_manual_session  # type: ignore

        return replay_manual_session(
            case_dir=case_dir,
            pass1_response_path=pass1_mock,
            pass2_response_path=pass2_mock,
            session_id=session_id,
            project_root=PROJECT_ROOT,
        )
    except ImportError:
        return _replay_with_shim(
            case_dir=case_dir,
            pass1_mock=pass1_mock,
            pass2_mock=pass2_mock,
            session_id=session_id,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", type=Path, default=DEFAULT_CASE)
    parser.add_argument("--pass1-mock", type=Path, default=MOCK_DIR / "pass1-empty-findings.json")
    parser.add_argument("--pass2-mock", type=Path, default=MOCK_DIR / "pass2-empty-findings.json")
    parser.add_argument("--session-id", default="eval-session-replay-001")
    parser.add_argument(
        "--report",
        type=Path,
        default=EVAL_ROOT / "reports" / "session-replay-latest.json",
    )
    args = parser.parse_args(argv)

    session_report = replay_session(
        case_dir=args.case_dir,
        pass1_mock=args.pass1_mock,
        pass2_mock=args.pass2_mock,
        session_id=args.session_id,
    )
    metrics = pass_counts(session_report)
    passed = bool(session_report.get("converged")) and bool(
        session_report.get("finalized")
    )

    report = {
        "harness": "run_session_replay",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "metrics": metrics,
        "session": session_report,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        f"critic session replay — case {session_report.get('case_id')}, "
        f"passes {metrics['passes_parsed_ok']}/{metrics['passes_attempted']}"
    )
    if not passed:
        return 1
    print("session replay converged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
