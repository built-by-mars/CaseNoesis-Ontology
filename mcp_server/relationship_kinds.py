"""Machine-readable relationship-kind registry and lint (CQ-40)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path(__file__).resolve().parent / "relationship_kinds.json"


@lru_cache(maxsize=1)
def load_relationship_kind_registry() -> dict[str, Any]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def known_relationship_kinds(*, vocab: str | None = None) -> frozenset[str]:
    reg = load_relationship_kind_registry()
    vocabs = reg.get("vocabularies") or {}
    if vocab:
        entry = vocabs.get(vocab) or {}
        return frozenset(entry.get("kinds") or [])
    kinds: set[str] = set()
    for entry in vocabs.values():
        kinds.update(entry.get("kinds") or [])
    return frozenset(kinds)


def graph_uses_relationship_kinds(graph: dict[str, Any] | list[Any]) -> bool:
    """Return True when any node carries ``uco-core:kindOfRelationship``."""
    nodes: list[Any]
    if isinstance(graph, dict):
        nodes = list(graph.get("@graph") or [])
        if not nodes and "uco-core:kindOfRelationship" in graph:
            return True
    else:
        nodes = list(graph)
    return any(
        isinstance(node, dict) and node.get("uco-core:kindOfRelationship") is not None
        for node in nodes
    )


def lint_relationship_kinds(
    graph: dict[str, Any] | list[Any],
    *,
    allow_open_vocabulary: bool = True,
) -> dict[str, Any]:
    """Lint ``uco-core:kindOfRelationship`` values against the registry.

    When ``allow_open_vocabulary`` is True (UCO default), unknown kinds are
    reported as warnings rather than errors. Returns a structured report.
    """

    nodes: list[Any]
    if isinstance(graph, dict):
        nodes = list(graph.get("@graph") or [])
        if not nodes and ("@type" in graph or "uco-core:kindOfRelationship" in graph):
            nodes = [graph]
    else:
        nodes = list(graph)

    known = known_relationship_kinds()
    findings: list[dict[str, Any]] = []
    checked = 0
    for node in nodes:
        if not isinstance(node, dict):
            continue
        kind = node.get("uco-core:kindOfRelationship")
        if kind is None:
            continue
        checked += 1
        values = kind if isinstance(kind, list) else [kind]
        for value in values:
            if isinstance(value, dict):
                value = value.get("@value", value)
            text = str(value)
            if text in known:
                continue
            findings.append({
                "node_id": node.get("@id"),
                "kind": text,
                "severity": "warning" if allow_open_vocabulary else "error",
                "message": (
                    f"kindOfRelationship {text!r} is not in "
                    "ObservableObjectRelationshipVocab / ActionRelationshipVocab"
                ),
            })

    errors = [f for f in findings if f["severity"] == "error"]
    return {
        "ok": not errors,
        "checked": checked,
        "findings": findings,
        "known_kind_count": len(known),
        "registry": str(REGISTRY_PATH.name),
    }
