"""Source/coverage fidelity using exact node/facet lookup (Round 2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from critic.canonical import (
    IRI_CONTENT_FACET,
    IRI_HASH,
    IRI_HASH_VALUE,
    IRI_HAS_FACET,
    IRI_NAME,
    CanonicalGraphView,
    RuleExecution,
)
from critic.finding_diff import make_stable_finding_id
from critic.models import CriticFinding, CriticTarget

RULE_VERSION = "1.1.0"


def compare_coverage_contract(
    view: CanonicalGraphView,
    contract_path: Path,
    *,
    artifact_hash: str,
) -> tuple[list[CriticFinding], list[RuleExecution]]:
    findings: list[CriticFinding] = []
    executions: list[RuleExecution] = []
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        f = _finding(
            "CRIT-C-CONTRACT-PARSE",
            "high",
            "coverage",
            CriticTarget(path=contract_path.name),
            [type(exc).__name__],
            "Coverage contract could not be parsed.",
            "Provide valid JSON coverage contract.",
            "json.loads coverage_contract_path",
            evidence_kind="source",
        )
        return [f], [
            RuleExecution(
                rule_id="CRIT-C-CONTRACT-PARSE",
                rule_version=RULE_VERSION,
                status="failed",
                input_artifact_hash=artifact_hash,
                finding_ids=[f.finding_id],
                error_code=type(exc).__name__,
            )
        ]

    if not view.usable_for_heuristics:
        return [], [
            RuleExecution(
                rule_id="CRIT-C-COVERAGE",
                rule_version=RULE_VERSION,
                status="skipped",
                input_artifact_hash=artifact_hash,
                error_code="graph_unavailable",
            )
        ]

    # First-class node label coverage (not prose-only)
    required_labels = contract.get("required_artifact_labels") or {}
    missing_labels: list[str] = []
    prose_only: list[str] = []
    examined = 0
    for _group, labels in required_labels.items() if isinstance(required_labels, dict) else []:
        if not isinstance(labels, list):
            continue
        for label in labels:
            examined += 1
            text = str(label)
            if _first_class_label(view, text):
                continue
            if _prose_only_label(view, text):
                prose_only.append(text)
            else:
                missing_labels.append(text)

    for label in missing_labels:
        findings.append(
            _finding(
                "CRIT-C-MISSING-LABEL",
                "medium",
                "coverage",
                CriticTarget(predicate=label),
                [f"missing_label={label}"],
                "Coverage contract requires an artifact label not modeled as a first-class node.",
                f"Ensure {label} is represented as a node name or IRI suffix.",
                "First-class node name/@id match for label.",
                evidence_kind="source",
            )
        )
    for label in prose_only:
        findings.append(
            _finding(
                "CRIT-C-PROSE-ONLY-LABEL",
                "medium",
                "coverage",
                CriticTarget(predicate=label),
                [f"prose_only_label={label}"],
                "Identifier appears only in descriptions, not as a first-class node.",
                f"Promote {label} to a typed node rather than prose mention.",
                "Distinguish description literals from node name/@id.",
                evidence_kind="source",
            )
        )

    case_id = contract.get("case_identifier")
    if isinstance(case_id, str) and case_id:
        examined += 1
        if not _first_class_case_id(view, case_id) and not _any_literal_equals(view, case_id):
            findings.append(
                _finding(
                    "CRIT-C-CASE-ID-MISSING",
                    "high",
                    "source_fidelity",
                    CriticTarget(),
                    [f"case_identifier={case_id}"],
                    "Declared case identifier from coverage contract is absent.",
                    "Include the case identifier on Investigation fields.",
                    "Search node properties for case identifier.",
                    evidence_kind="source",
                )
            )

    min_nodes = contract.get("min_nodes")
    if isinstance(min_nodes, int):
        examined += 1
        count = len(view.top_level_order) or len(view.nodes)
        if count < min_nodes:
            findings.append(
                _finding(
                    "CRIT-C-MIN-NODES",
                    "high",
                    "coverage",
                    CriticTarget(),
                    [f"node_count={count}", f"min_nodes={min_nodes}"],
                    "Graph node count is below the coverage contract minimum.",
                    "Regenerate the full scenario graph.",
                    "Count top-level nodes versus min_nodes.",
                    evidence_kind="source",
                )
            )

    # Phantom Gate-style extras when present
    for phrase in contract.get("required_authorizations") or []:
        examined += 1
        if not _name_contains(view, str(phrase)):
            findings.append(
                _finding(
                    "CRIT-C-MISSING-AUTHORIZATION",
                    "high",
                    "coverage",
                    CriticTarget(predicate=str(phrase)),
                    [f"auth={phrase}"],
                    "Required authorization phrase not found in node names.",
                    "Model the authorization as a first-class Authorization node.",
                    "Search uco-core:name for authorization phrase.",
                    evidence_kind="source",
                )
            )

    for docket in contract.get("required_charging_dockets") or []:
        examined += 1
        if not _any_literal_equals(view, str(docket)):
            findings.append(
                _finding(
                    "CRIT-C-MISSING-DOCKET",
                    "high",
                    "coverage",
                    CriticTarget(predicate=str(docket)),
                    [f"docket={docket}"],
                    "Required charging docket not found as a literal property value.",
                    "Set legalproc:caseIdentifier (or equivalent) on the Investigation.",
                    "Exact literal match for docket identifier.",
                    evidence_kind="source",
                )
            )

    grouping = contract.get("required_grouping")
    if isinstance(grouping, str) and grouping:
        examined += 1
        if not _name_contains(view, grouping):
            findings.append(
                _finding(
                    "CRIT-C-MISSING-GROUPING",
                    "medium",
                    "coverage",
                    CriticTarget(predicate=grouping),
                    [f"grouping={grouping}"],
                    "Required grouping name not found.",
                    "Include the grouping Investigation/name.",
                    "Search uco-core:name for grouping phrase.",
                    evidence_kind="source",
                )
            )

    executions.append(
        RuleExecution(
            rule_id="CRIT-C-COVERAGE",
            rule_version=RULE_VERSION,
            status="evaluated",
            input_artifact_hash=artifact_hash,
            targets_examined=examined,
            finding_ids=[f.finding_id for f in findings],
        )
    )
    return findings, executions


def check_source_document_hash(
    view: CanonicalGraphView,
    *,
    source_name: str,
    expected_sha256: str,
    artifact_hash: str,
) -> tuple[list[CriticFinding], list[RuleExecution]]:
    """Compare expected file hash to the named source document's ContentDataFacet."""

    findings: list[CriticFinding] = []
    if not view.usable_for_heuristics:
        return [], [
            RuleExecution(
                rule_id="CRIT-C-SOURCE-HASH",
                rule_version=RULE_VERSION,
                status="skipped",
                input_artifact_hash=artifact_hash,
                error_code="graph_unavailable",
            )
        ]

    matched_node = None
    for node in view.iter_nodes():
        names = node.literals(IRI_NAME)
        if source_name in names or any(source_name in n for n in names):
            matched_node = node
            break
    if matched_node is None:
        f = _finding(
            "CRIT-C-SOURCE-NODE-MISSING",
            "high",
            "source_fidelity",
            CriticTarget(path=source_name),
            [f"source_name={source_name}"],
            "Source document node with matching name was not found.",
            "Add an ObservableObject named after the source file with ContentDataFacet hash.",
            "Find node where uco-core:name equals source file name.",
            evidence_kind="source",
        )
        return [f], [
            RuleExecution(
                rule_id="CRIT-C-SOURCE-HASH",
                rule_version=RULE_VERSION,
                status="evaluated",
                input_artifact_hash=artifact_hash,
                targets_examined=0,
                finding_ids=[f.finding_id],
            )
        ]

    graph_hash = _facet_hash_for_node(view, matched_node.iri)
    if graph_hash is None:
        f = _finding(
            "CRIT-C-SOURCE-HASH-MISSING",
            "high",
            "source_fidelity",
            CriticTarget(node_id=matched_node.iri, path=source_name),
            ["no ContentDataFacet hash"],
            "Source document node lacks a ContentDataFacet hash value.",
            "Attach ContentDataFacet with SHA-256 hash of the source file.",
            "Traverse hasFacet → ContentDataFacet → hash → hashValue.",
            evidence_kind="source",
        )
        return [f], [
            RuleExecution(
                rule_id="CRIT-C-SOURCE-HASH",
                rule_version=RULE_VERSION,
                status="evaluated",
                input_artifact_hash=artifact_hash,
                targets_examined=1,
                finding_ids=[f.finding_id],
            )
        ]

    if graph_hash.lower() != expected_sha256.lower():
        f = _finding(
            "CRIT-C-SOURCE-HASH-MISMATCH",
            "high",
            "source_fidelity",
            CriticTarget(node_id=matched_node.iri, path=source_name),
            [f"file_sha256={expected_sha256}", f"graph_sha256={graph_hash}"],
            "Embedded source ContentDataFacet hash does not match the source file.",
            "Update the embedded hash to match sha256(source file).",
            "Compare ContentDataFacet hashValue to sha256_file(source).",
            evidence_kind="source",
        )
        return [f], [
            RuleExecution(
                rule_id="CRIT-C-SOURCE-HASH",
                rule_version=RULE_VERSION,
                status="evaluated",
                input_artifact_hash=artifact_hash,
                targets_examined=1,
                finding_ids=[f.finding_id],
            )
        ]

    return [], [
        RuleExecution(
            rule_id="CRIT-C-SOURCE-HASH",
            rule_version=RULE_VERSION,
            status="evaluated",
            input_artifact_hash=artifact_hash,
            targets_examined=1,
            finding_ids=[],
        )
    ]


