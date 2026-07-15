"""Deterministic structural modeling heuristics using CanonicalGraphView."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Callable

from critic.canonical import (
    IRI_ACCOUNT,
    IRI_ACTION_OBJECT,
    IRI_ACTION_RESULT,
    IRI_CONTENT_FACET,
    IRI_CONTEXTUAL_COMPILATION,
    IRI_DICT,
    IRI_DICT_ENTRY_PROP,
    IRI_FILE,
    IRI_HASH,
    IRI_HASH_VALUE,
    IRI_HAS_FACET,
    IRI_IMAGE,
    IRI_INSTRUMENT,
    IRI_INVESTIGATION,
    IRI_INVESTIGATIVE_ACTION,
    IRI_KIND,
    IRI_NAME,
    IRI_OBJECT,
    IRI_OBJECT_MARKING,
    IRI_OBSERVABLE,
    IRI_PERFORMER,
    IRI_PERSON,
    IRI_PROVENANCE_RECORD,
    IRI_RASTER,
    IRI_RELATIONSHIP,
    IRI_RELEVANT_AUTH,
    IRI_ROLE,
    IRI_SOURCE,
    IRI_TAG,
    IRI_TARGET,
    CanonicalGraphView,
    CanonicalNode,
    RuleExecution,
)
from critic.finding_diff import make_stable_finding_id
from critic.models import CriticFinding, CriticTarget

RULE_VERSION = "1.3.2"

_ACTION_NAME_TOKENS = ("acquir", "extract", "analy", "hash", "image", "export")
_ACQUISITION_NAME_TOKENS = ("acquir", "extract", "image", "export")
_CUSTODY_NAME_TOKENS = ("custody", "transfer", "release", "receipt")
_FORENSIC_IMAGE_TOKENS = ("e01", "dd", "ufed", "raw image", ".raw", "aff4", "ewf")
_LINK_KINDS = frozenset({
    "Contained_Within",
    "Extracted_From",
    "Parent_Of",
    "Moved_To",
    "Moved_From",
    "Copied_To",
    "Copied_From",
    "Renamed_To",
    "Renamed_From",
})
_PROVENANCE_KINDS = frozenset({"Extracted_From", "Created_By", "Contained_Within"})
_DERIVED_KINDS = frozenset({"Extracted_From", "Contained_Within"})


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
        ("CRIT-H-ACTION-COMPLETENESS", _action_profile_completeness),
        ("CRIT-H-IDENTITY-CONFLATION", _person_account_role_conflation),
        ("CRIT-H-PROXY-DUPLICATE", _proxy_duplicate_artifacts),
        ("CRIT-H-DERIVED-NO-HASH", _derived_without_hash),
        ("CRIT-H-DERIVED-NO-PROVENANCE", _derived_without_provenance),
        ("CRIT-H-MARKING-INHERITANCE", _marking_inheritance_gap),
        ("CRIT-H-CUSTODY-UNPAIRED", _custody_release_unpaired),
        ("CRIT-H-IMAGE-CONTAINER-MISMATCH", _physical_logical_image_mismatch),
        ("CRIT-H-CONTEXTUAL-COMPILATION-OMISSION", _final_artifact_not_in_compilation),
        ("CRIT-H-ACTION-ROLE-CONTRADICTION", _action_role_contradiction),
        ("CRIT-H-ORPHAN-TOP-LEVEL", _orphan_top_level_nodes),
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
    "CRIT-H-ACTION-COMPLETENESS",
    "CRIT-H-IDENTITY-CONFLATION",
    "CRIT-H-PROXY-DUPLICATE",
    "CRIT-H-DERIVED-NO-HASH",
    "CRIT-H-DERIVED-NO-PROVENANCE",
    "CRIT-H-MARKING-INHERITANCE",
    "CRIT-H-CUSTODY-UNPAIRED",
    "CRIT-H-IMAGE-CONTAINER-MISMATCH",
    "CRIT-H-CONTEXTUAL-COMPILATION-OMISSION",
    "CRIT-H-ACTION-ROLE-CONTRADICTION",
    "CRIT-H-ORPHAN-TOP-LEVEL",
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
        rule_version=RULE_VERSION,
        verifier_rule_id=rule_id,
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
            "Charge" in lit for lit in source_node.literals(IRI_TAG)
        ) or any(
            "charge" in lit.lower() for lit in source_node.literals(IRI_NAME)
        )
        target_is_person = target_node.has_type(IRI_PERSON) or any(
            "Person" in t or "Identity" in t for t in target_node.types
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
        has_facet = bool(node.refs(IRI_HAS_FACET))
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


def _action_profile_completeness(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not _is_action_node(node):
            continue
        names = " ".join(node.literals(IRI_NAME)).lower()
        if not names or not any(tok in names for tok in _ACTION_NAME_TOKENS):
            continue
        examined += 1
        has_actor = bool(node.refs(IRI_PERFORMER) or node.refs(IRI_INSTRUMENT))
        has_object = bool(node.refs(IRI_ACTION_OBJECT))
        has_result = bool(node.refs(IRI_ACTION_RESULT))
        acquisition_like = any(tok in names for tok in _ACQUISITION_NAME_TOKENS)
        missing: list[str] = []
        if not has_actor:
            missing.append("performer|instrument")
        if not has_object:
            missing.append("object")
        if acquisition_like and not has_result:
            missing.append("result")
        if not missing:
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-ACTION-COMPLETENESS",
                severity="high" if acquisition_like else "medium",
                category="action_grammar",
                target=CriticTarget(
                    node_id=node.iri,
                    predicate=IRI_ACTION_OBJECT if "object" in missing else IRI_ACTION_RESULT,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=[f"missing={missing}", f"name={names}"],
                rationale=(
                    "Action profile roles are incomplete for an acquisition/analysis/"
                    "hash/export-like InvestigativeAction."
                ),
                recommended_change=(
                    "Add performer or instrument, action object, and (for acquisition-"
                    "like actions) result."
                ),
                verification_method=(
                    "CanonicalGraphView: performer/instrument + object (+ result)."
                ),
            )
        )
    return findings, examined


def _person_account_role_conflation(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_PERSON):
            continue
        examined += 1
        accountish = node.has_type(IRI_ACCOUNT) or any(
            t == IRI_ROLE or t.endswith("/Role") or t.endswith("Account")
            for t in node.types
        )
        if not accountish:
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-IDENTITY-CONFLATION",
                severity="high",
                category="identity_conflation",
                target=CriticTarget(
                    node_id=node.iri,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=[f"types={sorted(node.types)}"],
                rationale=(
                    "A Person node is also typed as Account/Role; person and "
                    "account/role identities should remain distinct."
                ),
                recommended_change=(
                    "Split Person from Account/Role and relate them with a governed kind."
                ),
                verification_method="CanonicalNode types intersect Person and Account/Role.",
            )
        )
    return findings, examined


def _proxy_duplicate_artifacts(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    by_hash: dict[str, list[str]] = defaultdict(list)
    examined = 0
    for node in view.iter_nodes():
        if not node.has_type(IRI_FILE, IRI_OBSERVABLE):
            continue
        if any("Facet" in t for t in node.types):
            continue
        hashes = _node_hash_values(view, node)
        if not hashes:
            continue
        examined += 1
        for hv in hashes:
            by_hash[hv.lower()].append(node.iri)
    linked = _linked_pairs(view, _LINK_KINDS)
    linked |= _action_co_referenced_pairs(view)
    findings: list[CriticFinding] = []
    for hv, iris in by_hash.items():
        unique = sorted(set(iris))
        if len(unique) < 2:
            continue
        for i, left in enumerate(unique):
            for right in unique[i + 1 :]:
                pair = frozenset({left, right})
                if pair in linked:
                    continue
                findings.append(
                    _finding(
                        rule_id="CRIT-H-PROXY-DUPLICATE",
                        severity="high",
                        category="provenance",
                        target=CriticTarget(
                            node_id=left,
                            counterpart_id=right,
                            predicate=IRI_HASH_VALUE,
                        ),
                        evidence=[f"hashValue={hv}"],
                        rationale=(
                            "Distinct File/Observable IRIs share the same ContentDataFacet "
                            "hashValue without Contained_Within/Extracted_From/Parent_Of "
                            "or a shared Action object/result/instrument link."
                        ),
                        recommended_change=(
                            "Link proxies with a governed containment/extraction relationship, "
                            "connect them via the install/move Action that relates the "
                            "instances, or collapse duplicate nodes."
                        ),
                        verification_method=(
                            "Group ContentDataFacet hashValue; check link kinds and "
                            "shared Action endpoints."
                        ),
                    )
                )
    return findings, examined


def _derived_without_hash(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    """Flag derived artifacts lacking digests.

    Forensic acquisition results without a digest remain high-severity.
    CTI-style contained/extracted artifacts that are otherwise identifiable
    (name/filename + inbound Contained_Within/Extracted_From) degrade to
    medium completeness warnings so builders are not forced to invent hashes
    or weaken source-faithful containment relationships.
    """
    derived = _derived_file_iris(view)
    inbound_prov = _inbound_provenance_targets(view)
    findings: list[CriticFinding] = []
    examined = 0
    for iri in sorted(derived):
        node = view.get(iri)
        if not node:
            continue
        examined += 1
        if _node_hash_values(view, node):
            continue
        identifiable = _node_has_accountable_identity(node)
        has_provenance = iri in inbound_prov
        tags = {t.lower() for t in node.literals(IRI_TAG)}
        hash_not_published = "hash-status:not-published" in tags or (
            "source-bytes:not-acquired" in tags
        )
        if (identifiable and has_provenance) or hash_not_published:
            evidence = [
                "derived_without_ContentDataFacet_hashValue",
            ]
            if identifiable:
                evidence.append("accountable_identity_present")
            if has_provenance:
                evidence.append("inbound_containment_or_extraction_present")
            if hash_not_published:
                evidence.append("hash-status:not-published_or_source-bytes:not-acquired")
            findings.append(
                _finding(
                    rule_id="CRIT-H-DERIVED-NO-HASH",
                    severity="medium",
                    category="provenance",
                    target=CriticTarget(
                        node_id=iri,
                        predicate=IRI_HASH_VALUE,
                        json_pointer=node.location.json_pointer,
                        path=node.location.path,
                    ),
                    evidence=evidence,
                    rationale=(
                        "A derived File/Observable lacks a ContentDataFacet hashValue, "
                        "but CTI-accountable identity/containment or an explicit "
                        "hash-status:not-published / source-bytes:not-acquired tag "
                        "explains the gap."
                    ),
                    recommended_change=(
                        "Attach a digest when bytes are available; otherwise keep "
                        "source-faithful Contained_Within/Extracted_From and tag "
                        "hash-status:not-published (do not invent digests)."
                    ),
                    verification_method=(
                        "hashValue absent; identity/provenance or hash-status tag present."
                    ),
                )
            )
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-DERIVED-NO-HASH",
                severity="high",
                category="provenance",
                target=CriticTarget(
                    node_id=iri,
                    predicate=IRI_HASH_VALUE,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=["derived_without_ContentDataFacet_hashValue"],
                rationale=(
                    "A derived File/Observable (action result or Extracted_From target) "
                    "lacks a ContentDataFacet hashValue."
                ),
                recommended_change="Attach ContentDataFacet with hashMethod/hashValue.",
                verification_method="Traverse hasFacet → ContentDataFacet → hash → hashValue.",
            )
        )
    return findings, examined


def _derived_without_provenance(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    derived = _derived_file_iris(view)
    container_members = _container_object_members(view)
    inbound = _inbound_provenance_targets(view)
    findings: list[CriticFinding] = []
    examined = 0
    for iri in sorted(derived):
        node = view.get(iri)
        if not node:
            continue
        examined += 1
        if iri in container_members or iri in inbound:
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-DERIVED-NO-PROVENANCE",
                severity="high",
                category="provenance",
                target=CriticTarget(
                    node_id=iri,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=["no_container_membership_or_inbound_provenance_edge"],
                rationale=(
                    "Derived artifact is not a member of Investigation/ProvenanceRecord/"
                    "ContextualCompilation and has no Extracted_From/Created_By/"
                    "Contained_Within inbound edge."
                ),
                recommended_change=(
                    "Attach the artifact via uco-core:object or add a provenance relationship."
                ),
                verification_method="Container membership + inbound provenance kind scan.",
            )
        )
    return findings, examined


def _marking_inheritance_gap(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    derived_from_source = _derived_source_pairs(view)
    for derived_iri, source_iri in derived_from_source:
        source = view.get(source_iri)
        derived = view.get(derived_iri)
        if not source or not derived:
            continue
        source_marks = source.refs(IRI_OBJECT_MARKING)
        if not source_marks:
            continue
        examined += 1
        if derived.refs(IRI_OBJECT_MARKING):
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-MARKING-INHERITANCE",
                severity="high",
                category="markings",
                target=CriticTarget(
                    node_id=derived_iri,
                    predicate=IRI_OBJECT_MARKING,
                    counterpart_id=source_iri,
                    json_pointer=derived.location.json_pointer,
                    path=derived.location.path,
                ),
                evidence=[f"source_markings={source_marks}"],
                rationale=(
                    "Source object carries objectMarking but a derived Extracted_From/"
                    "action-result node does not inherit markings."
                ),
                recommended_change="Copy or explicitly restate objectMarking on the derived node.",
                verification_method="Compare objectMarking on source vs derived pair.",
            )
        )
    return findings, examined


def _custody_release_unpaired(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    transferred_pairs = _linked_pairs(view, frozenset({"Transferred_To", "Transferred_From"}))
    for node in view.iter_nodes():
        if not _is_action_node(node):
            continue
        names = " ".join(node.literals(IRI_NAME)).lower()
        if not any(tok in names for tok in _CUSTODY_NAME_TOKENS):
            continue
        examined += 1
        has_object = bool(node.refs(IRI_ACTION_OBJECT))
        has_result = bool(node.refs(IRI_ACTION_RESULT))
        endpoints = set(node.refs(IRI_ACTION_OBJECT) + node.refs(IRI_ACTION_RESULT))
        paired = False
        if has_object and has_result:
            paired = True
        else:
            for a in endpoints:
                for b in endpoints:
                    if a != b and frozenset({a, b}) in transferred_pairs:
                        paired = True
                        break
                if paired:
                    break
            # Also accept any Transferred_To involving this action itself
            if not paired:
                for pair in transferred_pairs:
                    if node.iri in pair:
                        paired = True
                        break
        if paired:
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-CUSTODY-UNPAIRED",
                severity="high",
                category="custody",
                target=CriticTarget(
                    node_id=node.iri,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=[f"name={names}", f"has_object={has_object}", f"has_result={has_result}"],
                rationale=(
                    "Custody/transfer/release/receipt action lacks both object and result "
                    "(or a Transferred_To pairing)."
                ),
                recommended_change=(
                    "Set action object and result (custodians/exhibits) or add Transferred_To."
                ),
                verification_method="Custody-named action roles + Transferred_To scan.",
            )
        )
    return findings, examined


def _physical_logical_image_mismatch(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if node.has_type(IRI_RASTER):
            examined += 1
            text = " ".join(
                node.literals(IRI_NAME) + node.literals(IRI_TAG)
            ).lower()
            if any(tok in text for tok in _FORENSIC_IMAGE_TOKENS):
                findings.append(
                    _finding(
                        rule_id="CRIT-H-IMAGE-CONTAINER-MISMATCH",
                        severity="high",
                        category="facet_placement",
                        target=CriticTarget(
                            node_id=node.iri,
                            json_pointer=node.location.json_pointer,
                            path=node.location.path,
                        ),
                        evidence=[f"raster_named_as_forensic_image={text}"],
                        rationale=(
                            "RasterPicture is labeled like a forensic disk/raw image "
                            "(E01/dd/UFED/raw); use Image/File instead of RasterPicture."
                        ),
                        recommended_change="Retype forensic image as Image/File (not RasterPicture).",
                        verification_method="RasterPicture name/tag forensic-image tokens.",
                    )
                )
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        kinds = set(node.literals(IRI_KIND))
        kinds.update(r.rsplit("/", 1)[-1] for r in node.refs(IRI_KIND))
        if "Contained_Within" not in kinds:
            continue
        examined += 1
        for src in node.refs(IRI_SOURCE):
            for tgt in node.refs(IRI_TARGET):
                source_node = view.get(src)
                target_node = view.get(tgt)
                if not source_node or not target_node:
                    continue
                if source_node.has_type(IRI_FILE) and target_node.has_type(IRI_RASTER):
                    findings.append(
                        _finding(
                            rule_id="CRIT-H-IMAGE-CONTAINER-MISMATCH",
                            severity="high",
                            category="facet_placement",
                            target=CriticTarget(
                                node_id=node.iri,
                                predicate=IRI_KIND,
                                counterpart_id=f"{src}->{tgt}",
                                json_pointer=node.location.json_pointer,
                                path=node.location.path,
                            ),
                            evidence=[f"file={src}", f"raster_container={tgt}"],
                            rationale=(
                                "File Contained_Within a RasterPicture — forensic "
                                "containers should be Image/File, not RasterPicture."
                            ),
                            recommended_change="Retype container as Image or File.",
                            verification_method="Contained_Within target typed RasterPicture.",
                        )
                    )
    return findings, examined


def _final_artifact_not_in_compilation(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    members = _container_object_members(view)
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not _is_action_node(node):
            continue
        for result_iri in node.refs(IRI_ACTION_RESULT):
            result = view.get(result_iri)
            if not result or not result.has_type(IRI_FILE, IRI_OBSERVABLE, IRI_IMAGE):
                continue
            if any("Facet" in t for t in result.types):
                continue
            examined += 1
            if result_iri in members:
                continue
            findings.append(
                _finding(
                    rule_id="CRIT-H-CONTEXTUAL-COMPILATION-OMISSION",
                    severity="high",
                    category="investigation_structure",
                    target=CriticTarget(
                        node_id=result_iri,
                        predicate=IRI_OBJECT,
                        counterpart_id=node.iri,
                        json_pointer=result.location.json_pointer,
                        path=result.location.path,
                    ),
                    evidence=[f"action_result_of={node.iri}"],
                    rationale=(
                        "File/Observable action result is not referenced from any "
                        "Investigation/ProvenanceRecord/ContextualCompilation via object."
                    ),
                    recommended_change=(
                        "Add the artifact to Investigation or ProvenanceRecord/"
                        "ContextualCompilation object lists."
                    ),
                    verification_method="Action result membership in container object sets.",
                )
            )
    return findings, examined


def _action_role_contradiction(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    """Flag actions whose name implies a victim/user role but performer is an actor."""

    victim_tokens = (
        "victim",
        "user opens",
        "user open",
        "recipient",
        "target opens",
        "user executes",
        "user execution",
    )
    actor_tokens = (
        "threat-actor",
        "threat actor",
        "operator",
        "apt",
        "adversary",
        "attacker",
    )
    findings: list[CriticFinding] = []
    examined = 0
    for node in view.iter_nodes():
        if not _is_action_node(node):
            continue
        examined += 1
        names = [n.lower() for n in node.literals(IRI_NAME)]
        if not any(any(tok in name for tok in victim_tokens) for name in names):
            continue
        for pref in node.refs(IRI_PERFORMER):
            performer = view.get(pref)
            if not performer:
                continue
            labels = [x.lower() for x in performer.literals(IRI_NAME)]
            tags = [x.lower() for x in performer.literals(IRI_TAG)]
            hay = " ".join(labels + tags)
            if any(tok in hay for tok in actor_tokens):
                findings.append(
                    _finding(
                        rule_id="CRIT-H-ACTION-ROLE-CONTRADICTION",
                        severity="high",
                        category="action_grammar",
                        target=CriticTarget(
                            node_id=node.iri,
                            predicate=IRI_PERFORMER,
                            counterpart_id=pref,
                            json_pointer=node.location.json_pointer,
                            path=node.location.path,
                        ),
                        evidence=[
                            f"action_name={names[0] if names else ''}",
                            f"performer={labels[0] if labels else pref}",
                        ],
                        rationale=(
                            "Action name implies a victim/user execution role, but "
                            "performer is tagged/named as a threat actor/operator."
                        ),
                        recommended_change=(
                            "Omit performer, or assign the victim/user as performer; "
                            "keep the adversary as campaign participant if needed."
                        ),
                        verification_method=(
                            "Action name victim/user tokens vs performer name/tag "
                            "actor tokens."
                        ),
                    )
                )
                break
    return findings, examined


def _orphan_top_level_nodes(
    view: CanonicalGraphView,
) -> tuple[list[CriticFinding], int]:
    """Report top-level @graph nodes not reachable from Investigation/compilation roots."""

    _TOP_LEVEL = re.compile(r"^/@graph/\d+$")
    _IRI_GROUPING = "https://ontology.unifiedcyberontology.org/uco/core/Grouping"
    _IRI_ANNOTATION = "https://ontology.unifiedcyberontology.org/uco/core/Annotation"
    _IRI_EVENT = "https://ontology.unifiedcyberontology.org/uco/core/Event"
    _IRI_EVENT_CONTEXT = (
        "https://ontology.unifiedcyberontology.org/uco/core/eventContext"
    )

    roots = set()
    for node in view.iter_nodes():
        if node.has_type(
            IRI_INVESTIGATION,
            IRI_PROVENANCE_RECORD,
            IRI_CONTEXTUAL_COMPILATION,
            _IRI_GROUPING,
        ):
            roots.add(node.iri)
            roots.update(node.refs(IRI_OBJECT))

    reachable = set(roots)
    changed = True
    while changed:
        changed = False
        before = len(reachable)
        for node in view.iter_nodes():
            if node.has_type(IRI_RELATIONSHIP):
                srcs = set(node.refs(IRI_SOURCE))
                tgts = set(node.refs(IRI_TARGET))
                if (srcs & reachable) or (tgts & reachable):
                    reachable.update(srcs)
                    reachable.update(tgts)
                    reachable.add(node.iri)
            # Expand membership / annotation / event context from reached nodes
            if node.iri in reachable:
                reachable.update(node.refs(IRI_OBJECT))
                reachable.update(node.refs(_IRI_EVENT_CONTEXT))
                if _is_action_node(node):
                    reachable.update(node.refs(IRI_PERFORMER))
                    reachable.update(node.refs(IRI_INSTRUMENT))
                    reachable.update(node.refs(IRI_ACTION_OBJECT))
                    reachable.update(node.refs(IRI_ACTION_RESULT))
            if node.has_type(_IRI_ANNOTATION, _IRI_GROUPING, _IRI_EVENT):
                about = set(node.refs(IRI_OBJECT)) | set(node.refs(_IRI_EVENT_CONTEXT))
                if node.iri in reachable or (about & reachable):
                    reachable.add(node.iri)
                    reachable.update(about)
        if len(reachable) > before:
            changed = True

    findings: list[CriticFinding] = []
    examined = 0
    orphans: list[str] = []
    for node in view.iter_nodes():
        pointer = node.location.json_pointer or ""
        # Nested facet/hash/registry-value expansions are not independent subjects
        if not _TOP_LEVEL.match(pointer):
            continue
        if node.has_type(IRI_RELATIONSHIP):
            continue
        if node.has_type(
            IRI_INVESTIGATION, IRI_PROVENANCE_RECORD, IRI_CONTEXTUAL_COMPILATION
        ):
            continue
        if any("Facet" in t for t in node.types):
            continue
        examined += 1
        if node.iri not in reachable:
            orphans.append(node.iri)

    for iri in orphans[:25]:
        node = view.get(iri)
        if not node:
            continue
        findings.append(
            _finding(
                rule_id="CRIT-H-ORPHAN-TOP-LEVEL",
                severity="medium",
                category="investigation_structure",
                target=CriticTarget(
                    node_id=iri,
                    json_pointer=node.location.json_pointer,
                    path=node.location.path,
                ),
                evidence=[
                    f"orphan_count={len(orphans)}",
                    f"reachable_count={len(reachable)}",
                    f"examined_top_level={examined}",
                ],
                rationale=(
                    "Top-level @graph node is not reachable from any Investigation / "
                    "ProvenanceRecord / ContextualCompilation / Grouping via object "
                    "membership, annotation/event links, or connecting relationships."
                ),
                recommended_change=(
                    "Add a relationship or compilation membership, or nest under a "
                    "contextual compilation that is itself investigation-linked."
                ),
                verification_method=(
                    "BFS from investigation/compilation/grouping roots across object, "
                    "annotation, eventContext, action endpoint, and relationship edges; "
                    "only /@graph/N nodes are examined."
                ),
            )
        )
    return findings, examined


# --- helpers -----------------------------------------------------------------


def _node_has_accountable_identity(node: CanonicalNode) -> bool:
    if node.literals(IRI_NAME):
        return True
    raw = node.raw_json or {}
    for facet in raw.get("uco-core:hasFacet") or []:
        if not isinstance(facet, dict):
            continue
        if facet.get("uco-observable:fileName") or facet.get("uco-observable:filePath"):
            return True
        if facet.get("uco-observable:sizeInBytes") is not None:
            return True
    return False


def _is_action_node(node: CanonicalNode) -> bool:
    return node.has_type(IRI_INVESTIGATIVE_ACTION) or any(
        t.endswith("/Action") or t.endswith("Action") for t in node.types
    )


def _relationship_kinds(node: CanonicalNode) -> set[str]:
    kinds = set(node.literals(IRI_KIND))
    kinds.update(r.rsplit("/", 1)[-1] for r in node.refs(IRI_KIND))
    return kinds


def _linked_pairs(view: CanonicalGraphView, kinds: frozenset[str]) -> set[frozenset[str]]:
    pairs: set[frozenset[str]] = set()
    for node in view.iter_nodes():
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        if not (_relationship_kinds(node) & kinds):
            continue
        for src in node.refs(IRI_SOURCE):
            for tgt in node.refs(IRI_TARGET):
                pairs.add(frozenset({src, tgt}))
    return pairs


def _action_co_referenced_pairs(view: CanonicalGraphView) -> set[frozenset[str]]:
    """Pairs that share object/result/instrument roles on the same Action."""

    pairs: set[frozenset[str]] = set()
    for node in view.iter_nodes():
        if not _is_action_node(node):
            continue
        endpoints = sorted(
            set(node.refs(IRI_ACTION_OBJECT))
            | set(node.refs(IRI_ACTION_RESULT))
            | set(node.refs(IRI_INSTRUMENT))
        )
        for i, left in enumerate(endpoints):
            for right in endpoints[i + 1 :]:
                pairs.add(frozenset({left, right}))
    return pairs


def _node_hash_values(view: CanonicalGraphView, node: CanonicalNode) -> list[str]:
    out: list[str] = []
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
                if isinstance(val, str) and val:
                    out.append(val)
    for facet_iri in node.refs(IRI_HAS_FACET):
        facet = view.get(facet_iri)
        if not facet or not facet.has_type(IRI_CONTENT_FACET):
            # Accept type local-name match when RDF expansion missed ContentDataFacet
            if not facet or not any("ContentDataFacet" in t for t in facet.types):
                continue
        for href in facet.refs(IRI_HASH) if facet else []:
            hnode = view.get(href)
            if not hnode:
                continue
            out.extend(hnode.literals(IRI_HASH_VALUE))
        if facet:
            out.extend(facet.literals(IRI_HASH_VALUE))
    return out


def _derived_file_iris(view: CanonicalGraphView) -> set[str]:
    derived: set[str] = set()
    for node in view.iter_nodes():
        if _is_action_node(node):
            for ref in node.refs(IRI_ACTION_RESULT):
                target = view.get(ref)
                if target and target.has_type(IRI_FILE, IRI_OBSERVABLE, IRI_IMAGE):
                    if not any("Facet" in t for t in target.types):
                        derived.add(ref)
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        kinds = _relationship_kinds(node)
        if not (kinds & _DERIVED_KINDS):
            continue
        # Extracted_From: source is derived, target is origin
        # Contained_Within: source is contained (derived), target is container
        for src in node.refs(IRI_SOURCE):
            source_node = view.get(src)
            if source_node and source_node.has_type(IRI_FILE, IRI_OBSERVABLE, IRI_IMAGE):
                if not any("Facet" in t for t in source_node.types):
                    derived.add(src)
    return derived


def _container_object_members(view: CanonicalGraphView) -> set[str]:
    members: set[str] = set()
    for node in view.iter_nodes():
        if node.has_type(
            IRI_INVESTIGATION, IRI_PROVENANCE_RECORD, IRI_CONTEXTUAL_COMPILATION
        ):
            members.update(node.refs(IRI_OBJECT))
    return members


def _inbound_provenance_targets(view: CanonicalGraphView) -> set[str]:
    """IRIs that appear as relationship source with provenance kinds (derived→origin)."""

    inbound: set[str] = set()
    for node in view.iter_nodes():
        if not node.has_type(IRI_RELATIONSHIP):
            continue
        if not (_relationship_kinds(node) & _PROVENANCE_KINDS):
            continue
        inbound.update(node.refs(IRI_SOURCE))
    return inbound


def _derived_source_pairs(view: CanonicalGraphView) -> list[tuple[str, str]]:
    """Return (derived_iri, source_iri) pairs from Extracted_From and action object→result."""

    pairs: list[tuple[str, str]] = []
    for node in view.iter_nodes():
        if node.has_type(IRI_RELATIONSHIP):
            kinds = _relationship_kinds(node)
            if "Extracted_From" in kinds:
                for src in node.refs(IRI_SOURCE):
                    for tgt in node.refs(IRI_TARGET):
                        pairs.append((src, tgt))
        if _is_action_node(node):
            objects = node.refs(IRI_ACTION_OBJECT)
            results = node.refs(IRI_ACTION_RESULT)
            for src in objects:
                for derived in results:
                    pairs.append((derived, src))
    return pairs
