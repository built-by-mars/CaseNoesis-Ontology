#!/usr/bin/env python3
"""Build validated JSON-LD for Operation PHANTOM GATE (INV-2026-PGA-001).

Synthetic Tier-T0 composite cyber investigation scenario behind:
  examples/scenarios/operation-phantom-gate.md

Models elder-fraud couriers (E.D. La.), RICO/crypto escalation (D.D.C.),
insider/export tracks (N.D. Cal.), APT/ATT&CK CTI (GateRunner), CAC
sextortion (ICAC), weapons/drugs takedown (Fargo), SOLVE-IT acquisition
workflows, chain of custody, data-handling markings, AI/ML pipelines, and
semantic refinements from external review (identity links, custody I/O,
criminal vs investigative action separation, fail-closed validation).

Grounded exemplar patterns:
  examples/pacer/edla_2022_cr_00115/     — elder fraud, calls, legalproc
  examples/pacer/ddc_2024_cr_00417/       — RICO, cryptoinv
  examples/solveit/                       — SOLVE-IT acquisition
  examples/cti/lotus_blossom_2025/        — ATT&CK technique metaclass
  examples/pacer/ndnd_2025_cr_00005/      — weapons, drugs
  examples/pacer/dma_2023_cr_10159/       — marking definitions

Run:
  python3 examples/scenarios/build_phantom_gate_scenario.py

Validation (fail-closed):
  Raises RuntimeError if case_validate is unavailable or the graph does not
  conform with verification_status == "complete".
"""

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "mcp_server"))

from graph_validator import validate_graph_file, validator_available  # noqa: E402

from phantom_gate_longtail import add_longtail
from phantom_gate_acceptance import (
    add_weakness_evaluation_set,
    authorize,
    run_acceptance_gates,
)

CASE_ID = "operation-phantom-gate-2026"
NS = f"https://example.org/scenarios/{CASE_ID}/"
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "operation-phantom-gate.jsonld"
SCENARIO_DOC = HERE / "operation-phantom-gate.md"

EXTENSIONS = [
    "legalproc",
    "rico",
    "cryptoinv",
    "attack-technique:full",
    "solveit",
    "weapons",
    "drugs",
    "cac",
]

SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"

PREDICATE_STATUTES = [
    "18 U.S.C. § 1028 (fraud and related activity in connection with identification documents)",
    "18 U.S.C. § 1029 (fraud and related activity in connection with access devices)",
    "18 U.S.C. § 1343 (wire fraud)",
    "18 U.S.C. § 1512 (tampering with a witness, victim, or an informant)",
    "18 U.S.C. § 1956 (laundering of monetary instruments)",
    "18 U.S.C. § 1957 (engaging in monetary transactions in property derived from specified unlawful activity)",
    "18 U.S.C. § 1960 (illegal money transmitters)",
    "18 U.S.C. § 2314 (interstate transportation of stolen property)",
]

SCENARIO_SHA256 = hashlib.sha256(SCENARIO_DOC.read_bytes()).hexdigest()


def lit(dtype: str, value: str | int | bool | float) -> dict:
    if isinstance(value, bool):
        val = str(value).lower()
    else:
        val = str(value)
    return {"@type": dtype, "@value": val}


def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def rel(
    source: str,
    target: str,
    kind: str,
    directional: bool = True,
    description: str | None = None,
) -> dict:
    node: dict = {
        "@id": uid(f"rel-{source}-{target}-{kind}"),
        "@type": "uco-core:Relationship",
        "uco-core:source": [{"@id": source}],
        "uco-core:target": [{"@id": target}],
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": lit("xsd:boolean", directional),
    }
    if description:
        node["uco-core:description"] = description
    return node


def link_with_desc(source: str, target: str, kind: str, description: str) -> dict:
    """Relationship with semantic note (preferred over ad-hoc kind strings)."""
    return rel(source, target, kind, description=description)


def dict_entries(parent_label: str, entries: dict[str, str]) -> dict:
    """Build a scoped uco-types:Dictionary (IDs unique per parent event/action)."""
    return {
        "@id": uid(f"{parent_label}:dictionary"),
        "@type": "uco-types:Dictionary",
        "uco-types:entry": [
            {
                "@id": uid(f"{parent_label}:entry:{key}"),
                "@type": "uco-types:DictionaryEntry",
                "uco-types:key": key,
                "uco-types:value": value,
            }
            for key, value in entries.items()
        ],
    }


def artifact_id(label: str) -> str:
    """Stable human-readable IRI for scenario artifact IDs (ART-001, CALL-002, …)."""
    return f"{NS}{label}"


def marking_definition(label: str, name: str, statement: str) -> list[dict]:
    return [
        {
            "@id": uid(f"{label}-def"),
            "@type": ["marking:MarkingDefinition", "uco-core:UcoObject"],
            "uco-core:name": name,
            "marking:definitionType": "statement",
            "marking:definition": [{"@id": uid(f"{label}-stmt")}],
        },
        {
            "@id": uid(f"{label}-stmt"),
            "@type": "marking:StatementMarking",
            "marking:definitionType": "statement",
            "marking:statement": statement,
        },
    ]


def hash_facet(label: str, method: str, value: str) -> dict:
    return {
        "@id": uid(f"{label}-hash"),
        "@type": "uco-types:Hash",
        "uco-types:hashMethod": method,
        "uco-types:hashValue": lit("xsd:hexBinary", value),
    }


def synthetic_hash(label: str) -> str:
    """Deterministic 64-char SHA-256 placeholder for synthetic exemplar hashes."""
    return hashlib.sha256(f"{CASE_ID}:{label}".encode()).hexdigest()


def email_address(g: list[dict], label: str, address: str, display: str | None = None) -> str:
    """ObservableObject + EmailAddressFacet for EmailMessageFacet from/to."""
    facet = uid(f"{label}-email-facet")
    eid = uid(label)
    g.extend([
        {
            "@id": facet,
            "@type": "uco-observable:EmailAddressFacet",
            "uco-observable:addressValue": address,
        },
        {
            "@id": eid,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": display or address,
            "uco-core:hasFacet": [{"@id": facet}],
        },
    ])
    return eid


