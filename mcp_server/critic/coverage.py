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

RULE_VERSION = "1.3.1"


def _exec(
    rule_id: str,
    status: str,
    artifact_hash: str,
    finding_ids: list[str],
    *,
    examined: int = 0,
    error: str | None = None,
    required: bool = True,
) -> RuleExecution:
    return RuleExecution(
        rule_id=rule_id,
        rule_version=RULE_VERSION,
        status=status,  # type: ignore[arg-type]
        input_artifact_hash=artifact_hash,
        targets_examined=examined,
        finding_ids=finding_ids,
        error_code=error,
        required_for_scope=required,
        verifies_rule_ids=[rule_id],
    )


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
            _exec(
                "CRIT-C-CONTRACT-PARSE",
                "failed",
                artifact_hash,
                [f.finding_id],
                error=type(exc).__name__,
            )
        ]

    if not view.usable_for_heuristics:
        return [], _skipped_coverage_executions(contract, artifact_hash)

    # First-class node label coverage (not prose-only)
    required_labels = contract.get("required_artifact_labels") or {}
    missing_labels: list[str] = []
    prose_only: list[str] = []
    label_examined = 0
    for _group, labels in required_labels.items() if isinstance(required_labels, dict) else []:
        if not isinstance(labels, list):
            continue
        for label in labels:
            label_examined += 1
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

    if isinstance(required_labels, dict) and required_labels:
        executions.append(
            _exec(
                "CRIT-C-MISSING-LABEL",
                "evaluated",
                artifact_hash,
                [f.finding_id for f in findings if f.rule_id == "CRIT-C-MISSING-LABEL"],
                examined=label_examined,
            )
        )
        executions.append(
            _exec(
                "CRIT-C-PROSE-ONLY-LABEL",
                "evaluated",
                artifact_hash,
                [f.finding_id for f in findings if f.rule_id == "CRIT-C-PROSE-ONLY-LABEL"],
                examined=label_examined,
            )
        )

    case_id = contract.get("case_identifier")
    if isinstance(case_id, str) and case_id:
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
        executions.append(
            _exec(
                "CRIT-C-CASE-ID-MISSING",
                "evaluated",
                artifact_hash,
                [f.finding_id for f in findings if f.rule_id == "CRIT-C-CASE-ID-MISSING"],
                examined=1,
            )
        )

    min_nodes = contract.get("min_nodes")
    if isinstance(min_nodes, int):
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
        executions.append(
            _exec(
                "CRIT-C-MIN-NODES",
                "evaluated",
                artifact_hash,
                [f.finding_id for f in findings if f.rule_id == "CRIT-C-MIN-NODES"],
                examined=1,
            )
        )

    # Phantom Gate-style extras when present
    auth_phrases = contract.get("required_authorizations") or []
    auth_examined = 0
    for phrase in auth_phrases:
        auth_examined += 1
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
    if auth_phrases:
        executions.append(
            _exec(
                "CRIT-C-MISSING-AUTHORIZATION",
                "evaluated",
                artifact_hash,
                [
                    f.finding_id
                    for f in findings
                    if f.rule_id == "CRIT-C-MISSING-AUTHORIZATION"
                ],
                examined=auth_examined,
            )
        )

    dockets = contract.get("required_charging_dockets") or []
    docket_examined = 0
    for docket in dockets:
        docket_examined += 1
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
    if dockets:
        executions.append(
            _exec(
                "CRIT-C-MISSING-DOCKET",
                "evaluated",
                artifact_hash,
                [f.finding_id for f in findings if f.rule_id == "CRIT-C-MISSING-DOCKET"],
                examined=docket_examined,
            )
        )

    grouping = contract.get("required_grouping")
    if isinstance(grouping, str) and grouping:
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
            _exec(
                "CRIT-C-MISSING-GROUPING",
                "evaluated",
                artifact_hash,
                [f.finding_id for f in findings if f.rule_id == "CRIT-C-MISSING-GROUPING"],
                examined=1,
            )
        )

    return findings, executions


