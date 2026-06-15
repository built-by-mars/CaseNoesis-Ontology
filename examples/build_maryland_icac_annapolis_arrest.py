#!/usr/bin/env python3
"""Build and validate JSON-LD for Maryland ICAC Annapolis arrest press article.

Source: Eye On Annapolis article PDF (Maryland_ICAC_Arrest_Test_PDF.pdf)
Recipes applied:
  - cac-multi-jurisdiction-task-force
  - cac-icac-search-warrant-arrest
  - grooming-chat-modeling (online sexual solicitation)
  - cac-legal-sentencing-outcomes (charges)
  - cac-csam-forensic-provenance (CSAM purchasing operation context)
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mcp_server"))

from graph_validator import load_extension_ontology_paths, validate_graph_file, validator_available
OUTPUT = ROOT / "examples" / "maryland-icac-annapolis-arrest-2025.jsonld"
CASE_ID = "maryland-icac-annapolis-arrest-2025"
NS = f"https://example.org/cac/{CASE_ID}/"
SOURCE_URL = (
    "https://www.eyeonannapolis.net/2025/12/"
    "38-year-old-annapolis-man-charged-with-online-sexual-solicitation-of-minor/"
)
SOURCE_SHA256 = "5580BC17B225B1DED95A11F8208E378D1CD0C05903860DAE339751DE1764F59E"


def lit(dtype: str, value: str | int | bool) -> dict:
    return {"@type": dtype, "@value": str(value).lower() if isinstance(value, bool) else str(value)}


def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def build_graph() -> dict:
    inv = uid("investigation")
    suspect = uid("suspect")
    task_force = uid("md-icac-task-force")
    ccu = uid("msp-computer-crimes-unit")
    ceu = uid("msp-child-exploitation-unit")
    aacpd = uid("anne-arundel-county-pd")
    initial_phase = uid("phase-initial")
    legal_phase = uid("phase-legal")
    conclusion_phase = uid("phase-conclusion")
    purchase_op = uid("csam-purchasing-operation")
    online_grooming = uid("online-solicitation-behavior")
    inv_action = uid("investigation-action")
    evidence_dev = uid("exploitation-evidence-development")
    warrant_auth = uid("search-warrant-authorization")
    warrant_exec = uid("search-warrant-execution")
    arrest = uid("arrest-operation")
    booking = uid("booking-action")
    jail = uid("detention-center")
    charge_solicit = uid("charge-sexual-solicitation")
    charge_permit = uid("charge-permitting-solicitation")
    funding_state = uid("funding-governor-office")
    funding_combined = uid("funding-state-federal")
    residence = uid("residence-annapolis")
    source_doc = uid("source-pdf")
    source_ref = uid("source-external-reference")
    provenance = uid("provenance-record")
    tool = uid("case-uco-mcp-tool")

    graph = [
        {
            "@id": inv,
            "@type": [
                "case-investigation:Investigation",
                "cacontology:CACInvestigation",
            ],
            "uco-core:name": "Maryland ICAC Annapolis Online Solicitation Investigation",
            "uco-core:description": (
                "Maryland State Police Computer Crimes Unit and Maryland ICAC Task Force "
                "investigation into online child sex abuse material purchasing and sexual "
                "solicitation of a minor; search warrant executed in Annapolis December 2025."
            ),
            "cacontology:caseNumber": "MSP-ICAC-ANNAPOLIS-2025",
            "cacontology:investigationStatus": "Arrest Made",
            "cacontology:startDate": {"@type": "xsd:date", "@value": "2025-04-01"},
            "cacontology:leadAgency": "Maryland State Police Computer Crimes Unit",
            "cacontology:jurisdiction": "Anne Arundel County, Maryland",
            "cacontology:hasPhase": [
                {"@id": initial_phase},
                {"@id": legal_phase},
                {"@id": conclusion_phase},
            ],
            "cacontology:hasStep": [{"@id": inv_action}],
            "uco-core:object": [{"@id": source_doc}],
        },
        {
            "@id": suspect,
            "@type": ["uco-identity:Person"],
            "uco-core:name": "Unnamed 38-Year-Old Annapolis Man",
            "uco-core:description": (
                "38-year-old Annapolis man arrested following ICAC investigation for "
                "online sexual solicitation of a minor and CSAM purchasing-related conduct. "
                f"Residence searched in Annapolis ({residence})."
            ),
            "cacontology-legal-outcomes:chargedWith": [
                {"@id": charge_solicit},
                {"@id": charge_permit},
            ],
        },
        {
            "@id": task_force,
            "@type": [
                "cacontology-taskforce:MarylandICACtaskForce",
                "cacontology-taskforce:ICACtaskForce",
                "cacontology-taskforce:StateICACtaskForce",
                "uco-identity:Organization",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Maryland Internet Crimes Against Children Task Force",
            "uco-core:description": (
                "Statewide ICAC task force overseen by Maryland State Police Computer Crimes Unit."
            ),
            "cacontology-taskforce:dojGrantFunded": lit("xsd:boolean", True),
            "cacontology-taskforce:nationalTaskForceNetwork": lit("xsd:boolean", True),
            "cacontology-taskforce:partnersWith": [
                {"@id": ccu},
                {"@id": aacpd},
            ],
            "uco-core:object": [
                {"@id": funding_state},
                {"@id": funding_combined},
            ],
        },
        {
            "@id": ccu,
            "@type": [
                "cacontology-specialized:MarylandStatePoliceComputerCrimesUnit",
                "uco-identity:Organization",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "Maryland State Police Computer Crimes Unit",
            "uco-core:description": (
                "Lead investigative unit coordinating Maryland ICAC Task Force investigations statewide."
            ),
        },
        {
            "@id": ceu,
            "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
            "uco-core:name": "Maryland State Police Child Exploitation Unit",
            "uco-core:description": (
                "MSP unit that executed the residence search warrant with Anne Arundel County Police."
            ),
        },
        {
            "@id": aacpd,
            "@type": ["uco-identity:Organization"],
            "uco-core:name": "Anne Arundel County Police Department",
            "uco-core:description": (
                "County law enforcement partner supporting search warrant execution."
            ),
        },
        {
            "@id": initial_phase,
            "@type": ["cac-core:Phase", "cacontology:InitialPhase"],
            "uco-core:name": "Initial Investigation Phase",
            "uco-core:description": (
                "Online CSAM purchasing and sexual solicitation investigation (April–December 2025)."
            ),
            "cacontology:hasPhaseBeginPoint": lit("xsd:dateTimeStamp", "2025-04-01T00:00:00Z"),
            "cacontology:hasPhaseEndPoint": lit("xsd:dateTimeStamp", "2025-12-10T23:59:59Z"),
            "cacontology:transitionsTo": {"@id": legal_phase},
        },
        {
            "@id": legal_phase,
            "@type": ["cac-core:Phase", "cacontology:LegalProcessPhase"],
            "uco-core:name": "Legal Process Phase",
            "uco-core:description": "Search warrant execution, arrest, and charging.",
            "cacontology:hasPhaseBeginPoint": lit("xsd:dateTimeStamp", "2025-12-11T00:00:00Z"),
            "cacontology:hasPhaseEndPoint": lit("xsd:dateTimeStamp", "2025-12-11T23:59:59Z"),
            "cacontology:transitionsTo": {"@id": conclusion_phase},
        },
        {
            "@id": conclusion_phase,
            "@type": ["cac-core:Phase", "cacontology:ConclusionPhase"],
            "uco-core:name": "Conclusion Phase",
            "uco-core:description": "Booking and detention without bond.",
            "cacontology:hasPhaseBeginPoint": lit("xsd:dateTimeStamp", "2025-12-11T00:00:00Z"),
            "cacontology:hasPhaseEndPoint": lit("xsd:dateTimeStamp", "2025-12-11T23:59:59Z"),
        },
        {
            "@id": purchase_op,
            "@type": ["cacontology-physical:OnlinePurchase"],
            "uco-core:name": "Online CSAM Purchasing Operation",
            "uco-core:description": (
                "Investigation began in April 2025 into an online child sex abuse material "
                "purchasing operation."
            ),
            "uco-action:performer": {"@id": suspect},
            "cacontology-physical:hasProcurementBeginPoint": lit("xsd:dateTimeStamp", "2025-04-01T00:00:00Z"),
        },
        {
            "@id": online_grooming,
            "@type": ["cacontology-grooming:OnlineGrooming"],
            "uco-core:name": "Online Sexual Solicitation of Minor",
            "uco-core:description": (
                "Detectives developed evidence that the suspect was sexually soliciting "
                "a minor online."
            ),
            "uco-action:performer": {"@id": suspect},
            "cacontology-grooming:targetsVictim": {"@id": uid("minor-victim-unknown")},
        },
        {
            "@id": uid("minor-victim-unknown"),
            "@type": ["uco-identity:Person", "cacontology-grooming:ChildVictim"],
            "uco-core:name": "Unidentified Minor Victim",
            "uco-core:description": "Minor victim referenced in solicitation allegations.",
        },
        {
            "@id": evidence_dev,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
            ],
            "uco-core:name": "Online Exploitation Evidence Development",
            "uco-core:description": (
                "Detectives developed evidence of online sexual solicitation of a minor "
                f"({online_grooming}) and an online CSAM purchasing operation ({purchase_op})."
            ),
            "uco-action:performer": {"@id": ccu},
            "uco-action:object": {"@id": suspect},
            "uco-action:result": {"@id": inv_action},
            "cacontology:occursDuringPhase": {"@id": initial_phase},
        },
        {
            "@id": inv_action,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
            ],
            "uco-core:name": "Maryland ICAC Online Exploitation Investigation",
            "uco-core:description": (
                "Investigation by MSP Computer Crimes Unit and Maryland ICAC Task Force."
            ),
            "uco-action:startTime": lit("xsd:dateTime", "2025-04-01T00:00:00Z"),
            "uco-action:endTime": lit("xsd:dateTime", "2025-12-11T23:59:59Z"),
            "uco-action:performer": {"@id": ccu},
            "uco-action:object": {"@id": suspect},
            "uco-action:result": {"@id": warrant_exec},
            "case-investigation:wasInformedBy": {"@id": evidence_dev},
            "cacontology:occursDuringPhase": {"@id": initial_phase},
        },
        {
            "@id": warrant_auth,
            "@type": ["case-investigation:Authorization"],
            "uco-core:name": "Residence Search Warrant",
            "uco-core:description": "Search warrant for suspect residence in Annapolis.",
        },
        {
            "@id": warrant_exec,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
            ],
            "uco-core:name": "Search Warrant Execution",
            "uco-core:description": (
                "Troopers from MSP Child Exploitation Unit and Anne Arundel County Police "
                "executed a search warrant at the suspect's Annapolis residence."
            ),
            "uco-action:startTime": lit("xsd:dateTime", "2025-12-11T00:00:00Z"),
            "uco-action:authorization": {"@id": warrant_auth},
            "uco-action:performer": {"@id": ceu},
            "uco-action:location": {"@id": residence},
            "uco-action:object": {"@id": suspect},
            "uco-action:result": {"@id": arrest},
            "case-investigation:wasInformedBy": {"@id": inv_action},
            "cacontology:occursDuringPhase": {"@id": legal_phase},
        },
        {
            "@id": arrest,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
                "cacontology-tactical:ArrestOperation",
            ],
            "uco-core:name": "Suspect Arrest Without Incident",
            "uco-core:description": (
                "Suspect taken into custody on scene without incident during warrant service."
            ),
            "uco-action:startTime": lit("xsd:dateTime", "2025-12-11T00:00:00Z"),
            "cacontology-tactical:arrestType": "warrant_arrest",
            "cacontology-tactical:targetCount": lit("xsd:nonNegativeInteger", 1),
            "cacontology-tactical:resistanceExpected": lit("xsd:boolean", False),
            "cacontology-tactical:weaponsExpected": lit("xsd:boolean", False),
            "uco-action:object": {"@id": suspect},
            "uco-action:result": {"@id": booking},
            "cacontology:occursDuringPhase": {"@id": legal_phase},
        },
        {
            "@id": booking,
            "@type": [
                "case-investigation:InvestigativeAction",
                "cac-core:InvestigativeAction",
                "cacontology-tactical:BookingAction",
            ],
            "uco-core:name": "Booking at Anne Arundel County Detention Center",
            "uco-core:description": (
                "Suspect transported to Anne Arundel County Detention Center and held without bond."
            ),
            "uco-action:location": {"@id": jail},
            "uco-action:object": {"@id": suspect},
            "cacontology:occursDuringPhase": {"@id": conclusion_phase},
        },
        {
            "@id": jail,
            "@type": [
                "cacontology-tactical:CorrectionalFacility",
                "uco-core:UcoObject",
                "uco-location:Location",
            ],
            "uco-core:name": "Anne Arundel County Detention Center",
            "cacontology-tactical:facilityName": "Anne Arundel County Detention Center",
        },
        {
            "@id": charge_solicit,
            "@type": ["cacontology-legal-outcomes:StateCharge"],
            "uco-core:name": "Sexual Solicitation of a Minor",
            "uco-core:description": (
                "Maryland state charge for sexual solicitation of a minor; "
                f"underlying conduct modeled as {online_grooming}."
            ),
            "cacontology-legal-outcomes:chargeLevel": "felony",
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 1),
        },
        {
            "@id": charge_permit,
            "@type": ["cacontology-legal-outcomes:StateCharge"],
            "uco-core:name": "Knowingly Permitting Sexual Solicitation of a Minor",
            "uco-core:description": (
                "Maryland state charge for knowingly permitting sexual solicitation of a minor; "
                f"related to conduct at {online_grooming}."
            ),
            "cacontology-legal-outcomes:chargeLevel": "felony",
            "cacontology-legal-outcomes:chargeCount": lit("xsd:nonNegativeInteger", 1),
        },
        {
            "@id": funding_state,
            "@type": ["cacontology-taskforce:GovernorsOfficeCrimePreventionFunding"],
            "uco-core:name": (
                "Governor's Office of Crime Prevention, Youth and Victim Services Funding"
            ),
        },
        {
            "@id": funding_combined,
            "@type": ["cacontology-taskforce:StateLocalFundingCombination"],
            "uco-core:name": "Combined State and Federal ICAC Funding",
            "uco-core:description": (
                "Grant funding from Maryland Governor's Office and U.S. Department of Justice."
            ),
        },
        {
            "@id": residence,
            "@type": ["uco-location:Location"],
            "uco-core:name": "Suspect Residence - Annapolis, Maryland",
            "uco-core:description": "Annapolis residence where search warrant was executed.",
        },
        {
            "@id": source_ref,
            "@type": ["uco-core:ExternalReference"],
            "uco-core:url": SOURCE_URL,
        },
        {
            "@id": source_doc,
            "@type": ["uco-observable:ObservableObject"],
            "uco-core:name": "Maryland_ICAC_Arrest_Test_PDF.pdf",
            "uco-core:description": "Eye On Annapolis press article used as synthetic test source.",
            "uco-core:externalReference": {"@id": source_ref},
            "uco-core:hasFacet": [
                {
                    "@id": uid("source-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "Maryland_ICAC_Arrest_Test_PDF.pdf",
                    "uco-observable:extension": "pdf",
                },
                {
                    "@id": uid("source-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        {
                            "@id": uid("source-sha256"),
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": "SHA256",
                            "uco-types:hashValue": lit("xsd:hexBinary", SOURCE_SHA256),
                        }
                    ],
                },
            ],
        },
        {
            "@id": tool,
            "@type": ["uco-tool:Tool"],
            "uco-core:name": "CASE-UCO MCP Document Processor",
            "uco-tool:version": "1.12.0",
        },
        {
            "@id": provenance,
            "@type": ["case-investigation:ProvenanceRecord"],
            "uco-core:name": "Graph derivation from press article PDF",
            "uco-core:description": (
                "Knowledge graph produced from Eye On Annapolis article via CASE-UCO MCP "
                "document extraction and CAC recipe-guided mapping."
            ),
            "case-investigation:createdTime": "2026-06-15T00:00:00Z",
            "case-investigation:wasInformedBy": [
                {"@id": source_doc},
                {"@id": tool},
            ],
        },
    ]

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "cacontology": "https://cacontology.projectvic.org#",
            "cac-core": "https://cacontology.projectvic.org/core#",
            "cacontology-taskforce": "https://cacontology.projectvic.org/taskforce#",
            "cacontology-specialized": "https://cacontology.projectvic.org/specialized-units#",
            "cacontology-legal-outcomes": "https://cacontology.projectvic.org/legal-outcomes#",
            "cacontology-tactical": "https://cacontology.projectvic.org/tactical#",
            "cacontology-grooming": "https://cacontology.projectvic.org/grooming#",
            "cacontology-physical": "https://cacontology.projectvic.org/physical#",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": graph,
    }


def validate(path: Path) -> int:
    """Validate against the shared CAC press-release subset."""

    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    report = validate_graph_file(path, extensions=["cac"], project_root=ROOT)
    print(report.safe_summary)
    paths = load_extension_ontology_paths("cac", mode="subset", project_root=ROOT)
    print(f"Validated with {len(paths)} CAC subset ontology files")
    return 0 if report.conforms else 1


def main() -> int:
    payload = build_graph()
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