def build_graph() -> dict:
    g: list[dict] = []

    def add(*nodes: dict) -> None:
        g.extend(nodes)

    def link(source: str, target: str, kind: str) -> None:
        g.append(rel(source, target, kind))

    def apply_marking(node_id: str, *marking_ids: str) -> None:
        for node in g:
            if node.get("@id") != node_id:
                continue
            existing = [
                m["@id"] if isinstance(m, dict) else m
                for m in node.get("uco-core:objectMarking", [])
            ]
            for mid in marking_ids:
                if mid not in existing:
                    existing.append(mid)
            node["uco-core:objectMarking"] = [{"@id": m} for m in existing]
            return
        raise KeyError(f"Cannot apply marking: unknown node {node_id}")

    investigation_contents: list[str] = []

    def include_in_investigation(*node_ids: str) -> None:
        investigation_contents.extend(node_ids)

    # ------------------------------------------------------------------
    # Investigation container
    # ------------------------------------------------------------------
    investigation = uid("investigation")
    investigation_authorizations: list[str] = []

    def register_auth(auth_id: str) -> None:
        if auth_id not in investigation_authorizations:
            investigation_authorizations.append(auth_id)

    def authorize_action(action_id: str, auth_id: str, *, note: str | None = None) -> None:
        authorize(g, rel, action_id, auth_id, description=note)
        register_auth(auth_id)

    add({
        "@id": investigation,
        "@type": ["case-investigation:Investigation", "cacontology:CACInvestigation"],
        "uco-core:name": "Operation PHANTOM GATE (INV-2026-PGA-001)",
        "legalproc:caseIdentifier": "INV-2026-PGA-001",
        "cacontology:caseNumber": "INV-2026-PGA-001",
        "cacontology:investigationStatus": "Active — multi-phase synthetic exercise",
        "uco-core:description": (
            "Synthetic multipart investigation of the Phantom Gate Alliance "
            "(PGA) criminal enterprise: elder-fraud couriers (E.D. La. "
            "2:26-cr-00115), RICO/crypto social engineering (D.D.C. "
            "1:26-cr-00417), insider/export (N.D. Cal.), APT GateRunner "
            "malware, CAC sextortion (D. Alaska 3:26-cr-00029), and Fargo "
            "safehouse weapons/drugs takedown. Tier T0 — all identifiers "
            "fabricated. Source narrative: operation-phantom-gate.md."
        ),
    })

    # Scenario source markdown
    scenario_doc = uid("scenario-source-doc")
    add({
        "@id": scenario_doc,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "operation-phantom-gate.md",
        "uco-core:description": (
            "Synthetic scenario specification for MCP/recipe exercise; "
            "INV-2026-PGA-001 artifact catalog and phase timeline."
        ),
        "uco-core:hasFacet": [
            {
                "@id": uid("scenario-source-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "operation-phantom-gate.md",
                "uco-observable:extension": "md",
            },
            {
                "@id": uid("scenario-source-hash-facet"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [hash_facet("scenario-source", "SHA256", SCENARIO_SHA256)],
            },
        ],
    })
    link(scenario_doc, investigation, "part_of")

    # ------------------------------------------------------------------
    # Marking definitions
    # ------------------------------------------------------------------
    add(*marking_definition(
        "marking-leo-sensitive",
        "Law enforcement sensitive — PGA task force",
        "LAW ENFORCEMENT SENSITIVE — PGA JTF. Unauthorized disclosure subject to 5 U.S.C. § 552(b)(7).",
    ))
    add(*marking_definition(
        "marking-ts-sci",
        "TOP SECRET//SCI",
        "TOP SECRET//SCI — unauthorized disclosure subject to 18 U.S.C. § 793 et seq.",
    ))
    add(*marking_definition(
        "marking-cac-restricted",
        "CAC-RESTRICTED",
        "CAC-RESTRICTED — crimes-against-children investigation material; "
        "restricted to ICAC task force and designated prosecutors.",
    ))
    add(*marking_definition(
        "marking-juvenile-privacy",
        "JUVENILE-PRIVACY",
        "JUVENILE-PRIVACY — minor victim identifying information; "
        "limited to named UC, prosecutor, and court-authorized personnel.",
    ))
    add(*marking_definition(
        "marking-fincen-sar",
        "FINCEN-SAR-PROTECTED",
        "FINCEN-SAR-PROTECTED — Bank Secrecy Act SAR cluster data; "
        "no public filing attachment without FinCEN authorization.",
    ))
    add(*marking_definition(
        "marking-malware-live",
        "MALWARE-LIVE",
        "MALWARE-LIVE — live malware sample; air-gapped examination only; "
        "hash-only sharing to external CTI partners.",
    ))
    add(*marking_definition(
        "marking-company-confidential",
        "COMPANY-CONFIDENTIAL",
        "COMPANY-CONFIDENTIAL — Apex Semi proprietary network capture and EDR data; "
        "restricted to company counsel and designated law-enforcement liaisons.",
    ))
    leo_marking = uid("marking-leo-sensitive-def")
    ts_marking = uid("marking-ts-sci-def")
    cac_marking = uid("marking-cac-restricted-def")
    juvenile_marking = uid("marking-juvenile-privacy-def")
    fincen_marking = uid("marking-fincen-sar-def")
    malware_marking = uid("marking-malware-live-def")
    corp_marking = uid("marking-company-confidential-def")

    # ------------------------------------------------------------------
    # Locations (uco-core:UcoObject dual typing)
    # ------------------------------------------------------------------
    loc_001 = uid("loc-001")
    loc_003 = uid("loc-003")
    loc_004 = uid("loc-004")
    loc_007 = uid("loc-007")
    loc_009 = uid("loc-009")
    loc_010 = uid("loc-010")

    def location(
        lid: str,
        name: str,
        description: str,
        *,
        street: str | None = None,
        locality: str | None = None,
        region: str | None = None,
        postal: str | None = None,
        latitude: str | None = None,
        longitude: str | None = None,
    ) -> dict:
        facets: list[dict] = []
        if street or locality or region or postal:
            facets.append({
                "@id": uid(f"{lid}-address-facet"),
                "@type": "uco-location:SimpleAddressFacet",
                **({"uco-location:street": street} if street else {}),
                **({"uco-location:locality": locality} if locality else {}),
                **({"uco-location:region": region} if region else {}),
                **({"uco-location:postalCode": postal} if postal else {}),
            })
        if latitude is not None and longitude is not None:
            facets.append({
                "@id": uid(f"{lid}-latlong-facet"),
                "@type": "uco-location:LatLongCoordinatesFacet",
                "uco-location:latitude": lit("xsd:decimal", latitude),
                "uco-location:longitude": lit("xsd:decimal", longitude),
            })
        node: dict = {
            "@id": lid,
            "@type": ["uco-location:Location", "uco-core:UcoObject"],
            "uco-core:name": name,
            "uco-core:description": description,
        }
        if facets:
            node["uco-core:hasFacet"] = facets
        return node

    add(
        location(
            loc_001, "LOC-001 Victim A residence",
            "124 Oak Lane, Hammond, LA 70403 — elder fraud victim.",
            street="124 Oak Lane", locality="Hammond", region="LA", postal="70403",
        ),
        location(
            loc_003, "LOC-003 Tangipahoa sting lot",
            "Shell rear lot, Highway 190, Hammond LA; controlled delivery COC-001.",
            street="Highway 190 rear lot (Shell)", locality="Hammond", region="LA",
            latitude="30.5042", longitude="-90.4621",
        ),
        location(
            loc_004, "LOC-004 Victim-7 residence",
            "1800 Massachusetts Ave NW, Washington, DC — $47M ETH theft.",
            street="1800 Massachusetts Ave NW", locality="Washington", region="DC",
        ),
        location(loc_007, "LOC-007 Apex Semi HQ",
                 "San Jose, CA campus — insider spear-phish and EDR alerts.",
                 locality="San Jose", region="CA"),
        location(loc_009, "LOC-009 PGA Fargo safehouse",
                 "884 1st Ave N, Fargo, ND — weapons and controlled substances seizure.",
                 street="884 1st Ave N", locality="Fargo", region="ND"),
        location(loc_010, "LOC-010 ICAC undercover meet",
                 "Anchorage, AK park — CAC sting location (synthetic).",
                 locality="Anchorage", region="AK"),
    )

    # TOWER-004 — cell-site corroboration (Keel phone at LOC-003 handoff)
    tower_004 = uid("tower-004")
    tower_004_facet = uid("tower-004-facet")
    add(
        {
            "@id": tower_004_facet,
            "@type": "uco-observable:CellSiteFacet",
            "uco-observable:cellSiteCountryCode": "310",
            "uco-observable:cellSiteNetworkCode": "410",
            "uco-observable:cellSiteLocationAreaCode": "88421",
            "uco-observable:cellSiteIdentifier": "210",
            "uco-observable:cellSiteType": "850 MHz sector",
        },
        {
            "@id": tower_004,
            "@type": ["uco-observable:CellSite", "uco-core:UcoObject"],
            "uco-core:name": "TOWER-004 — Hammond handoff sector",
            "uco-core:description": (
                "Sector 210°, 850 MHz; Keel phone ACC-001 at LOC-003 "
                "2022-04-04T10:28:00 CDT; corroborates FS-008 EXIF GPS."
            ),
            "uco-core:hasFacet": [{"@id": tower_004_facet}],
        },
    )

    # ------------------------------------------------------------------
    # Persons
    # ------------------------------------------------------------------
    def person(label: str, name: str, description: str) -> str:
        pid = uid(label)
        add({
            "@id": pid,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": name,
            "uco-core:description": description,
        })
        return pid

    keel = person("person-keel", "Darius Keel",
                  "Money courier; arrested 2022-04-04 controlled delivery. ACC-001 +1-504-555-0177.")
    king_k = person("person-king-k", 'Raj "King K" Mehta',
                    "Call-center operator (unindicted, India). ACC-002 +1-646-555-0191.")
    victim_a = person("person-victim-a", "Victim A",
                      "Elder fraud victim, 77, Hammond LA. +1-985-555-0142.")
    victor_lam = person("person-victor-lam", "Victor Lam",
                        "Voice social engineer; CALL-002 to Victim-7.")
    victim_7 = person("person-victim-7", "Victim-7",
                      "Cryptocurrency holder; $47M ETH theft 2024-08-18.")
    mei_chen = person("person-mei-chen", "Mei Chen",
                      "Apex Semi insider; MSG-004 WeChat, EMAIL-001 spear-phish target.")
    wei_zhang = person("person-wei-zhang", "Wei Zhang",
                       "Jade Horizon import; EMAIL-002 false AES filing recipient.")
    juvenile_j1 = person("person-juvenile-j1", "Juvenile J-1",
                         "CAC sextortion victim; StreamVault money mule recruitment.")
    novablade = person("person-novablade", 'alias "NovaBlade"',
                       "Juvenile recruiter; StreamVault @novablade_884.")
    kyle_marsh = person("person-kyle-marsh", "Kyle Marsh",
                        "Insider; Discord ACC-008 k_marsh_gaming#8842; D. Mass. § 793(e).")
    wl_recruiter = person("person-wl-recruiter", "COCONSPIRATOR W.L.",
                          "Insider recruiter; WeChat ACC-010 wxid_wl88421 (MSG-004).")

    # ------------------------------------------------------------------
    # Phone accounts
    # ------------------------------------------------------------------
    def phone_account(label: str, name: str, number: str) -> tuple[str, str]:
        facet = uid(f"{label}-facet")
        pid = uid(label)
        add(
            {
                "@id": facet,
                "@type": "uco-observable:PhoneAccountFacet",
                "uco-observable:phoneNumber": number,
            },
            {
                "@id": pid,
                "@type": "uco-observable:PhoneAccount",
                "uco-core:name": name,
                "uco-core:hasFacet": [{"@id": facet}],
            },
        )
        return pid, facet

    victim_a_phone, _ = phone_account("acc-victim-a-phone", "Victim A mobile", "+1-985-555-0142")
    treasury_spoof, _ = phone_account("acc-treasury-spoof", "Spoofed US Treasury CID", "+1-202-555-0199")
    keel_phone, _ = phone_account("acc-keel-phone", "ACC-001 Keel courier phone", "+1-504-555-0177")
    king_k_phone, _ = phone_account("acc-king-k-phone", 'ACC-002 "King K" dispatch', "+1-646-555-0191")
    lam_voip, _ = phone_account("acc-lam-voip", 'VoIP "CoinShield Security"', "+1-786-555-0133")
    victim_7_phone, _ = phone_account("acc-victim-7-phone", "Victim-7 mobile", "+1-202-555-0881")
    king_k_india, _ = phone_account("acc-king-k-india", "King K India alias line", "+91-98-5555-0144")

    # Digital / online accounts (explicit identity-correlation targets)
    def digital_account(
        label: str,
        name: str,
        identifier: str,
        *,
        display: str | None = None,
        platform: str | None = None,
    ) -> str:
        account_facet = uid(f"{label}-account-facet")
        digital_facet = uid(f"{label}-digital-facet")
        aid = uid(label)
        desc = name if not platform else f"{name} ({platform})"
        facets: list[dict] = [
            {
                "@id": account_facet,
                "@type": "uco-observable:AccountFacet",
                "uco-observable:accountIdentifier": identifier,
            },
            {
                "@id": digital_facet,
                "@type": "uco-observable:DigitalAccountFacet",
                **({"uco-observable:displayName": display or identifier} if display or identifier else {}),
            },
        ]
        add({
            "@id": aid,
            "@type": [
                "uco-observable:DigitalAccount",
                "uco-observable:ObservableObject",
                "uco-core:UcoObject",
            ],
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-core:hasFacet": facets,
        })
        return aid

    keel_icloud = digital_account(
        "acc-keel-icloud", "ACC-003 Keel iCloud",
        "keel.darius@icloud.com", display="Darius Keel", platform="Apple iCloud",
    )
    telegram_coach = digital_account(
        "acc-telegram-coach", "ACC-004 Telegram @coach_elena_pga",
        "coach_elena_pga", display="Coach Elena PGA", platform="Telegram",
    )
    anydesk_session = digital_account(
        "acc-anydesk-victim7", "ACC-005 AnyDesk session (Victim-7)",
        "1234567890", display="AnyDesk 8.0.8 remote session", platform="AnyDesk",
    )
    binance_mule = digital_account(
        "acc-binance-mule", "ACC-006 Binance UID (MLAR return)",
        "8847129033", platform="Binance",
    )
    discord_marsh = digital_account(
        "acc-discord-kyle", "ACC-008 Discord k_marsh_gaming#8842",
        "k_marsh_gaming#8842", display="Kyle Marsh", platform="Discord",
    )
    streamvault_nova = digital_account(
        "acc-streamvault-nova", "ACC-009 StreamVault @novablade_884",
        "novablade_884", display='alias "NovaBlade"', platform="StreamVault",
    )
    wechat_wl = digital_account(
        "acc-wechat-wl", "ACC-010 WeChat wxid_wl88421 (W.L.)",
        "wxid_wl88421", display="COCONSPIRATOR W.L.", platform="WeChat",
    )
    mei_chen_wechat = digital_account(
        "acc-mei-chen-wechat", "Mei Chen WeChat", "wxid_meichen_apexsemi",
        display="Mei Chen", platform="WeChat",
    )
    link(mei_chen, mei_chen_wechat, "Has_Account")

    # Cell-site corroboration: Keel phone connected to sector during handoff
    link(keel_phone, tower_004, "Connected_To")
    g.append(rel(keel_phone, loc_003, "Observed_At",
                 description="Keel phone ACC-001 at LOC-003 during controlled delivery handoff"))

    # ------------------------------------------------------------------
    # Phase 1 — Elder fraud: calls, messages, device, COC, legalproc
    # ------------------------------------------------------------------
    call_001_facet = uid("call-001-facet")
    call_001 = uid("call-001")
    add(
        {
            "@id": call_001_facet,
            "@type": "uco-observable:CallFacet",
            "uco-observable:callType": "incoming (caller ID spoofed as 'US Treasury')",
            "uco-observable:from": {"@id": treasury_spoof},
            "uco-observable:to": {"@id": victim_a_phone},
            "uco-observable:startTime": lit("xsd:dateTime", "2022-04-04T09:17:23-05:00"),
            "uco-observable:duration": lit("xsd:integer", 2832),
        },
        {
            "@id": call_001,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CALL-001 Spoofed Treasury call to Victim A",
            "uco-core:description": (
                "2022-04-04T09:17:23-05:00 incoming to +1-985-555-0142; "
                "caller ID +1-202-555-0199 displays 'US Treasury'. "
                "Det. D'Amato observed live. Exhibit GX-14 (E.D. La.)."
            ),
            "uco-core:hasFacet": [{"@id": call_001_facet}],
        },
    )

    call_003_facet = uid("call-003-facet")
    call_003 = uid("call-003")
    add(
        {
            "@id": call_003_facet,
            "@type": "uco-observable:CallFacet",
            "uco-observable:from": {"@id": king_k_india},
            "uco-observable:to": {"@id": keel_phone},
            "uco-observable:startTime": lit("xsd:dateTime", "2022-03-29T16:05:11-05:00"),
        },
        {
            "@id": call_003,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CALL-003 Title III intercept (King K → Keel dispatch)",
            "uco-core:description": (
                "Title III order 2:22-mj-00062-DM ¶¶ 8–12. King K: 'Package ready "
                "Hammond. Victim A confirmed ten thousand cash.' Cell-site TOWER-004."
            ),
            "uco-core:hasFacet": [{"@id": call_003_facet}],
        },
    )

    msg_001_facet = uid("msg-001-facet")
    msg_001 = uid("msg-001")
    add(
        {
            "@id": msg_001_facet,
            "@type": "uco-observable:MessageFacet",
            "uco-observable:from": {"@id": king_k_phone},
            "uco-observable:to": {"@id": keel_phone},
            "uco-observable:messageText": (
                "[2022-04-04 10:31:07 CDT] King K → Keel: Tangipahoa Sheriff on scene. ABORT."
            ),
            "uco-observable:sentTime": lit("xsd:dateTime", "2022-04-04T10:31:07-05:00"),
        },
        {
            "@id": msg_001,
            "@type": "uco-observable:Message",
            "uco-core:name": "MSG-001 King K dispatch thread (Keel iPhone)",
            "uco-core:description": (
                "iMessage thread iMessage;+1-504-555-0177;+1-646-555-0191. "
                "Dispatch, package photo IMG_0042, ABORT after sting. Source ART-001."
            ),
            "uco-core:hasFacet": [{"@id": msg_001_facet}],
        },
    )

    art_001 = artifact_id("ART-001")
    art_001_image = artifact_id("ART-001-UFED")
    add(
        {
            "@id": art_001,
            "@type": ["uco-observable:MobileDevice", "uco-core:UcoObject"],
            "uco-core:name": "ART-001 Keel iPhone 13 Pro",
            "uco-core:description": (
                "Serial F2LD88421; seized 2022-04-04 controlled delivery; "
                "exhibit E.D. La. 1-A. DH-PGA-001 CJIS / LEO-SENSITIVE."
            ),
            "uco-core:objectMarking": [{"@id": leo_marking}],
        },
        {
            "@id": art_001_image,
            "@type": [
                "solveit-observable:FileSet",
                "uco-observable:ObservableObject",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "keel-iphone-UFED.zip",
            "uco-core:description": (
                "Cellebrite UFED 7.69 logical extraction of ART-001; "
                "synthetic-placeholder-hash on ContentDataFacet."
            ),
            "uco-core:objectMarking": [{"@id": leo_marking}],
            "uco-core:hasFacet": [
                {
                    "@id": uid("art-001-ufed-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "keel-iphone-UFED.zip",
                    "uco-observable:extension": "zip",
                },
                {
                    "@id": uid("art-001-ufed-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        hash_facet("art-001-ufed", "SHA256", synthetic_hash("art-001-ufed")),
                    ],
                },
            ],
        },
    )
    include_in_investigation(art_001, art_001_image)

    # COC-001 performers, tools, and custody locations
    det_fontenot = uid("person-det-fontenot")
    sa_holt = uid("person-sa-holt")
    examiner_keel = uid("examiner-keel")
    evidence_custodian = uid("person-evidence-custodian")
    ufed_tool = uid("tool-cellebrite-ufed")
    keel_hash_result = uid("keel-ufed-hash-verification")
    loc_tpso_evidence = uid("loc-tpso-evidence")
    loc_hsi_nola = uid("loc-hsi-nola")
    loc_hsi_lab = uid("loc-hsi-lab")
    loc_fbi_locker = uid("loc-fbi-locker")
    add(
        {
            "@id": det_fontenot,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Det. B. Fontenot (TPSO)",
        },
        {
            "@id": sa_holt,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "SA Rebecca Holt (HSI NOLA)",
        },
        {
            "@id": examiner_keel,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "DF Examiner J. Price (HSI NOLA)",
        },
        {
            "@id": evidence_custodian,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "FBI NOLA evidence custodian",
        },
        {
            "@id": ufed_tool,
            "@type": "uco-tool:Tool",
            "uco-core:name": "Cellebrite UFED",
            "uco-tool:version": "7.69",
        },
        {
            "@id": keel_hash_result,
            "@type": "solveit-observable:HashVerificationResult",
            "uco-core:name": "Keel UFED zip SHA-256 verification (DFT-1042)",
        },
        location(loc_tpso_evidence, "LOC-TPSO evidence room",
                 "Tangipahoa Parish Sheriff evidence room — Faraday storage post-seizure."),
        location(loc_hsi_nola, "LOC-HSI NOLA field office",
                 "HSI New Orleans field office — custody receipt step 4."),
        location(loc_hsi_lab, "LOC-HSI digital forensics lab",
                 "HSI NOLA DF lab — logical extraction and hash verification."),
        location(loc_fbi_locker, "LOC-FBI NOLA locker L-14",
                 "FBI New Orleans evidence locker L-14 — final storage."),
    )

    title_iii_auth = uid("auth-title-iii")
    add({
        "@id": title_iii_auth,
        "@type": "case-investigation:Authorization",
        "uco-core:name": "Title III intercept order 2:22-mj-00062-DM",
        "uco-core:description": "Wire intercept authorization ¶¶ 8–12 for CALL-003 India dispatch line.",
    })

    register_auth(title_iii_auth)
    intercept_action = uid("ia-title-iii-intercept")
    add({
        "@id": intercept_action,
        "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
        "uco-core:name": "Title III intercept of King K → Keel dispatch (CALL-003)",
        "uco-action:startTime": lit("xsd:dateTime", "2022-03-29T16:05:11-05:00"),
        "uco-action:object": [{"@id": call_003}],
    })
    authorize_action(
        intercept_action,
        title_iii_auth,
        note="Wire intercept performed under Title III order 2:22-mj-00062-DM",
    )

    # COC-001 — seven chain-of-custody steps (structured performers, locations, I/O)
    coc_step_specs = [
        ("coc-001-step1", "Collection/seizure Keel iPhone 13 Pro", "2022-04-04T10:35:00-05:00",
         det_fontenot, loc_003, [art_001], [], "Bag TPSO-2022-044-A seal S-9912 intact."),
        ("coc-001-step2", "Faraday placement", "2022-04-04T11:20:00-05:00",
         det_fontenot, loc_tpso_evidence, [art_001], [], "DFT-1010 — airplane mode confirmed."),
        ("coc-001-step3", "Custody release TPSO → HSI", "2022-04-04T14:00:00-05:00",
         det_fontenot, loc_tpso_evidence, [art_001], [], "Seal S-9912 intact; release half of transfer."),
        ("coc-001-step4", "Custody receipt HSI NOLA", "2022-04-04T16:30:00-05:00",
         sa_holt, loc_hsi_nola, [art_001], [], "Seal verified; receipt half of transfer."),
        ("coc-001-step5", "Logical extraction (Cellebrite UFED 7.69)", "2022-04-05T09:00:00-05:00",
         examiner_keel, loc_hsi_lab, [art_001], [art_001_image], "Output keel-iphone-UFED.zip."),
        ("coc-001-step6", "Hash verify UFED zip", "2022-04-05T11:45:00-05:00",
         examiner_keel, loc_hsi_lab, [art_001_image], [keel_hash_result], "DFT-1042; matches UFED report."),
        ("coc-001-step7", "Evidence storage FBI NOLA locker L-14", "2022-04-05T12:00:00-05:00",
         evidence_custodian, loc_fbi_locker, [art_001, art_001_image], [], "DH-PGA-001 CJIS enclave."),
    ]
    coc_action_ids: list[str] = []
    for label, name, start, performer_id, location_id, objects, results, notes in coc_step_specs:
        aid = uid(label)
        coc_action_ids.append(aid)
        action: dict = {
            "@id": aid,
            "@type": "case-investigation:InvestigativeAction",
            "uco-core:name": f"COC-001 — {name}",
            "uco-core:description": notes,
            "uco-action:startTime": lit("xsd:dateTime", start),
            "uco-action:performer": {"@id": performer_id},
            "uco-action:location": {"@id": location_id},
            "uco-action:object": [{"@id": o} for o in objects],
        }
        if results:
            action["uco-action:result"] = [{"@id": r} for r in results]
        if label == "coc-001-step5":
            action["uco-action:instrument"] = {"@id": ufed_tool}
        add(action)
        link(aid, investigation, "part_of")
        include_in_investigation(aid)

    link(coc_action_ids[2], coc_action_ids[3], "Transferred_To")

    prov_art_001_physical = uid("prov-art-001-physical")
    prov_art_001_digital = uid("prov-art-001-digital")
    add(
        {
            "@id": prov_art_001_physical,
            "@type": "case-investigation:ProvenanceRecord",
            "uco-core:name": "prov-art-001-physical (Keel iPhone)",
            "case-investigation:exhibitNumber": "E.D. La. 1-A",
            "uco-core:object": [{"@id": art_001}] + [{"@id": a} for a in coc_action_ids[:4]],
        },
        {
            "@id": prov_art_001_digital,
            "@type": "case-investigation:ProvenanceRecord",
            "uco-core:name": "prov-art-001-digital (UFED extraction)",
            "uco-core:object": [{"@id": art_001_image}] + [{"@id": a} for a in coc_action_ids[4:]],
        },
    )

    # E.D. La. legalproc charge
    instrument_edla = uid("instrument-edla-00115")
    charge_edla = uid("charge-edla-wire-fraud")
    add(
        {
            "@id": instrument_edla,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "E.D. La. 2:26-cr-00115 — wire fraud conspiracy",
            "legalproc:instrumentType": "indictment",
            "legalproc:caseIdentifier": "2:26-cr-00115-ILRL",
            "uco-core:objectCreatedTime": lit("xsd:dateTime", "2026-01-15T00:00:00-06:00"),
        },
        {
            "@id": charge_edla,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count 1: Conspiracy to Commit Wire Fraud (couriers)",
            "legalproc:statuteCitation": "18 U.S.C. § 1349 (object offense 18 U.S.C. § 1343)",
            "legalproc:countLabel": "Count 1",
            "legalproc:countNumber": lit("xsd:nonNegativeInteger", 1),
            "legalproc:offenseForm": "conspiracy",
            "legalproc:chargeClassification": "Felony",
            "legalproc:assertedIn": {"@id": instrument_edla},
            "uco-core:description": (
                "Federal courier wing: transnational elder-fraud call-center "
                "network with in-person cash pickups including Keel controlled "
                "delivery 2022-04-04 at LOC-003."
            ),
        },
    )
    link(keel, charge_edla, "Charged_With")
    link(instrument_edla, investigation, "part_of")

    # Events EVT-001, EVT-002
    evt_001 = uid("evt-001")
    evt_002 = uid("evt-002")
    loc_002 = uid("loc-002-walgreens")
    add(
        {
            "@id": evt_001,
            "@type": "uco-core:Event",
            "uco-core:name": "EVT-001 Green Dot card purchase (Victim A)",
            "uco-core:startTime": lit("xsd:dateTime", "2022-04-04T11:45:00-05:00"),
            "uco-core:eventType": ["FinancialTransaction"],
            "uco-core:eventAttribute": [dict_entries("evt-001", {
                "merchant": "Walgreens, Hammond LA",
                "amount_usd": "500.00",
                "card_type": "prepaid",
                "triggered_by": "CALL-001",
            })],
        },
        location(loc_002, "LOC-002 Walgreens Hammond",
                 "45000 Highway 190, Hammond, LA — card purchase EVT-001."),
        {
            "@id": evt_002,
            "@type": "uco-core:Event",
            "uco-core:name": "EVT-002 Controlled delivery arrest trigger",
            "uco-core:startTime": lit("xsd:dateTime", "2022-04-04T10:35:00-05:00"),
            "uco-core:eventType": ["LawEnforcementOperation"],
            "uco-core:eventAttribute": [dict_entries("evt-002", {
                "operation_id": "TPSO-CD-2022-044",
                "target": "Darius Keel",
                "victim": "Victim A (77)",
            })],
        },
    )
    g.append(rel(evt_001, call_001, "Related_To",
                 description="Prepaid card purchase triggered by elder-fraud CALL-001"))
    link(evt_001, loc_002, "Occurred_At")
    link(evt_002, coc_action_ids[0], "Related_To")
    link(evt_002, loc_003, "Occurred_At")

    # ------------------------------------------------------------------
    # Phase 2 — RICO enterprise, crypto, Lam / Victim-7
    # ------------------------------------------------------------------
    enterprise = uid("org-pga-enterprise")
    add({
        "@id": enterprise,
        "@type": ["rico:RacketeeringEnterprise", "uco-identity:Organization"],
        "uco-core:name": "Phantom Gate Alliance (PGA)",
        "uco-core:description": (
            "Association-in-fact criminal enterprise: elder-fraud call centers, "
            "crypto social engineering, peel-chain laundering, insider recruitment, "
            "APT malware (GateRunner), juvenile sextortion money mules."
        ),
        "rico:enterpriseType": "association-in-fact",
        "uco-core:tag": ["criminal-enterprise", "PGA"],
    })

    roles = {
        "call-center-operator": ("Call-center operator", "Raj 'King K' Mehta (India)"),
        "voice-social-engineer": ("Voice social engineer", "Victor Lam"),
        "target-identifier": ("Target identifier", "COCONSPIRATOR T.I."),
        "money-launderer": ("Money launderer", "Ferro, Tangeman"),
        "apt-operator": ("APT operator", "COCONSPIRATOR A.P."),
        "juvenile-recruiter": ("Juvenile recruiter", 'alias "NovaBlade"'),
    }
    role_ids: dict[str, str] = {}
    for slug, (title, holder) in roles.items():
        rid = uid(f"role-{slug}")
        role_ids[slug] = rid
        add({
            "@id": rid,
            "@type": ["rico:EnterpriseRole", "uco-role:Role"],
            "uco-core:name": f"PGA role: {title}",
            "uco-core:description": f"Enterprise division of labor — {holder}.",
            "rico:roleFunction": slug,
        })
        link(rid, enterprise, "Role_Within")

    link(victor_lam, role_ids["voice-social-engineer"], "Has_Role")
    link(king_k, role_ids["call-center-operator"], "Has_Role")
    link(novablade, role_ids["juvenile-recruiter"], "Has_Role")

    call_002_facet = uid("call-002-facet")
    call_002 = uid("call-002")
    msg_003_facet = uid("msg-003-facet")
    msg_003 = uid("msg-003")
    add(
        {
            "@id": call_002_facet,
            "@type": "uco-observable:CallFacet",
            "uco-observable:from": {"@id": lam_voip},
            "uco-observable:to": {"@id": victim_7_phone},
            "uco-observable:startTime": lit("xsd:dateTime", "2024-08-18T14:22:00-04:00"),
            "uco-observable:duration": lit("xsd:integer", 1904),
        },
        {
            "@id": call_002,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CALL-002 Lam cold-call to Victim-7",
            "uco-core:description": (
                "Caller claimed unauthorized login from Singapore; instructed "
                "Victim-7 to install AnyDesk. Linked MSG-003."
            ),
            "uco-core:hasFacet": [{"@id": call_002_facet}],
        },
        {
            "@id": msg_003_facet,
            "@type": "uco-observable:MessageFacet",
            "uco-observable:from": {"@id": lam_voip},
            "uco-observable:to": {"@id": victim_7_phone},
            "uco-observable:messageText": (
                "CoinShield: secure remote verification required. Install AnyDesk "
                "(Session ID 1 234 567 890)"
            ),
            "uco-observable:sentTime": lit("xsd:dateTime", "2024-08-18T14:58:33-04:00"),
        },
        {
            "@id": msg_003,
            "@type": "uco-observable:Message",
            "uco-core:name": "MSG-003 AnyDesk link SMS to Victim-7",
            "uco-core:hasFacet": [{"@id": msg_003_facet}],
        },
    )
    link(call_002, victor_lam, "Attributed_To")
    link(call_002, msg_003, "Followed_By")

    evt_003 = uid("evt-003")
    add({
        "@id": evt_003,
        "@type": "uco-core:Event",
        "uco-core:name": "EVT-003 AnyDesk remote session (Victim-7)",
        "uco-core:startTime": lit("xsd:dateTime", "2024-08-18T15:02:11-04:00"),
        "uco-core:endTime": lit("xsd:dateTime", "2024-08-18T15:47:28-04:00"),
        "uco-core:eventType": ["RemoteAccessSession"],
        "uco-core:eventAttribute": [dict_entries("evt-003", {
            "software": "AnyDesk 8.0.8",
            "session_id": "1234567890",
            "remote_ip": "198.51.100.44",
            "local_ip": "192.168.1.44",
            "bytes_out": "1288490188",
            "file_transfer": "seed-backup.txt",
        })],
    })
    link(evt_003, call_002, "Related_To")
    link(evt_003, msg_003, "Related_To")

    evt_004 = uid("evt-004")
    add({
        "@id": evt_004,
        "@type": "uco-core:Event",
        "uco-core:name": "EVT-004 Wallet transfer (Victim-7 theft)",
        "uco-core:startTime": lit("xsd:dateTime", "2024-08-18T19:52:11Z"),
        "uco-core:eventType": ["CryptocurrencyTransfer"],
        "uco-core:eventAttribute": [dict_entries("evt-004", {
            "chain": "Ethereum mainnet",
            "tx_hash": "0xabc88421def",
            "from": "0x7a3F8c2D9b1C4f8A",
            "to": "0x9b1C2d8E4f8A1a3B",
            "amount_eth": "12441.0",
            "usd_spot": "47093000",
        })],
    })

    # CRYPTO-001 peel chain
    crypto_victim_wallet = artifact_id("CRYPTO-001-VICTIM-WALLET")
    crypto_pass_through = uid("crypto-pass-through")
    crypto_peel_hop = uid("crypto-peel-hop")
    thorswap = uid("org-thorswap")
    add(
        {
            "@id": crypto_victim_wallet,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CRYPTO-001 — Victim-7 hot wallet (ACC-007)",
            "uco-core:hasFacet": [
                {
                    "@id": uid("crypto-victim-addr-facet"),
                    "@type": "cryptoinv:CryptocurrencyAddressFacet",
                    "cryptoinv:addressValue": "0x7a3F8c2D9b1C4f8A",
                    "cryptoinv:cryptocurrencyType": "ETH",
                    "cryptoinv:blockchainNetwork": "Ethereum",
                },
            ],
        },
        {
            "@id": crypto_pass_through,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CRYPTO-001 — PGA pass-through wallet",
            "uco-core:hasFacet": [
                {
                    "@id": uid("crypto-pass-addr-facet"),
                    "@type": "cryptoinv:CryptocurrencyAddressFacet",
                    "cryptoinv:addressValue": "0x9b1C2d8E4f8A1a3B",
                    "cryptoinv:cryptocurrencyType": "ETH",
                    "cryptoinv:blockchainNetwork": "Ethereum",
                },
            ],
        },
        {
            "@id": crypto_peel_hop,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CRYPTO-001 — peel hop 1 (0.5 ETH)",
            "uco-core:hasFacet": [
                {
                    "@id": uid("crypto-peel-addr-facet"),
                    "@type": "cryptoinv:CryptocurrencyAddressFacet",
                    "cryptoinv:addressValue": "0x2d8E1a3B4c5D6e7F",
                    "cryptoinv:cryptocurrencyType": "ETH",
                    "cryptoinv:blockchainNetwork": "Ethereum",
                },
            ],
        },
        {
            "@id": thorswap,
            "@type": ["cryptoinv:VirtualAssetServiceProvider", "uco-identity:Organization"],
            "uco-core:name": "Thorswap (no-KYC router)",
            "uco-core:description": "Decentralized exchange router in CRYPTO-001 peel chain hop 2.",
        },
    )
    link(crypto_victim_wallet, evt_004, "Related_To")
    link(crypto_pass_through, crypto_peel_hop, "Related_To")
    link(crypto_peel_hop, thorswap, "Transferred_Via")
    g.append(rel(crypto_victim_wallet, crypto_pass_through, "Transferred_To",
                 description="EVT-004 primary theft transfer (12,441 ETH)"))
    g.append(rel(crypto_pass_through, crypto_peel_hop, "Transferred_To",
                 description="CRYPTO-001 peel hop 1 (0.5 ETH segment)"))

    crypto_laundering_crime = uid("action-crypto-peel-laundering")
    chainalysis_tool = uid("tool-chainalysis-reactor")
    usss_analyst = uid("person-usss-crypto-analyst")
    mlar_csv = uid("crypto-mlar-binance-csv")
    crypto_trace_report = uid("crypto-trace-report-001")
    add(
        {
            "@id": crypto_laundering_crime,
            "@type": "uco-action:Action",
            "uco-core:name": "CRYPTO-001 peel chain laundering (subject conduct)",
            "uco-core:description": (
                "PGA subject conduct: peel chain via Thorswap and eXch.io; "
                "chain-hopping toward Monero — not an investigator action."
            ),
            "cryptoinv:launderingTechnique": [
                "peel-chain",
                "chain-hopping-to-monero",
                "crypto-to-cash",
            ],
            "uco-action:performer": {"@id": enterprise},
            "uco-action:object": [{"@id": crypto_victim_wallet}, {"@id": evt_004}],
            "uco-action:result": [
                {"@id": crypto_pass_through},
                {"@id": crypto_peel_hop},
            ],
        },
        {
            "@id": chainalysis_tool,
            "@type": "uco-tool:ConfiguredTool",
            "uco-core:name": "Chainalysis Reactor",
            "uco-core:description": "TRM/Chainalysis cluster trace configuration for CRYPTO-001.",
        },
        {
            "@id": usss_analyst,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "USSS cryptocurrency analyst (synthetic)",
        },
        {
            "@id": mlar_csv,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "FinCEN MLAR Binance return (ACC-006 cluster)",
            "uco-core:description": "DH-PGA-008 FINCEN-SAR-PROTECTED source CSV; synthetic fixture.",
            "uco-core:objectMarking": [{"@id": fincen_marking}],
            "uco-core:hasFacet": [
                {
                    "@id": uid("mlar-csv-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "mlar-binance-8847129033.csv",
                    "uco-observable:extension": "csv",
                },
            ],
        },
        {
            "@id": crypto_trace_report,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CRYPTO-001 wallet-cluster trace report",
            "uco-core:description": "Investigative analytic output linking peel hops to Thorswap router.",
        },
    )
    crypto_trace_action = uid("ia-crypto-trace-analysis")
    add({
        "@id": crypto_trace_action,
        "@type": "case-investigation:InvestigativeAction",
        "uco-core:name": "USSS blockchain trace of CRYPTO-001 peel chain",
        "uco-core:description": (
            "Investigator analytic action over EVT-004 and FinCEN MLAR return; "
            "distinct from subject laundering conduct."
        ),
        "uco-action:performer": {"@id": usss_analyst},
        "uco-action:instrument": {"@id": chainalysis_tool},
        "uco-action:object": [{"@id": evt_004}, {"@id": mlar_csv}, {"@id": crypto_victim_wallet}],
        "uco-action:result": [{"@id": crypto_trace_report}],
    })
    g.append(rel(crypto_trace_report, mlar_csv, "Derived_From",
                 description="Trace report derived from FINCEN-protected MLAR source"))

    instrument_ddc = uid("instrument-ddc-00417")
    charge_rico = uid("charge-ddc-rico")
    add(
        {
            "@id": instrument_ddc,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "D.D.C. 1:26-cr-00417 — RICO indictment",
            "legalproc:instrumentType": "indictment",
            "legalproc:caseIdentifier": "1:26-cr-00417-CKK",
        },
        {
            "@id": charge_rico,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Count 1: RICO Conspiracy (PGA enterprise)",
            "legalproc:statuteCitation": "18 U.S.C. § 1962(d)",
            "legalproc:countLabel": "Count 1",
            "legalproc:countNumber": lit("xsd:nonNegativeInteger", 1),
            "legalproc:offenseForm": "conspiracy",
            "legalproc:assertedIn": {"@id": instrument_ddc},
            "rico:predicateStatute": list(PREDICATE_STATUTES),
            "uco-core:description": (
                "Phantom Gate Alliance association-in-fact enterprise; "
                "predicate pattern includes wire fraud, money laundering, obstruction."
            ),
        },
    )
    link(victor_lam, charge_rico, "Charged_With")
    link(charge_rico, enterprise, "Targets_Enterprise")
    link(instrument_ddc, investigation, "part_of")

    # ART-002 Victim-7 source media + E01 + COC-002
    art_002_source_macbook = uid("art-002-source-macbook")
    art_002_source_ssd = uid("art-002-source-ssd")
    art_002 = artifact_id("ART-002")
    tableau_td3 = uid("tool-tableau-td3")
    ftk_imager = uid("tool-ftk-imager")
    examiner_v7 = uid("examiner-victim7")
    add(
        {
            "@id": art_002_source_macbook,
            "@type": ["uco-observable:Computer", "uco-core:UcoObject"],
            "uco-core:name": 'Victim-7 MacBook Pro 16" (source)',
            "uco-core:description": "APFS/FileVault laptop seized 2024-08-20; source for ART-002 imaging.",
        },
        {
            "@id": art_002_source_ssd,
            "@type": ["uco-observable:StorageMedium", "uco-core:UcoObject"],
            "uco-core:name": "Victim-7 internal SSD (source medium)",
            "uco-core:description": "Write-blocked imaging source for evidence-2024-001.E01.",
        },
        {
            "@id": art_002,
            "@type": [
                "uco-observable:ObservableObject",
                "uco-core:UcoObject",
                "solveit-observable:PhysicalImageContainer",
            ],
            "uco-core:name": "ART-002 evidence-2024-001.E01",
            "uco-core:description": (
                "Victim-7 MacBook SSD forensic image (E01) and SOLVE-IT physical "
                "image container; DCFO vault DV-2024-881; LEO-SENSITIVE."
            ),
            "uco-core:objectMarking": [{"@id": leo_marking}],
            "uco-core:hasFacet": [
                {
                    "@id": uid("art-002-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "evidence-2024-001.E01",
                    "uco-observable:extension": "E01",
                },
                {
                    "@id": uid("art-002-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        hash_facet("art-002-e01", "SHA256", synthetic_hash("art-002-e01")),
                    ],
                },
            ],
        },
        {
            "@id": tableau_td3,
            "@type": "uco-tool:Tool",
            "uco-core:name": "Tableau TD3 write blocker",
        },
        {
            "@id": ftk_imager,
            "@type": "uco-tool:Tool",
            "uco-core:name": "FTK Imager",
            "uco-tool:version": "4.7",
        },
        {
            "@id": examiner_v7,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Examiner M. Okonkwo (FBI DCFO)",
        },
    )
    link(art_002_source_ssd, art_002_source_macbook, "Contained_Within")

    prov_art_002 = uid("prov-art-002-digital")
    coc_002_imaging = uid("coc-002-imaging")
    add(
        {
            "@id": coc_002_imaging,
            "@type": "solveit-core:SolveitInvestigativeAction",
            "uco-core:name": "COC-002 — write-blocked imaging Victim-7 SSD",
            "uco-action:startTime": lit("xsd:dateTime", "2024-08-20T10:15:00-04:00"),
            "uco-action:performer": {"@id": examiner_v7},
            "uco-action:instrument": [{"@id": tableau_td3}, {"@id": ftk_imager}],
            "uco-action:object": [{"@id": art_002_source_ssd}],
            "uco-action:result": [{"@id": art_002}],
            "solveit-core:usedTechnique": [
                {"@id": SOLVEIT_DATA + "techniqueDFT-1002"},
                {"@id": SOLVEIT_DATA + "techniqueDFT-1012"},
            ],
            "solveit-core:appliedMitigation": [
                {"@id": SOLVEIT_DATA + "mitigationDFM-1003"},
                {"@id": SOLVEIT_DATA + "mitigationDFM-1004"},
            ],
            "uco-core:description": "Tableau TD3 + FTK Imager 4.7 → evidence-2024-001.E01.",
        },
        {
            "@id": prov_art_002,
            "@type": "case-investigation:ProvenanceRecord",
            "uco-core:name": "prov-art-002-digital (Victim-7 E01)",
            "case-investigation:exhibitNumber": "D.D.C. GX-101",
            "uco-core:object": [
                {"@id": art_002_source_macbook},
                {"@id": art_002_source_ssd},
                {"@id": art_002},
                {"@id": coc_002_imaging},
            ],
        },
    )
    include_in_investigation(art_002, art_002_source_macbook, coc_002_imaging)

    # FS-001 AnyDesk.exe
    fs_001 = uid("fs-001-anydesk")
    add({
        "@id": fs_001,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "FS-001 /Users/victim7/Downloads/AnyDesk.exe",
        "uco-core:hasFacet": [
            {
                "@id": uid("fs-001-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "AnyDesk.exe",
                "uco-observable:filePath": "/Users/victim7/Downloads/AnyDesk.exe",
                "uco-observable:sizeInBytes": lit("xsd:integer", 3421952),
                "uco-observable:observableCreatedTime": lit("xsd:dateTime", "2024-08-18T14:59:01-04:00"),
            },
            {
                "@id": uid("fs-001-hash-facet"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [
                    hash_facet("fs-001", "SHA256", synthetic_hash("fs-001-anydesk")),
                ],
            },
        ],
    })
    link(fs_001, art_002, "Contained_Within")
    link(fs_001, evt_003, "Related_To")

    # ART-003 Apex Semi PCAP (NET-001 flow summary modeled separately in long-tail)
    art_003 = artifact_id("ART-003")
    add({
        "@id": art_003,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "ART-003 apex-semi-20241103.pcap",
        "uco-core:objectMarking": [{"@id": leo_marking}, {"@id": corp_marking}],
        "uco-core:hasFacet": [
            {
                "@id": uid("art-003-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "apex-semi-20241103.pcap",
                "uco-observable:extension": "pcap",
            },
            {
                "@id": uid("art-003-hash-facet"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [
                    hash_facet("art-003", "SHA256", synthetic_hash("art-003-pcap")),
                ],
            },
        ],
        "uco-core:description": (
            "72-hour warrant mirror; gate-c2.darknet.invalid TLS 847 MB; "
            "AWS S3 ap-southeast-1 exfil 2.1 GB."
        ),
    })
    include_in_investigation(art_003)

    # ------------------------------------------------------------------
    # Phase 3 — Insider: MSG-004, EMAIL-001, EVT-006, EMAIL-002
    # ------------------------------------------------------------------
    msg_004_facet = uid("msg-004-facet")
    msg_004 = uid("msg-004")
    add(
        {
            "@id": msg_004_facet,
            "@type": "uco-observable:MessageFacet",
            "uco-observable:from": {"@id": mei_chen_wechat},
            "uco-observable:to": [{"@id": wechat_wl}],
            "uco-observable:messageText": (
                "Copied DTX-150 calibration folder to personal iCloud. Delete after read."
            ),
            "uco-observable:sentTime": lit("xsd:dateTime", "2024-09-05T07:12:00+08:00"),
        },
        {
            "@id": msg_004,
            "@type": "uco-observable:Message",
            "uco-core:name": "MSG-004 WeChat insider recruitment (Mei Chen ↔ W.L.)",
            "uco-core:description": "GX-22 N.D. Cal.; trade-secret theft via WeChat wxid_wl88421.",
            "uco-core:hasFacet": [{"@id": msg_004_facet}],
        },
    )
    link(msg_004, mei_chen_wechat, "Sent_By")
    link(msg_004, wechat_wl, "Addressed_To")

    email_001 = uid("email-001")
    email_from_001 = email_address(g, "email-001-from", "security-review@apexsemi-mail.net",
                                   "IT Security <security-review@apexsemi-mail.net>")
    email_to_001 = email_address(g, "email-001-to", "mei.chen@apexsemi.com")
    add({
        "@id": email_001,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "EMAIL-001 Spear-phish to Mei Chen",
        "uco-core:description": (
            "Message-ID <a7f3c2@mail-security-apexsemi.net>; SPF FAIL; "
            "Tor exit 185.220.101.44; attachment security_policy.pdf."
        ),
        "uco-core:hasFacet": [
            {
                "@id": uid("email-001-facet"),
                "@type": "uco-observable:EmailMessageFacet",
                "uco-observable:messageID": "<a7f3c2@mail-security-apexsemi.net>",
                "uco-observable:from": {"@id": email_from_001},
                "uco-observable:to": [{"@id": email_to_001}],
                "uco-observable:subject": "Mandatory credential rotation — action by EOD",
                "uco-observable:sentTime": lit("xsd:dateTime", "2024-09-12T09:01:22-07:00"),
            },
        ],
    })

    evt_006 = uid("evt-006")
    add({
        "@id": evt_006,
        "@type": "uco-core:Event",
        "uco-core:name": "EVT-006 Spear-phish click (Mei Chen)",
        "uco-core:startTime": lit("xsd:dateTime", "2024-09-12T09:04:18-07:00"),
        "uco-core:eventType": ["Authentication"],
        "uco-core:eventAttribute": [dict_entries("evt-006", {
            "method": "credential_phishing",
            "target_url": "https://apexsemi-mail.net/validate",
            "source_ip": "185.220.101.44",
            "outcome": "credentials_not_entered",
        })],
    })
    link(evt_006, email_001, "Related_To")
    g.append(rel(email_001, loc_007, "Delivered_To",
                 description="Spear-phish received/clicked at Apex Semi HQ campus"))

    email_002 = uid("email-002")
    email_from_002 = email_address(g, "email-002-from", "freight@jadehorizon-import.com")
    email_to_002 = email_address(g, "email-002-to", "wei.zhang@jadehorizon-import.com")
    add({
        "@id": email_002,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "EMAIL-002 False AES filing (Wei Zhang)",
        "uco-core:description": (
            "DTX-150 shipment AES confirmation; claimed EAR99 / JHI Nanjing; "
            "true end user GaStone Chengdu (Entity List 2014)."
        ),
        "uco-core:hasFacet": [
            {
                "@id": uid("email-002-facet"),
                "@type": "uco-observable:EmailMessageFacet",
                "uco-observable:from": {"@id": email_from_002},
                "uco-observable:to": [{"@id": email_to_002}],
                "uco-observable:subject": "RE: DTX-150 shipment — AES confirmation 20240318-88421",
                "uco-observable:sentTime": lit("xsd:dateTime", "2024-03-18T14:22:00-04:00"),
            },
        ],
    })
    link(email_002, wei_zhang, "Addressed_To")

    # ------------------------------------------------------------------
    # Phase 4 — GateRunner malware, registry persistence, ATT&CK
    # ------------------------------------------------------------------
    gatehelper = artifact_id("ART-007")
    gatehelper_hash = synthetic_hash("gatehelper-dll")
    add({
        "@id": gatehelper,
        "@type": [
            "uco-observable:File",
            "uco-observable:ObservableObject",
            "uco-core:UcoObject",
        ],
        "uco-core:name": "gatehelper.dll (GateRunner / Sagerunex-variant)",
        "uco-core:description": "Malware sample ART-007; air-gapped AG-07; SHA-256 from EVT-005.",
        "uco-core:hasFacet": [
            {
                "@id": uid("gatehelper-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "gatehelper.dll",
                "uco-observable:filePath": r"C:\ProgramData\Microsoft\Network\gatehelper.dll",
            },
            {
                "@id": uid("gatehelper-hash-facet"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [hash_facet("gatehelper", "SHA256", gatehelper_hash)],
            },
        ],
    })

    reg_key = artifact_id("FS-004")
    reg_facet = uid("fs-004-registry-facet")
    reg_val_image = uid("fs-004-regval-imagepath")
    reg_val_dll = uid("fs-004-regval-servicedll")
    service_tapisrv = uid("fs-004-service-tapisrv")
    add(
        {
            "@id": reg_val_image,
            "@type": "uco-observable:WindowsRegistryValue",
            "uco-core:name": "ImagePath",
            "uco-observable:data": r"%SystemRoot%\System32\svchost.exe -k LocalService -p -s TapiSrv",
            "uco-observable:dataType": "reg_expand_sz",
        },
        {
            "@id": reg_val_dll,
            "@type": "uco-observable:WindowsRegistryValue",
            "uco-core:name": "Parameters/ServiceDll",
            "uco-observable:data": r"C:\ProgramData\Microsoft\Network\gatehelper.dll",
            "uco-observable:dataType": "reg_expand_sz",
        },
        {
            "@id": reg_facet,
            "@type": "uco-observable:WindowsRegistryKeyFacet",
            "uco-observable:key": r"HKLM\SYSTEM\CurrentControlSet\Services\tapisrv",
            "uco-observable:registryValues": [
                {"@id": reg_val_image},
                {"@id": reg_val_dll},
            ],
        },
        {
            "@id": reg_key,
            "@type": "uco-observable:WindowsRegistryKey",
            "uco-core:name": "FS-004 GateRunner registry persistence (tapisrv)",
            "uco-core:hasFacet": [{"@id": reg_facet}],
        },
        {
            "@id": service_tapisrv,
            "@type": "uco-observable:WindowsService",
            "uco-core:name": "tapisrv (GateRunner persistence service)",
            "uco-core:hasFacet": [{
                "@id": uid("service-tapisrv-facet"),
                "@type": "uco-observable:WindowsServiceFacet",
                "uco-observable:serviceName": "TapiSrv",
                "uco-observable:startType": "service_auto_start",
                "uco-observable:startCommandLine": (
                    r"%SystemRoot%\System32\svchost.exe -k LocalService -p -s TapiSrv"
                ),
            }],
        },
    )
    gate_runner_actor = uid("threat-gaterunner-apt")
    add({
        "@id": gate_runner_actor,
        "@type": ["uco-identity:Organization", "uco-core:UcoObject"],
        "uco-core:name": "GateRunner APT (PGA affiliate)",
        "uco-core:description": "Threat actor behind GateRunner persistence on Apex Semi hosts.",
    })
    link(reg_key, gatehelper, "Related_To")
    link(reg_key, service_tapisrv, "Related_To")

    evt_005 = uid("evt-005")
    add({
        "@id": evt_005,
        "@type": "uco-core:Event",
        "uco-core:name": "EVT-005 Apex Semi EDR alert (GateRunner)",
        "uco-core:startTime": lit("xsd:dateTime", "2024-11-03T02:14:33Z"),
        "uco-core:eventType": ["SecurityAlert"],
        "uco-core:eventAttribute": [dict_entries("evt-005", {
            "edr_product": "CrowdStrike Falcon",
            "severity": "critical",
            "tactic": "Persistence",
            "technique": "T1543.003",
            "host": "apex-ws-88421.corp.apexsemi.com",
            "sha256": gatehelper_hash,
        })],
    })
    link(evt_005, gatehelper, "Related_To")
    link(evt_005, loc_007, "Occurred_At")

    persistence_action = uid("action-gaterunner-persistence")
    cookie_stealer_action = uid("action-gaterunner-cookie-stealer")
    add(
        {
            "@id": persistence_action,
            "@type": "uco-action:Action",
            "uco-core:name": "GateRunner service DLL registry persistence",
            "uco-core:description": (
                "GateRunner sideload via tapisrv ServiceDll pointing to gatehelper.dll "
                "(FS-004). ATT&CK T1543.003 via technique metaclass."
            ),
            "uco-action:object": [{"@id": reg_key}, {"@id": gatehelper}],
            "uco-action:result": [{"@id": service_tapisrv}],
            "uco-action:performer": {"@id": gate_runner_actor},
        },
        {
            "@id": cookie_stealer_action,
            "@type": "uco-action:Action",
            "uco-core:name": "Chrome cookie stealer execution",
            "uco-core:description": (
                "GateRunner post-compromise toolkit — steals Chrome cookies (T1539)."
            ),
        },
    )

    def exhibit_attack(action_id: str, tids: list[str]) -> None:
        attack_iri = "https://attack.mitre.org/techniques/"
        for node in g:
            if node.get("@id") == action_id:
                cur = node["@type"]
                types = [cur] if isinstance(cur, str) else list(cur)
                for tid in tids:
                    iri = attack_iri + tid
                    if iri not in types:
                        types.append(iri)
                node["@type"] = types
                return
        raise KeyError(action_id)

    exhibit_attack(persistence_action, ["T1543.003"])
    exhibit_attack(cookie_stealer_action, ["T1539"])

    # ------------------------------------------------------------------
    # Phase 5 — CAC: CyberTip, sextortion, PhotoDNA (subset-safe types)
    # ------------------------------------------------------------------
    streamvault = uid("org-streamvault")
    cybertip_images = uid("cybertip-001-image-set")
    add(
        {
            "@id": streamvault,
            "@type": "uco-identity:Organization",
            "uco-core:name": "StreamVault ESP",
            "uco-core:description": "Platform ACC-009 @novablade_884; NCMEC CyberTip pipeline.",
        },
        {
            "@id": cybertip_images,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CYBERTIP-001 image set (5 images)",
            "uco-core:description": "ART-005 StreamVault CyberTip bundle; CAC-RESTRICTED handling.",
        },
    )

    evt_008 = uid("evt-008")
    add({
        "@id": evt_008,
        "@type": "uco-core:Event",
        "uco-core:name": "EVT-008 NCMEC CyberTip submission",
        "uco-core:startTime": lit("xsd:dateTime", "2025-08-19T18:02:00Z"),
        "uco-core:eventType": ["CyberTipReport"],
        "uco-core:eventAttribute": [dict_entries("evt-008", {
            "cybertip_id": "2025-88421",
            "esp": "StreamVault",
            "reporter": "automated CSAM classifier",
            "ip_preservation": "185.220.101.55",
        })],
    })
    link(evt_008, streamvault, "Related_To")
    link(evt_008, cybertip_images, "Related_To")

    msg_006_facet = uid("msg-006-facet")
    msg_006 = uid("msg-006")
    grooming = uid("cac-grooming-sextortion")
    juvenile_ce_auth = uid("auth-juvenile-ce")
    add({
        "@id": juvenile_ce_auth,
        "@type": "case-investigation:Authorization",
        "uco-core:name": "ICAC CE warrant — Juvenile J-1 device (chat-only scope)",
        "uco-core:description": (
            "Device-only examination authorization; SOLVE-IT DFT-1048 limits "
            "processing to chat-only messages; no joint storage with adult devices; "
            "JUVENILE-PRIVACY marking required on all exports."
        ),
    })
    register_auth(juvenile_ce_auth)
    add(
        {
            "@id": msg_006_facet,
            "@type": "uco-observable:MessageFacet",
            "uco-observable:from": {"@id": streamvault_nova},
            "uco-observable:to": [{"@id": uid("acc-j1-streamvault")}],
            "uco-observable:messageText": (
                "Send another or I post the edited pics to your school group."
            ),
            "uco-observable:sentTime": lit("xsd:dateTime", "2025-08-19T21:33:00-08:00"),
        },
        {
            "@id": msg_006,
            "@type": ["uco-observable:Message", "cacontology-grooming:GroomingMessage"],
            "uco-core:name": "MSG-006 ICAC grooming / sextortion (J-1 ↔ NovaBlade)",
            "uco-core:hasFacet": [{"@id": msg_006_facet}],
        },
        {
            "@id": grooming,
            "@type": ["cacontology-grooming:OnlineGrooming", "uco-action:Action"],
            "uco-core:name": "NovaBlade sextortion of Juvenile J-1",
            "uco-core:description": (
                "Financial sextortion via StreamVault; Cash App routing 041215663; "
                "DFT-1048 partial processing scope."
            ),
            "uco-action:performer": {"@id": novablade},
            "cacontology-grooming:targetsVictim": {"@id": juvenile_j1},
            "uco-action:object": [{"@id": msg_006}],
        },
    )
    authorize_action(
        grooming,
        juvenile_ce_auth,
        note="ICAC CE warrant scoped grooming/sexual coercion interpretation",
    )
    # Re-type juvenile as ChildVictim for CAC subset
    for node in g:
        if node.get("@id") == juvenile_j1:
            node["@type"] = ["uco-identity:Person", "cacontology-grooming:ChildVictim"]
            break

    prov_coc_005 = uid("prov-coc-005-juvenile")
    add({
        "@id": prov_coc_005,
        "@type": "case-investigation:ProvenanceRecord",
        "uco-core:name": "COC-005 — Juvenile J-1 device (isolated provenance)",
        "uco-core:description": (
            "ICAC CE warrant device-only; DFT-1048 chat-only scope; "
            "JUVENILE-PRIVACY marking; no joint storage with adult devices."
        ),
        "uco-core:objectMarking": [{"@id": cac_marking}, {"@id": juvenile_marking}],
        "uco-core:object": [{"@id": grooming}],
    })

    photodna_tool = uid("tool-photodna-v2")
    photodna_detection = uid("detection-photodna-001")
    ai_001 = uid("ia-ai-001-photodna")
    add(
        {
            "@id": photodna_tool,
            "@type": "uco-tool:Tool",
            "uco-core:name": "PhotoDNA Cloud API v2",
            "uco-tool:version": "2.0",
        },
        {
            "@id": photodna_detection,
            "@type": ["uco-core:UcoObject", "cacontology-detection:DetectionResult"],
            "uco-core:name": "PhotoDNA hash match — CyberTip 2025-88421",
            "cacontology-detection:confidenceScore": lit("xsd:decimal", "0.997"),
        },
        {
            "@id": ai_001,
            "@type": ["case-investigation:InvestigativeAction", "cac-core:InvestigativeAction"],
            "uco-core:name": "PhotoDNA hash analysis — CyberTip 2025-88421 (AI-001)",
            "uco-action:instrument": {"@id": photodna_tool},
            "uco-action:object": [{"@id": cybertip_images}],
            "uco-action:result": [{"@id": photodna_detection}],
        },
    )

    # ------------------------------------------------------------------
    # Phase 6 — Weapons and drugs (LOC-009 Fargo safehouse)
    # ------------------------------------------------------------------
    sig_p365 = uid("item-sig-p365")
    meth = uid("item-meth-482g")
    add(
        {
            "@id": sig_p365,
            "@type": "weap:Handgun",
            "uco-core:name": "SIG Sauer P365 (Fargo safehouse seizure)",
            "uco-core:description": "Seized at LOC-009 PGA Fargo safehouse during coordinated takedown.",
            "weap:make": "SIG Sauer",
            "weap:model": "P365",
            "weap:caliber": "9mm",
        },
        {
            "@id": meth,
            "@type": "drug:ControlledSubstance",
            "uco-core:name": "482g methamphetamine mixture (Fargo safehouse)",
            "uco-core:description": (
                "482 grams methamphetamine mixture seized at LOC-009; Schedule II."
            ),
            "drug:substance": {"@id": "obo:CHEBI_6809"},
            "drug:substanceName": "methamphetamine mixture",
            "drug:csaSchedule": "II",
            "drug:mass": lit("xsd:decimal", "482"),
            "drug:massUnit": "g",
            "drug:purityBasis": "mixture",
        },
    )
    link(sig_p365, loc_009, "Seized_At")
    link(meth, loc_009, "Seized_At")

    # ------------------------------------------------------------------
    # Phase 7 — SOLVE-IT acquisition overlays (Keel logical + Victim-7 verify)
    # ------------------------------------------------------------------
    keel_logical_container = uid("keel-logical-image-container")
    add(
        {
            "@id": keel_logical_container,
            "@type": "solveit-observable:LogicalImageContainer",
            "uco-core:name": "keel-iphone-UFED.zip logical container",
            "solveit-observable:contains": [{"@id": art_001_image}],
        },
    )

    solveit_keel = uid("solveit-keel-acquisition")
    add({
        "@id": solveit_keel,
        "@type": "solveit-core:SolveitInvestigativeAction",
        "uco-core:name": "Keel iPhone logical extraction (DFT-1019, DFT-1042)",
        "uco-core:description": (
            "SOLVE-IT overlay for COC-001 step 5; source device → logical UFED output."
        ),
        "solveit-core:usedTechnique": [
            {"@id": SOLVEIT_DATA + "techniqueDFT-1019"},
            {"@id": SOLVEIT_DATA + "techniqueDFT-1042"},
        ],
        "uco-action:performer": {"@id": examiner_keel},
        "uco-action:instrument": {"@id": ufed_tool},
        "uco-action:object": [{"@id": art_001}],
        "uco-action:result": [{"@id": art_001_image}, {"@id": keel_logical_container}],
        "uco-action:startTime": lit("xsd:dateTime", "2022-04-05T09:00:00-05:00"),
    })

    v7_bitstream = uid("v7-bitstream")
    hash_verify_result = uid("v7-hash-verification")
    add(
        {
            "@id": v7_bitstream,
            "@type": "solveit-observable:Bitstream",
            "uco-core:name": "Victim-7 SSD sector bitstream",
        },
        {
            "@id": hash_verify_result,
            "@type": "solveit-observable:HashVerificationResult",
            "uco-core:name": "SHA-256 match source vs E01 image",
        },
    )
    for node in g:
        if node.get("@id") == art_002:
            node["solveit-observable:contains"] = [{"@id": v7_bitstream}]
            break

    solveit_v7_acquire = uid("solveit-v7-acquisition")
    solveit_v7_verify = uid("solveit-v7-hash-verify")
    add(
        {
            "@id": solveit_v7_acquire,
            "@type": "solveit-core:SolveitInvestigativeAction",
            "uco-core:name": "Victim-7 SSD imaging overlay (DFT-1002, DFT-1012)",
            "uco-core:description": "SOLVE-IT overlay aligned with COC-002 imaging action.",
            "solveit-core:usedTechnique": [
                {"@id": SOLVEIT_DATA + "techniqueDFT-1002"},
                {"@id": SOLVEIT_DATA + "techniqueDFT-1012"},
            ],
            "uco-action:performer": {"@id": examiner_v7},
            "uco-action:instrument": [{"@id": tableau_td3}, {"@id": ftk_imager}],
            "uco-action:object": [{"@id": art_002_source_ssd}],
            "uco-action:result": [{"@id": art_002}, {"@id": v7_bitstream}],
            "uco-action:startTime": lit("xsd:dateTime", "2024-08-20T10:15:00-04:00"),
        },
        {
            "@id": solveit_v7_verify,
            "@type": ["uco-action:Action", "solveit-data:techniqueDFT-1042"],
            "uco-core:name": "Hash verify Victim-7 source vs E01 (DFT-1042)",
            "uco-action:performer": {"@id": examiner_v7},
            "uco-action:object": [{"@id": art_002_source_ssd}, {"@id": art_002}],
            "uco-action:result": [{"@id": hash_verify_result}],
        },
    )

    # ------------------------------------------------------------------
    # DH-PGA-003 discovery redaction (DFT-1046)
    # ------------------------------------------------------------------
    redacted_keel_export = uid("keel-ufed-redacted-discovery")
    redaction_action = uid("ia-redaction-dft-1046")
    add(
        {
            "@id": redacted_keel_export,
            "@type": ["solveit-observable:RedactedFileSet", "uco-core:UcoObject"],
            "uco-core:name": "keel-iphone-UFED-redacted-discovery.zip",
            "uco-core:description": (
                "DH-PGA-003 minimization export; third-party victim PII redacted "
                "for defense discovery; full content retained in prosecutor vault."
            ),
            "uco-core:objectMarking": [{"@id": leo_marking}],
            "uco-core:hasFacet": [
                {
                    "@id": uid("keel-redacted-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "keel-iphone-UFED-redacted-discovery.zip",
                    "uco-observable:extension": "zip",
                },
                {
                    "@id": uid("keel-redacted-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        hash_facet(
                            "keel-redacted",
                            "SHA256",
                            synthetic_hash("keel-ufed-redacted-discovery"),
                        ),
                    ],
                },
            ],
        },
        {
            "@id": redaction_action,
            "@type": "solveit-core:SolveitInvestigativeAction",
            "uco-core:name": "Discovery redaction — Keel UFED export (DFT-1046)",
            "uco-core:description": (
                "DH-PGA-003 minimization: redact third-party victim PII before "
                "defense discovery; prosecutor vault retains full UFED image."
            ),
            "solveit-core:usedTechnique": [
                {"@id": SOLVEIT_DATA + "techniqueDFT-1046"},
            ],
            "uco-action:performer": {"@id": examiner_keel},
            "uco-action:object": [{"@id": art_001_image}],
            "uco-action:result": [{"@id": redacted_keel_export}],
            "uco-action:startTime": lit("xsd:dateTime", "2022-04-12T14:00:00-05:00"),
        },
    )
    g.append(rel(redacted_keel_export, art_001_image, "Derived_From",
                 description="Redacted discovery export derived from full UFED image"))

    # ------------------------------------------------------------------
    # AI-002 CLIP semantic search — IMG_0042 + ConfidenceFacet 0.89
    # ------------------------------------------------------------------
    img_0042 = artifact_id("FS-008")
    clip_conf_facet = uid("img-0042-confidence-facet")
    clip_tool = uid("tool-clip-vit-b32")
    ai_002 = uid("ia-ai-002-clip")
    img_0038 = uid("img-0038-clip-rank2")
    img_0011 = uid("img-0011-clip-rank3")
    add(
        {
            "@id": img_0038,
            "@type": ["uco-observable:RasterPicture", "uco-core:UcoObject"],
            "uco-core:name": "IMG_0038.JPG CLIP rank 2 (0.71)",
            "uco-core:hasFacet": [{"@id": uid("img-0038-conf"), "@type": "uco-core:ConfidenceFacet",
                                   "uco-core:confidence": lit("xsd:nonNegativeInteger", 71)}],
        },
        {
            "@id": img_0011,
            "@type": ["uco-observable:RasterPicture", "uco-core:UcoObject"],
            "uco-core:name": "IMG_0011.JPG CLIP rank 3 (0.68)",
            "uco-core:hasFacet": [{"@id": uid("img-0011-conf"), "@type": "uco-core:ConfidenceFacet",
                                   "uco-core:confidence": lit("xsd:nonNegativeInteger", 68)}],
        },
    )
    add(
        {
            "@id": clip_conf_facet,
            "@type": "uco-core:ConfidenceFacet",
            "uco-core:confidence": lit("xsd:nonNegativeInteger", 89),
        },
        {
            "@id": img_0042,
            "@type": ["uco-observable:RasterPicture", "uco-core:UcoObject"],
            "uco-core:name": "IMG_0042.JPG package confirmation photo",
            "uco-core:description": (
                "Keel iPhone DCIM; EXIF GPS 30.5042°N 90.4621°W corroborates LOC-003; "
                "CLIP query 'cash in envelope package confirmation' rank 1 similarity 0.89."
            ),
            "uco-core:hasFacet": [
                {
                    "@id": uid("img-0042-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "IMG_0042.JPG",
                    "uco-observable:filePath": "private/var/mobile/Media/DCIM/100APPLE/IMG_0042.JPG",
                },
                {
                    "@id": uid("img-0042-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        hash_facet("img-0042", "SHA256", synthetic_hash("img-0042")),
                    ],
                },
                {"@id": clip_conf_facet},
            ],
        },
        {
            "@id": clip_tool,
            "@type": "uco-tool:ConfiguredTool",
            "uco-core:name": "CLIP ViT-B/32",
            "uco-core:description": "Semantic image search over Keel DCIM folder (842 images).",
        },
        {
            "@id": ai_002,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "AI-002 CLIP semantic image search — courier package photos",
            "uco-action:instrument": {"@id": clip_tool},
            "uco-action:object": [{"@id": art_001_image}],
            "uco-action:result": [
                {"@id": img_0042},
                {"@id": img_0038},
                {"@id": img_0011},
            ],
            "uco-action:startTime": lit("xsd:dateTime", "2022-04-06T10:30:00-05:00"),
            "uco-action:actionStatus": "Success",
        },
    )
    g.append(rel(img_0042, loc_003, "Related_To",
                 description="EXIF GPS corroborates Tangipahoa handoff location LOC-003"))
    g.append(rel(img_0042, art_001_image, "Selected_From",
                 description="CLIP rank-1 from Keel DCIM folder (842 images)"))

    # ------------------------------------------------------------------
    # Identity links, expanded markings, victim impact
    # ------------------------------------------------------------------
    # Has_Account — person ↔ account observables (identity-correlation recipe)
    identity_links = [
        (keel, keel_phone, "Has_Account"),
        (keel, keel_icloud, "Has_Account"),
        (king_k, king_k_phone, "Has_Account"),
        (king_k, king_k_india, "Has_Account"),
        (victim_a, victim_a_phone, "Has_Account"),
        (victor_lam, lam_voip, "Has_Account"),
        (victim_7, victim_7_phone, "Has_Account"),
        (victim_7, crypto_victim_wallet, "Has_Account"),
        (mei_chen, email_to_001, "Has_Account"),
        (wl_recruiter, wechat_wl, "Has_Account"),
        (wei_zhang, email_to_002, "Has_Account"),
        (novablade, streamvault_nova, "Has_Account"),
        (kyle_marsh, discord_marsh, "Has_Account"),
    ]
    for source, target, kind in identity_links:
        link(source, target, kind)

    # Cross-platform wallet / messenger correlation (scenario identity-correlation action)
    g.append(rel(telegram_coach, crypto_pass_through, "Associated_Account",
                 description="USSS wallet clustering linked ACC-004 Telegram to peel-chain pass-through"))
    g.append(rel(binance_mule, crypto_peel_hop, "Associated_Account",
                 description="FinCEN MLAR Binance UID 8847129033 associated with peel hop 1"))
    link(anydesk_session, evt_003, "Related_To")
    link(victim_7, evt_003, "Related_To")
    link(streamvault_nova, streamvault, "Related_To")

    # Victim-centric financial impact
    g.append(rel(victim_a, evt_001, "Related_To",
                 description="Elder fraud victim financial loss ($500 prepaid card purchase)"))
    g.append(rel(victim_7, evt_004, "Related_To",
                 description="Cryptocurrency theft victim; $47,093,000 USD spot value at transfer"))

    # Expanded objectMarking application
    for nid in (call_003, msg_001, intercept_action):
        apply_marking(nid, leo_marking)
    apply_marking(mlar_csv, fincen_marking)
    apply_marking(crypto_trace_report, fincen_marking)
    for nid in (cybertip_images, msg_006, grooming, ai_001, photodna_detection):
        apply_marking(nid, cac_marking)
    apply_marking(juvenile_j1, juvenile_marking)
    apply_marking(gatehelper, malware_marking)
    apply_marking(art_003, leo_marking, corp_marking)

    # Discord NDI with TS//SCI marking
    discord_ndi = uid("msg-005-ndi-attachment")
    add({
        "@id": discord_ndi,
        "@type": ["uco-observable:RasterPicture", "uco-core:UcoObject"],
        "uco-core:name": "IMG-NDI-001.jpg — TS//SCI slide photograph",
        "uco-core:description": "Kyle Marsh Discord #vault-leaks attachment; ART-004 handling.",
        "uco-core:objectMarking": [{"@id": ts_marking}],
        "uco-core:hasFacet": [
            {
                "@id": uid("ndi-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "IMG-NDI-001.jpg",
            },
        ],
    })
    link(discord_ndi, discord_marsh, "Related_To")
    link(discord_ndi, kyle_marsh, "Attributed_To")

    # ------------------------------------------------------------------
    # Long-tail coverage (ChatGPT deferred items): per-docket investigations,
    # ART-003..008, MSG threads, PROC-001..010, COC-003/004, AI-003/004, etc.
    # ------------------------------------------------------------------
    longtail_added = add_longtail({
        "g": g,
        "add": add,
        "link": link,
        "rel": rel,
        "uid": uid,
        "lit": lit,
        "artifact_id": artifact_id,
        "dict_entries": dict_entries,
        "hash_facet": hash_facet,
        "synthetic_hash": synthetic_hash,
        "location": location,
        "apply_marking": apply_marking,
        "include_in_investigation": include_in_investigation,
        "SOLVEIT_DATA": SOLVEIT_DATA,
        "investigation": investigation,
        "leo_marking": leo_marking,
        "ts_marking": ts_marking,
        "cac_marking": cac_marking,
        "juvenile_marking": juvenile_marking,
        "fincen_marking": fincen_marking,
        "malware_marking": malware_marking,
        "corp_marking": corp_marking,
        "art_001": art_001,
        "art_001_image": art_001_image,
        "art_002": art_002,
        "art_002_source_macbook": art_002_source_macbook,
        "art_002_source_ssd": art_002_source_ssd,
        "art_003": art_003,
        "gatehelper": gatehelper,
        "mlar_csv": mlar_csv,
        "crypto_trace_action": crypto_trace_action,
        "crypto_trace_report": crypto_trace_report,
        "chainalysis_tool": chainalysis_tool,
        "cybertip_images": cybertip_images,
        "photodna_detection": photodna_detection,
        "ai_001": ai_001,
        "ai_002": ai_002,
        "img_0042": img_0042,
        "msg_001": msg_001,
        "msg_003": msg_003,
        "msg_004": msg_004,
        "msg_006": msg_006,
        "msg_006_facet": msg_006_facet,
        "grooming": grooming,
        "juvenile_j1": juvenile_j1,
        "juvenile_ce_auth": juvenile_ce_auth,
        "prov_coc_005": prov_coc_005,
        "discord_ndi": discord_ndi,
        "discord_marsh": discord_marsh,
        "kyle_marsh": kyle_marsh,
        "keel_phone": keel_phone,
        "king_k_phone": king_k_phone,
        "victim_7_phone": victim_7_phone,
        "telegram_coach": telegram_coach,
        "wechat_wl": wechat_wl,
        "wl_recruiter": wl_recruiter,
        "mei_chen": mei_chen,
        "mei_chen_wechat": mei_chen_wechat,
        "register_auth": register_auth,
        "authorize_action": authorize_action,
        "wei_zhang": wei_zhang,
        "victor_lam": victor_lam,
        "victim_7": victim_7,
        "novablade": novablade,
        "streamvault_nova": streamvault_nova,
        "evt_003": evt_003,
        "evt_005": evt_005,
        "evt_008": evt_008,
        "call_003": call_003,
        "call_002": call_002,
        "loc_003": loc_003,
        "loc_004": loc_004,
        "loc_007": loc_007,
        "loc_009": loc_009,
        "loc_010": loc_010,
        "instrument_edla": instrument_edla,
        "instrument_ddc": instrument_ddc,
        "charge_edla": charge_edla,
        "charge_rico": charge_rico,
        "examiner_keel": examiner_keel,
        "examiner_v7": examiner_v7,
        "ufed_tool": ufed_tool,
        "ftk_imager": ftk_imager,
        "fs_001": fs_001,
        "reg_key": reg_key,
        "enterprise": enterprise,
        "streamvault": streamvault,
        "email_001": email_001,
        "email_002": email_002,
        "email_to_001": email_to_001,
        "coc_action_ids": coc_action_ids,
        "coc_002_imaging": coc_002_imaging,
        "solveit_keel": solveit_keel,
        "solveit_v7_acquire": solveit_v7_acquire,
        "solveit_v7_verify": solveit_v7_verify,
        "hash_verify_result": hash_verify_result,
        "crypto_victim_wallet": crypto_victim_wallet,
        "title_iii_auth": title_iii_auth,
    })

    # Link key entities to investigation + populate Investigation.object
    part_of_nodes = (
        call_001, call_002, call_003, msg_001, msg_003, msg_004, msg_006,
        email_001, email_002, art_001, art_002, art_003, fs_001,
        enterprise, gatehelper, evt_001, evt_002, evt_003, evt_004,
        evt_005, evt_006, evt_008, crypto_victim_wallet, solveit_keel,
        solveit_v7_acquire, sig_p365, meth, grooming, ai_001,
        redaction_action, tower_004, kyle_marsh, discord_ndi,
        prov_art_001_physical, prov_art_001_digital, prov_art_002,
        crypto_laundering_crime, crypto_trace_action, mlar_csv,
        instrument_edla, instrument_ddc, wl_recruiter,
    )
    investigation_object_ids = sorted(set(
        investigation_contents + list(part_of_nodes) + longtail_added
    ))
    for node in g:
        if node.get("@id") == investigation:
            node["uco-core:object"] = [{"@id": nid} for nid in investigation_object_ids]
            node["case-investigation:relevantAuthorization"] = [
                {"@id": a} for a in investigation_authorizations
            ]
            break

    add_weakness_evaluation_set(
        g, add, uid, lit,
        label="art-002-imaging",
        technique="DFT-1002",
        weakness="DFW-1004",
        evaluator_id=examiner_v7,
        likelihood=1,
        impact=3,
        likelihood_rationale="Tableau TD3 write blocker and verified imaging firmware.",
        impact_rationale="Omitted sectors could exclude seed-backup carve evidence.",
        solvit_data=SOLVEIT_DATA,
    )
    add_weakness_evaluation_set(
        g, add, uid, lit,
        label="art-001-logical",
        technique="DFT-1019",
        weakness="DFW-1019",
        evaluator_id=examiner_keel,
        likelihood=2,
        impact=3,
        likelihood_rationale="Faraday bag and airplane mode before UFED logical extraction.",
        impact_rationale="Remote wipe could destroy iMessage thread evidence.",
        solvit_data=SOLVEIT_DATA,
    )
    add_weakness_evaluation_set(
        g, add, uid, lit,
        label="art-006-partial",
        technique="DFT-1019",
        weakness="DFW-1048",
        evaluator_id=examiner_keel,
        likelihood=2,
        impact=3,
        likelihood_rationale="Partial iOS logical gap documented; chat-only DFT-1048 scope.",
        impact_rationale="Unrelated media carve would violate juvenile privacy scope.",
        solvit_data=SOLVEIT_DATA,
    )
    add_weakness_evaluation_set(
        g, add, uid, lit,
        label="dft-1046-redaction",
        technique="DFT-1046",
        weakness="DFW-1046",
        evaluator_id=examiner_keel,
        likelihood=1,
        impact=2,
        likelihood_rationale="Structured redaction workflow with human review checkpoint.",
        impact_rationale="Over-redaction could remove probative non-CSAM context.",
        solvit_data=SOLVEIT_DATA,
    )

    run_acceptance_gates(g, SCENARIO_SHA256)

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-analysis": "https://ontology.unifiedcyberontology.org/uco/analysis/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "uco-marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
            "marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
            "legalproc": "https://ontology.caseontology.org/case/criminal/",
            "rico": "http://example.org/ontology/rico/",
            "cryptoinv": "http://example.org/ontology/cryptoinv/",
            "solveit-core": "https://ontology.solveit-df.org/solveit/core/",
            "solveit-observable": "https://ontology.solveit-df.org/solveit/observable/",
            "solveit-data": "https://ontology.solveit-df.org/solveit/data/",
            "solveit-wa": "https://ontology.solveit-df.org/solveit/weakness-assessment/",
            "weap": "http://example.org/ontology/weapons/",
            "drug": "http://example.org/ontology/drugs/",
            "obo": "http://purl.obolibrary.org/obo/",
            "cacontology": "https://cacontology.projectvic.org#",
            "cac-core": "https://cacontology.projectvic.org/core#",
            "cacontology-grooming": "https://cacontology.projectvic.org/grooming#",
            "cacontology-detection": "https://cacontology.projectvic.org/detection#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": g,
    }


def validate(path: Path) -> None:
    """Validate graph; raise on unavailable validator or non-conformance (fail-closed)."""
    if not validator_available():
        raise RuntimeError("validator_unavailable: case_validate not installed")

    report = validate_graph_file(
        path,
        project_root=ROOT,
        extensions=EXTENSIONS,
        extra_ontology_graphs=[ROOT / "ontology/solveit/solve-it-kb.ttl"],
        force_rdfs_inference=True,
    )
    print(f"combined conforms: {report.conforms}")
    print(report.safe_summary)

    if report.conforms is not True or report.verification_status != "complete":
        raise RuntimeError(report.safe_summary)


def main() -> int:
    graph = build_graph()
    OUTPUT.write_text(
        json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    node_count = len(graph["@graph"])
    print(f"wrote {OUTPUT} ({node_count} nodes)")
    print(f"scenario: {SCENARIO_DOC}")

    try:
        validate(OUTPUT)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
