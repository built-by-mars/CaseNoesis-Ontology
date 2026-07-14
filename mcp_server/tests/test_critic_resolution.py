"""P0-1: two-pass heuristic resolution evidence (rule_version-aware)."""

from __future__ import annotations

from pathlib import Path

import pytest

from critic import CriticArtifactRequest, analyze_artifact
from critic.graph_heuristics import RULE_VERSION, run_graph_heuristics
from critic.canonical import load_canonical_graph

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"
EVAL_MICRO = (
    Path(__file__).resolve().parents[2]
    / "evaluation"
    / "critic"
    / "cases"
    / "micro"
)


def _open_by_rule(review) -> dict[str, object]:
    return {
        f.rule_id: f
        for f in review.merged_findings
        if f.rule_id and f.status not in {"resolved"}
    }


def _resolved_by_rule(review) -> dict[str, object]:
    return {
        f.rule_id: f
        for f in review.merged_findings
        if f.rule_id and f.status == "resolved"
    }


def _two_pass(
    *,
    pass1: Path,
    pass2: Path,
    project_root: Path | None = None,
):
    root = str(project_root or Path(__file__).resolve().parents[2])
    r1 = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(pass1),
            critic_scope="graph",
            project_root=root,
            pass_number=1,
        )
    )
    r2 = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(pass2),
            critic_scope="graph",
            project_root=root,
            pass_number=2,
            prior_findings=list(r1.merged_findings),
        )
    )
    return r1, r2


def test_heuristic_findings_stamp_rule_version_1_2_0():
    view = load_canonical_graph(FIXTURES / "seeded-defects.jsonld")
    findings, executions = run_graph_heuristics(view, artifact_hash="rv")
    assert RULE_VERSION == "1.2.0"
    assert findings
    assert all(f.rule_version == "1.2.0" for f in findings)
    assert all(e.rule_version == "1.2.0" for e in executions)


@pytest.mark.parametrize(
    "rule_id,pass1,pass2",
    [
        (
            "CRIT-H-CHARGED-WITH-REVERSED",
            FIXTURES / "seeded-defects.jsonld",
            FIXTURES / "gold-charged-with.jsonld",
        ),
        (
            "CRIT-H-CHARGED-WITH-REVERSED",
            EVAL_MICRO / "charged-with-reversed" / "graph.jsonld",
            EVAL_MICRO / "gold-charged-with" / "graph.jsonld",
        ),
        (
            "CRIT-H-INV-NO-OBJECT",
            FIXTURES / "seeded-defects.jsonld",
            FIXTURES / "gold-charged-with.jsonld",
        ),
        (
            "CRIT-H-AUTH-NON-INVESTIGATION",
            FIXTURES / "seeded-defects.jsonld",
            FIXTURES / "gold-charged-with.jsonld",
        ),
        (
            "CRIT-H-ACTION-COMPLETENESS",
            FIXTURES / "seeded-defects.jsonld",
            FIXTURES / "gold-charged-with.jsonld",
        ),
        (
            "CRIT-H-IDENTITY-CONFLATION",
            FIXTURES / "heuristic-identity-conflation.jsonld",
            FIXTURES / "heuristic-identity-conflation-fixed.jsonld",
        ),
        (
            "CRIT-H-DERIVED-NO-HASH",
            FIXTURES / "heuristic-derived-no-hash.jsonld",
            FIXTURES / "heuristic-derived-no-hash-fixed.jsonld",
        ),
    ],
    ids=[
        "charged-with-seeded-to-gold",
        "charged-with-eval-micro",
        "inv-no-object",
        "auth-non-investigation",
        "action-completeness",
        "identity-conflation",
        "derived-no-hash",
    ],
)
def test_heuristic_finding_resolves_on_repair(rule_id: str, pass1: Path, pass2: Path):
    assert pass1.is_file(), pass1
    assert pass2.is_file(), pass2
    r1, r2 = _two_pass(pass1=pass1, pass2=pass2)
    open1 = _open_by_rule(r1)
    assert rule_id in open1, sorted(open1)
    finding = open1[rule_id]
    assert finding.rule_version == "1.2.0"
    assert finding.status in {"new", "persisting"}

    resolved = _resolved_by_rule(r2)
    assert rule_id in resolved, {
        "open": sorted(_open_by_rule(r2)),
        "resolved": sorted(resolved),
        "statuses": [(f.rule_id, f.status) for f in r2.merged_findings],
    }
    assert resolved[rule_id].finding_id == finding.finding_id
    assert rule_id not in _open_by_rule(r2)
