#!/usr/bin/env python3
"""BFO foundational typing exemplar for docs/recipes/foundational-typing-bfo-gufo.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.identity import Organization, Person
from case_uco.uco.location import Location, SimpleAddressFacet
from case_uco.uco.observable import ContentDataFacet, ObservableObject, FileFacet
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

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

    org_id = "kb:lab-org"
    org = graph.create(Organization, id=org_id, name="Regional DF Lab (synthetic)")
    graph.add_type(org_id, "obo:BFO_0000027")  # Object aggregate

    site_id = "kb:seizure-site"
    site = graph.create(
        Location,
        id=site_id,
        name="Seizure address (synthetic)",
        has_facet=[SimpleAddressFacet(
            street="100 Main St",
            locality="Springfield",
            region="IL",
            postal_code="62701",
            country="US",
        )],
    )
    graph.add_type(site_id, "obo:BFO_0000006")  # Spatial region

    storage_id = "kb:storage-medium"
    storage = graph.create(
        ObservableObject,
        id=storage_id,
        name="Seized workstation HDD (physical storage medium)",
        has_facet=[FileFacet(file_name="\\\\.\\PhysicalDrive0", size_in_bytes=500_000_000_000)],
    )
    graph.add_type(storage_id, "obo:BFO_0000040")  # Material entity

    carrier_id = "kb:e01-carrier"
    carrier = graph.create(
        ObservableObject,
        id=carrier_id,
        name="E01 forensic container file (physical carrier)",
        has_facet=[FileFacet(file_name="workstation.e01", size_in_bytes=500_000_000_000)],
    )
    graph.add_type(carrier_id, "obo:BFO_0000040")  # Material entity — distinct from source medium

    content_id = "kb:disk-content"
    content = graph.create(
        ObservableObject,
        id=content_id,
        name="Recovered disk information content (logical artifact)",
        has_facet=[
            ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="c" * 64)]),
        ],
    )
    # BFO_0000031 (generically dependent continuant) — information content artifact
    graph.add_type(content_id, "obo:BFO_0000031")

    tool_id = "kb:imager"
    tool = graph.create(Tool, id=tool_id, name="Forensic imager", version="4.21.0")
    graph.add_type(tool_id, "obo:BFO_0000040")  # Material entity (instrument)

    action_id = "kb:action-image"
    action = graph.create(
        InvestigativeAction,
        id=action_id,
        name="Forensic imaging",
        start_time=datetime(2026, 3, 15, 10, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 15, 12, 30, tzinfo=tz),
        performer=person,
        object=[storage],
        result=[carrier, content],
        instrument=[tool],
        location=[site],
    )
    graph.add_type(action_id, "obo:BFO_0000015")  # Process — not spatiotemporal region

    graph.create(
        Investigation,
        name="Synthetic case 2026-BFO-001",
        description=[
            "BFO enrichment on CASE/UCO domain types (same IRI).",
            "Storage medium, E01 carrier, and information content are distinct nodes.",
        ],
        object=[storage, carrier, content, action, org],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
