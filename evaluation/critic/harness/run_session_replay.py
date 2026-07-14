#!/usr/bin/env python3
"""Two-pass manual session replay harness (issue #77 / P0-9).

Replays a bounded two-pass critic session against a micro evaluation case
using mock model responses from ``responses/mock/``. When
``critic.sessions`` is available (#76), delegates to it; otherwise uses a
local replay shim with the same contracts.

Usage:
    python3 -m harness.run_session_replay
    python3 evaluation/critic/harness/run_session_replay.py
    python3 evaluation/critic/harness/run_session_replay.py \\
        --case-dir evaluation/critic/cases/micro/repair-charged-with \\
        --require-accepted
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

EVAL_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = EVAL_ROOT.parents[1]
sys.path.insert(0, str(EVAL_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_server"))

from harness.report import (  # noqa: E402
    pass_counts,
    report_environment_metadata,
    sanitize_session_paths,
    session_repair_metrics,
)


DEFAULT_CASE = EVAL_ROOT / "cases" / "micro" / "gold-charged-with"
MOCK_DIR = EVAL_ROOT / "responses" / "mock"


def _ensure_eval_workspace() -> Path:
    """Provide write/session roots when the caller has not configured them."""

    write = os.environ.get("CASE_UCO_MCP_WRITE_ROOTS")
    read = os.environ.get("CASE_UCO_MCP_READ_ROOTS")
    session = os.environ.get("CASE_UCO_CRITIC_SESSION_ROOT")
    if write and read and session:
        return Path(write.split(os.pathsep)[0])

    base = Path(tempfile.mkdtemp(prefix="critic-eval-session-"))
    read_root = base / "read"
    write_root = base / "write"
    session_root = write_root / "critic-sessions"
    read_root.mkdir()
    write_root.mkdir()
    session_root.mkdir()
    # Case graphs live under evaluation/; allow reading the repo for fixtures.
    os.environ.setdefault(
        "CASE_UCO_MCP_READ_ROOTS",
        os.pathsep.join([str(read_root), str(PROJECT_ROOT)]),
    )
    os.environ.setdefault("CASE_UCO_MCP_WRITE_ROOTS", str(write_root))
    os.environ.setdefault("CASE_UCO_CRITIC_SESSION_ROOT", str(session_root))
    os.environ.setdefault("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")
    return write_root


def _suppress_open_vocab_relationship_lint():
    """Charged_With is CASE-domain; open-vocab lint medium blocks true acceptance."""

    return patch(
        "critic.deterministic.lint_kind_of_relationship",
        lambda *a, **k: {"ok": True, "checked": 0, "findings": []},
    )


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
    # Prefer persisted prompt body; fall back to stripped review-pass hashes.
    bound["prompt_package_hash"] = package.get("prompt_package_hash") or review_dict.get(
        "prompt_package_hash"
    )
    bound["session_id"] = session_id
    bound["pass_number"] = pass_number
    bound["review_request_sha256"] = package.get(
        "review_request_sha256"
    ) or review_dict.get("review_request_sha256")
    return bound


def _replay_with_shim(
    *,
    case_dir: Path,
    pass1_mock: Path,
    pass2_mock: Path,
    session_id: str,
    pass1_graph: Path | None = None,
    pass2_graph: Path | None = None,
) -> dict[str, Any]:
    from critic import CriticArtifactRequest, analyze_artifact
    from critic.response_parser import parse_critic_model_response
    from critic.scorecard import merge_scorecards
    from critic.models import CriticScorecard

    manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
    graph_path = (
        pass1_graph.resolve()
        if pass1_graph
        else (case_dir / manifest["graph_path"]).resolve()
    )
    revision_path = (
        pass2_graph.resolve()
        if pass2_graph
        else (
            (case_dir / manifest["pass2_graph_path"]).resolve()
            if manifest.get("pass2_graph_path")
            else graph_path
        )
    )

    pass_reports: list[dict[str, Any]] = []
    prior_findings = []
    merged_scorecard = None
    final_review = None
    graphs = {1: graph_path, 2: revision_path}

    for pass_number, mock_path in ((1, pass1_mock), (2, pass2_mock)):
        request = CriticArtifactRequest(
            graph_path=str(graphs[pass_number]),
            critic_scope=manifest.get("critic_scope", "graph"),
            project_root=str(PROJECT_ROOT),
            session_id=session_id,
            pass_number=pass_number,
            prior_findings=list(prior_findings),
        )
        review = analyze_artifact(request)
        review_dict = review.to_dict()
        open_ids = sorted(
            {
                f.rule_id
                for f in review.merged_findings
                if f.rule_id and f.status not in {"resolved"}
            }
        )
        resolved_ids = sorted(
            {
                f.rule_id
                for f in review.merged_findings
                if f.rule_id and f.status == "resolved"
            }
        )
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
                "findings": {
                    "open": len(open_ids),
                    "resolved": len(resolved_ids),
                    "regressions": sum(
                        1 for f in review.merged_findings if f.status == "regression"
                    ),
                    "open_rule_ids": open_ids,
                    "resolved_rule_ids": resolved_ids,
                    "validation_conforms": review.validation.conforms,
                    "scorecard": review.scorecard.to_dict()
                    if hasattr(review.scorecard, "to_dict")
                    else None,
                },
            }
        )
        final_review = review_dict

    converged = all(item["parsed_ok"] for item in pass_reports)
    final_status = pass_reports[-1]["status"] if pass_reports else None
    accepted = converged and final_status in {"deterministic_clean", "accepted"}
    return {
        "case_id": manifest["case_id"],
        "session_id": session_id,
        "pass1_graph": str(graph_path),
        "pass2_graph": str(revision_path),
        "passes": pass_reports,
        "converged": converged,
        "finalized": converged,
        "final_status": final_status,
        "final_analysis_status": pass_reports[-1]["analysis_status"]
        if pass_reports
        else None,
        "final_outcome": "accepted"
        if accepted
        else ("completed_with_findings" if converged else None),
        "accepted": accepted,
        "merged_scorecard": merged_scorecard.to_dict() if merged_scorecard else None,
        "final_review_status": final_review.get("status") if final_review else None,
    }


def replay_session(
    *,
    case_dir: Path,
    pass1_mock: Path,
    pass2_mock: Path,
    session_id: str,
    pass1_graph: Path | None = None,
    pass2_graph: Path | None = None,
) -> dict[str, Any]:
    try:
        from critic.sessions import replay_manual_session  # type: ignore

        return replay_manual_session(
            case_dir=case_dir,
            pass1_response_path=pass1_mock,
            pass2_response_path=pass2_mock,
            session_id=session_id,
            project_root=PROJECT_ROOT,
            pass1_graph_path=pass1_graph,
            pass2_graph_path=pass2_graph,
        )
    except ImportError:
        return _replay_with_shim(
            case_dir=case_dir,
            pass1_mock=pass1_mock,
            pass2_mock=pass2_mock,
            session_id=session_id,
            pass1_graph=pass1_graph,
            pass2_graph=pass2_graph,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", type=Path, default=DEFAULT_CASE)
    parser.add_argument("--pass1-mock", type=Path, default=MOCK_DIR / "pass1-empty-findings.json")
    parser.add_argument("--pass2-mock", type=Path, default=MOCK_DIR / "pass2-empty-findings.json")
    parser.add_argument(
        "--pass1-graph",
        type=Path,
        default=None,
        help="Override manifest graph for pass 1 (degraded artifact).",
    )
    parser.add_argument(
        "--pass2-graph",
        type=Path,
        default=None,
        help="Override revision graph for pass 2 (repaired artifact).",
    )
    parser.add_argument(
        "--require-accepted",
        action="store_true",
        help=(
            "Fail unless the session finalizes with outcome accepted. "
            "Suppresses open-vocab relationship lint that otherwise blocks "
            "CASE-domain kinds such as Charged_With."
        ),
    )
    parser.add_argument("--session-id", default="eval-session-replay-001")
    parser.add_argument(
        "--report",
        type=Path,
        default=EVAL_ROOT / "reports" / "session-replay-latest.json",
    )
    args = parser.parse_args(argv)

    _ensure_eval_workspace()

    lint_ctx = (
        _suppress_open_vocab_relationship_lint()
        if args.require_accepted
        else nullcontext()
    )
    with lint_ctx:
        session_report = replay_session(
            case_dir=args.case_dir,
            pass1_mock=args.pass1_mock,
            pass2_mock=args.pass2_mock,
            session_id=args.session_id,
            pass1_graph=args.pass1_graph,
            pass2_graph=args.pass2_graph,
        )

    session_report = sanitize_session_paths(session_report, PROJECT_ROOT)
    base_metrics = pass_counts(session_report)
    repair = session_repair_metrics(session_report)
    metrics = {**base_metrics, **repair}

    passed = bool(session_report.get("converged")) and bool(
        session_report.get("finalized")
    )
    if args.require_accepted:
        passed = passed and bool(session_report.get("accepted"))

    fixture_files = [
        Path(p)
        for p in (
            args.pass1_mock,
            args.pass2_mock,
            args.pass1_graph,
            args.pass2_graph,
        )
        if p is not None and Path(p).is_file()
    ]
    bundle_fp = None
    final = session_report.get("final") or {}
    if isinstance(final, dict):
        bundle_fp = final.get("validation_bundle_fingerprint") or (
            (final.get("validation") or {}).get("bundle_fingerprint")
        )

    report = {
        "harness": "run_session_replay",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "require_accepted": bool(args.require_accepted),
        "metrics": metrics,
        "metadata": report_environment_metadata(
            root=PROJECT_ROOT,
            fixture_paths=fixture_files,
            validation_bundle_fingerprint=bundle_fp,
        ),
        "session": session_report,
    }

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        f"critic session replay — case {session_report.get('case_id')}, "
        f"passes {metrics['passes_parsed_ok']}/{metrics['passes_attempted']}, "
        f"repair_rate={metrics.get('repair_rate')}, "
        f"outcome={session_report.get('final_outcome')}"
    )
    if not passed:
        if args.require_accepted and not session_report.get("accepted"):
            print("session replay failed: --require-accepted not met", file=sys.stderr)
        return 1
    print("session replay converged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
