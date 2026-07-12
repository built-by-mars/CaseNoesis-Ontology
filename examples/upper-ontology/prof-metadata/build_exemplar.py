#!/usr/bin/env python3
"""PROF validation profile metadata exemplar for docs/recipes/prof-validation-profile-metadata.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "prof-metadata.jsonld"

CASE_SHAPES_IRI = "https://github.com/casework/CASE-UCO/releases/download/case-1.4.0/case-shapes.ttl"
VALIDATION_ROLE_IRI = "http://www.w3.org/ns/dx/prof/role/ValidationRole"
TURTLE_MEDIA_TYPE = "https://www.iana.org/assignments/media-types/text/turtle"

EXTRA_CONTEXT = {
    "prof": "http://www.w3.org/ns/dx/prof/",
    "dcterms": "http://purl.org/dc/terms/",
    "prov": "http://www.w3.org/ns/prov#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    profile_id = "kb:profile-case-uco-1.4"
    graph.upsert_node(
        profile_id,
        types="prof:Profile",
        properties={
            "dcterms:title": "CASE/UCO 1.4.0 investigation graph",
            "prof:isProfileOf": {"@id": "https://ontology.unifiedcyberontology.org/uco/"},
        },
    )

    shapes_descriptor_id = "kb:descriptor-shacl"
    graph.upsert_node(
        shapes_descriptor_id,
        types="prof:ResourceDescriptor",
        properties={
            "prof:hasRole": {"@id": VALIDATION_ROLE_IRI},
            "dcterms:format": {"@id": TURTLE_MEDIA_TYPE},
            "dcterms:description": "CASE/UCO SHACL shapes bundle used for conformance checking.",
            "prof:hasArtifact": {"@id": CASE_SHAPES_IRI},
        },
    )
    graph.add_property(profile_id, "prof:hasResource", {"@id": shapes_descriptor_id})

    report_v1_id = "kb:validation-report-11111111-1111-4111-8111-111111111111"
    graph.upsert_node(
        report_v1_id,
        types=["prov:Entity", "uco-core:UcoObject"],
        properties={
            "uco-core:name": "Validation run 2026-03-15 (initial)",
            "uco-core:description": [
                "SHACL conformance result for synthetic exemplar — distinct from profile intent metadata.",
            ],
        },
    )

    report_v2_id = "kb:validation-report-22222222-2222-4222-8222-222222222222"
    graph.upsert_node(
        report_v2_id,
        types=["prov:Entity", "uco-core:UcoObject"],
        properties={
            "uco-core:name": "Validation run 2026-03-16 (re-run)",
            "uco-core:description": [
                "Re-validated after graph update; supersedes the initial report.",
            ],
        },
    )
    graph.link(report_v2_id, "prov:wasRevisionOf", report_v1_id)

    validator_action_id = "kb:action-validate-33333333-3333-4333-8333-333333333333"
    graph.upsert_node(
        validator_action_id,
        types="prov:Activity",
        properties={
            "uco-core:name": "case_validate SHACL run",
            "prov:startedAtTime": {
                "@type": "xsd:dateTime",
                "@value": datetime(2026, 3, 16, 14, 0, tzinfo=tz).isoformat(),
            },
            "prov:endedAtTime": {
                "@type": "xsd:dateTime",
                "@value": datetime(2026, 3, 16, 14, 5, tzinfo=tz).isoformat(),
            },
        },
    )
    graph.link(report_v2_id, "prov:wasGeneratedBy", validator_action_id)

    graph.create(
        Investigation,
        name="Synthetic case 2026-PROF-001",
        description=[
            "Graph carries PROF profile intent; validation results are separate prov:Entity resources.",
            "prof:hasResource links Profile to ResourceDescriptor; hasArtifact on descriptor points to shapes/report.",
        ],
        object=[],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
