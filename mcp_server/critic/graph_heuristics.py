"""Deterministic structural modeling heuristics for the critic (issue #75).

These are review prompts / high-confidence warnings, not a replacement for SHACL.
Each rule has a stable ``rule_id`` and documented false-positive boundary in
``docs/critic/RULES.md``.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from critic.graph_integrity import iter_nodes
from critic.models import CriticFinding, CriticTarget


def run_graph_heuristics(document: dict[str, Any]) -> list[CriticFinding]:
    nodes = iter_nodes(document)
    findings: list[CriticFinding] = []
    findings.extend(_investigation_without_object(nodes))
    findings.extend(_relevant_authorization_misuse(nodes))
    findings.extend(_acquisition_input_result_inversion(nodes))
    findings.extend(_generic_related_to_overuse(nodes))
    findings.extend(_charged_with_direction(nodes))
    findings.extend(_dictionary_entry_collisions(nodes))
    findings.extend(_facet_like_props_on_observable(nodes))
    return findings


def _has_type(node: dict[str, Any], *needles: str) -> bool:
    raw = node.get("@type")
    types = raw if isinstance(raw, list) else [raw]
    texts = [str(t) for t in types if t is not None]
    for text in texts:
        for needle in needles:
            if needle in text:
                return True
    return False


def _prop(node: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in node:
            return node[key]
    return None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _investigation_without_object(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in nodes:
        if not _has_type(node, "Investigation"):
            continue
        obj = _prop(node, "uco-core:object", "object")
        if obj:
            continue
        findings.append(
            _h(
                rule_id="CRIT-H-INV-NO-OBJECT",
                severity="high",
                category="investigation_structure",
                target=CriticTarget(
                    node_id=node.get("@id") if isinstance(node.get("@id"), str) else None,
                    predicate="uco-core:object",
                ),
                evidence=["Investigation present without uco-core:object"],
                rationale=(
                    "An Investigation container is present but does not reference "
                    "contained objects via uco-core:object."
                ),
                recommended_change=(
                    "Attach evidence, actions, and related objects with uco-core:object."
                ),
                verification_method="SPARQL/JSON scan for Investigation lacking object.",
            )
        )
    return findings


def _relevant_authorization_misuse(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in nodes:
        auth = _prop(node, "uco-core:relevantAuthorization", "relevantAuthorization")
        if auth is None:
            continue
        if _has_type(node, "Investigation"):
            continue
        findings.append(
            _h(
                rule_id="CRIT-H-AUTH-NON-INVESTIGATION",
                severity="high",
                category="authorization",
                target=CriticTarget(
                    node_id=node.get("@id") if isinstance(node.get("@id"), str) else None,
                    predicate="uco-core:relevantAuthorization",
                ),
                evidence=[f"types={node.get('@type')}"],
                rationale=(
                    "relevantAuthorization is attached to a non-Investigation node; "
                    "CASE patterns typically hang authorizations on the Investigation."
                ),
                recommended_change=(
                    "Move relevantAuthorization to the Investigation (or justify via recipe)."
                ),
                verification_method="Find relevantAuthorization on nodes whose @type lacks Investigation.",
            )
        )
    return findings


def _acquisition_input_result_inversion(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    """Flag acquisition-like actions where a likely image/result is only an input."""

    findings: list[CriticFinding] = []
    id_index = {
        n.get("@id"): n for n in nodes if isinstance(n.get("@id"), str)
    }
    for node in nodes:
        if not _has_type(node, "InvestigativeAction", "Action"):
            continue
        name = str(_prop(node, "uco-core:name", "name") or "").lower()
        if "acquir" not in name and "image" not in name and "extract" not in name:
            continue
        inputs = _as_list(_prop(node, "uco-action:object", "object"))
        results = _as_list(_prop(node, "uco-action:result", "result"))
        if results:
            continue
        for item in inputs:
            ref = item.get("@id") if isinstance(item, dict) else item
            if not isinstance(ref, str):
                continue
            target = id_index.get(ref)
            if target and _has_type(target, "File", "RasterPicture", "DiskImage", "Image"):
                findings.append(
                    _h(
                        rule_id="CRIT-H-ACQ-INPUT-RESULT-INVERSION",
                        severity="high",
                        category="action_grammar",
                        target=CriticTarget(
                            node_id=node.get("@id") if isinstance(node.get("@id"), str) else None,
                            predicate="uco-action:result",
                        ),
                        evidence=[f"likely_result_only_as_input={ref}"],
                        rationale=(
                            "Acquisition-like action lists a file/image only as input "
                            "and has no result — often an input/result inversion."
                        ),
                        recommended_change=(
                            "Place the acquired image/artifact on uco-action:result; "
                            "keep the source device/media as object/instrument."
                        ),
                        verification_method="Check InvestigativeAction name + object/result roles.",
                    )
                )
                break
    return findings


def _generic_related_to_overuse(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    kinds: list[str] = []
    for node in nodes:
        if not _has_type(node, "Relationship"):
            continue
        kind = _prop(node, "uco-core:kindOfRelationship", "kindOfRelationship")
        if kind is None:
            continue
        for value in _as_list(kind):
            text = value.get("@value") if isinstance(value, dict) else value
            kinds.append(str(text))
    if not kinds:
        return []
    counts = Counter(kinds)
    related = counts.get("Related_To", 0)
    if related < 3:
        return []
    ratio = related / max(len(kinds), 1)
    if related < 5 and ratio < 0.5:
        return []
    return [
        _h(
            rule_id="CRIT-H-RELATED-TO-OVERUSE",
            severity="medium",
            category="generic_relationship",
            target=CriticTarget(predicate="uco-core:kindOfRelationship"),
            evidence=[f"Related_To_count={related}", f"relationship_count={len(kinds)}"],
            rationale=(
                "Many relationships use generic Related_To when a governed "
                "ObservableObjectRelationshipVocab member may be available."
            ),
            recommended_change=(
                "Replace Related_To with specific kinds (Contained_Within, "
                "Extracted_From, etc.) where the recipe defines them."
            ),
            verification_method="Count kindOfRelationship == Related_To versus total.",
        )
    ]


def _charged_with_direction(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    """Charged_With should be person → charge (not charge → person)."""

    findings: list[CriticFinding] = []
    id_index = {
        n.get("@id"): n for n in nodes if isinstance(n.get("@id"), str)
    }
    for node in nodes:
        if not _has_type(node, "Relationship"):
            continue
        kind = _prop(node, "uco-core:kindOfRelationship", "kindOfRelationship")
        texts = []
        for value in _as_list(kind):
            texts.append(str(value.get("@value") if isinstance(value, dict) else value))
        if "Charged_With" not in texts:
            continue
        source = _prop(node, "uco-core:source", "source")
        target = _prop(node, "uco-core:target", "target")
        source_ref = source.get("@id") if isinstance(source, dict) else source
        target_ref = target.get("@id") if isinstance(target, dict) else target
        if not isinstance(source_ref, str) or not isinstance(target_ref, str):
            continue
        source_node = id_index.get(source_ref)
        target_node = id_index.get(target_ref)
        if not source_node or not target_node:
            continue
        if _has_type(source_node, "CriminalCharge", "Charge") and _has_type(
            target_node, "Person", "Identity"
        ):
            findings.append(
                _h(
                    rule_id="CRIT-H-CHARGED-WITH-REVERSED",
                    severity="high",
                    category="relationship_direction",
                    target=CriticTarget(
                        node_id=node.get("@id") if isinstance(node.get("@id"), str) else None,
                        predicate="uco-core:kindOfRelationship",
                    ),
                    evidence=[
                        f"source={source_ref}",
                        f"target={target_ref}",
                    ],
                    rationale=(
                        "Charged_With is modeled person→charge in CASE legal-process recipes; "
                        "this relationship has charge→person."
                    ),
                    recommended_change="Reverse source and target.",
                    verification_method=(
                        "Assert Relationship source is Person and target is CriminalCharge."
                    ),
                )
            )
    return findings


def _dictionary_entry_collisions(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    """Same dictionary-entry IRI appearing under multiple parent dictionaries."""

    parents: dict[str, set[str]] = {}
    for node in nodes:
        if not _has_type(node, "Dictionary"):
            continue
        parent_id = node.get("@id")
        if not isinstance(parent_id, str):
            continue
        entries = _as_list(_prop(node, "uco-types:entry", "entry"))
        for entry in entries:
            ref = entry.get("@id") if isinstance(entry, dict) else entry
            if not isinstance(ref, str):
                continue
            parents.setdefault(ref, set()).add(parent_id)
    findings: list[CriticFinding] = []
    for entry_id, parent_ids in parents.items():
        if len(parent_ids) < 2:
            continue
        findings.append(
            _h(
                rule_id="CRIT-H-DICT-ENTRY-COLLISION",
                severity="high",
                category="dictionary_collision",
                target=CriticTarget(node_id=entry_id),
                evidence=[f"parents={sorted(parent_ids)}"],
                rationale="Dictionary entry IRI is referenced by multiple Dictionary parents.",
                recommended_change="Mint parent-scoped entry IRIs (or distinct entries).",
                verification_method="Group dictionary entry refs by @id across Dictionary nodes.",
            )
        )
    return findings


def _facet_like_props_on_observable(nodes: list[dict[str, Any]]) -> list[CriticFinding]:
    """Heuristic: Windows service / file facet properties placed on ObservableObject."""

    facetish = {
        "uco-observable:serviceName",
        "uco-observable:serviceType",
        "uco-observable:fileName",
        "uco-observable:sizeInBytes",
    }
    findings: list[CriticFinding] = []
    for node in nodes:
        if not _has_type(node, "ObservableObject"):
            continue
        if _has_type(node, "Facet"):
            continue
        bad = [k for k in facetish if k in node]
        if not bad:
            continue
        # Allow if hasFacet present — properties might still be wrong, but softer
        has_facet = _prop(node, "uco-core:hasFacet", "hasFacet")
        severity = "medium" if has_facet else "high"
        findings.append(
            _h(
                rule_id="CRIT-H-FACET-PROPS-ON-OBSERVABLE",
                severity=severity,  # type: ignore[arg-type]
                category="facet_placement",
                target=CriticTarget(
                    node_id=node.get("@id") if isinstance(node.get("@id"), str) else None,
                    predicate=bad[0],
                ),
                evidence=bad,
                rationale=(
                    "Facet-scoped properties appear directly on ObservableObject; "
                    "CASE/UCO expects them on Facet instances via hasFacet."
                ),
                recommended_change="Move properties onto the appropriate *Facet and link via hasFacet.",
                verification_method="Detect facet properties on ObservableObject nodes.",
            )
        )
    return findings


def _h(
    *,
    rule_id: str,
    severity: str,
    category: str,
    target: CriticTarget,
    evidence: list[str],
    rationale: str,
    recommended_change: str,
    verification_method: str,
) -> CriticFinding:
    finding = CriticFinding(
        finding_id="CRIT-PENDING",
        severity=severity,  # type: ignore[arg-type]
        category=category,
        confidence=0.9,
        status="new",
        target=target,
        evidence_kind="deterministic",
        evidence=evidence,
        rationale=rationale,
        recommended_change=recommended_change,
        verification_method=verification_method,
        rule_id=rule_id,
    )
    finding.ensure_identity_key()
    return finding
