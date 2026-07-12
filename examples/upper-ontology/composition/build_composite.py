#!/usr/bin/env python3
"""Cross-ontology composition exemplar for docs/recipes/cross-ontology-composition.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Identity, Person
from case_uco.uco.location import Location, LatLongCoordinatesFacet
from case_uco.uco.observable import ContentDataFacet, ObservableObject, FileFacet
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cross-ontology-composite.jsonld"

EXTRA_CONTEXT = {
    "gufo": "http://purl.org/nemo/gufo#",
    "prov": "http://www.w3.org/ns/prov#",
    "time": "http://www.w3.org/2006/time#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "sf": "http://www.opengis.net/ont/sf#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "org": "http://www.w3.org/ns/org#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    """Composite graph: gUFO (not BFO) + PROV-O + OWL-Time + GeoSPARQL + FOAF/ORG."""
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    org_id = "kb:taskforce"
    org = graph.create(Identity, id=org_id, name="Metro ICAC Task Force (synthetic)")
    graph.add_type(org_id, "org:Organization")
    graph.add_type(org_id, "foaf:Organization")

    person_id = "kb:examiner-1"
    person = graph.create(Person, id=person_id, name="Examiner One (synthetic)")
    graph.add_type(person_id, "foaf:Person")
    graph.add_type(person_id, "gufo:Object")
    graph.add_type(person_id, "prov:Agent")

    site_id = "kb:seizure-site"
    site = graph.create(
        Location,
        id=site_id,
        name="Seizure coordinates (synthetic)",
        has_facet=[LatLongCoordinatesFacet(latitude=39.7817, longitude=-89.6501)],
    )
    graph.add_type(site_id, "geo:Feature")
    geom_id = "kb:site-point"
    graph.upsert_node(
        geom_id,
        types=["geo:Geometry", "sf:Point"],
        properties={
            "geo:asWKT": {"@type": "geo:wktLiteral", "@value": "POINT(-89.6501 39.7817)"},
        },
    )
    graph.add_property(site_id, "geo:hasGeometry", {"@id": geom_id})

    evidence_id = "kb:evidence-phone"
    evidence = graph.create(
        ObservableObject,
        id=evidence_id,
        name="Seized mobile device image (synthetic)",
        has_facet=[
            FileFacet(file_name="phone.ufd", size_in_bytes=64_000_000_000),
            ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="b" * 64)]),
        ],
    )
    graph.add_type(evidence_id, "prov:Entity")
    graph.add_type(evidence_id, "gufo:FunctionalComplex")

    tool_id = "kb:imager"
    tool = graph.create(Tool, id=tool_id, name="Mobile imager", version="5.2")
    graph.add_type(tool_id, "prov:Entity")

    action_id = "kb:action-acquire"
    action = graph.create(
        InvestigativeAction,
        id=action_id,
        name="Mobile device acquisition",
        start_time=datetime(2026, 3, 15, 10, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 15, 11, 30, tzinfo=tz),
        performer=person,
        object=[evidence],
        instrument=[tool],
        location=[site],
    )
    graph.add_type(action_id, "prov:Activity")
    graph.add_type(action_id, "gufo:Event")
    graph.link(evidence_id, "prov:wasGeneratedBy", action_id)

    interval_id = "kb:interval-custody"
    graph.upsert_node(
        interval_id,
        types="time:Interval",
        properties={
            "time:hasBeginning": {"@id": "kb:instant-custody-start"},
            "time:hasEnd": {"@id": "kb:instant-custody-end"},
        },
    )
    graph.upsert_node(
        "kb:instant-custody-start",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2026-03-15T10:00:00Z",
            },
        },
    )
    graph.upsert_node(
        "kb:instant-custody-end",
        types="time:Instant",
        properties={
            "time:inXSDDateTimeStamp": {
                "@type": "xsd:dateTimeStamp",
                "@value": "2026-03-15T18:00:00Z",
            },
        },
    )
    graph.add_property(evidence_id, "time:hasTime", {"@id": interval_id})

    provenance = graph.create(
        ProvenanceRecord,
        name="Exhibit 1 provenance",
        exhibit_number="EX-001",
        object=[evidence, action],
    )

    graph.create(
        Investigation,
        name="Synthetic composite case 2026-COMP-001",
        description=[
            "Cross-ontology composition: gUFO + PROV-O + OWL-Time + GeoSPARQL + FOAF/ORG on one graph.",
            "BFO deliberately omitted — never combine BFO and gUFO on the same graph.",
        ],
        object=[evidence, provenance, org],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