def _facet_hash_for_node(view: CanonicalGraphView, node_iri: str) -> str | None:
    node = view.get(node_iri)
    if not node:
        return None
    # Inline facets in raw JSON (Phantom Gate style)
    if node.raw_json:
        for facet in node.raw_json.get("uco-core:hasFacet") or []:
            if not isinstance(facet, dict):
                continue
            types = facet.get("@type")
            type_list = types if isinstance(types, list) else [types]
            if "uco-observable:ContentDataFacet" not in type_list and not any(
                t and "ContentDataFacet" in str(t) for t in type_list
            ):
                continue
            for h in facet.get("uco-observable:hash") or []:
                if not isinstance(h, dict):
                    continue
                val = h.get("uco-types:hashValue")
                if isinstance(val, dict):
                    val = val.get("@value")
                if isinstance(val, str) and len(val) == 64:
                    return val
    # Linked facets
    for facet_iri in node.refs(IRI_HAS_FACET):
        facet = view.get(facet_iri)
        if not facet or not facet.has_type(IRI_CONTENT_FACET):
            continue
        for href in facet.refs(IRI_HASH):
            hnode = view.get(href)
            if not hnode:
                continue
            lits = hnode.literals(IRI_HASH_VALUE)
            if lits:
                return lits[0]
        lits = facet.literals(IRI_HASH_VALUE)
        if lits:
            return lits[0]
    return None


