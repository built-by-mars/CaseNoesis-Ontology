"""Graph parse/integrity helpers for the deterministic critic."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from critic.models import CriticFinding, CriticTarget

SUPPORTED_EXTENSIONS = {".json", ".jsonld", ".json-ld", ".ttl", ".turtle"}
MAX_GRAPH_BYTES = 50 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonld_graph(path: Path) -> tuple[dict[str, Any] | None, list[CriticFinding]]:
    """Load a JSON-LD graph document; Turtle returns parse-deferred findings."""

    findings: list[CriticFinding] = []
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        findings.append(
            _finding(
                rule_id="CRIT-G-UNSUPPORTED-TYPE",
                severity="critical",
                category="syntax_integrity",
                target=CriticTarget(path=path.name),
                evidence=[f"extension={suffix}"],
                rationale="Graph file type is not a supported CASE/UCO serialization.",
                recommended_change="Provide .jsonld/.json or .ttl/.turtle.",
                verification_method="Check file extension against supported set.",
            )
        )
        return None, findings

    size = path.stat().st_size
    if size > MAX_GRAPH_BYTES:
        findings.append(
            _finding(
                rule_id="CRIT-G-SIZE-BOUND",
                severity="critical",
                category="syntax_integrity",
                target=CriticTarget(path=path.name),
                evidence=[f"size_bytes={size}"],
                rationale="Graph exceeds the critic size bound.",
                recommended_change="Split by forensic boundary or raise the bound deliberately.",
                verification_method="Compare file size to MAX_GRAPH_BYTES.",
            )
        )
        return None, findings

    if suffix in {".ttl", ".turtle"}:
        # Turtle is validated via case_validate; JSON heuristics need JSON-LD.
        findings.append(
            _finding(
                rule_id="CRIT-G-TTL-JSON-HEURISTICS-SKIPPED",
                severity="info",
                category="syntax_integrity",
                target=CriticTarget(path=path.name),
                evidence=["format=turtle"],
                rationale=(
                    "Turtle graphs receive SHACL/coverage via the validator; "
                    "JSON-structure heuristics require JSON-LD."
                ),
                recommended_change="Optionally also emit JSON-LD for richer critic heuristics.",
                verification_method="Confirm validator stages completed for the Turtle file.",
            )
        )
        return None, findings

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        findings.append(
            _finding(
                rule_id="CRIT-G-PARSE-FAILED",
                severity="critical",
                category="syntax_integrity",
                target=CriticTarget(path=path.name),
                evidence=[type(exc).__name__],
                rationale="Graph JSON could not be parsed.",
                recommended_change="Fix JSON syntax before critic review.",
                verification_method="Re-parse with json.loads.",
            )
        )
        return None, findings

    if not isinstance(data, dict):
        findings.append(
            _finding(
                rule_id="CRIT-G-ROOT-TYPE",
                severity="critical",
                category="syntax_integrity",
                target=CriticTarget(path=path.name),
                evidence=[f"root_type={type(data).__name__}"],
                rationale="JSON-LD root must be an object with @context/@graph.",
                recommended_change="Wrap nodes in a JSON-LD document object.",
                verification_method="Assert isinstance(root, dict).",
            )
        )
        return None, findings

    return data, findings


def iter_nodes(document: dict[str, Any]) -> list[dict[str, Any]]:
    graph = document.get("@graph")
    if isinstance(graph, list):
        return [n for n in graph if isinstance(n, dict)]
    if "@type" in document or "@id" in document:
        return [document]
    return []


def check_integrity(document: dict[str, Any]) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    nodes = iter_nodes(document)
    if not nodes:
        findings.append(
            _finding(
                rule_id="CRIT-G-EMPTY",
                severity="critical",
                category="syntax_integrity",
                target=CriticTarget(),
                evidence=["node_count=0"],
                rationale="Graph contains no nodes.",
                recommended_change="Emit at least one typed CASE/UCO object.",
                verification_method="Count @graph entries.",
            )
        )
        return findings

    ids: dict[str, int] = {}
    id_to_node: dict[str, dict[str, Any]] = {}
    for node in nodes:
        node_id = node.get("@id")
        if not isinstance(node_id, str) or not node_id:
            findings.append(
                _finding(
                    rule_id="CRIT-G-MISSING-ID",
                    severity="high",
                    category="syntax_integrity",
                    target=CriticTarget(
                        json_pointer="/@graph",
                        predicate="@id",
                    ),
                    evidence=[f"types={_types(node)}"],
                    rationale="Top-level graph node is missing @id (SHACL often requires IRI nodeKind).",
                    recommended_change="Assign a stable IRI @id to every top-level object.",
                    verification_method="Assert every @graph entry has string @id.",
                )
            )
            continue
        ids[node_id] = ids.get(node_id, 0) + 1
        prior = id_to_node.get(node_id)
        if prior is not None and _normalized(prior) != _normalized(node):
            findings.append(
                _finding(
                    rule_id="CRIT-G-CONFLICTING-DUPLICATE",
                    severity="critical",
                    category="syntax_integrity",
                    target=CriticTarget(node_id=node_id),
                    evidence=["incompatible_duplicate_assertions"],
                    rationale="The same @id appears with incompatible property sets.",
                    recommended_change="Merge into one node or use distinct IRIs.",
                    verification_method="Compare normalized property maps for duplicate @id.",
                )
            )
        id_to_node[node_id] = node

    for node_id, count in ids.items():
        if count > 1:
            findings.append(
                _finding(
                    rule_id="CRIT-G-DUPLICATE-ID",
                    severity="high",
                    category="syntax_integrity",
                    target=CriticTarget(node_id=node_id),
                    evidence=[f"occurrences={count}"],
                    rationale="Duplicate top-level @id values present in @graph.",
                    recommended_change="Deduplicate or use CASEGraph upsert/reject policy.",
                    verification_method="Group @graph by @id and count > 1.",
                )
            )

    known_ids = set(id_to_node)
    for node in nodes:
        node_id = node.get("@id") if isinstance(node.get("@id"), str) else None
        for predicate, value in node.items():
            if predicate.startswith("@"):
                continue
            for ref in _extract_id_refs(value):
                if ref.startswith("_:"):
                    continue
                if ref.startswith("kb:") or ref.startswith("urn:") or "://" in ref or ref.startswith("#"):
                    # Local compact IRIs / same-document refs that should resolve in-graph
                    if ref.startswith("#") and ref[1:] and f"kb:{ref[1:]}" not in known_ids:
                        # soft: fragment-only
                        pass
                    if (
                        ref.startswith("kb:")
                        or ref.startswith("urn:case:")
                        or ref.startswith("urn:example:")
                    ) and ref not in known_ids:
                        findings.append(
                            _finding(
                                rule_id="CRIT-G-DANGLING-REF",
                                severity="high",
                                category="syntax_integrity",
                                target=CriticTarget(
                                    node_id=node_id,
                                    predicate=predicate,
                                ),
                                evidence=[f"missing_ref={ref}"],
                                rationale="Local graph reference does not resolve to a top-level @id.",
                                recommended_change="Add the referenced node or fix the IRI.",
                                verification_method="Membership check of referenced @id in @graph.",
                            )
                        )

    ctx = document.get("@context")
    if isinstance(ctx, dict):
        # Detect obvious prefix remapping collisions (same prefix, different IRI)
        # — rare in compact docs; still cheap to scan nested maps.
        _scan_context_collisions(ctx, findings)

    return findings


def _scan_context_collisions(ctx: dict[str, Any], findings: list[CriticFinding]) -> None:
    seen: dict[str, str] = {}
    for key, value in ctx.items():
        if key.startswith("@"):
            continue
        iri = value if isinstance(value, str) else (
            value.get("@id") if isinstance(value, dict) else None
        )
        if not isinstance(iri, str):
            continue
        prior = seen.get(key)
        if prior and prior != iri:
            findings.append(
                _finding(
                    rule_id="CRIT-G-CONTEXT-COLLISION",
                    severity="critical",
                    category="syntax_integrity",
                    target=CriticTarget(predicate=key),
                    evidence=[f"{prior} vs {iri}"],
                    rationale="Context prefix is bound to conflicting IRIs.",
                    recommended_change="Use a single consistent prefix binding.",
                    verification_method="Compare @context entries for duplicate keys.",
                )
            )
        seen[key] = iri


def _extract_id_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        if isinstance(value.get("@id"), str):
            refs.append(value["@id"])
        for nested in value.values():
            refs.extend(_extract_id_refs(nested))
    elif isinstance(value, list):
        for item in value:
            refs.extend(_extract_id_refs(item))
    elif isinstance(value, str) and (
        value.startswith("kb:")
        or value.startswith("urn:")
        or value.startswith("#")
    ):
        refs.append(value)
    return refs


def _types(node: dict[str, Any]) -> str:
    raw = node.get("@type")
    if isinstance(raw, list):
        return ",".join(str(t) for t in raw)
    return str(raw or "")


def _normalized(node: dict[str, Any]) -> str:
    return json.dumps(node, sort_keys=True, separators=(",", ":"))


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
) -> CriticFinding:
    finding = CriticFinding(
        finding_id="CRIT-PENDING",
        severity=severity,  # type: ignore[arg-type]
        category=category,
        confidence=1.0,
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
