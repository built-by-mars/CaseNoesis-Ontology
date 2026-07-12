#!/usr/bin/env python3
"""BFO foundational typing exemplar for docs/recipes/foundational-typing-bfo-gufo.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.identity import Person
from case_uco.uco.observable import ObservableObject, FileFacet

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "foundational-typing-bfo.jsonld"

EXTRA_CONTEXT = {
    "obo": "http://purl.obolibrary.org/obo/",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    person_id = "kb:examiner-1"
    person = graph.create(Person, id=person_id, name="Examiner One (synthetic)")
    graph.add_type(person_id, "obo:BFO_0000002")  # Continuant

    evidence_id = "kb:evidence-1"
    evidence = graph.create(
        ObservableObject,
        id=evidence_id,
        name="Seized workstation drive image (synthetic)",
        has_facet=[FileFacet(file_name="workstation.e01", size_in_bytes=500_000_000_000)],
    )
    graph.add_type(evidence_id, "obo:BFO_0000040")  # Material entity

    action_id = "kb:action-image"
    action = graph.create(
        InvestigativeAction,
        id=action_id,
        name="Forensic imaging",
        start_time=datetime(2026, 3, 15, 10, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 15, 12, 30, tzinfo=tz),
        performer=person,
        object=[evidence],
    )
    graph.add_type(action_id, "obo:BFO_0000011")  # Spatiotemporal region / process

    graph.create(
        Investigation,
        name="Synthetic case 2026-BFO-001",
        description=["BFO enrichment on CASE/UCO domain types (same IRI)."],
        object=[evidence, action],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
