"""Deterministic structural modeling heuristics using CanonicalGraphView."""

from __future__ import annotations

from collections import Counter
from typing import Callable

from critic.canonical import (
    IRI_ACTION_OBJECT,
    IRI_ACTION_RESULT,
    IRI_DICT,
    IRI_DICT_ENTRY_PROP,
    IRI_FILE,
    IRI_INVESTIGATION,
    IRI_INVESTIGATIVE_ACTION,
    IRI_KIND,
    IRI_NAME,
    IRI_OBJECT,
    IRI_OBSERVABLE,
    IRI_PERSON,
    IRI_RELATIONSHIP,
    IRI_RELEVANT_AUTH,
    IRI_SOURCE,
    IRI_TARGET,
    CanonicalGraphView,
    RuleExecution,
)
from critic.finding_diff import make_stable_finding_id
from critic.models import CriticFinding, CriticTarget

RULE_VERSION = "1.1.0"


def run_graph_heuristics(
    view: CanonicalGraphView,
    *,
    artifact_hash: str,
) -> tuple[list[CriticFinding], list[RuleExecution]]:
    findings: list[CriticFinding] = []
    executions: list[RuleExecution] = []
    if not view.usable_for_heuristics:
        for rule_id in _ALL_RULE_IDS:
            executions.append(
                RuleExecution(
                    rule_id=rule_id,
                    rule_version=RULE_VERSION,
                    status="skipped",
                    input_artifact_hash=artifact_hash,
                    error_code="graph_heuristics_unavailable",
                )
            )
        return findings, executions

    runners: list[tuple[str, Callable[..., tuple[list[CriticFinding], int]]]] = [
        ("CRIT-H-INV-NO-OBJECT", _investigation_without_object),
        ("CRIT-H-AUTH-NON-INVESTIGATION", _relevant_authorization_misuse),
        ("CRIT-H-ACQ-INPUT-RESULT-INVERSION", _acquisition_input_result_inversion),
        ("CRIT-H-RELATED-TO-OVERUSE", _generic_related_to_overuse),
        ("CRIT-H-CHARGED-WITH-REVERSED", _charged_with_direction),
        ("CRIT-H-DICT-ENTRY-COLLISION", _dictionary_entry_collisions),
        ("CRIT-H-FACET-PROPS-ON-OBSERVABLE", _facet_like_props_on_observable),
    ]
    for rule_id, runner in runners:
        try:
            rule_findings, examined = runner(view)
            for finding in rule_findings:
                finding.ensure_identity_key()
            findings.extend(rule_findings)
            executions.append(
                RuleExecution(
                    rule_id=rule_id,
                    rule_version=RULE_VERSION,
                    status="evaluated",
                    input_artifact_hash=artifact_hash,
                    targets_examined=examined,
                    finding_ids=[f.finding_id for f in rule_findings],
                )
            )
        except Exception as exc:  # noqa: BLE001
            executions.append(
                RuleExecution(
                    rule_id=rule_id,
                    rule_version=RULE_VERSION,
                    status="failed",
                    input_artifact_hash=artifact_hash,
                    error_code=type(exc).__name__,
                )
            )
    return findings, executions


_ALL_RULE_IDS = [
    "CRIT-H-INV-NO-OBJECT",
    "CRIT-H-AUTH-NON-INVESTIGATION",
    "CRIT-H-ACQ-INPUT-RESULT-INVERSION",
    "CRIT-H-RELATED-TO-OVERUSE",
    "CRIT-H-CHARGED-WITH-REVERSED",
    "CRIT-H-DICT-ENTRY-COLLISION",
    "CRIT-H-FACET-PROPS-ON-OBSERVABLE",
]


def _finding(
    *,
    rule_id: str,
    severity: str,
    category: str,
    target: CriticTarget,
    evidence: list[str],
    rationale: str,
    recommended_change: str,
    verification_method: str,
    confidence: float = 0.9,
) -> CriticFinding:
    finding_id = make_stable_finding_id(rule_id, *target.semantic_parts())
    return CriticFinding(
        finding_id=finding_id,
        severity=severity,  # type: ignore[arg-type]
        category=category,
        confidence=confidence,
        status="new",
        target=target,
        evidence_kind="deterministic",
        evidence=evidence,
        rationale=rationale,
        recommended_change=recommended_change,
        verification_method=verification_method,
        rule_id=rule_id,
        identity_key=finding_id,
    )


