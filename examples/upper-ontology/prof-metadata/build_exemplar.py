#!/usr/bin/env python3
"""PROF validation profile metadata exemplar for docs/recipes/prof-validation-profile-metadata.md."""

from __future__ import annotations

from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "prof-metadata.jsonld"

EXTRA_CONTEXT = {
    "prof": "http://www.w3.org/ns/dx/prof/",
    "dcterms": "http://purl.org/dc/terms/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)

    profile_id = "kb:profile-case-uco-1.4"
    graph.upsert_node(
        profile_id,
        types="prof:Profile",
        properties={
            "dcterms:title": "CASE/UCO 1.4.0 investigation graph",
            "prof:isProfileOf": "https://ontology.unifiedcyberontology.org/uco/",
        },
    )

    shapes_descriptor_id = "kb:descriptor-shacl"
    graph.upsert_node(
        shapes_descriptor_id,
        types="prof:ResourceDescriptor",
        properties={
            "prof:hasRole": "http://www.w3.org/ns/dx/prof/ValidationRole",
            "dcterms:format": "text/turtle",
            "dcterms:description": "CASE/UCO SHACL shapes bundle used for conformance checking.",
        },
    )
    graph.add_property(profile_id, "prof:hasResource", {"@id": shapes_descriptor_id})

    validation_report_id = "kb:validation-report-1"
    graph.upsert_node(
        validation_report_id,
        types="uco-core:UcoObject",
        properties={
            "uco-core:name": "Validation run 2026-03-15",
            "uco-core:description": [
                "SHACL conformance result for synthetic exemplar — distinct from profile intent metadata.",
            ],
        },
    )

    graph.create(
        Investigation,
        name="Synthetic case 2026-PROF-001",
        description=["Graph carries PROF profile intent; validation results are separate resources."],
        object=[],
    )
    graph.add_property("kb:profile-case-uco-1.4", "prof:hasArtifact", {"@id": validation_report_id})
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
