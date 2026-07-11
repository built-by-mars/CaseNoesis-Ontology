#!/usr/bin/env python3
"""Build a validated CASE/UCO graph for a SOLVE-IT-documented acquisition.

Synthetic worked example behind docs/recipes/solve-it-investigation-planning.md.
A seized laptop SSD is imaged and hash-verified, and every step is
documented the SOLVE-IT way (https://solveit-df.org):

* The investigation states its objective — SOLVE-IT objective DFO-1006
  "Acquire data".
* The acquisition is a solveit-core:SolveitInvestigativeAction whose
  solveit-core:usedTechnique points at the canonical knowledge-base
  technique DFT-1002 ("Copy sectors from storage media") and whose
  solveit-core:appliedMitigation records the mitigations actively applied
  (DFM-1003 image-size check, DFM-1004 source/image hash comparison).
* The technique's known weakness DFW-1004 (incomplete sector copy, ASTM
  E3016-18 category INCOMP) is risk-rated for this specific acquisition
  with solveit-wa:WeaknessEvaluation — SOLVE-IT's systematic Error
  Mitigation Analysis.
* The hash verification is also shown in the UCO 1.5.0 *metaclass* style:
  the action is typed directly with the punned technique class
  solveit-data:techniqueDFT-1042 from
  ontology/solveit/solveit-technique-catalog.ttl (ucoProject/UCO PR #676
  pattern, same as MITRE ATT&CK techniques in
  extensions/attack-technique/).

The technique/weakness/mitigation IRIs are the canonical SOLVE-IT
knowledge-base IRIs vendored in ontology/solveit/solve-it-kb.ttl, so
tools that resolve them get the full upstream record. Discover them with
the MCP tools: search_solveit, get_solveit_details, plan_solveit_workflow.

All data is synthetic (Tier T0).
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "mcp_server"))

from graph_validator import validate_graph_file, validator_available  # noqa: E402

CASE_ID = "solveit-laptop-acquisition-2026"
NS = f"https://example.org/cases/{CASE_ID}/"
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "laptop-acquisition-solveit.jsonld"

SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"


def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def lit(dtype: str, value) -> dict:
    return {"@type": dtype, "@value": str(value)}


def build_graph() -> dict:
    g: list[dict] = []

    g.append({
        "@id": uid("investigation"),
        "@type": "case-investigation:Investigation",
        "uco-core:name": "Synthetic case 2026-XX-0001: laptop acquisition",
        "uco-core:description": (
            "SOLVE-IT objective DFO-1006 (Acquire data): image the seized "
            "laptop SSD and verify integrity before examination. Planned "
            "with plan_solveit_workflow; techniques and mitigations below "
            "reference the pinned SOLVE-IT knowledge base."
        ),
    })

    examiner = uid("examiner")
    g.append({
        "@id": examiner,
        "@type": "uco-identity:Person",
        "uco-core:name": "Examiner One (synthetic)",
    })

    unit = uid("df-unit")
    g.append({
        "@id": unit,
        "@type": "uco-identity:Identity",
        "uco-core:name": "Digital Forensics Unit (synthetic)",
    })

    workstation = uid("imaging-workstation")
    g.append({
        "@id": workstation,
        "@type": "uco-tool:Tool",
        "uco-core:name": "Imaging workstation with hardware write blocker",
        "uco-tool:version": "2026.1",
    })

    ssd = uid("laptop-ssd")
    g.append({
        "@id": ssd,
        "@type": "uco-observable:Device",
        "uco-core:name": "Seized laptop internal SSD (synthetic serial SN-0000)",
    })

    bitstream = uid("bitstream")
    g.append({
        "@id": bitstream,
        "@type": "solveit-observable:Bitstream",
        "uco-core:name": "Sector-by-sector bitstream LBA0..LBAmax",
    })

    image = uid("physical-image")
    g.append({
        "@id": image,
        "@type": "solveit-observable:PhysicalImageContainer",
        "uco-core:name": "E01 physical image of laptop SSD",
        # PhysicalImageContainerShape: must contain at least one Bitstream.
        "solveit-observable:contains": [{"@id": bitstream}],
    })

    hash_result = uid("hash-verification-result")
    g.append({
        "@id": hash_result,
        "@type": "solveit-observable:HashVerificationResult",
        "uco-core:name": "SHA-256 of image matches SHA-256 of source device",
    })

    # Native SOLVE-IT style: the action records which technique was executed
    # and which mitigations were actively applied.
    g.append({
        "@id": uid("acquire-action"),
        "@type": "solveit-core:SolveitInvestigativeAction",
        "uco-core:name": "acquire-laptop-image",
        "uco-core:description": (
            "Physical acquisition of the seized laptop SSD (SOLVE-IT "
            "DFT-1002) with image-size check (DFM-1003) and source/image "
            "hash verification (DFM-1004) applied."
        ),
        "solveit-core:usedTechnique": [
            {"@id": SOLVEIT_DATA + "techniqueDFT-1002"},
        ],
        "solveit-core:appliedMitigation": [
            {"@id": SOLVEIT_DATA + "mitigationDFM-1003"},
            {"@id": SOLVEIT_DATA + "mitigationDFM-1004"},
        ],
        "uco-action:startTime": lit("xsd:dateTime", "2026-06-01T09:15:00Z"),
        "uco-action:endTime": lit("xsd:dateTime", "2026-06-01T11:42:00Z"),
        "uco-action:performer": {"@id": examiner},
        "uco-action:instrument": {"@id": workstation},
        "uco-action:object": [{"@id": ssd}],
        "uco-action:result": [{"@id": image}, {"@id": hash_result}],
    })

    # Error Mitigation Analysis: rate the technique's known weakness for
    # this specific acquisition.
    evaluation = uid("dfw-1004-evaluation")
    g.append({
        "@id": evaluation,
        "@type": "solveit-wa:WeaknessEvaluation",
        "uco-core:name": "DFW-1004 evaluation for laptop SSD acquisition",
        "solveit-wa:evaluatesWeakness": {"@id": SOLVEIT_DATA + "weaknessDFW-1004"},
        "solveit-wa:likelihoodRating": lit("xsd:integer", 1),
        "solveit-wa:likelihoodRationale": (
            "Hardware write blocker and current imaging firmware; no "
            "damaged-media indicators."
        ),
        "solveit-wa:impactRating": lit("xsd:integer", 3),
        "solveit-wa:impactRationale": (
            "Missing sectors would silently omit evidence from the examination."
        ),
        "solveit-wa:liImpactScore": lit("xsd:integer", 3),
    })
    g.append({
        "@id": uid("weakness-assessment-session"),
        "@type": "solveit-wa:WeaknessEvaluationSet",
        "uco-core:name": "Acquisition weakness assessment session",
        "solveit-wa:scopedToTechnique": {"@id": SOLVEIT_DATA + "techniqueDFT-1002"},
        "solveit-wa:evaluatedBy": {"@id": unit},
        "solveit-wa:hasEvaluation": [{"@id": evaluation}],
        "solveit-wa:evaluationDate": lit("xsd:date", "2026-06-01"),
    })

    # UCO 1.5.0 metaclass style: the hash-verification action is typed
    # directly with the punned SOLVE-IT technique class (DFT-1042).
    g.append({
        "@id": uid("verify-hash-action"),
        "@type": ["uco-action:Action", "solveit-data:techniqueDFT-1042"],
        "uco-core:name": "verify-image-hash",
        "uco-core:description": (
            "Computed SHA-256 over the acquired image and compared with the "
            "source-device hash (SOLVE-IT DFT-1042, metaclass style)."
        ),
        "uco-action:performer": {"@id": examiner},
        "uco-action:result": [{"@id": hash_result}],
    })

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
            "solveit-observable": "https://ontology.solveit-df.org/solveit/observable/",
            "solveit-wa": "https://ontology.solveit-df.org/solveit/weakness-assessment/",
            "solveit-data": SOLVEIT_DATA,
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": g,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    report = validate_graph_file(path, project_root=ROOT, extensions=["solveit"])
    print(f"conforms: {report.conforms}")
    print(report.safe_summary)
    return 0 if report.conforms else 1


def main() -> int:
    graph = build_graph()
    OUTPUT.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(graph['@graph'])} nodes)")
    return validate(OUTPUT)


if __name__ == "__main__":
    sys.exit(main())
