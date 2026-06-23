# Cargo Theft, Route Staging, and Warehouse Movement

> See [Recipe Index](INDEX.md) for all recipes.

Model freight route theft, warehouse staging, manifest anomalies, and geofence-correlated movement investigations using core CASE/UCO types. This recipe supports synthetic public-safe cargo-theft fixtures and real cases where planners discuss routes in chat, trailers deviate from geofenced corridors, and stolen goods move through leased storage facilities.

## Scope

| Layer | What it captures | Primary classes |
|---|---|---|
| **Planning communications** | Route timing chats, staging notes | `MessageThread`, `Message`, `Person` |
| **Movement evidence** | GPS/geofence hits, ELD logs, toll records | `Location`, `GeoLocationEntryFacet`, `Event` |
| **Cargo artifacts** | Manifests, bills of lading, seal numbers | `File`, `FileFacet`, `ContentDataFacet` |
| **Vehicles & trailers** | Tractor/trailer IDs, VINs, license plates | `Vehicle`, `DeviceFacet`, `ObservableObject` |
| **Storage staging** | Warehouse leases, unit numbers | `Location`, `Organization`, `Relationship` |
| **Proceeds linkage** | Resale listings, downstream transfers (when present) | `InvestigativeAction`, `Relationship` |

## Key classes

| Class | Role |
|---|---|
| `Investigation` | Case container for route theft or warehouse staging |
| `InvestigativeAction` | Manifest review, geofence analysis, warehouse search |
| `Person` / `Organization` | Drivers, dispatchers, lessees, carrier companies |
| `Vehicle` + `DeviceFacet` | Tractors, trailers, GPS/telematics devices |
| `Location` + facets | Warehouses, geofence polygons, corridor waypoints |
| `Event` | Deviation alerts, arrival/departure timestamps |
| `File` + `FileFacet` | Manifest PDFs, ELD exports, lease agreements |
| `MessageThread` | Planning chats coordinating theft or staging |
| `Relationship` | `Located_At`, `Contained_Within`, `Associated_With`, `Transferred_To` |
| `ProvenanceRecord` | Links manifest analysis back to source TMS export |

## Pattern

```
Investigation
    ├── object ──▶ MessageThread (route planning chat)
    ├── object ──▶ Vehicle (tractor + trailer observables)
    ├── object ──▶ File (manifest / BOL) with ContentDataFacet hash
    ├── object ──▶ InvestigativeAction (geofence deviation analysis)
    │                 ├── object ──▶ Location corridor + deviation Event nodes
    │                 └── result ──▶ staging Location (warehouse unit)
    └── object ──▶ InvestigativeAction (warehouse search)
                      └── result ──▶ recovered cargo ObservableObject
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Person, Organization
from case_uco.uco.core import Relationship, Event
from case_uco.uco.tool import Tool
from case_uco.uco.observable import (
    ObservableObject, Vehicle, File,
    FileFacet, ContentDataFacet, MessageFacet, MessageThreadFacet,
    DeviceFacet,
)
from case_uco.uco.location import Location, SimpleAddressFacet, GeoLocationEntryFacet
from case_uco.uco.types import Hash

graph = CASEGraph(kb_prefix="http://example.org/kb/")

carrier = graph.create(Organization, name="Pacific Rim Logistics")
driver = graph.create(Person, name="Jordan Ellis")
dispatcher = graph.create(Person, name="Riley Chen")

planning_thread = graph.create(
    ObservableObject,
    has_facet=[MessageThreadFacet(participant=[driver, dispatcher])],
)
graph.create(
    ObservableObject,
    has_facet=[
        MessageFacet(
            message_text="Switch to staging yard after mile marker 112.",
            from_=dispatcher,
        )
    ],
)

tractor = graph.create(
    Vehicle,
    has_facet=[
        DeviceFacet(device_identifier="TRK-4410"),
    ],
)
manifest = graph.create(
    File,
    has_facet=[
        FileFacet(file_name="manifest-seal-8841.pdf", size_in_bytes=128000),
        ContentDataFacet(
            hash=[Hash(hash_method=["SHA-256"], hash_value="abc123…")],
        ),
    ],
)

corridor = graph.create(
    Location,
    name="I-5 southbound corridor segment",
    has_facet=[GeoLocationEntryFacet(location_value="37.3,-121.8")],
)
staging_yard = graph.create(
    Location,
    has_facet=[
        SimpleAddressFacet(
            street="2200 Industrial Blvd",
            locality="Stockton",
            region="California",
            postal_code="95206",
        )
    ],
)
deviation_event = graph.create(
    Event,
    name="Geofence deviation alert",
    event_type=["route deviation"],
    description="Trailer TRL-902 left authorized corridor at 02:14 UTC.",
)

geofence_tool = graph.create(Tool, name="Fleet Geofence Analyzer", version="3.2")
geofence_action = graph.create(
    InvestigativeAction,
    name="Analyze ELD geofence export",
    instrument=geofence_tool,
    object=[tractor, manifest],
    result=[deviation_event, staging_yard],
)

warehouse_search = graph.create(
    InvestigativeAction,
    name="Search leased warehouse unit 14B",
    object=[staging_yard],
)

investigation = graph.create(
    Investigation,
    name="Synthetic cargo theft route staging 2026-001",
    object=[planning_thread, geofence_action, warehouse_search],
)

graph.create(
    Relationship,
    source=[tractor],
    target=[deviation_event],
    kind_of_relationship="Associated_With",
    is_directional=True,
)
graph.create(
    Relationship,
    source=[staging_yard],
    target=[carrier],
    kind_of_relationship="Leased_By",
    is_directional=True,
)

graph.write("cargo-theft-route.jsonld")
graph.validate()
```

</details>

## Validation queries

```sparql
PREFIX case-investigation: <https://unifiedcyberontology.org/ontology/case/investigation#>
PREFIX uco-action: <https://unifiedcyberontology.org/ontology/uco/action#>

# Manifest review actions should reference the manifest file as object or result
SELECT ?action ?manifest WHERE {
  ?action a case-investigation:InvestigativeAction ;
          uco-action:object|uco-action:result ?manifest .
  ?manifest a uco-observable:File .
}

# Staging locations should link to at least one investigative action
SELECT ?loc WHERE {
  ?loc a uco-location:Location .
  FILTER NOT EXISTS {
    ?action uco-action:object|uco-action:result ?loc .
    ?action a case-investigation:InvestigativeAction .
  }
}
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Modeling the trailer deviation as only a `Location` label | Add an explicit `Event` with timestamp and link the `Vehicle` via `Relationship` |
| Flattening manifest anomalies into investigation description text | Create `File` nodes with hashes and an `InvestigativeAction` that references them |
| Treating warehouse lease PDFs as unstructured blobs | Extract lease holder `Organization`/`Person` and warehouse `Location` as typed nodes |
| Skipping chat planning evidence | Use `MessageThread` + `MessageFacet` rather than paraphrasing in `Investigation.description` |
| Merging carrier, driver, and lessee without role separation | Keep distinct `Person`/`Organization` nodes until identity resolution is documented |

## Related recipes

- [threaded-messaging.md](threaded-messaging.md) — route planning chats
- [location.md](location.md) — warehouse addresses and geofences
- [device.md](device.md) — telematics hardware on tractors/trailers
- [file-system.md](file-system.md) — manifest and lease document handling
- [chain-of-custody.md](chain-of-custody.md) — recovered cargo handling