def _investigation_without_object(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_INVESTIGATION):
            continue
        examined += 1
        if node.refs(IRI_OBJECT):
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-INV-NO-OBJECT",
                severity="high",
                category="investigation_structure",
                target=CriticTarget(
                    node_id=node.iri,
                    predicate=IRI_OBJECT,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=["Investigation present without uco-core:object"],
                rationale=(
                    "An Investigation container is present but does not reference "
                    "contained objects via uco-core:object."
                ),
                recommended_change=(
                    "Attach evidence, actions, and related objects with uco-core:object."
                ),
                verification_method="CanonicalGraphView: Investigation.refs(object).",
            )
        )
    return findings, examined


def _relevant_authorization_misuse(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.values(IRI_RELEVANT_AUTH):
            continue
        examined += 1
        if node.has_type(IRI_INVESTIGATION):
            continue
        # Authorization nodes may carry the property in some patterns — skip
        if any("Authorization" in t for t in node.types):
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-AUTH-NON-INVESTIGATION",
                severity="high",
                category="authorization",
                target=CriticTarget(
                    node_id=node.iri,
                    predicate=IRI_RELEVANT_AUTH,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=[f"types={sorted(node.types)}"],
                rationale=(
                    "case-investigation:relevantAuthorization is attached to a "
                    "non-Investigation node."
                ),
                recommended_change=(
                    "Move relevantAuthorization to the Investigation (use Authorized_By "
                    "for actions)."
                ),
                verification_method=(
                    "CanonicalGraphView values(case-investigation:relevantAuthorization)."
                ),
            )
        )
    return findings, examined


def _acquisition_input_result_inversion(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_INVESTIGATIVE_ACTION) and not any(
            "Action" in t for t in node.types
        ):
            continue
        names = " ".join(node.literals(IRI_NAME)).lower()
        if "acquir" not in names and "image" not in names and "extract" not in names:
            continue
        examined += 1
        if node.refs(IRI_ACTION_RESULT):
            continue
        for ref in node.refs(IRI_ACTION_OBJECT):
            target = view.get(ref)
            if target and target.has_type(IRI_FILE, IRI_OBSERVABLE):
                findings.append(
                    _finding(
                        rule_id="CRIT-H-ACQ-INPUT-RESULT-INVERSION",
                        severity="high",
                        category="action_grammar",
                        target=CriticTarget(
                            node_id=node.iri,
                            predicate=IRI_ACTION_RESULT,
                            counterpart_id=ref,
                            json_pointer=node.location.json_pointer,
                            path=node.location.path,
                        ),
                        evidence=[f"likely_result_only_as_input={ref}"],
                        rationale=(
                            "Acquisition-like action lists a file/image only as input "
                            "and has no result — often an input/result inversion."
                        ),
                        recommended_change=(
                            "Place the acquired image/artifact on uco-action:result."
                        ),
                        verification_method="Check InvestigativeAction object/result roles.",
                    )
                )
                break
    return findings, examined


