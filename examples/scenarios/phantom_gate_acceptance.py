"""Acceptance gates for Operation PHANTOM GATE graph fidelity."""

from __future__ import annotations

from typing import Any, Callable


INVESTIGATIVE_ACTION_TYPES = (
    "case-investigation:InvestigativeAction",
    "solveit-core:SolveitInvestigativeAction",
    "cac-core:InvestigativeAction",
)

MARKING_PROPAGATION_KINDS = frozenset({
    "Derived_From",
    "Contained_Within",
    "Part_Of",
    "Attachment_Of",
})


def authorize(
    g: list[dict],
    rel: Callable[..., dict],
    action_id: str,
    auth_id: str,
    *,
    description: str | None = None,
) -> None:
    """Link an action to an Authorization via Authorized_By (not relevantAuthorization)."""
    g.append(rel(
        action_id,
        auth_id,
        "Authorized_By",
        description=description or "Action performed under scoped authorization",
    ))


def merge_markings(node: dict, marking_ids: list[str]) -> None:
    existing = [
        m["@id"] if isinstance(m, dict) else m
        for m in node.get("uco-core:objectMarking", [])
    ]
    for mid in marking_ids:
        if mid not in existing:
            existing.append(mid)
    if existing:
        node["uco-core:objectMarking"] = [{"@id": m} for m in existing]


def propagate_markings(g: list[dict], *, max_passes: int = 5) -> None:
    """Inherit parent/container markings along governed derivation/containment edges."""
    for _ in range(max_passes):
        changed = False
        by_id = {n["@id"]: n for n in g if n.get("@id")}
        for node in g:
            if node.get("@type") != "uco-core:Relationship":
                continue
            kind = node.get("uco-core:kindOfRelationship")
            if kind not in MARKING_PROPAGATION_KINDS:
                continue
            sources = node.get("uco-core:source") or []
            targets = node.get("uco-core:target") or []
            if not sources or not targets:
                continue
            src = sources[0]["@id"] if isinstance(sources[0], dict) else sources[0]
            tgt = targets[0]["@id"] if isinstance(targets[0], dict) else targets[0]
            src_node = by_id.get(src)
            tgt_node = by_id.get(tgt)
            if not src_node or not tgt_node:
                continue
            parent_markings = [
                m["@id"] if isinstance(m, dict) else m
                for m in tgt_node.get("uco-core:objectMarking", [])
            ]
            if parent_markings:
                before = [
                    m["@id"] if isinstance(m, dict) else m
                    for m in src_node.get("uco-core:objectMarking", [])
                ]
                merge_markings(src_node, parent_markings)
                after = [
                    m["@id"] if isinstance(m, dict) else m
                    for m in src_node.get("uco-core:objectMarking", [])
                ]
                if after != before:
                    changed = True

        by_id = {n["@id"]: n for n in g if n.get("@id")}
        for node in g:
            contains = node.get("solveit-observable:contains") or []
            if not contains:
                continue
            container_markings = [
                m["@id"] if isinstance(m, dict) else m
                for m in node.get("uco-core:objectMarking", [])
            ]
            if not container_markings:
                continue
            for child_ref in contains:
                cid = child_ref["@id"] if isinstance(child_ref, dict) else child_ref
                child_node = by_id.get(cid)
                if not child_node:
                    continue
                before = [
                    m["@id"] if isinstance(m, dict) else m
                    for m in child_node.get("uco-core:objectMarking", [])
                ]
                merge_markings(child_node, container_markings)
                after = [
                    m["@id"] if isinstance(m, dict) else m
                    for m in child_node.get("uco-core:objectMarking", [])
                ]
                if after != before:
                    changed = True

        by_id = {n["@id"]: n for n in g if n.get("@id")}
        for node in g:
            types = node.get("@type", [])
            if isinstance(types, str):
                types = [types]
            if not any(t in INVESTIGATIVE_ACTION_TYPES for t in types):
                continue
            results = node.get("uco-action:result") or []
            objects = node.get("uco-action:object") or []
            input_markings: list[str] = []
            for obj in objects:
                oid = obj["@id"] if isinstance(obj, dict) else obj
                obj_node = by_id.get(oid)
                if not obj_node:
                    continue
                input_markings.extend(
                    m["@id"] if isinstance(m, dict) else m
                    for m in obj_node.get("uco-core:objectMarking", [])
                )
            if not input_markings:
                continue
            for res in results:
                rid = res["@id"] if isinstance(res, dict) else res
                res_node = by_id.get(rid)
                if not res_node:
                    continue
                before = [
                    m["@id"] if isinstance(m, dict) else m
                    for m in res_node.get("uco-core:objectMarking", [])
                ]
                merge_markings(res_node, input_markings)
                after = [
                    m["@id"] if isinstance(m, dict) else m
                    for m in res_node.get("uco-core:objectMarking", [])
                ]
                if after != before:
                    changed = True

        if not changed:
            break


