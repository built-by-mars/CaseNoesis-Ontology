"""Shared document extraction models used by the processor and semantic mapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MAX_EVENT_CONTEXT = 12


@dataclass(frozen=True)
class ExtractedRecord:
    """One reviewable record extracted from a source document.

    ``anchor`` (Spec026 extraction-bundle contract 1.0) locates the record in
    the canonical extracted content. Records that cannot be honestly located
    carry ``anchor=None`` and are simply absent from ``annotations.jsonld`` —
    anchors are never fabricated.

    When ``ontology_class`` is set (semantic mapping stage), the case graph
    node uses that verified CASE/UCO class instead of a generic
    ``uco-observable:ObservableObject`` ExtractedString wrapper.
    """

    label: str
    text: str
    anchor: dict[str, Any] | None = None
    ontology_class: str | None = None
    graph_facets: tuple[dict[str, Any], ...] = ()
    extra_properties: dict[str, Any] | None = None
