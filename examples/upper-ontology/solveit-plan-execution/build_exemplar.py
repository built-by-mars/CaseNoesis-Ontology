#!/usr/bin/env python3
"""SOLVE-IT plan vs execution exemplar for docs/recipes/solveit-plan-execution-provenance.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation
from case_uco.uco.identity import Person
from case_uco.uco.observable import ObservableObject, FileFacet
from case_uco.uco.tool import Tool

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "solveit-plan-execution.jsonld"

SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"

EXTRA_CONTEXT = {
    "prov": "http://www.w3.org/ns/prov#",
    "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
    "solveit-data": SOLVEIT_DATA,
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    plan_id = "kb:acquisition-plan"
    graph.upsert_node(
        plan_id,
        types="prov:Plan",
        properties={
            "uco-core:name": "Laptop acquisition plan (synthetic)",
            "uco-core:description": [
                "Planned steps: write-block, sector copy (DFT-1002), hash verify (DFT-1042).",
            ],
        },
    )

    examiner_id = "kb:examiner-1"
    examiner = graph.create(Person, id=examiner_id, name="Examiner One (synthetic)")

    tool = graph.create(Tool, name="Hardware write blocker + imager", version="2026.1")
    source_id = "kb:laptop-ssd"
    source = graph.create(
        ObservableObject,
        id=source_id,
        name="Seized laptop SSD (synthetic)",
        has_facet=[FileFacet(file_name="\\\\.\\PhysicalDrive2")],
    )

    image_id = "kb:disk-image"
    image = graph.create(
        ObservableObject,
        id=image_id,
        name="E01 physical image",
        has_facet=[FileFacet(file_name="laptop.e01", size_in_bytes=256_000_000_000)],
    )

    planned_action_id = "kb:action-planned-image"
    graph.upsert_node(
        planned_action_id,
        types=[
            "case-investigation:InvestigativeAction",
            "solveit-core:SolveitInvestigativeAction",
            "prov:Activity",
        ],
        properties={
            "uco-core:name": "Acquire laptop image (planned)",
            "solveit-core:usedTechnique": [{"@id": "solveit-data:techniqueDFT-1002"}],
            "uco-action:performer": {"@id": examiner_id},
            "uco-action:object": [{"@id": source_id}],
            "uco-action:instrument": [{"@id": graph.get_id(tool)}],
            "prov:hadPlan": {"@id": plan_id},
        },
    )

    executed_action_id = "kb:action-executed-image"
    graph.upsert_node(
        executed_action_id,
        types=[
            "case-investigation:InvestigativeAction",
            "solveit-core:SolveitInvestigativeAction",
            "prov:Activity",
        ],
        properties={
            "uco-core:name": "Acquire laptop image (executed — partial sectors)",
            "uco-core:description": [
                "Deviation: imaging stopped at 40% due to bad sector cluster; re-execution scheduled.",
            ],
            "solveit-core:usedTechnique": [{"@id": "solveit-data:techniqueDFT-1002"}],
            "solveit-core:appliedMitigation": [{"@id": "solveit-data:mitigationDFM-1003"}],
            "uco-action:startTime": {
                "@type": "xsd:dateTime",
                "@value": datetime(2026, 3, 15, 10, 0, tzinfo=tz).isoformat(),
            },
            "uco-action:endTime": {
                "@type": "xsd:dateTime",
                "@value": datetime(2026, 3, 15, 11, 20, tzinfo=tz).isoformat(),
            },
            "uco-action:performer": {"@id": examiner_id},
            "uco-action:object": [{"@id": source_id}],
            "uco-action:result": [{"@id": image_id}],
            "prov:hadPlan": {"@id": plan_id},
        },
    )

    reexec_action_id = "kb:action-reexecute-image"
    graph.upsert_node(
        reexec_action_id,
        types=[
            "case-investigation:InvestigativeAction",
            "solveit-core:SolveitInvestigativeAction",
            "prov:Activity",
        ],
        properties={
            "uco-core:name": "Re-execute imaging after bad-sector remediation",
            "solveit-core:usedTechnique": [{"@id": "solveit-data:techniqueDFT-1002"}],
            "solveit-core:appliedMitigation": [
                {"@id": "solveit-data:mitigationDFM-1003"},
                {"@id": "solveit-data:mitigationDFM-1004"},
            ],
            "uco-action:performer": {"@id": examiner_id},
            "uco-action:object": [{"@id": source_id}],
            "prov:hadPlan": {"@id": plan_id},
        },
    )
    graph.link(reexec_action_id, "prov:wasRevisionOf", executed_action_id)

    graph.create(
        Investigation,
        name="Synthetic case 2026-SOLVEIT-PLAN-001",
        description=["prov:Plan vs SolveitInvestigativeAction execution with deviation and re-execution."],
        object=[source, image],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
