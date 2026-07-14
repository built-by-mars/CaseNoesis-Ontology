"""P0-2 marking-aware sampling egress + P0-3 assessment-ledger sampling."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

import graph_validator
from critic.models import CriticFinding, CriticTarget, make_stable_finding_id
from critic.response_parser import (
    CriticResponseError,
    build_assessment_ledger,
    parse_critic_model_response,
)
from critic.sampling import (
    FakeSampleContext,
    build_sampling_disclosure,
    extract_markings_from_jsonld,
    maybe_sample_critic,
)
from critic.sessions import (
    start_critic_review,
    submit_critic_revision,
    submit_manual_critic_response,
)
from critic_tools import (
    tool_start_critic_review_with_sampling,
    tool_submit_critic_revision_with_sampling,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "critic"
PHANTOM_GATE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "scenarios"
    / "operation-phantom-gate.jsonld"
)
MARKED_FIXTURE = FIXTURES / "phantom-gate-marked-restricted.jsonld"


def _conforming_report(**kwargs) -> graph_validator.GraphValidationReport:
    return graph_validator.GraphValidationReport(
        conforms=True,
        warning_count=0,
        violation_count=0,
        exit_code=0,
        validator_name="case_validate",
        safe_summary="conforms",
        verification_status="complete",
        **kwargs,
    )


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    read = tmp_path / "read"
    write = tmp_path / "write"
    read.mkdir()
    write.mkdir()
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", str(read))
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(write))
    monkeypatch.setenv("CASE_UCO_CRITIC_SESSION_ROOT", str(write / "critic-sessions"))
    monkeypatch.setenv("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")
    monkeypatch.delenv("CASE_UCO_MCP_CRITIC_MODE", raising=False)
    monkeypatch.delenv("CASE_UCO_MCP_PROFILE", raising=False)
    monkeypatch.delenv("CASE_UCO_CRITIC_SAMPLING_RESTRICTED_ALLOW", raising=False)
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)

    # Align mocked validation with live bundle identity used by session config binding.
    try:
        from critic.sessions import _resolve_and_hash_bundle

        live = _resolve_and_hash_bundle(
            {
                "critic_scope": "graph",
                "serializer_mode": "auto",
                "force_rdfs_inference": False,
                "extensions": [],
                "profiles": [],
                "extra_ontology_graphs": [],
            }
        )
    except Exception:  # noqa: BLE001
        live = {}

    def _report(*_a, **_k):
        return _conforming_report(
            bundle_fingerprint=live.get("bundle_fingerprint"),
            validator_version=live.get("validator_version"),
        )

    monkeypatch.setattr(graph_validator, "validate_graph_file", _report)
    return read, write


def _copy(read: Path, src: Path, name: str = "graph.jsonld") -> Path:
    dest = read / name
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def _empty_response(package: dict) -> dict:
    return {
        "schema_version": "1.2.0",
        "session_id": package["session_id"],
        "pass_number": package["pass_number"],
        "graph_sha256": package["artifact_hashes"]["graph_sha256"],
        "serializer_sha256": package["artifact_hashes"].get("serializer_sha256"),
        "prompt_package_hash": package["prompt_package_hash"],
        "review_request_sha256": package.get("review_request_sha256"),
        "review_config_sha256": package.get("review_config_sha256"),
        "findings": [],
        "finding_assessments": [],
        "scorecard": {},
    }


def _assessment(
    finding_id: str,
    assessment: str,
    *,
    evidence: list[str] | None = None,
) -> dict:
    return {
        "assesses_finding_id": finding_id,
        "assessment": assessment,
        "evidence": evidence or ["sampled evidence"],
        "verification_method": "re-check graph",
        "rationale": f"assessment={assessment}",
    }


# --- P0-2 -----------------------------------------------------------------


def test_phantom_gate_markings_extracted_from_gold_graph():
    data = json.loads(PHANTOM_GATE.read_text(encoding="utf-8"))
    ids, names = extract_markings_from_jsonld(data)
    assert ids
    joined = " ".join(names).upper()
    assert "CAC" in joined or "TOP SECRET" in joined
    disclosure = build_sampling_disclosure(
        {
            "source_excerpts": [],
            "serializer_excerpts": [],
            "graph_neighborhoods": [],
            "structural_stats": {"node_count": 1},
            "token_estimate": 10,
        },
        graph_jsonld=data,
    )
    assert disclosure["restricted_content_detected"] is True
    assert disclosure["egress_decision"] == "deny"
    assert disclosure["marking_names"]


def test_marked_phantom_gate_sampling_blocked(workspace, monkeypatch):
    """Marked Phantom Gate–style graph: ctx.sample never called; prompt still returned."""

    import asyncio
    from critic_tools import tool_start_critic_review_with_sampling

    read, _ = workspace
    graph = _copy(read, MARKED_FIXTURE, "phantom-marked.jsonld")
    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "client_sampling")

    started = start_critic_review(
        graph_path=str(graph),
        critic_scope="graph",
        model_policy="client_sampling",
    )
    package = started["prompt_package"]
    assert package is not None
    assert "sampling_disclosure" in package
    assert package["sampling_disclosure"]["restricted_content_detected"] is True
    assert package["sampling_disclosure"]["egress_decision"] == "deny"

    ctx = FakeSampleContext(_empty_response(package))

    async def _run():
        return await maybe_sample_critic(
            ctx, package, model_policy="client_sampling"
        )

    sampled = asyncio.run(_run())
    assert ctx.calls == 0
    assert sampled.status == "critic_sampling_restricted_content"
    assert sampled.fallback is True
    assert sampled.metadata["sampling_disclosure"]["egress_decision"] == "deny"

    async def _tool():
        return await tool_start_critic_review_with_sampling(
            FakeSampleContext(_empty_response(package)),
            graph_path=str(graph),
            critic_scope="graph",
            model_policy="client_sampling",
        )

    tool_result = asyncio.run(_tool())
    assert tool_result["ok"] is True
    assert tool_result["sampling"]["status"] == "critic_sampling_restricted_content"
    assert tool_result["prompt_package"] is not None
    assert tool_result["prompt_package"]["sampling_disclosure"]["egress_decision"] == (
        "deny"
    )
    assert tool_result["next_action"] == "submit_manual_critic_response"


def test_marked_non_restricted_requires_manual(workspace, monkeypatch):
    read, _ = workspace
    # Strip restricted marking names → LES only.
    data = json.loads(MARKED_FIXTURE.read_text(encoding="utf-8"))
    for node in data.get("@graph") or []:
        if not isinstance(node, dict):
            continue
        name = node.get("uco-core:name")
        if isinstance(name, str) and (
            "SECRET" in name.upper()
            or "CAC" in name.upper()
            or "JUVENILE" in name.upper()
        ):
            node["uco-core:name"] = "Law enforcement sensitive — PGA task force"
        stmt = node.get("marking:statement")
        if isinstance(stmt, str):
            node["marking:statement"] = "LAW ENFORCEMENT SENSITIVE"
    path = read / "marked-les.jsonld"
    path.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "client_sampling")

    started = start_critic_review(
        graph_path=str(path), critic_scope="graph", model_policy="client_sampling"
    )
    package = started["prompt_package"]
    ctx = FakeSampleContext(_empty_response(package))
    sampled = asyncio.run(
        maybe_sample_critic(ctx, package, model_policy="client_sampling")
    )
    assert ctx.calls == 0
    assert sampled.status == "critic_manual_response_required"
    assert package["sampling_disclosure"]["egress_decision"] == "manual_required"


def test_restricted_allow_env_permits_sampling(workspace, monkeypatch):
    read, _ = workspace
    graph = _copy(read, MARKED_FIXTURE)
    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "client_sampling")
    monkeypatch.setenv("CASE_UCO_CRITIC_SAMPLING_RESTRICTED_ALLOW", "1")

    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="client_sampling"
    )
    package = started["prompt_package"]
    assert package["sampling_disclosure"]["egress_decision"] == "allow"
    ctx = FakeSampleContext(_empty_response(package))
    sampled = asyncio.run(
        maybe_sample_critic(ctx, package, model_policy="client_sampling")
    )
    assert ctx.calls == 1
    assert sampled.status == "ok"


def test_offline_investigation_never_samples_without_explicit_mode(
    workspace, monkeypatch
):
    read, _ = workspace
    graph = _copy(read, FIXTURES / "gold-charged-with.jsonld")
    monkeypatch.delenv("CASE_UCO_MCP_CRITIC_MODE", raising=False)
    monkeypatch.setenv("CASE_UCO_MCP_PROFILE", "offline-investigation")

    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="client_sampling"
    )
    # Deployment clamps session to manual.
    assert started["model_policy"] == "manual"
    package = started["prompt_package"]
    ctx = FakeSampleContext(_empty_response(package))
    sampled = asyncio.run(
        maybe_sample_critic(ctx, package, model_policy="client_sampling")
    )
    assert ctx.calls == 0
    assert sampled.status == "critic_manual_response_required"
    assert sampled.metadata.get("reason") == "deployment_mode"


def test_source_excerpts_unknown_classification_manual(monkeypatch):
    monkeypatch.delenv("CASE_UCO_CRITIC_SAMPLING_RESTRICTED_ALLOW", raising=False)
    disclosure = build_sampling_disclosure(
        {
            "source_excerpts": [{"path": "src.md", "text": "excerpt"}],
            "serializer_excerpts": [],
            "graph_neighborhoods": [],
            "structural_stats": {"node_count": 0},
            "token_estimate": 8,
        }
    )
    assert disclosure["contains_source_excerpts"] is True
    assert disclosure["egress_decision"] == "manual_required"


# --- P0-3 -----------------------------------------------------------------


def _det_finding(node_id: str = "urn:example:n1") -> CriticFinding:
    return CriticFinding(
        finding_id="",
        severity="high",
        category="investigation_structure",
        confidence=1.0,
        status="new",
        target=CriticTarget(node_id=node_id),
        evidence_kind="deterministic",
        evidence=["det"],
        rationale="deterministic defect",
        recommended_change="fix",
        verification_method="re-run heuristics",
        rule_id="CRIT-H-INV-NO-OBJECT",
        rule_version="1.2.0",
    )


def _model_finding(node_id: str = "urn:example:model-n") -> CriticFinding:
    claim = "missing_link"
    target = CriticTarget(node_id=node_id)
    finding_id = make_stable_finding_id(
        "MODEL-investigation_structure", *target.semantic_parts(), claim
    )
    return CriticFinding(
        finding_id=finding_id,
        severity="medium",
        category="investigation_structure",
        confidence=0.8,
        status="new",
        target=target,
        evidence_kind="critic_inference",
        evidence=["model"],
        rationale="model claim",
        recommended_change="link object",
        verification_method="inspect graph",
        claim_type=claim,
    )


def test_parse_unknown_finding_assessment_rejected():
    ledger = build_assessment_ledger([_det_finding()])
    with pytest.raises(CriticResponseError) as exc:
        parse_critic_model_response(
            {
                "schema_version": "1.2.0",
                "graph_sha256": "a" * 64,
                "prompt_package_hash": "b" * 64,
                "findings": [],
                "finding_assessments": [
                    _assessment("CRIT-does-not-exist", "persists")
                ],
                "scorecard": {},
            },
            expected_graph_sha256="a" * 64,
            expected_prompt_package_hash="b" * 64,
            allowed_assessments=ledger,
        )
    assert exc.value.code == "critic_assessment_unknown_finding"


def test_parse_resolve_deterministic_forbidden():
    finding = _det_finding()
    finding.ensure_identity_key()
    ledger = build_assessment_ledger([finding])
    with pytest.raises(CriticResponseError) as exc:
        parse_critic_model_response(
            {
                "schema_version": "1.2.0",
                "graph_sha256": "a" * 64,
                "prompt_package_hash": "b" * 64,
                "findings": [],
                "finding_assessments": [
                    _assessment(finding.finding_id, "resolved")
                ],
                "scorecard": {},
            },
            expected_graph_sha256="a" * 64,
            expected_prompt_package_hash="b" * 64,
            allowed_assessments=ledger,
        )
    assert exc.value.code == "critic_assessment_deterministic_resolve_forbidden"


def test_parse_dispute_deterministic_allowed():
    finding = _det_finding()
    finding.ensure_identity_key()
    ledger = build_assessment_ledger([finding])
    ok = parse_critic_model_response(
        {
            "schema_version": "1.2.0",
            "graph_sha256": "a" * 64,
            "prompt_package_hash": "b" * 64,
            "findings": [],
            "finding_assessments": [_assessment(finding.finding_id, "disputed")],
            "scorecard": {},
        },
        expected_graph_sha256="a" * 64,
        expected_prompt_package_hash="b" * 64,
        allowed_assessments=ledger,
    )
    assert ok["finding_assessments"][0]["assessment"] == "disputed"


def test_parse_resolve_model_finding_allowed():
    finding = _model_finding()
    ledger = build_assessment_ledger([finding])
    ok = parse_critic_model_response(
        {
            "schema_version": "1.2.0",
            "graph_sha256": "a" * 64,
            "prompt_package_hash": "b" * 64,
            "findings": [],
            "finding_assessments": [_assessment(finding.finding_id, "resolved")],
            "scorecard": {},
        },
        expected_graph_sha256="a" * 64,
        expected_prompt_package_hash="b" * 64,
        allowed_assessments=ledger,
    )
    assert ok["finding_assessments"][0]["assessment"] == "resolved"


def test_parse_persists_model_finding_allowed():
    finding = _model_finding()
    ledger = build_assessment_ledger([finding])
    ok = parse_critic_model_response(
        {
            "schema_version": "1.2.0",
            "graph_sha256": "a" * 64,
            "prompt_package_hash": "b" * 64,
            "findings": [],
            "finding_assessments": [_assessment(finding.finding_id, "persists")],
            "scorecard": {},
        },
        expected_graph_sha256="a" * 64,
        expected_prompt_package_hash="b" * 64,
        allowed_assessments=ledger,
    )
    assert ok["finding_assessments"][0]["assessment"] == "persists"


def test_sampling_unknown_assessment_retries_then_fallback(workspace, monkeypatch):
    read, _ = workspace
    graph = _copy(read, FIXTURES / "gold-charged-with.jsonld")
    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "client_sampling")
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="client_sampling"
    )
    package = started["prompt_package"]
    ledger = started["assessment_ledger"]
    bad = _empty_response(package)
    bad["finding_assessments"] = [_assessment("CRIT-unknown-xyz", "persists")]
    ctx = FakeSampleContext(bad)

    async def _run():
        return await maybe_sample_critic(
            ctx,
            package,
            model_policy="client_sampling",
            allowed_assessments=ledger,
            retries=1,
        )

    sampled = asyncio.run(_run())
    assert ctx.calls >= 1
    assert sampled.status == "critic_sampling_invalid_response"
    assert sampled.fallback is True
    assert sampled.metadata.get("reason") == "critic_assessment_unknown_finding"

    async def _tool():
        return await tool_start_critic_review_with_sampling(
            FakeSampleContext(bad),
            graph_path=str(graph),
            critic_scope="graph",
            model_policy="client_sampling",
        )

    tool_result = asyncio.run(_tool())
    assert tool_result["ok"] is True
    assert tool_result["sampling"]["status"] == "critic_sampling_invalid_response"
    assert tool_result["next_action"] == "submit_manual_critic_response"


def test_sampling_resolve_deterministic_fallback(workspace, monkeypatch):
    read, _ = workspace
    graph = _copy(read, FIXTURES / "gold-charged-with.jsonld")
    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "client_sampling")
    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="client_sampling"
    )
    package = started["prompt_package"]
    ledger = started["assessment_ledger"]
    # Prefer a real deterministic finding id when present.
    det_ids = [
        fid
        for fid, meta in ledger.items()
        if meta.get("evidence_kind") in {"deterministic", "source"}
    ]
    if not det_ids:
        pytest.skip("gold graph produced no deterministic findings")
    bad = _empty_response(package)
    bad["finding_assessments"] = [_assessment(det_ids[0], "resolved")]
    ctx = FakeSampleContext(bad)
    sampled = asyncio.run(
        maybe_sample_critic(
            ctx,
            package,
            model_policy="client_sampling",
            allowed_assessments=ledger,
            retries=1,
        )
    )
    assert ctx.calls >= 1
    assert sampled.status == "critic_sampling_invalid_response"
    assert sampled.metadata.get("reason") == (
        "critic_assessment_deterministic_resolve_forbidden"
    )


def test_two_pass_sampled_vs_manual_completed_pass_equivalent(workspace, monkeypatch):
    """Pass-1 emits a model finding; pass-2 assesses it. Manual ≡ sampled completed-pass."""

    read, _ = workspace
    graph = _copy(read, FIXTURES / "gold-charged-with.jsonld")
    monkeypatch.setenv("CASE_UCO_MCP_CRITIC_MODE", "client_sampling")

    def _pass1_finding_payload(package: dict) -> dict:
        payload = _empty_response(package)
        payload["findings"] = [
            {
                "severity": "medium",
                "category": "investigation_structure",
                "confidence": 0.85,
                "claim_type": "sampled_model_claim",
                "target": {"node_id": "urn:example:investigation"},
                "evidence": ["model observed structure"],
                "rationale": "pass-1 model finding",
                "recommended_change": "clarify object link",
                "verification_method": "re-analyze",
            }
        ]
        return payload

    def _pass2_assess_payload(package: dict, finding_id: str) -> dict:
        payload = _empty_response(package)
        payload["finding_assessments"] = [
            _assessment(finding_id, "persists", evidence=["still present"])
        ]
        return payload

    # --- Manual path ---
    manual = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="manual"
    )
    p1 = _pass1_finding_payload(manual["prompt_package"])
    r1 = submit_manual_critic_response(manual["session_id"], p1)
    assert r1["completed_critic_responses"] == 1
    model_ids = [
        fid
        for fid in (r1.get("prior_finding_ids") or [])
        if fid.startswith("CRIT-")
    ]
    # Recover model finding id from completed pass / ledger on revision.
    revised = submit_critic_revision(
        manual["session_id"], graph_path=str(graph), change_summary="confirm"
    )
    ledger2 = revised["assessment_ledger"]
    model_open = [
        fid
        for fid, meta in ledger2.items()
        if meta.get("evidence_kind") == "critic_inference"
    ]
    assert model_open, "expected pass-1 model finding in pass-2 ledger"
    model_fid = model_open[0]
    p2 = _pass2_assess_payload(revised["prompt_package"], model_fid)
    r2 = submit_manual_critic_response(manual["session_id"], p2)
    assert r2["completed_critic_responses"] == 2

    import os

    session_root = Path(os.environ["CASE_UCO_CRITIC_SESSION_ROOT"])
    manual_completed = json.loads(
        (session_root / manual["session_id"] / "completed-pass-2.json").read_text(
            encoding="utf-8"
        )
    )

    # --- Sampled path ---
    sampled_started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="client_sampling"
    )

    def factory_pass1(call_n: int, kwargs: dict) -> dict:
        messages = kwargs.get("messages") or ""
        content = json.loads(messages) if isinstance(messages, str) else {}
        package = content.get("prompt_package") or sampled_started["prompt_package"]
        return _pass1_finding_payload(package)

    ctx1 = FakeSampleContext(payload_factory=factory_pass1)
    s1 = asyncio.run(
        maybe_sample_critic(
            ctx1,
            sampled_started["prompt_package"],
            model_policy="client_sampling",
            allowed_assessments=sampled_started["assessment_ledger"],
        )
    )
    assert s1.status == "ok"
    submit_manual_critic_response(
        sampled_started["session_id"], s1.response, sampling=s1.to_dict()
    )
    revised_s = submit_critic_revision(
        sampled_started["session_id"],
        graph_path=str(graph),
        change_summary="confirm",
    )
    ledger_s2 = revised_s["assessment_ledger"]
    model_open_s = [
        fid
        for fid, meta in ledger_s2.items()
        if meta.get("evidence_kind") == "critic_inference"
    ]
    assert model_open_s
    model_fid_s = model_open_s[0]

    def factory_pass2(call_n: int, kwargs: dict) -> dict:
        messages = kwargs.get("messages") or ""
        content = json.loads(messages) if isinstance(messages, str) else {}
        package = content.get("prompt_package") or revised_s["prompt_package"]
        return _pass2_assess_payload(package, model_fid_s)

    ctx2 = FakeSampleContext(payload_factory=factory_pass2)
    s2 = asyncio.run(
        maybe_sample_critic(
            ctx2,
            revised_s["prompt_package"],
            model_policy="client_sampling",
            allowed_assessments=ledger_s2,
        )
    )
    assert s2.status == "ok"
    submit_manual_critic_response(
        sampled_started["session_id"], s2.response, sampling=s2.to_dict()
    )
    sampled_completed = json.loads(
        (
            session_root
            / sampled_started["session_id"]
            / "completed-pass-2.json"
        ).read_text(encoding="utf-8")
    )

    def _norm(completed: dict) -> dict:
        findings = sorted(
            completed.get("merged_findings") or [],
            key=lambda f: f.get("finding_id") or "",
        )
        assessments = sorted(
            completed.get("finding_assessments") or [],
            key=lambda a: (
                a.get("assesses_finding_id") or "",
                a.get("assessment") or "",
            ),
        )
        return {
            "status": completed.get("status"),
            "finding_ids": [f.get("finding_id") for f in findings],
            "finding_statuses": {
                f.get("finding_id"): f.get("status") for f in findings
            },
            "assessments": [
                (a.get("assesses_finding_id"), a.get("assessment"))
                for a in assessments
            ],
        }

    assert _norm(manual_completed) == _norm(sampled_completed)
    assert model_fid == model_fid_s
