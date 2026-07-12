#!/usr/bin/env python3
"""Cross-ontology composition exemplar for docs/recipes/cross-ontology-composition.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Organization, Person
from case_uco.uco.location import Location, LatLongCoordinatesFacet
from case_uco.uco.observable import (
    ContentDataFacet,
    DeviceFacet,
    FileFacet,
    MobileDeviceFacet,
    ObservableObject,
)
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
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    """Composite graph: gUFO (not BFO) + PROV-O + OWL-Time + GeoSPARQL + FOAF/ORG."""
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    role_id = "kb:role-examiner"
    graph.upsert_node(
        role_id,
        types=["org:Role", "skos:Concept"],
        properties={"skos:prefLabel": "Mobile forensic examiner"},
    )

    org_id = "kb:taskforce"
    org = graph.create(Organization, id=org_id, name="Metro ICAC Task Force (synthetic)")
    graph.add_type(org_id, "org:Organization")
    graph.add_type(org_id, "foaf:Organization")

    person_id = "kb:examiner-1"
    person = graph.create(Person, id=person_id, name="Examiner One (synthetic)")
    graph.add_type(person_id, "foaf:Person")
    graph.add_type(person_id, "gufo:Object")
    graph.add_type(person_id, "prov:Agent")

    membership_id = "kb:membership-1"
    graph.upsert_node(
        membership_id,
        types="org:Membership",
        properties={
            "org:member": {"@id": person_id},
            "org:organization": {"@id": org_id},
            "org:role": {"@id": role_id},
        },
    )
    graph.add_property(org_id, "org:hasMembership", {"@id": membership_id})

    site_id = "kb:seizure-site"
    site = graph.create(
        Location,
        id=site_id,
        name="Seizure coordinates (synthetic)",
        has_facet=[LatLongCoordinatesFacet(latitude=39.7817, longitude=-89.6501)],
    )
    graph.add_type(site_id, "geo:Feature")
    graph.add_type(site_id, "gufo:Object")
    geom_id = "kb:site-point"
    graph.upsert_node(
        geom_id,
        types=["geo:Geometry", "sf:Point"],
        properties={
            "geo:asWKT": {"@type": "geo:wktLiteral", "@value": "POINT(-89.6501 39.7817)"},
        },
    )
    graph.add_property(site_id, "geo:hasGeometry", {"@id": geom_id})

    source_id = "kb:source-phone"
    source = graph.create(
        ObservableObject,
        id=source_id,
        name="Seized mobile device (source storage, synthetic)",
        has_facet=[
            DeviceFacet(device_type="mobile phone", model="Synthetic Phone X", serial_number="SYN-PHONE-001"),
            MobileDeviceFacet(imei=["990000862471854"], storage_capacity_in_bytes=128_000_000_000),
        ],
    )
    graph.add_type(source_id, "prov:Entity")
    graph.add_type(source_id, "gufo:FunctionalComplex")

    image_id = "kb:evidence-phone-image"
    image = graph.create(
        ObservableObject,
        id=image_id,
        name="Mobile device forensic image (acquisition result, synthetic)",
        has_facet=[
            FileFacet(file_name="phone.ufd", size_in_bytes=64_000_000_000),
            ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="b" * 64)]),
        ],
    )
    graph.add_type(image_id, "prov:Entity")
    graph.add_type(image_id, "gufo:FunctionalComplex")

    tool_id = "kb:imager"
    tool = graph.create(Tool, id=tool_id, name="Mobile imager", version="5.2")
    graph.add_type(tool_id, "prov:Entity")

    # Acquisition chain: source device → InvestigativeAction → forensic image
    # (never reuse the same ObservableObject as both input and generated result).
    action_id = "kb:action-acquire"
    action = graph.create(
        InvestigativeAction,
        id=action_id,
        name="Mobile device acquisition",
        start_time=datetime(2026, 3, 15, 10, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 15, 11, 30, tzinfo=tz),
        performer=person,
        object=[source],
        result=[image],
        instrument=[tool],
        location=[site],
    )
    graph.add_type(action_id, "prov:Activity")
    graph.add_type(action_id, "gufo:Event")
    graph.link(image_id, "prov:wasGeneratedBy", action_id)
    graph.link(image_id, "prov:wasDerivedFrom", source_id)
    graph.link(action_id, "prov:used", tool_id)
    graph.link(action_id, "prov:wasAssociatedWith", person_id)

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
    graph.add_property(image_id, "time:hasTime", {"@id": interval_id})

    provenance = graph.create(
        ProvenanceRecord,
        name="Exhibit 1 provenance",
        exhibit_number="EX-001",
        object=[source, image, action],
    )

    graph.create(
        Investigation,
        name="Synthetic composite case 2026-COMP-001",
        description=[
            "Cross-ontology composition: gUFO + PROV-O + OWL-Time + GeoSPARQL + FOAF/ORG on one graph.",
            "Acquisition chain: source device/storage → acquisition activity → forensic image (distinct IRIs).",
            "BFO deliberately omitted — never combine BFO and gUFO on the same graph.",
        ],
        object=[source, image, provenance, org],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
