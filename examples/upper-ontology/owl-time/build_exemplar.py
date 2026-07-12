#!/usr/bin/env python3
"""OWL-Time temporal evidence exemplar for docs/recipes/owl-time-temporal-evidence.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.observable import ObservableObject, FileFacet

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "owl-time-temporal.jsonld"

EXTRA_CONTEXT = {
    "time": "http://www.w3.org/2006/time#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    evidence = graph.create(
        ObservableObject,
        name="Chat export (synthetic)",
        has_facet=[FileFacet(file_name="messages.json", size_in_bytes=4096)],
    )

    action_id = "kb:action-parse"
    action = graph.create(
        InvestigativeAction,
        id=action_id,
        name="Parse chat export",
        start_time=datetime(2026, 3, 15, 14, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 15, 14, 45, tzinfo=tz),
        object=[evidence],
    )

    interval_id = "kb:interval-examination"
    graph.upsert_node(
        interval_id,
        types="time:Interval",
        properties={
            "time:hasBeginning": {"@id": "kb:instant-start"},
            "time:hasEnd": {"@id": "kb:instant-end"},
        },
    )
    graph.upsert_node(
        "kb:instant-start",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2026-03-15T14:00:00Z",
            },
        },
    )
    graph.upsert_node(
        "kb:instant-end",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2026-03-15T14:45:00Z",
            },
        },
    )
    graph.add_property(action_id, "time:hasTime", {"@id": interval_id})

    open_interval_id = "kb:interval-open-custody"
    graph.upsert_node(
        open_interval_id,
        types="time:Interval",
        properties={
            "time:hasBeginning": {"@id": "kb:instant-custody-start"},
        },
    )
    graph.upsert_node(
        "kb:instant-custody-start",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2026-03-10T09:00:00-05:00",
            },
        },
    )
    graph.add_property(graph.get_id(evidence), "time:hasTime", {"@id": open_interval_id})

    graph.create(
        Investigation,
        name="Synthetic case 2026-TIME-001",
        description=[
            "Native Action timestamps plus OWL-Time Interval/Instant resources.",
            "Open interval models ongoing custody; clock-corrected instant uses offset.",
        ],
        object=[evidence, action],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