def _first_class_label(view: CanonicalGraphView, label: str) -> bool:
    for node in view.iter_nodes():
        if node.iri.endswith(f"/{label}") or node.iri.endswith(label):
            return True
        if any(label == n or label in n for n in node.literals(IRI_NAME)):
            # Prefer exact/name containment on name property only
            if any(label == n or n.startswith(label) or f" {label}" in f" {n}" for n in node.literals(IRI_NAME)):
                return True
    return False


def _prose_only_label(view: CanonicalGraphView, label: str) -> bool:
    """True when label appears in a non-name description-like literal only."""

    desc_iris = {
        "https://ontology.unifiedcyberontology.org/uco/core/description",
        "https://ontology.unifiedcyberontology.org/uco/core/tag",
    }
    found_prose = False
    for node in view.iter_nodes():
        for prop, values in node.properties.items():
            for value in values:
                if value.literal and label in value.literal:
                    if prop in desc_iris or prop.endswith("description"):
                        found_prose = True
                    elif prop == IRI_NAME or prop.endswith("name"):
                        return False
    return found_prose


def _name_contains(view: CanonicalGraphView, phrase: str) -> bool:
    return any(phrase in n for node in view.iter_nodes() for n in node.literals(IRI_NAME))


def _any_literal_equals(view: CanonicalGraphView, text: str) -> bool:
    for node in view.iter_nodes():
        for values in node.properties.values():
            for value in values:
                if value.literal == text:
                    return True
    return False


def _first_class_case_id(view: CanonicalGraphView, case_id: str) -> bool:
    return _any_literal_equals(view, case_id) or _name_contains(view, case_id)


def _finding(
    rule_id: str,
    severity: str,
    category: str,
    target: CriticTarget,
    evidence: list[str],
    rationale: str,
    recommended_change: str,
    verification_method: str,
    *,
    evidence_kind: str = "source",
) -> CriticFinding:
    finding_id = make_stable_finding_id(rule_id, *target.semantic_parts(), *evidence[:1])
    # Keep identity semantic: rule + target primarily
    finding_id = make_stable_finding_id(rule_id, *target.semantic_parts())
    return CriticFinding(
        finding_id=finding_id,
        severity=severity,  # type: ignore[arg-type]
        category=category,
        confidence=0.9,
        status="new",
        target=target,
        evidence_kind=evidence_kind,  # type: ignore[arg-type]
        evidence=evidence,
        rationale=rationale,
        recommended_change=recommended_change,
        verification_method=verification_method,
        rule_id=rule_id,
        identity_key=finding_id,
    )