def _skipped_coverage_executions(
    contract: dict[str, Any], artifact_hash: str
) -> list[RuleExecution]:
    """Emit per-rule skipped executions when the graph is unavailable."""

    executions: list[RuleExecution] = []
    required_labels = contract.get("required_artifact_labels") or {}
    if isinstance(required_labels, dict) and required_labels:
        for rule_id in ("CRIT-C-MISSING-LABEL", "CRIT-C-PROSE-ONLY-LABEL"):
            executions.append(
                _exec(rule_id, "skipped", artifact_hash, [], error="graph_unavailable")
            )
    if isinstance(contract.get("case_identifier"), str) and contract.get("case_identifier"):
        executions.append(
            _exec(
                "CRIT-C-CASE-ID-MISSING",
                "skipped",
                artifact_hash,
                [],
                error="graph_unavailable",
            )
        )
    if isinstance(contract.get("min_nodes"), int):
        executions.append(
            _exec("CRIT-C-MIN-NODES", "skipped", artifact_hash, [], error="graph_unavailable")
        )
    if contract.get("required_authorizations"):
        executions.append(
            _exec(
                "CRIT-C-MISSING-AUTHORIZATION",
                "skipped",
                artifact_hash,
                [],
                error="graph_unavailable",
            )
        )
    if contract.get("required_charging_dockets"):
        executions.append(
            _exec(
                "CRIT-C-MISSING-DOCKET",
                "skipped",
                artifact_hash,
                [],
                error="graph_unavailable",
            )
        )
    if isinstance(contract.get("required_grouping"), str) and contract.get("required_grouping"):
        executions.append(
            _exec(
                "CRIT-C-MISSING-GROUPING",
                "skipped",
                artifact_hash,
                [],
                error="graph_unavailable",
            )
        )
    if not executions:
        executions.append(
            _exec("CRIT-C-COVERAGE", "skipped", artifact_hash, [], error="graph_unavailable")
        )
    return executions


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
            _exec(
                "CRIT-C-SOURCE-HASH",
                "skipped",
                artifact_hash,
                [],
                error="graph_unavailable",
            )
        ]

    matched_node = None
    for node in view.iter_nodes():
        names = node.literals(IRI_NAME)
        if source_name in names or any(source_name in n for n in names):
            matched_node = node
            break
    if matched_node is None:
        # Builder/recipe/source paths belong in the critic session manifest
        # (ArtifactHashes.source_sha256), not in the domain investigation graph.
        # When the graph does not embed a matching node, treat coverage as
        # not_applicable rather than forcing domain pollution.
        return [], [
            _exec(
                "CRIT-C-SOURCE-HASH",
                "not_applicable",
                artifact_hash,
                [],
                examined=0,
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
            verifier_rule_id="CRIT-C-SOURCE-HASH",
        )
        return [f], [
            _exec(
                "CRIT-C-SOURCE-HASH-MISSING",
                "evaluated",
                artifact_hash,
                [f.finding_id],
                examined=1,
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
            verifier_rule_id="CRIT-C-SOURCE-HASH",
        )
        return [f], [
            _exec(
                "CRIT-C-SOURCE-HASH-MISMATCH",
                "evaluated",
                artifact_hash,
                [f.finding_id],
                examined=1,
            )
        ]

    return [], [
        _exec("CRIT-C-SOURCE-HASH", "evaluated", artifact_hash, [], examined=1)
    ]


def check_provenance_manifest(
    manifest_path: Path,
    *,
    project_root: Path,
    artifact_hash: str,
    graph_sha256: str | None = None,
) -> tuple[list[CriticFinding], list[RuleExecution]]:
    """Verify builder/recipe/output hashes from a sidecar provenance manifest.

    Domain investigation graphs should not embed builder/recipe implementation
    files. This rule checks the sidecar instead.

    Supports schema 1.1 ``artifacts[]`` entries (preferred) and legacy
    ``builder`` / ``recipe`` / ``output`` objects. Every referenced path is
    resolved through ``workspace_policy.check_read_path``. When a manifest is
    supplied but yields no recognized entries, a high finding is emitted
    (incomplete verification) rather than ``not_applicable``. Exactly one
    ``output_artifact`` is required, and its digest must match ``graph_sha256``
    when that value is provided.
    """

    import hashlib

    import workspace_policy

    findings: list[CriticFinding] = []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        f = _finding(
            "CRIT-C-PROVENANCE-MANIFEST",
            "high",
            "source_fidelity",
            CriticTarget(path=manifest_path.name),
            [type(exc).__name__],
            "Provenance manifest could not be parsed.",
            "Provide a valid JSON build/provenance sidecar.",
            "json.loads provenance_manifest_path",
        )
        return [f], [
            _exec(
                "CRIT-C-PROVENANCE-MANIFEST",
                "failed",
                artifact_hash,
                [f.finding_id],
                error=type(exc).__name__,
            )
        ]

    def _sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    role_aliases = {
        "builder": "builder_source",
        "builder_source": "builder_source",
        "recipe": "modeling_guidance",
        "modeling_guidance": "modeling_guidance",
        "output": "output_artifact",
        "output_artifact": "output_artifact",
        "domain_source": "domain_source",
        "validation_bundle": "validation_bundle",
    }

    entries: list[tuple[str, dict[str, Any]]] = []
    artifacts = payload.get("artifacts")
    if isinstance(artifacts, list):
        for item in artifacts:
            if not isinstance(item, dict):
                continue
            role_raw = str(item.get("role") or "").strip()
            role = role_aliases.get(role_raw, role_raw)
            if role:
                entries.append((role, item))
    if not entries:
        for key, role in (
            ("builder", "builder_source"),
            ("recipe", "modeling_guidance"),
            ("output", "output_artifact"),
        ):
            entry = payload.get(key) or payload.get(role)
            if isinstance(entry, dict):
                entries.append((role, entry))

    examined = 0
    output_entries = 0
    for role, entry in entries:
        rel = entry.get("path")
        expected = entry.get("sha256")
        if not rel or not expected:
            continue
        examined += 1
        if role == "output_artifact":
            output_entries += 1
        try:
            candidate = workspace_policy.check_read_path(
                str(rel)
                if Path(str(rel)).is_absolute()
                else str((project_root / str(rel)).resolve()),
                include_write_roots=True,
            )
        except ValueError:
            findings.append(
                _finding(
                    "CRIT-C-PROVENANCE-MANIFEST-PATH-DENIED",
                    "high",
                    "source_fidelity",
                    CriticTarget(path=str(rel)),
                    [f"role={role}"],
                    f"Provenance manifest path for {role} is outside approved read roots.",
                    "Reference only paths under CASE_UCO_MCP_READ_ROOTS / WRITE_ROOTS.",
                    "workspace_policy.check_read_path for manifest entry",
                )
            )
            continue
        if not candidate.is_file():
            findings.append(
                _finding(
                    "CRIT-C-PROVENANCE-MANIFEST-MISSING",
                    "high",
                    "source_fidelity",
                    CriticTarget(path=str(rel)),
                    [f"role={role}"],
                    f"Provenance manifest path for {role} is missing on disk.",
                    "Update the sidecar path or restore the referenced file.",
                    "Path.exists for manifest entry",
                )
            )
            continue
        actual = _sha(candidate)
        if actual.lower() != str(expected).lower():
            findings.append(
                _finding(
                    "CRIT-C-PROVENANCE-MANIFEST-MISMATCH",
                    "high",
                    "source_fidelity",
                    CriticTarget(path=str(rel)),
                    [
                        f"role={role}",
                        f"manifest_sha256={expected}",
                        f"file_sha256={actual}",
                    ],
                    f"Provenance manifest hash for {role} does not match the file.",
                    "Rebuild the sidecar after changing builder/recipe/output.",
                    "Compare manifest sha256 to sha256(file)",
                )
            )
        if (
            role == "output_artifact"
            and graph_sha256
            and actual.lower() != graph_sha256.lower()
        ):
            findings.append(
                _finding(
                    "CRIT-C-PROVENANCE-MANIFEST-OUTPUT-MISMATCH",
                    "high",
                    "source_fidelity",
                    CriticTarget(path=str(rel)),
                    [
                        f"output_sha256={actual}",
                        f"graph_sha256={graph_sha256}",
                    ],
                    "Manifest output_artifact digest does not match the graph under review.",
                    "Rebuild the graph and refresh the sidecar output hash.",
                    "Compare output_artifact sha256 to ArtifactHashes.graph_sha256",
                )
            )

    if examined == 0:
        f = _finding(
            "CRIT-C-PROVENANCE-MANIFEST-EMPTY",
            "high",
            "source_fidelity",
            CriticTarget(path=manifest_path.name),
            ["recognized_entries=0"],
            "Provenance manifest path was supplied but no recognized artifacts were found.",
            "Include schema-1.1 artifacts[] (or legacy builder/recipe/output) with path+sha256.",
            "Parse artifacts[] / legacy keys",
        )
        findings.append(f)
        return findings, [
            _exec(
                "CRIT-C-PROVENANCE-MANIFEST",
                "failed",
                artifact_hash,
                [x.finding_id for x in findings],
                examined=0,
                error="empty_manifest",
            )
        ]

    if output_entries != 1:
        findings.append(
            _finding(
                "CRIT-C-PROVENANCE-MANIFEST-OUTPUT-COUNT",
                "high",
                "source_fidelity",
                CriticTarget(path=manifest_path.name),
                [f"output_artifact_count={output_entries}"],
                "Provenance manifest must declare exactly one output_artifact.",
                "Keep a single output_artifact entry for the reviewed JSON-LD graph.",
                "Count role=output_artifact entries",
            )
        )

    return findings, [
        _exec(
            "CRIT-C-PROVENANCE-MANIFEST",
            "evaluated",
            artifact_hash,
            [f.finding_id for f in findings],
            examined=examined,
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
    verifier_rule_id: str | None = None,
) -> CriticFinding:
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
        verifier_rule_id=verifier_rule_id or rule_id,
        rule_version=RULE_VERSION,
        identity_key=finding_id,
    )
