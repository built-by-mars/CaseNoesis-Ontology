"""Round-2 tests for the deterministic critic foundation (issue #75)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from critic import (
    CriticArtifactRequest,
    CriticError,
    analyze_artifact,
    diff_findings,
    make_stable_finding_id,
    parse_critic_model_response,
)
from critic.canonical import load_canonical_graph
from critic.graph_heuristics import run_graph_heuristics
from critic.models import CriticFinding, CriticScorecard, CriticTarget, ValidationSummary
from critic.scorecard import build_deterministic_scorecard, merge_scorecards
from critic.serializer_python import analyze_python_serializer
from critic.finding_diff import FindingDiffResult

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"


def test_production_shaped_seeded_heuristics():
    view = load_canonical_graph(FIXTURES / "seeded-defects.jsonld")
    assert view.usable_for_heuristics
    findings, executions = run_graph_heuristics(view, artifact_hash="abc")
    rules = {f.rule_id for f in findings}
    assert "CRIT-H-CHARGED-WITH-REVERSED" in rules
    assert "CRIT-H-AUTH-NON-INVESTIGATION" in rules
    assert "CRIT-H-ACQ-INPUT-RESULT-INVERSION" in rules
    assert "CRIT-H-DICT-ENTRY-COLLISION" in rules
    assert "CRIT-H-FACET-PROPS-ON-OBSERVABLE" in rules
    assert "CRIT-H-RELATED-TO-OVERUSE" in rules
    assert all(e.status == "evaluated" for e in executions)


def test_gold_charged_with_no_direction_finding():
    view = load_canonical_graph(FIXTURES / "gold-charged-with.jsonld")
    findings, _ = run_graph_heuristics(view, artifact_hash="abc")
    assert "CRIT-H-CHARGED-WITH-REVERSED" not in {f.rule_id for f in findings}
    assert "CRIT-H-AUTH-NON-INVESTIGATION" not in {f.rule_id for f in findings}


def test_jsonld_turtle_semantic_equivalence(tmp_path):
    # Minimal equivalent graphs: Investigation without object
    jsonld = {
        "@context": {
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [
            {
                "@id": "urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "@type": "case-investigation:Investigation",
                "uco-core:name": "Empty investigation",
            }
        ],
    }
    jp = tmp_path / "a.jsonld"
    jp.write_text(json.dumps(jsonld), encoding="utf-8")
    ttl = tmp_path / "a.ttl"
    ttl.write_text(
        "@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .\n"
        "@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .\n"
        "<urn:uuid:aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa> a case-investigation:Investigation ;\n"
        '  uco-core:name "Empty investigation" .\n',
        encoding="utf-8",
    )
    j_findings, _ = run_graph_heuristics(load_canonical_graph(jp), artifact_hash="j")
    t_findings, _ = run_graph_heuristics(load_canonical_graph(ttl), artifact_hash="t")
    assert "CRIT-H-INV-NO-OBJECT" in {f.rule_id for f in j_findings}
    assert "CRIT-H-INV-NO-OBJECT" in {f.rule_id for f in t_findings}
    assert j_findings[0].finding_id == t_findings[0].finding_id


def test_stable_id_ignores_line_and_evidence_wording():
    a = make_stable_finding_id(
        "CRIT-S-PY-PRIVATE-OBJECTS", "bad_serializer.py", "_objects"
    )
    b = make_stable_finding_id(
        "CRIT-S-PY-PRIVATE-OBJECTS", "bad_serializer.py", "_objects"
    )
    assert a == b
    # Line is not part of identity
    f1 = CriticFinding(
        finding_id="",
        severity="high",
        category="serializer_api",
        confidence=1.0,
        status="new",
        target=CriticTarget(path="bad_serializer.py", line=10, qualified_name="_objects"),
        evidence_kind="deterministic",
        evidence=["old wording"],
        rationale="r1",
        recommended_change="c",
        verification_method="v",
        rule_id="CRIT-S-PY-PRIVATE-OBJECTS",
    )
    f1.ensure_identity_key()
    f2 = CriticFinding(
        finding_id="",
        severity="high",
        category="serializer_api",
        confidence=1.0,
        status="new",
        target=CriticTarget(path="bad_serializer.py", line=99, qualified_name="_objects"),
        evidence_kind="deterministic",
        evidence=["new wording completely different"],
        rationale="r2",
        recommended_change="c2",
        verification_method="v2",
        rule_id="CRIT-S-PY-PRIVATE-OBJECTS",
    )
    f2.ensure_identity_key()
    assert f1.finding_id == f2.finding_id


def test_absence_without_rule_evaluation_is_unevaluated_not_resolved():
    prior = CriticFinding(
        finding_id="",
        severity="high",
        category="relationship_direction",
        confidence=1.0,
        status="new",
        target=CriticTarget(node_id="urn:uuid:1"),
        evidence_kind="deterministic",
        evidence=["x"],
        rationale="r",
        recommended_change="c",
        verification_method="v",
        rule_id="CRIT-H-CHARGED-WITH-REVERSED",
    )
    prior.ensure_identity_key()
    diff = diff_findings(
        [prior],
        [],
        unevaluated_finding_ids={prior.finding_id},
    )
    assert diff.resolved == []
    assert len(diff.unevaluated) == 1

    diff2 = diff_findings(
        [prior],
        [],
        resolved_finding_ids={prior.finding_id},
    )
    assert len(diff2.resolved) == 1


def test_regression_when_resolved_finding_returns():
    prior = CriticFinding(
        finding_id=make_stable_finding_id("CRIT-H-CHARGED-WITH-REVERSED", "n1"),
        severity="high",
        category="relationship_direction",
        confidence=1.0,
        status="resolved",
        target=CriticTarget(node_id="n1"),
        evidence_kind="deterministic",
        evidence=["x"],
        rationale="r",
        recommended_change="c",
        verification_method="v",
        rule_id="CRIT-H-CHARGED-WITH-REVERSED",
    )
    current = CriticFinding.from_dict({**prior.to_dict(), "status": "new"})
    diff = diff_findings([prior], [current])
    assert len(diff.regressions) == 1


def test_python_serializer_ast_findings():
    path = FIXTURES / "bad_serializer.py"
    findings = analyze_python_serializer(path, path.read_text(encoding="utf-8"))
    rules = {f.rule_id for f in findings}
    assert "CRIT-S-PY-PRIVATE-OBJECTS" in rules
    assert "CRIT-S-PY-JSON-DUMPS-ONLY" in rules
    assert "CRIT-S-PY-SWALLOWED-EXCEPTION" in rules
    assert "CRIT-S-PY-FAIL-OPEN-VALIDATION" in rules


def test_source_hash_ignores_unrelated_hashes(tmp_path, monkeypatch):
    import graph_validator

    monkeypatch.setattr(graph_validator, "validator_available", lambda: False)
    src = tmp_path / "fixture-source.md"
    src.write_text("hello source", encoding="utf-8")
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    doc = json.loads((FIXTURES / "seeded-defects.jsonld").read_text(encoding="utf-8"))
    # Fix embedded source hash to match file
    for node in doc["@graph"]:
        if node.get("uco-core:name") == "fixture-source.md":
            node["uco-core:hasFacet"][0]["uco-observable:hash"][0][
                "uco-types:hashValue"
            ] = digest
    graph_path = tmp_path / "g.jsonld"
    graph_path.write_text(json.dumps(doc), encoding="utf-8")
    review = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(graph_path),
            source_paths=[str(src)],
            critic_scope="graph",
        )
    )
    rules = {f.rule_id for f in review.merged_findings}
    assert "CRIT-C-SOURCE-HASH-MISMATCH" not in rules


def test_incorrect_source_hash_detected(tmp_path, monkeypatch):
    import graph_validator

    monkeypatch.setattr(graph_validator, "validator_available", lambda: False)
    src = tmp_path / "fixture-source.md"
    src.write_text("hello source", encoding="utf-8")
    graph_path = tmp_path / "g.jsonld"
    graph_path.write_text(
        (FIXTURES / "seeded-defects.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    review = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(graph_path),
            source_paths=[str(src)],
            critic_scope="graph",
        )
    )
    assert "CRIT-C-SOURCE-HASH-MISMATCH" in {f.rule_id for f in review.merged_findings}


def test_model_response_schema_enforcement():
    with pytest.raises(Exception) as exc:
        parse_critic_model_response(
            {
                "schema_version": "1.1.0",
                "graph_sha256": "a" * 64,
                "prompt_package_hash": "b" * 64,
                "findings": [
                    {
                        "severity": "high",
                        "category": "validation",
                        "confidence": 0.5,
                        "target": {"node_id": "urn:uuid:1"},
                        "evidence": ["x"],
                        "evidence_kind": "deterministic",
                        "rationale": "r",
                        "recommended_change": "c",
                        "verification_method": "v",
                    }
                ],
                "scorecard": {},
            },
            expected_graph_sha256="a" * 64,
            expected_prompt_package_hash="b" * 64,
        )
    assert exc.value.code == "critic_response_schema_mismatch"


def test_model_cannot_override_validation_cap():
    validation = ValidationSummary(
        conforms=False,
        verification_status="complete",
        violation_count=2,
    )
    det = build_deterministic_scorecard(
        validation, [], has_sources=False, has_serializer=False, has_coverage_contract=False
    )
    assert det.schema_concept_conformance.score == 0
    assert det.source_fidelity.assessed is False
    model = CriticScorecard.from_dict(
        {"schema_concept_conformance": {"score": 5, "assessed": True}}
    )
    merged = merge_scorecards(det, model)
    assert merged.schema_concept_conformance.score == 0


def test_analyze_artifact_offline(tmp_path, monkeypatch):
    import graph_validator

    monkeypatch.setattr(graph_validator, "validator_available", lambda: False)
    g = tmp_path / "seeded-defects.jsonld"
    s = tmp_path / "bad_serializer.py"
    g.write_text((FIXTURES / "seeded-defects.jsonld").read_text(encoding="utf-8"))
    s.write_text((FIXTURES / "bad_serializer.py").read_text(encoding="utf-8"))
    review = analyze_artifact(
        CriticArtifactRequest(graph_path=str(g), serializer_path=str(s), critic_scope="both")
    )
    assert review.prompt_package["prompt_package_hash"]
    assert review.prompt_package["byte_size"] >= len(
        json.dumps(review.prompt_package, sort_keys=True, separators=(",", ":"))
    ) - 200  # hash/size fields included
    assert review.rule_executions
    assert "CRIT-H-CHARGED-WITH-REVERSED" in {f.rule_id for f in review.merged_findings}
    assert review.handoff_suggestions == []


def test_workspace_policy_blocks_outside_path(tmp_path, monkeypatch):
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", str(tmp_path))
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(tmp_path / "out"))
    (tmp_path / "out").mkdir()
    with pytest.raises(CriticError) as exc:
        analyze_artifact(
            CriticArtifactRequest(graph_path="/tmp/case-uco-critic-outside.jsonld")
        )
    assert exc.value.code == "critic_path_outside_workspace"


@pytest.mark.skipif(
    __import__("shutil").which("case_validate") is None,
    reason="case_validate not installed",
)
def test_real_case_validate_integration_on_gold():
    review = analyze_artifact(
        CriticArtifactRequest(
            graph_path=str(FIXTURES / "gold-charged-with.jsonld"),
            critic_scope="graph",
        )
    )
    # May or may not fully conform depending on ontology completeness of the
    # tiny fixture; require that validation actually ran to completion or
    # reported structured nonconformance — never unavailable.
    assert review.validation.error_code != "critic_validation_unavailable"
    assert review.validation.verification_status in {"complete", "could_not_verify"}
    if review.validation.verification_status == "complete":
        assert review.validation.conforms is not None