def strip_action_authorizations(g: list[dict]) -> None:
    """Remove case-investigation:relevantAuthorization from non-Investigation nodes."""
    for node in g:
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if types == ["case-investigation:Investigation"] or (
            "case-investigation:Investigation" in types and len(types) <= 2
        ):
            continue
        node.pop("case-investigation:relevantAuthorization", None)


def dedupe_top_level_nodes(g: list[dict]) -> None:
    seen: set[str] = set()
    deduped: list[dict] = []
    for node in g:
        nid = node.get("@id")
        if nid and nid in seen:
            continue
        if nid:
            seen.add(nid)
        deduped.append(node)
    g[:] = deduped


def assert_unique_top_level_ids(g: list[dict]) -> None:
    ids = [n["@id"] for n in g if n.get("@id")]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise RuntimeError(f"Duplicate top-level @id values: {sorted(dupes)}")


def assert_no_action_authorizations(g: list[dict]) -> None:
    offenders: list[str] = []
    for node in g:
        if "case-investigation:relevantAuthorization" not in node:
            continue
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if "case-investigation:Investigation" in types:
            continue
        if "case-investigation:Authorization" in types:
            continue
        offenders.append(node.get("@id", "?"))
    if offenders:
        raise RuntimeError(
            "relevantAuthorization on non-Investigation nodes: "
            + ", ".join(sorted(offenders))
        )


def verify_embedded_scenario_hash(g: list[dict], expected_sha256: str) -> None:
    for node in g:
        if node.get("uco-core:name") != "operation-phantom-gate.md":
            continue
        for facet in node.get("uco-core:hasFacet", []):
            if facet.get("@type") != "uco-observable:ContentDataFacet":
                continue
            for h in facet.get("uco-observable:hash", []):
                val = h.get("uco-types:hashValue", {})
                if isinstance(val, dict):
                    val = val.get("@value")
                if val == expected_sha256:
                    return
                raise RuntimeError(
                    f"Embedded scenario SHA-256 mismatch: graph has {val!r}, "
                    f"file has {expected_sha256!r}"
                )
    raise RuntimeError("Scenario source document node with content hash not found")


def add_weakness_evaluation_set(
    g: list[dict],
    add: Callable[..., None],
    uid: Callable[[str], str],
    lit: Callable[[str, Any], dict],
    *,
    label: str,
    technique: str,
    weakness: str,
    evaluator_id: str,
    likelihood: int,
    impact: int,
    likelihood_rationale: str,
    impact_rationale: str,
    solvit_data: str,
) -> None:
    evaluation = uid(f"{label}-weakness-eval")
    eval_set = uid(f"{label}-weakness-set")
    add(
        {
            "@id": evaluation,
            "@type": "solveit-wa:WeaknessEvaluation",
            "uco-core:name": f"{label} — {weakness} evaluation",
            "solveit-wa:evaluatesWeakness": {"@id": solvit_data + f"weakness{weakness}"},
            "solveit-wa:likelihoodRating": lit("xsd:integer", likelihood),
            "solveit-wa:likelihoodRationale": likelihood_rationale,
            "solveit-wa:impactRating": lit("xsd:integer", impact),
            "solveit-wa:impactRationale": impact_rationale,
            "solveit-wa:liImpactScore": lit("xsd:integer", likelihood * impact),
        },
        {
            "@id": eval_set,
            "@type": "solveit-wa:WeaknessEvaluationSet",
            "uco-core:name": f"{label} — weakness assessment session",
            "solveit-wa:scopedToTechnique": {"@id": solvit_data + f"technique{technique}"},
            "solveit-wa:evaluatedBy": {"@id": evaluator_id},
            "solveit-wa:hasEvaluation": [{"@id": evaluation}],
        },
    )


def run_acceptance_gates(
    g: list[dict],
    scenario_sha256: str,
    *,
    investigation_id: str | None = None,
) -> None:
    strip_action_authorizations(g)
    propagate_markings(g)
    dedupe_top_level_nodes(g)
    assert_unique_top_level_ids(g)
    assert_no_action_authorizations(g)
    verify_embedded_scenario_hash(g, scenario_sha256)
