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
    "solveit-wa": "https://ontology.solveit-df.org/solveit/weakness-assessment/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    plan_id = "kb:acquisition-plan"
    graph.upsert_node(
        plan_id,
        types=["prov:Plan", "uco-core:UcoObject"],
        properties={
            "uco-core:name": "Laptop acquisition plan (synthetic)",
            "uco-core:description": [
                "Planned steps: write-block, sector copy (DFT-1002), hash verify (DFT-1042).",
            ],
        },
    )

    examiner_id = "kb:examiner-1"
    graph.create(Person, id=examiner_id, name="Examiner One (synthetic)")
    graph.add_type(examiner_id, "prov:Agent")

    tool = graph.create(Tool, name="Hardware write blocker + imager", version="2026.1")
    tool_id = graph.get_id(tool)
    graph.add_type(tool_id, "prov:Entity")

    source_id = "kb:laptop-ssd"
    source = graph.create(
        ObservableObject,
        id=source_id,
        name="Seized laptop SSD (synthetic)",
        has_facet=[FileFacet(file_name="\\\\.\\PhysicalDrive2")],
    )
    graph.add_type(source_id, "prov:Entity")

    partial_image_id = "kb:disk-image-partial"
    partial_image = graph.create(
        ObservableObject,
        id=partial_image_id,
        name="E01 physical image (partial — 40% sectors)",
        has_facet=[FileFacet(file_name="laptop-partial.e01", size_in_bytes=102_400_000_000)],
    )
    graph.add_type(partial_image_id, "prov:Entity")

    corrected_image_id = "kb:disk-image-corrected"
    corrected_image = graph.create(
        ObservableObject,
        id=corrected_image_id,
        name="E01 physical image (corrected — complete)",
        has_facet=[FileFacet(file_name="laptop.e01", size_in_bytes=256_000_000_000)],
    )
    graph.add_type(corrected_image_id, "prov:Entity")
    graph.link(corrected_image_id, "prov:wasRevisionOf", partial_image_id)

    association_id = "kb:association-examiner-plan"
    graph.upsert_node(
        association_id,
        types="prov:Association",
        properties={
            "prov:agent": {"@id": examiner_id},
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
            "uco-action:result": [{"@id": partial_image_id}],
            "uco-action:instrument": [{"@id": tool_id}],
            "prov:qualifiedAssociation": {"@id": association_id},
        },
    )
    graph.link(partial_image_id, "prov:wasGeneratedBy", executed_action_id)
    graph.link(partial_image_id, "prov:wasDerivedFrom", source_id)

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
            "uco-action:startTime": {
                "@type": "xsd:dateTime",
                "@value": datetime(2026, 3, 15, 14, 0, tzinfo=tz).isoformat(),
            },
            "uco-action:endTime": {
                "@type": "xsd:dateTime",
                "@value": datetime(2026, 3, 15, 16, 30, tzinfo=tz).isoformat(),
            },
            "uco-action:performer": {"@id": examiner_id},
            "uco-action:object": [{"@id": source_id}],
            "uco-action:result": [{"@id": corrected_image_id}],
            "uco-action:instrument": [{"@id": tool_id}],
            "prov:qualifiedAssociation": {"@id": association_id},
        },
    )
    graph.link(corrected_image_id, "prov:wasGeneratedBy", reexec_action_id)
    graph.link(corrected_image_id, "prov:wasDerivedFrom", source_id)
    graph.link(partial_image_id, "prov:wasInvalidatedBy", reexec_action_id)

    eval_dfw1002_id = "kb:eval-dfw-1002"
    graph.upsert_node(
        eval_dfw1002_id,
        types="solveit-wa:WeaknessEvaluation",
        properties={
            "uco-core:name": "DFW-1002 evaluation for laptop SSD acquisition",
            "solveit-wa:evaluatesWeakness": {"@id": "solveit-data:weaknessDFW-1002"},
            "solveit-wa:likelihoodRating": {"@type": "xsd:integer", "@value": "2"},
            "solveit-wa:likelihoodRationale": "Triage tooling not used; dedicated imager with write-blocker.",
            "solveit-wa:impactRating": {"@type": "xsd:integer", "@value": "3"},
            "solveit-wa:impactRationale": "Media alteration would undermine admissibility of the image.",
            "solveit-wa:liImpactScore": {"@type": "xsd:integer", "@value": "6"},
        },
    )

    eval_dfw1004_id = "kb:eval-dfw-1004"
    graph.upsert_node(
        eval_dfw1004_id,
        types="solveit-wa:WeaknessEvaluation",
        properties={
            "uco-core:name": "DFW-1004 evaluation for laptop SSD acquisition",
            "solveit-wa:evaluatesWeakness": {"@id": "solveit-data:weaknessDFW-1004"},
            "solveit-wa:likelihoodRating": {"@type": "xsd:integer", "@value": "1"},
            "solveit-wa:likelihoodRationale": "Hardware write blocker; no damaged-media indicators before run.",
            "solveit-wa:impactRating": {"@type": "xsd:integer", "@value": "3"},
            "solveit-wa:impactRationale": "Missing sectors would silently omit evidence from the examination.",
            "solveit-wa:liImpactScore": {"@type": "xsd:integer", "@value": "3"},
        },
    )

    eval_set_id = "kb:weakness-eval-set"
    graph.upsert_node(
        eval_set_id,
        types="solveit-wa:WeaknessEvaluationSet",
        properties={
            "uco-core:name": "Acquisition weakness assessment session",
            "solveit-wa:scopedToTechnique": {"@id": "solveit-data:techniqueDFT-1002"},
            "solveit-wa:evaluatedBy": {"@id": examiner_id},
            "solveit-wa:hasEvaluation": [
                {"@id": eval_dfw1002_id},
                {"@id": eval_dfw1004_id},
            ],
            "solveit-wa:evaluationDate": {"@type": "xsd:date", "@value": "2026-03-14"},
        },
    )

    graph.create(
        Investigation,
        name="Synthetic case 2026-SOLVEIT-PLAN-001",
        description=[
            "prov:Plan (UcoObject) vs SolveitInvestigativeAction execution with deviation, re-execution, and weakness assessment.",
            "Plan linkage via prov:Association + qualifiedAssociation; partial result invalidated by re-execution.",
        ],
        object=[source, partial_image, corrected_image],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
