"""Deterministic CASE/UCO semantic mapping over extracted document text.

The document processor's extraction stage produces canonical text; this
module maps high-confidence spans to verified ontology classes with
text-position anchors for the Spec026 extraction bundle. Mapping is
pattern-based (no LLM): emails, URLs, phones, dates, money, locations,
organizations, persons described in law-enforcement narratives, and a
bounded narrative Event when charge/arrest language is present.

Tier T0 synthetic fixtures only in committed tests; real officer documents
belong in local T1/T2 verification per Link-Look test-data handling.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import Any

MAX_SEMANTIC_ENTITIES = 48
MAX_EVENT_CONTEXT = 12

EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)"
)
URL_RE = re.compile(r"https?://[^\s<>\"']+|www\.[A-Za-z0-9.\-/]+")
MONEY_RE = re.compile(r"\$\s?\d{1,6}(?:,\d{3})*(?:\.\d{2})?")
DATE_RE = re.compile(
    r"\b(?:"
    r"\d{1,2}/\d{1,2}/\d{2,4}|"
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2},?\s+\d{4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}"
    r")\b",
    re.IGNORECASE,
)
HEADLINE_SUBJECT_RE = re.compile(
    r"\b(\d{1,3})-Year-Old\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\s+"
    r"(Man|Woman|male|female)\b",
    re.IGNORECASE,
)
CHARGE_NARRATIVE_RE = re.compile(
    r"\b(?:charged with|arrested|taken into custody|sexual solicitation|"
    r"child (?:sex|pornography|exploitation)|investigation into)\b",
    re.IGNORECASE,
)
ORGANIZATION_RE = re.compile(
    r"\b(?:"
    r"Maryland State Police(?:\s+[A-Za-z\s]+(?:Unit|Force|Task Force))?|"
    r"Anne Arundel County Police Department|"
    r"FBI|"
    r"Internet Crimes Against Children(?:\s+Task Force)?|"
    r"ICAC(?:\s+Task Force)?"
    r")\b",
    re.IGNORECASE,
)
# City/locality tokens immediately before "Man/Woman" in headlines or "in <City>".
LOCATION_RE = re.compile(
    r"\b(?:in|at|from|near)\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\b|"
    r"\b([A-Z][A-Za-z]+)\s+(?:Man|Woman)\b|"
    r"\bresidence in\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SemanticEntity:
    """One reviewable ontology mapping anchored in canonical section text."""

    ontology_class: str
    label: str
    matched_text: str
    start: int
    end: int
    section_id: str = "s1"
    graph_facets: tuple[dict[str, Any], ...] = ()
    extra_properties: dict[str, Any] = field(default_factory=dict)


def _anchor(section_id: str, start: int, end: int, exact: str) -> dict[str, Any]:
    return {
        "selector_kind": "text_position",
        "section_id": section_id,
        "start": start,
        "end": end,
        "exact": exact,
    }


def _facet_id(run_seed: str, kind: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{run_seed}:{kind}')}"


def _add_match(
    matches: list[SemanticEntity],
    seen_spans: set[tuple[int, int, str]],
    *,
    ontology_class: str,
    label: str,
    matched_text: str,
    start: int,
    end: int,
    section_id: str,
    run_seed: str,
    facets: tuple[dict[str, Any], ...] = (),
    extra_properties: dict[str, Any] | None = None,
) -> None:
    key = (start, end, ontology_class)
    if key in seen_spans or not matched_text.strip():
        return
    seen_spans.add(key)
    matches.append(
        SemanticEntity(
            ontology_class=ontology_class,
            label=label[:120],
            matched_text=matched_text,
            start=start,
            end=end,
            section_id=section_id,
            graph_facets=facets or (),
            extra_properties=extra_properties or {},
        )
    )


def extract_semantic_entities(
    full_text: str,
    *,
    section_id: str = "s1",
    run_seed: str = "semantic",
) -> list[SemanticEntity]:
    """Map bounded high-confidence spans in ``full_text`` to CASE/UCO classes."""

    if not full_text.strip():
        return []

    matches: list[SemanticEntity] = []
    seen_spans: set[tuple[int, int, str]] = set()

    for match in EMAIL_RE.finditer(full_text):
        value = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:EmailAddress",
            label=f"Email {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"email-{match.start()}"),
                    "@type": "uco-observable:EmailAddressFacet",
                    "uco-observable:addressValue": value,
                },
            ),
        )

    for match in PHONE_RE.finditer(full_text):
        value = match.group(0).strip()
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:PhoneAccount",
            label=f"Phone {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"phone-{match.start()}"),
                    "@type": "uco-observable:PhoneAccountFacet",
                    "uco-observable:accountIdentifier": value,
                },
            ),
        )

    for match in URL_RE.finditer(full_text):
        value = match.group(0).rstrip(".,;)")
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:URL",
            label=f"URL {value[:60]}",
            matched_text=value,
            start=match.start(),
            end=match.start() + len(value),
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"url-{match.start()}"),
                    "@type": "uco-observable:URLFacet",
                    "uco-observable:fullValue": value,
                },
            ),
        )

    for match in DATE_RE.finditer(full_text):
        value = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-core:Event",
            label=f"Date {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:eventType": ["document date reference"],
                "uco-core:description": f"Date reference in document text: {value}",
            },
        )

    for match in MONEY_RE.finditer(full_text):
        value = match.group(0).replace(" ", "")
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-observable:ObservableObject",
            label=f"Amount {value}",
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": f"Monetary amount referenced in document text: {value}",
            },
        )

    for match in HEADLINE_SUBJECT_RE.finditer(full_text):
        age = match.group(1)
        locality = match.group(2).strip()
        gender = match.group(3)
        span_text = match.group(0)
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-identity:Person",
            label=f"Subject ({age}-year-old {gender.lower()})",
            matched_text=span_text,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
            extra_properties={
                "uco-core:description": (
                    f"Person described in document text ({age}-year-old {gender.lower()})."
                ),
            },
        )
        if locality and locality.lower() not in {"man", "woman", "male", "female"}:
            loc_start = full_text.find(locality, match.start(), match.end())
            if loc_start >= 0:
                _add_match(
                    matches,
                    seen_spans,
                    ontology_class="uco-location:Location",
                    label=f"Location {locality}",
                    matched_text=locality,
                    start=loc_start,
                    end=loc_start + len(locality),
                    section_id=section_id,
                    run_seed=run_seed,
                    facets=(
                        {
                            "@id": _facet_id(run_seed, f"loc-{loc_start}"),
                            "@type": "uco-location:SimpleAddressFacet",
                            "uco-location:locality": locality,
                        },
                    ),
                )

    for match in ORGANIZATION_RE.finditer(full_text):
        value = re.sub(r"\s+", " ", match.group(0)).strip()
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-identity:Organization",
            label=value[:120],
            matched_text=value,
            start=match.start(),
            end=match.end(),
            section_id=section_id,
            run_seed=run_seed,
        )

    for match in LOCATION_RE.finditer(full_text):
        locality = None
        loc_start = match.start()
        loc_end = match.end()
        for group_index in range(1, (match.lastindex or 0) + 1):
            group_value = match.group(group_index)
            if group_value:
                locality = group_value.strip()
                loc_start = match.start(group_index)
                loc_end = match.end(group_index)
                break
        if not locality:
            continue
        if locality.lower() in {"man", "woman", "the", "his", "her"}:
            continue
        _add_match(
            matches,
            seen_spans,
            ontology_class="uco-location:Location",
            label=f"Location {locality}",
            matched_text=locality,
            start=loc_start,
            end=loc_end,
            section_id=section_id,
            run_seed=run_seed,
            facets=(
                {
                    "@id": _facet_id(run_seed, f"loc2-{loc_start}"),
                    "@type": "uco-location:SimpleAddressFacet",
                    "uco-location:locality": locality,
                },
            ),
        )

    charge_match = CHARGE_NARRATIVE_RE.search(full_text)
    if charge_match:
        window_start = max(0, charge_match.start() - 80)
        window_end = min(len(full_text), charge_match.end() + 120)
        window_text = full_text[window_start:window_end]
        narrative = window_text.strip()
        if narrative:
            lead_ws = window_text.index(narrative)
            anchored_start = window_start + lead_ws
            anchored_end = anchored_start + len(narrative)
            _add_match(
                matches,
                seen_spans,
                ontology_class="uco-core:Event",
                label="Law-enforcement charge or arrest narrative",
                matched_text=narrative[:400],
                start=anchored_start,
                end=min(anchored_end, anchored_start + 400),
                section_id=section_id,
                run_seed=run_seed,
                extra_properties={
                    "uco-core:eventType": ["criminal charge", "law-enforcement narrative"],
                    "uco-core:description": narrative[:500],
                },
            )

    # Stable ordering for deterministic graphs and tests.
    matches.sort(key=lambda item: (item.start, item.end, item.ontology_class, item.label))
    return matches[:MAX_SEMANTIC_ENTITIES]


def semantic_entities_to_records(
    entities: list[SemanticEntity],
) -> list[Any]:
    """Convert semantic entities into ``ExtractedRecord`` instances."""

    from document_processor import ExtractedRecord

    records: list[ExtractedRecord] = []
    for entity in entities:
        records.append(
            ExtractedRecord(
                label=entity.label,
                text=entity.matched_text[:400],
                anchor=_anchor(entity.section_id, entity.start, entity.end, entity.matched_text[:400]),
                ontology_class=entity.ontology_class,
                graph_facets=entity.graph_facets,
                extra_properties=entity.extra_properties,
            )
        )
    return records