def _generic_related_to_overuse(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    kinds: list[str] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        examined += 1
        for lit in node.literals(IRI_KIND):
            kinds.append(lit)
        # Also accept IRI-typed kinds as last path segment
        for ref in node.refs(IRI_KIND):
            kinds.append(ref.rsplit("/", 1)[-1])
    if not kinds:
        return [], examined
    counts = Counter(kinds)
    related = counts.get("Related_To", 0)
    if related >= 5 or (related >= 3 and related / max(len(kinds), 1) >= 0.5):
        return [
            _finding(
                rule_id="CRIT-H-RELATED-TO-OVERUSE",
                severity="medium",
                category="generic_relationship",
                target=CriticTarget(predicate=IRI_KIND),
                evidence=[
                    f"Related_To_count={related}",
                    f"relationship_count={len(kinds)}",
                ],
                rationale=(
                    "Many relationships use generic Related_To when a governed "
                    "vocabulary member may be available."
                ),
                recommended_change="Prefer specific relationship kinds from the registry.",
                verification_method="Count kindOfRelationship == Related_To.",
            )
        ], examined
    return [], examined


def _charged_with_direction(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        kinds = set(node.literals(IRI_KIND))
        kinds.update(r.rsplit("/", 1)[-1] for r in node.refs(IRI_KIND))
        if "Charged_With" not in kinds:
            continue
        examined += 1
        source_refs = node.refs(IRI_SOURCE)
        target_refs = node.refs(IRI_TARGET)
        if not source_refs or not target_refs:
            continue
        source_node = view.get(source_refs[0])
        target_node = view.get(target_refs[0])
        if not source_node or not target_node:
            continue
        source_is_charge = any("Charge" in t for t in source_node.types) or any(
            "Charge" in lit for lit in source_node.literals(
                "https://ontology.unifiedcyberontology.org/uco/core/tag"
            )
        ) or any(
            "charge" in lit.lower() for lit in source_node.literals(IRI_NAME)
        )
        target_is_charge = any("Charge" in t for t in target_node.types) or any(
            "Charge" in lit for lit in target_node.literals(
                "https://ontology.unifiedcyberontology.org/uco/core/tag"
            )
        ) or any(
            "charge" in lit.lower() for lit in target_node.literals(IRI_NAME)
        )
        target_is_person = target_node.has_type(IRI_PERSON) or any(
            "Person" in t or "Identity" in t for t in target_node.types
        )
        source_is_person = source_node.has_type(IRI_PERSON) or any(
            "Person" in t or "Identity" in t for t in source_node.types
        )
        if source_is_charge and target_is_person:
            findings.append(
                _finding(
                    rule_id="CRIT-H-CHARGED-WITH-REVERSED",
                    severity="high",
                    category="relationship_direction",
                    target=CriticTarget(
                        node_id=node.iri,
                        predicate=IRI_KIND,
                        counterpart_id=f"{source_refs[0]}->{target_refs[0]}",
                        json_pointer=node.location.json_pointer,
                        path=node.location.path,
                    ),
                    evidence=[
                        f"source={source_refs[0]}",
                        f"target={target_refs[0]}",
                    ],
                    rationale=(
                        "Charged_With is modeled person→charge; this edge is charge→person."
                    ),
                    recommended_change="Reverse source and target.",
                    verification_method=(
                        "CanonicalGraphView: Relationship source Person, target Charge."
                    ),
                )
            )
    return findings, examined


def _dictionary_entry_collisions(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    parents: dict[str, set[str]] = {}
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_DICT):
            continue
        examined += 1
        for ref in node.refs(IRI_DICT_ENTRY_PROP):
            parents.setdefault(ref, set()).add(node.iri)
    findings: list[CriticFinding] = []
    for entry_id, parent_ids in parents.items():
        if len(parent_ids) < 2:
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-DICT-ENTRY-COLLISION",
                severity="high",
                category="dictionary_collision",
                target=CriticTarget(node_id=entry_id),
                evidence=[f"parents={sorted(parent_ids)}"],
                rationale="Dictionary entry IRI is referenced by multiple Dictionary parents.",
                recommended_change="Mint parent-scoped entry IRIs.",
                verification_method="Group dictionary entry refs by @id.",
            )
        )
    return findings, examined


def _facet_like_props_on_observable(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    facet_props = {
        "https://ontology.unifiedcyberontology.org/uco/observable/serviceName",
        "https://ontology.unifiedcyberontology.org/uco/observable/serviceType",
        "https://ontology.unifiedcyberontology.org/uco/observable/fileName",
        "https://ontology.unifiedcyberontology.org/uco/observable/sizeInBytes",
    }
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_OBSERVABLE):
            continue
        if any("Facet" in t for t in node.types):
            continue
        examined += 1
        bad = [p for p in facet_props if node.values(p)]
        if not bad:
            continue
        has_facet = bool(
            node.refs("https://ontology.unifiedcyberontology.org/uco/core/hasFacet")
        )
        findings.append(
            _finding(
                rule_id="CRIT-H-FACET-PROPS-ON-OBSERVABLE",
                severity="medium" if has_facet else "high",
                category="facet_placement",
                target=CriticTarget(
                    node_id=node.iri,
                    predicate=bad[0],
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=bad,
                rationale=(
                    "Facet-scoped properties appear directly on ObservableObject."
                ),
                recommended_change="Move properties onto Facet instances via hasFacet.",
                verification_method="Canonical property presence on ObservableObject.",
            )
        )
    return findings, examined
