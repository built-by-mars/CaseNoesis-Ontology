#!/usr/bin/env python3
"""GeoSPARQL geospatial evidence exemplar for docs/recipes/geosparql-geospatial-evidence.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction
from case_uco.uco.identity import Person
from case_uco.uco.location import Location, SimpleAddressFacet

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "geosparql-geospatial.jsonld"

EXTRA_CONTEXT = {
    "geo": "http://www.opengis.net/ont/geosparql#",
    "sf": "http://www.opengis.net/ont/sf#",
    "prov": "http://www.w3.org/ns/prov#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

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
    graph.add_type(site_id, "geo:Feature")

    geometry_id = "kb:seizure-point"
    graph.upsert_node(
        geometry_id,
        types=["geo:Geometry", "sf:Point"],
        properties={
            "geo:asWKT": {
                "@type": "geo:wktLiteral",
                "@value": "POINT(-89.6501 39.7817)",
            },
        },
    )
    graph.add_property(site_id, "geo:hasGeometry", {"@id": geometry_id})

    warrant_geom_id = "kb:warrant-polygon"
    graph.upsert_node(
        warrant_geom_id,
        types=["geo:Geometry", "sf:Polygon"],
        properties={
            "geo:asWKT": {
                "@type": "geo:wktLiteral",
                "@value": "POLYGON((-89.655 39.776,-89.645 39.776,-89.645 39.787,-89.655 39.787,-89.655 39.776))",
            },
            "uco-core:description": ["Search warrant authorized area (synthetic)."],
        },
    )

    cell_sector_geom_id = "kb:cell-sector-polygon"
    graph.upsert_node(
        cell_sector_geom_id,
        types=["geo:Geometry", "sf:Polygon"],
        properties={
            "geo:asWKT": {
                "@type": "geo:wktLiteral",
                "@value": "POLYGON((-89.660 39.770,-89.640 39.770,-89.635 39.790,-89.665 39.790,-89.660 39.770))",
            },
            "uco-core:description": ["Cell-sector coverage polygon from tower dump (synthetic)."],
        },
    )

    route_geom_id = "kb:vehicle-route"
    graph.upsert_node(
        route_geom_id,
        types=["geo:Geometry", "sf:LineString"],
        properties={
            "geo:asWKT": {
                "@type": "geo:wktLiteral",
                "@value": "LINESTRING(-89.6501 39.7817,-89.6480 39.7830,-89.6450 39.7850)",
            },
            "uco-core:description": ["Suspect vehicle route reconstructed from ALPR hits (synthetic)."],
        },
    )

    analytic_geom_id = "kb:analyst-bounding-polygon"
    graph.upsert_node(
        analytic_geom_id,
        types=["geo:Geometry", "sf:Polygon"],
        properties={
            "geo:asWKT": {
                "@type": "geo:wktLiteral",
                "@value": "POLYGON((-89.66 39.77,-89.64 39.77,-89.64 39.79,-89.66 39.79,-89.66 39.77))",
            },
            "uco-core:description": [
                "Analyst-defined bounding polygon intersecting warrant and cell-sector areas — not a fixed-radius buffer.",
            ],
        },
    )

    analyst_id = "kb:analyst-1"
    analyst = graph.create(Person, id=analyst_id, name="GIS Analyst (synthetic)")

    derive_action_id = "kb:action-geofence"
    graph.create(
        InvestigativeAction,
        id=derive_action_id,
        name="Derive analyst-defined bounding polygon",
        start_time=datetime(2026, 3, 16, 9, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 16, 9, 15, tzinfo=tz),
        performer=analyst,
        location=[site],
    )
    graph.add_type(derive_action_id, "prov:Activity")
    graph.link(analytic_geom_id, "prov:wasDerivedFrom", geometry_id)
    graph.link(analytic_geom_id, "prov:wasDerivedFrom", warrant_geom_id)
    graph.link(analytic_geom_id, "prov:wasDerivedFrom", cell_sector_geom_id)
    graph.link(route_geom_id, "prov:wasDerivedFrom", geometry_id)
    graph.link(analytic_geom_id, "prov:wasGeneratedBy", derive_action_id)
    graph.link(route_geom_id, "prov:wasGeneratedBy", derive_action_id)

    graph.create(
        Investigation,
        name="Synthetic case 2026-GEO-001",
        description=[
            "Location as geo:Feature; geometry separate; warrant, cell-sector, route, and analyst bounding polygon with provenance.",
        ],
        object=[site],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
