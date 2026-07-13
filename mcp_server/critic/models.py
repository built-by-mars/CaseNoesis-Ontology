"""Typed critic review contracts (issue #75).

These models are deliberately free of MCP/session orchestration concerns.
Orchestration (#76) consumes these types and persists session state separately.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

CRITIC_SCHEMA_VERSION = "1.0.0"

Severity = Literal["critical", "high", "medium", "low", "info"]
FindingStatus = Literal["new", "persisting", "resolved", "regression", "disputed"]
EvidenceKind = Literal["deterministic", "source", "critic_inference"]
CriticScope = Literal["graph", "serializer", "both"]
HandoffType = Literal[
    "recipe_improvement",
    "routing_gap",
    "new_recipe_candidate",
    "ontology_gap",
    "extension_gap",
    "sdk_bug",
]

VOCAB_PATH = Path(__file__).resolve().parent / "vocabularies.json"


def load_vocabularies() -> dict[str, Any]:
    return json.loads(VOCAB_PATH.read_text(encoding="utf-8"))


@dataclass
class CriticTarget:
    path: str | None = None
    line: int | None = None
    node_id: str | None = None
    predicate: str | None = None
    json_pointer: str | None = None

    def identity_fragment(self) -> str:
        parts = [
            self.path or "",
            str(self.line) if self.line is not None else "",
            self.node_id or "",
            self.predicate or "",
            self.json_pointer or "",
        ]
        return "|".join(parts)


@dataclass
class CriticFinding:
    finding_id: str
    severity: Severity
    category: str
    confidence: float
    status: FindingStatus
    target: CriticTarget
    evidence_kind: EvidenceKind
    evidence: list[str]
    rationale: str
    recommended_change: str
    verification_method: str
    rule_id: str | None = None
    related_recipe: str | None = None
    related_validation_result: str | None = None
    identity_key: str | None = None
    suppressible: bool = True
    disputed_rationale: str | None = None

    def ensure_identity_key(self) -> str:
        if self.identity_key:
            return self.identity_key
        evidence_key = "|".join(sorted(self.evidence))[:240]
        raw = "|".join(
            [
                self.category,
                self.rule_id or "",
                self.target.identity_fragment(),
                evidence_key,
            ]
        )
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
        self.identity_key = f"CRIT-{digest}"
        return self.identity_key

    def to_dict(self) -> dict[str, Any]:
        self.ensure_identity_key()
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CriticFinding:
        target_raw = data.get("target") or {}
        target = CriticTarget(
            path=target_raw.get("path"),
            line=target_raw.get("line"),
            node_id=target_raw.get("node_id"),
            predicate=target_raw.get("predicate"),
            json_pointer=target_raw.get("json_pointer"),
        )
        finding = cls(
            finding_id=str(data["finding_id"]),
            severity=data["severity"],
            category=str(data["category"]),
            confidence=float(data["confidence"]),
            status=data.get("status", "new"),
            target=target,
            evidence_kind=data["evidence_kind"],
            evidence=list(data.get("evidence") or []),
            rationale=str(data.get("rationale") or ""),
            recommended_change=str(data.get("recommended_change") or ""),
            verification_method=str(data.get("verification_method") or ""),
            rule_id=data.get("rule_id"),
            related_recipe=data.get("related_recipe"),
            related_validation_result=data.get("related_validation_result"),
            identity_key=data.get("identity_key"),
            suppressible=bool(data.get("suppressible", True)),
            disputed_rationale=data.get("disputed_rationale"),
        )
        finding.ensure_identity_key()
        return finding


@dataclass
class CriticScorecard:
    schema_concept_conformance: int = 0
    source_fidelity: int = 0
    semantic_precision: int = 0
    provenance_custody: int = 0
    markings_authorization: int = 0
    coverage_completeness: int = 0
    serializer_quality: int = 0
    maintainability_reproducibility: int = 0
    caps_applied: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CriticScorecard:
        return cls(
            schema_concept_conformance=int(data.get("schema_concept_conformance", 0)),
            source_fidelity=int(data.get("source_fidelity", 0)),
            semantic_precision=int(data.get("semantic_precision", 0)),
            provenance_custody=int(data.get("provenance_custody", 0)),
            markings_authorization=int(data.get("markings_authorization", 0)),
            coverage_completeness=int(data.get("coverage_completeness", 0)),
            serializer_quality=int(data.get("serializer_quality", 0)),
            maintainability_reproducibility=int(
                data.get("maintainability_reproducibility", 0)
            ),
            caps_applied=list(data.get("caps_applied") or []),
        )


@dataclass
class SelfImprovementHandoffCandidate:
    handoff_type: HandoffType
    finding_ids: list[str]
    summary: str
    recurrence_key: str
    validation_evidence: list[str] = field(default_factory=list)
    requires_operator_approval: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CriticArtifactRequest:
    graph_path: str
    serializer_path: str | None = None
    source_paths: list[str] = field(default_factory=list)
    coverage_contract_path: str | None = None
    extensions: list[str] = field(default_factory=list)
    profiles: list[str] = field(default_factory=list)
    critic_scope: CriticScope = "both"
    project_root: str | None = None
    prior_findings: list[CriticFinding] = field(default_factory=list)
    disputed_identity_keys: dict[str, str] = field(default_factory=dict)


@dataclass
class ArtifactHashes:
    graph_sha256: str
    serializer_sha256: str | None = None
    source_sha256: dict[str, str] = field(default_factory=dict)
    coverage_contract_sha256: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationSummary:
    conforms: bool | None
    verification_status: str
    violation_count: int = 0
    warning_count: int = 0
    bundle_fingerprint: str | None = None
    selected_profiles: list[str] = field(default_factory=list)
    selected_extensions: list[str] = field(default_factory=list)
    stage_status: dict[str, str] = field(default_factory=dict)
    profile_not_selected: list[dict[str, Any]] = field(default_factory=list)
    role_mismatches: list[list[str]] = field(default_factory=list)
    relationship_lint_ok: bool | None = None
    relationship_lint_findings: list[dict[str, Any]] = field(default_factory=list)
    error_code: str | None = None
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CriticReview:
    schema_version: str
    artifact_hashes: ArtifactHashes
    validation: ValidationSummary
    deterministic_findings: list[CriticFinding]
    critic_findings: list[CriticFinding]
    merged_findings: list[CriticFinding]
    scorecard: CriticScorecard
    prompt_package: dict[str, Any]
    status: str
    model_identifier: str | None = None
    token_estimate: int | None = None
    elapsed_ms: int | None = None
    handoff_candidates: list[SelfImprovementHandoffCandidate] = field(
        default_factory=list
    )
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "artifact_hashes": self.artifact_hashes.to_dict(),
            "validation": self.validation.to_dict(),
            "deterministic_findings": [f.to_dict() for f in self.deterministic_findings],
            "critic_findings": [f.to_dict() for f in self.critic_findings],
            "merged_findings": [f.to_dict() for f in self.merged_findings],
            "scorecard": self.scorecard.to_dict(),
            "prompt_package": self.prompt_package,
            "status": self.status,
            "model_identifier": self.model_identifier,
            "token_estimate": self.token_estimate,
            "elapsed_ms": self.elapsed_ms,
            "handoff_candidates": [h.to_dict() for h in self.handoff_candidates],
            "errors": list(self.errors),
        }
