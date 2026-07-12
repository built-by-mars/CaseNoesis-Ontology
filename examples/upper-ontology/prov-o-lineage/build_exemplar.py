#!/usr/bin/env python3
"""PROV-O evidence lineage exemplar for docs/recipes/prov-o-evidence-lineage.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Person
from case_uco.uco.observable import ObservableObject, ContentDataFacet, FileFacet
from case_uco.uco.tool import Tool
from case_uco.uco.types import Hash

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "prov-o-lineage.jsonld"

EXTRA_CONTEXT = {
    "prov": "http://www.w3.org/ns/prov#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    examiner_id = "kb:examiner-1"
    examiner = graph.create(Person, id=examiner_id, name="Examiner One (synthetic)")
    graph.add_type(examiner_id, "prov:Agent")

    tool_id = "kb:hash-tool"
    tool = graph.create(Tool, id=tool_id, name="HashCalc", version="2.1.0")
    graph.add_type(tool_id, "prov:Entity")

    source_id = "kb:source-drive"
    source = graph.create(
        ObservableObject,
        id=source_id,
        name="Seized workstation drive (synthetic)",
        has_facet=[FileFacet(file_name="\\\\.\\PhysicalDrive1")],
    )
    graph.add_type(source_id, "prov:Entity")

    image_id = "kb:disk-image"
    image = graph.create(
        ObservableObject,
        id=image_id,
        name="Forensic E01 image",
        has_facet=[
            FileFacet(file_name="workstation.e01", size_in_bytes=500_000_000_000),
            ContentDataFacet(hash=[Hash(hash_method="SHA256", hash_value="a" * 64)]),
        ],
    )
    graph.add_type(image_id, "prov:Entity")
    graph.link(image_id, "prov:wasDerivedFrom", source_id)

    action_id = "kb:action-image"
    action = graph.create(
        InvestigativeAction,
        id=action_id,
        name="Forensic imaging and hashing",
        start_time=datetime(2026, 3, 15, 10, 0, tzinfo=tz),
        end_time=datetime(2026, 3, 15, 12, 30, tzinfo=tz),
        performer=examiner,
        object=[source],
        result=[image],
        instrument=[tool],
    )
    graph.add_type(action_id, "prov:Activity")
    graph.link(image_id, "prov:wasGeneratedBy", action_id)
    graph.link(action_id, "prov:used", tool_id)
    graph.link(action_id, "prov:wasAssociatedWith", examiner_id)

    provenance = graph.create(
        ProvenanceRecord,
        name="Exhibit 1 digital lineage",
        exhibit_number="EX-001",
        object=[source, image, action],
    )
    graph.add_type(graph.get_id(provenance), "prov:Entity")

    graph.create(
        Investigation,
        name="Synthetic case 2026-PROV-001",
        description=["PROV-O lineage on acquisition — Tool is instrument (Entity), not Agent."],
        object=[source, image, provenance],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
