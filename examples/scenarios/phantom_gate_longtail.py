"""Long-tail scenario coverage for Operation PHANTOM GATE.

Adds missing artifact IDs, per-docket investigations, messaging threads,
filesystem/network depth, PROC-001–010, AI-003/004, expanded COC/legal,
and CAC interpretation layers. Called from build_phantom_gate_scenario.py.
"""

from __future__ import annotations

from typing import Any, Callable


def add_longtail(ctx: dict[str, Any]) -> list[str]:
    """Append long-tail nodes; return IDs to include in investigation grouping."""
    g: list[dict] = ctx["g"]
    add: Callable[..., None] = ctx["add"]
    link: Callable[[str, str, str], None] = ctx["link"]
    rel: Callable[..., dict] = ctx["rel"]
    uid: Callable[[str], str] = ctx["uid"]
    lit: Callable[[str, Any], dict] = ctx["lit"]
    artifact_id: Callable[[str], str] = ctx["artifact_id"]
    dict_entries: Callable[[str, dict[str, str]], dict] = ctx["dict_entries"]
    hash_facet: Callable[[str, str, str], dict] = ctx["hash_facet"]
    synthetic_hash: Callable[[str], str] = ctx["synthetic_hash"]
    location: Callable[..., dict] = ctx["location"]
    apply_marking: Callable[[str, ...], None] = ctx["apply_marking"]
    include_in_investigation: Callable[[str, ...], None] = ctx["include_in_investigation"]
    SOLVEIT_DATA: str = ctx["SOLVEIT_DATA"]

    investigation = ctx["investigation"]
    grouping = uid("grouping-pga-operation")
    inv_elder = uid("inv-elder-fraud-edla")
    inv_rico = uid("inv-rico-crypto-ddc")
    inv_insider = uid("inv-insider-ndca")
    inv_export = uid("inv-export-ndca")
    inv_classified = uid("inv-classified-dmass")
    inv_cac = uid("inv-cac-alaska")
    inv_cti = uid("inv-cti-gaterunner")

    # Ensure longtail context carries the markings / refs expected by the
    # scenario contract (read values so CodeQL does not flag unused locals).
    required_ctx_keys = (
        "leo_marking",
        "corp_marking",
        "art_002_source_macbook",
        "ai_001",
        "ai_002",
        "msg_003",
        "msg_006_facet",
        "victor_lam",
        "victim_7",
        "loc_004",
        "loc_009",
        "examiner_keel",
        "streamvault",
        "coc_action_ids",
        "solveit_v7_acquire",
    )
    for key in required_ctx_keys:
        if key not in ctx or ctx[key] is None:
            raise KeyError(f"phantom_gate_longtail missing required ctx key: {key}")

    ts_marking = ctx["ts_marking"]
    cac_marking = ctx["cac_marking"]
    juvenile_marking = ctx["juvenile_marking"]
    fincen_marking = ctx["fincen_marking"]
    malware_marking = ctx["malware_marking"]

    # --- refs from main graph ---
    art_001 = ctx["art_001"]
    art_001_image = ctx["art_001_image"]
    art_002 = ctx["art_002"]
    art_003 = ctx["art_003"]
    gatehelper = ctx["gatehelper"]
    mlar_csv = ctx["mlar_csv"]
    crypto_trace_action = ctx["crypto_trace_action"]
    cybertip_images = ctx["cybertip_images"]
    photodna_detection = ctx["photodna_detection"]
    img_0042 = ctx["img_0042"]
    msg_001 = ctx["msg_001"]
    msg_004 = ctx["msg_004"]
    msg_006 = ctx["msg_006"]
    grooming = ctx["grooming"]
    juvenile_j1 = ctx["juvenile_j1"]
    juvenile_ce_auth = ctx["juvenile_ce_auth"]
    prov_coc_005 = ctx["prov_coc_005"]
    discord_ndi = ctx["discord_ndi"]
    discord_marsh = ctx["discord_marsh"]
    kyle_marsh = ctx["kyle_marsh"]
    keel_phone = ctx["keel_phone"]
    king_k_phone = ctx["king_k_phone"]
    victim_7_phone = ctx["victim_7_phone"]
    telegram_coach = ctx["telegram_coach"]
    wechat_wl = ctx["wechat_wl"]
    wl_recruiter = ctx["wl_recruiter"]
    mei_chen = ctx["mei_chen"]
    mei_chen_wechat = ctx["mei_chen_wechat"]
    authorize_action = ctx["authorize_action"]
    register_auth = ctx["register_auth"]
    novablade = ctx["novablade"]
    streamvault_nova = ctx["streamvault_nova"]
    evt_003 = ctx["evt_003"]
    evt_005 = ctx["evt_005"]
    evt_008 = ctx["evt_008"]
    call_003 = ctx["call_003"]
    call_002 = ctx["call_002"]
    loc_003 = ctx["loc_003"]
    loc_007 = ctx["loc_007"]
    loc_010 = ctx["loc_010"]
    instrument_edla = ctx["instrument_edla"]
    instrument_ddc = ctx["instrument_ddc"]
    charge_edla = ctx["charge_edla"]
    charge_rico = ctx["charge_rico"]
    examiner_v7 = ctx["examiner_v7"]
    ufed_tool = ctx["ufed_tool"]
    fs_001 = ctx["fs_001"]
    reg_key = ctx["reg_key"]
    enterprise = ctx["enterprise"]
    email_001 = ctx["email_001"]
    email_002 = ctx["email_002"]
    coc_002_imaging = ctx["coc_002_imaging"]
    solveit_keel = ctx["solveit_keel"]
    crypto_victim_wallet = ctx["crypto_victim_wallet"]
    title_iii_auth = ctx["title_iii_auth"]

    added: list[str] = []

    def track(*ids: str) -> None:
        added.extend(ids)
        include_in_investigation(*ids)

    # ------------------------------------------------------------------
    # Operation grouping + per-docket investigations
    # ------------------------------------------------------------------
    sub_investigations = [
        (inv_elder, "E.D. La. elder-fraud courier track", "2:26-cr-00115", instrument_edla),
        (inv_rico, "D.D.C. RICO/crypto social engineering", "1:26-cr-00417", instrument_ddc),
        (inv_insider, "N.D. Cal. insider trade-secret track", "3:26-cr-00141", None),
        (inv_export, "N.D. Cal. export-control false AES track", "3:26-cr-00446", None),
        (inv_classified, "D. Mass. classified disclosure (Kyle Marsh)", "1:26-cr-10159", None),
        (inv_cac, "D. Alaska CAC sextortion wing", "3:26-cr-00029", None),
        (inv_cti, "GateRunner CTI / Apex Semi intrusion analysis", None, None),
    ]
    add({
        "@id": grouping,
        "@type": ["uco-core:Grouping", "uco-core:UcoObject"],
        "uco-core:name": "Operation PHANTOM GATE — multi-docket grouping",
        "uco-core:description": (
            "Synthetic Tier-T0 umbrella grouping for elder fraud, RICO/crypto, "
            "insider/export, classified disclosure, CAC, and CTI sub-tracks."
        ),
    })
    track(grouping)
    sub_inv_ids: list[str] = []
    for iid, name, docket, instrument in sub_investigations:
        node: dict = {
            "@id": iid,
            "@type": "case-investigation:Investigation",
            "uco-core:name": name,
            "legalproc:caseIdentifier": docket,
        }
        add(node)
        link(iid, grouping, "part_of")
        sub_inv_ids.append(iid)
        track(iid)
    link(investigation, grouping, "part_of")
    link(inv_elder, charge_edla, "Related_To")
    link(inv_rico, charge_rico, "Related_To")
    link(inv_cac, grooming, "Related_To")
    link(inv_cti, gatehelper, "Related_To")
    link(inv_classified, kyle_marsh, "Related_To")
    link(inv_insider, mei_chen, "Related_To")
    link(inv_export, ctx["wei_zhang"], "Related_To")

    # ------------------------------------------------------------------
    # Authorizations (legal process breadth)
    # ------------------------------------------------------------------
    rule41_keel = uid("auth-rule41-keel")
    rule41_v7 = uid("auth-rule41-victim7")
    apex_consent = uid("auth-apex-consent")
    discord_lp = uid("auth-discord-lp-marsh")
    ncmec_preservation = uid("auth-ncmec-streamvault")
    mlart_romania = uid("auth-mlat-romania-vps")
    add(
        {
            "@id": rule41_keel,
            "@type": "case-investigation:Authorization",
            "uco-core:name": "Rule 41 search warrant — Keel iPhone (COC-001)",
            "uco-core:description": "Device seizure and examination authorization for ART-001.",
        },
        {
            "@id": rule41_v7,
            "@type": "case-investigation:Authorization",
            "uco-core:name": "Rule 41 search warrant — Victim-7 MacBook (COC-002)",
            "uco-core:description": "MacBook imaging authorization; FileVault key from victim interview.",
        },
        {
            "@id": apex_consent,
            "@type": "case-investigation:Authorization",
            "uco-core:name": "Apex Semi corporate consent — 72-hour PCAP mirror",
            "uco-core:description": "Corporate legal hold LH-2024-112; warrant ¶14 PCAP preservation.",
        },
        {
            "@id": discord_lp,
            "@type": "case-investigation:Authorization",
            "uco-core:name": "Discord law-enforcement preservation — Kyle Marsh",
            "uco-core:description": "LP request for #vault-leaks channel; ART-004 export scope.",
        },
        {
            "@id": ncmec_preservation,
            "@type": "case-investigation:Authorization",
            "uco-core:name": "NCMEC / StreamVault preservation order",
            "uco-core:description": "CyberTip 2025-88421 IP and account preservation.",
        },
        {
            "@id": mlart_romania,
            "@type": "case-investigation:Authorization",
            "uco-core:name": "MLAT Romania — VPS hosting preservation",
            "uco-core:description": "International MLAT for elder-fraud call-center VPS.",
        },
    )
    track(rule41_keel, rule41_v7, apex_consent, discord_lp, ncmec_preservation, mlart_romania)
    for auth in (rule41_keel, rule41_v7, juvenile_ce_auth, title_iii_auth):
        g.append(rel(auth, investigation, "Related_To", description="Authorization scoped to PGA investigation"))

    # Additional charging instruments
    instrument_ndca_insider = uid("instrument-ndca-00141")
    instrument_ndca_export = uid("instrument-ndca-00446")
    instrument_dmass = uid("instrument-dmass-10159")
    instrument_alaska = uid("instrument-alaska-00029")
    charge_ndca_insider = uid("charge-ndca-1832")
    charge_ndca_export = uid("charge-ndca-ieepa")
    charge_dmass = uid("charge-dmass-793e")
    charge_alaska = uid("charge-alaska-2422b")
    add(
        {
            "@id": instrument_ndca_insider,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "N.D. Cal. 3:26-cr-00141 — trade secret theft (Mei Chen)",
            "legalproc:instrumentType": "indictment",
            "legalproc:caseIdentifier": "3:26-cr-00141",
        },
        {
            "@id": charge_ndca_insider,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Economic Espionage Act / trade secret theft",
            "legalproc:statuteCitation": "18 U.S.C. § 1832",
            "legalproc:assertedIn": {"@id": instrument_ndca_insider},
        },
        {
            "@id": instrument_ndca_export,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "N.D. Cal. 3:26-cr-00446 — false AES / IEEPA",
            "legalproc:instrumentType": "indictment",
            "legalproc:caseIdentifier": "3:26-cr-00446",
        },
        {
            "@id": charge_ndca_export,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": "False AES filing / export control violation",
            "legalproc:statuteCitation": "50 U.S.C. § 1702 (IEEPA)",
            "legalproc:assertedIn": {"@id": instrument_ndca_export},
        },
        {
            "@id": instrument_dmass,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "D. Mass. 1:26-cr-10159 — espionage (Kyle Marsh)",
            "legalproc:instrumentType": "indictment",
            "legalproc:caseIdentifier": "1:26-cr-10159",
        },
        {
            "@id": charge_dmass,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Unauthorized retention of national defense information",
            "legalproc:statuteCitation": "18 U.S.C. § 793(e)",
            "legalproc:assertedIn": {"@id": instrument_dmass},
        },
        {
            "@id": instrument_alaska,
            "@type": ["legalproc:ChargingInstrument", "uco-core:UcoObject"],
            "uco-core:name": "D. Alaska 3:26-cr-00029 — CAC production",
            "legalproc:instrumentType": "indictment",
            "legalproc:caseIdentifier": "3:26-cr-00029",
        },
        {
            "@id": charge_alaska,
            "@type": ["legalproc:CriminalCharge", "uco-core:UcoObject"],
            "uco-core:name": "Coercion and enticement of a minor",
            "legalproc:statuteCitation": "18 U.S.C. § 2422(b)",
            "legalproc:assertedIn": {"@id": instrument_alaska},
        },
    )
    link(mei_chen, charge_ndca_insider, "Charged_With")
    link(ctx["wei_zhang"], charge_ndca_export, "Charged_With")
    link(kyle_marsh, charge_dmass, "Charged_With")
    link(novablade, charge_alaska, "Charged_With")
    track(instrument_ndca_insider, instrument_ndca_export, instrument_dmass, instrument_alaska)

    # ------------------------------------------------------------------
    # ART-004..006, ART-008 (ART-003 and ART-007 are canonical in main builder)
    # ------------------------------------------------------------------
    art_004 = artifact_id("ART-004")
    art_005 = artifact_id("ART-005")
    art_006 = artifact_id("ART-006")
    art_006_image = artifact_id("ART-006-LOGICAL")
    art_008 = artifact_id("ART-008")
    add(
        {
            "@id": art_004,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "ART-004 Discord #vault-leaks export",
            "uco-core:objectMarking": [{"@id": ts_marking}],
            "uco-core:hasFacet": [{
                "@id": uid("art-004-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "discord-vault-leaks-export.json",
                "uco-observable:extension": "json",
            }],
        },
        {
            "@id": art_005,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "ART-005 StreamVault CyberTip bundle",
            "uco-core:objectMarking": [{"@id": cac_marking}],
        },
        {
            "@id": art_006,
            "@type": ["uco-observable:MobileDevice", "uco-core:UcoObject"],
            "uco-core:name": "ART-006 Juvenile J-1 device (source)",
            "uco-core:objectMarking": [{"@id": cac_marking}, {"@id": juvenile_marking}],
        },
        {
            "@id": art_006_image,
            "@type": [
                "solveit-observable:FileSet",
                "uco-observable:ObservableObject",
                "uco-core:UcoObject",
            ],
            "uco-core:name": "ART-006 partial logical extraction (chat-only)",
            "uco-core:objectMarking": [{"@id": cac_marking}, {"@id": juvenile_marking}],
            "uco-core:hasFacet": [{
                "@id": uid("art-006-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "j1-streamvault-logical.zip",
                "uco-observable:extension": "zip",
            }],
        },
        {
            "@id": art_008,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "ART-008 sar_cluster_4412.csv (FinCEN MLAR cluster)",
            "uco-core:objectMarking": [{"@id": fincen_marking}],
            "uco-core:hasFacet": [{
                "@id": uid("art-008-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": "sar_cluster_4412.csv",
                "uco-observable:extension": "csv",
            }],
        },
    )
    link(art_005, cybertip_images, "Related_To")
    link(art_008, mlar_csv, "Related_To")
    link(discord_ndi, art_004, "Contained_Within")
    track(art_004, art_005, art_006, art_006_image, art_008)

    # LOC-005, LOC-006, LOC-008
    loc_005 = uid("loc-005")
    loc_006 = uid("loc-006")
    loc_008 = uid("loc-008")
    add(
        location(loc_005, "LOC-005 Victim-4 residence",
                 "Albuquerque, NM (redacted street) — home invasion attempt.",
                 locality="Albuquerque", region="NM"),
        location(loc_006, "LOC-006 Lam Miami residence",
                 "8841 Biscayne Blvd, Miami, FL — obstruction phone into bay.",
                 street="8841 Biscayne Blvd", locality="Miami", region="FL"),
        location(loc_008, "LOC-008 SCIF-NATGRD-884",
                 "Otis ANGB, MA SCIF — classified removal (synthetic, not public).",
                 locality="Otis ANGB", region="MA"),
    )
    track(loc_005, loc_006, loc_008)

    # EVT-007 SCIF badge swipe
    evt_007 = uid("evt-007")
    add({
        "@id": evt_007,
        "@type": "uco-core:Event",
        "uco-core:name": "EVT-007 SCIF badge swipe (Kyle Marsh)",
        "uco-core:startTime": lit("xsd:dateTime", "2025-01-10T07:42:11-05:00"),
        "uco-core:eventType": ["PhysicalAccess"],
        "uco-core:eventAttribute": [dict_entries("evt-007", {
            "badge_id": "NATGRD-88421",
            "reader": "SCIF-NATGRD-884 main",
            "result": "granted",
        })],
    })
    link(evt_007, kyle_marsh, "Related_To")
    link(evt_007, loc_008, "Occurred_At")
    track(evt_007)

    # ------------------------------------------------------------------
    # MSG-001 thread expansion (4 messages + thread)
    # ------------------------------------------------------------------
    msg_001_thread = artifact_id("MSG-001")
    thread_facet = uid("msg-001-thread-facet")
    msg_001_m1 = uid("msg-001-01")
    msg_001_m2 = uid("msg-001-02")
    msg_001_m4 = uid("msg-001-04")
    add(
        {
            "@id": thread_facet,
            "@type": "uco-observable:MessageThreadFacet",
            "uco-observable:participant": [
                {"@id": king_k_phone},
                {"@id": keel_phone},
            ],
        },
        {
            "@id": msg_001_thread,
            "@type": ["uco-observable:MessageThread", "uco-core:UcoObject"],
            "uco-core:name": "MSG-001 Courier dispatch thread (Keel iPhone iMessage)",
            "uco-core:description": "Thread iMessage;+1-504-555-0177;+1-646-555-0191",
            "uco-core:hasFacet": [{"@id": thread_facet}],
        },
        _message(msg_001_m1, "MSG-001 message 1 — King K dispatch confirm",
                   king_k_phone, keel_phone,
                   "Confirm tomorrow 10am. Victim A Hammond. Cash only. No cards.",
                   "2022-04-03T19:44:02-05:00", uid),
        _message(msg_001_m2, "MSG-001 message 2 — Keel package photo",
                   keel_phone, king_k_phone,
                   "[Attachment: IMG_0042 package confirmation photo — see FS-008]",
                   "2022-04-04T08:12:33-05:00", uid),
        _message(msg_001_m4, "MSG-001 message 4 — Keel in custody",
                   keel_phone, king_k_phone,
                   "Already in custody.",
                   "2022-04-04T10:31:19-05:00", uid),
    )
    # Retype existing abort message as MSG-001 message 3
    for node in g:
        if node.get("@id") == msg_001:
            node["uco-core:name"] = "MSG-001 message 3 — King K ABORT dispatch"
            break
    for mid in (msg_001, msg_001_m1, msg_001_m2, msg_001_m4):
        link(mid, msg_001_thread, "Part_Of")
    link(msg_001_m2, img_0042, "Attachment_Of")
    link(msg_001_thread, art_001_image, "Contained_Within")
    track(msg_001_thread, msg_001_m1, msg_001_m2, msg_001_m4)

    # MSG-002 Telegram pig-butchering
    msg_002 = artifact_id("MSG-002")
    msg_002_m1, msg_002_m2, msg_002_m3 = uid("msg-002-01"), uid("msg-002-02"), uid("msg-002-03")
    add(
        _message(msg_002_m1, "MSG-002 Coach Elena staking pitch",
                   telegram_coach, victim_7_phone,
                   "Your ETH staking pool matured. Reinvest through ApexVault Pro for 12% APY.",
                   "2024-06-12T11:03:00Z", uid),
        _message(msg_002_m2, "MSG-002 Victim-7 transfer confirmation",
                   victim_7_phone, telegram_coach,
                   "Transferred 15 ETH to the wallet you sent.",
                   "2024-07-01T09:17:00Z", uid),
        _message(msg_002_m3, "MSG-002 compliance hold escalation",
                   telegram_coach, victim_7_phone,
                   "Compliance hold — verify identity with exchange security team.",
                   "2024-07-15T14:55:00Z", uid),
        {
            "@id": msg_002,
            "@type": ["uco-observable:MessageThread", "uco-core:UcoObject"],
            "uco-core:name": "MSG-002 Pig-butchering Telegram (Victim-7 ↔ Coach Elena)",
        },
    )
    for mid in (msg_002_m1, msg_002_m2, msg_002_m3):
        link(mid, msg_002, "Part_Of")
    link(msg_002_m3, call_002, "Related_To")
    track(msg_002, msg_002_m1, msg_002_m2, msg_002_m3)

    # MSG-004 additional WeChat messages
    msg_004_m1 = uid("msg-004-01")
    msg_004_m3 = uid("msg-004-03")
    add(
        _message(msg_004_m1, "MSG-004 W.L. recruitment opener",
                   wechat_wl, mei_chen_wechat,
                   "Jade Horizon needs wafer scriber maintenance logs. USB is fine.",
                   "2024-09-03T22:41:00+08:00", uid),
        _message(msg_004_m3, "MSG-004 W.L. AES filing instruction",
                   wechat_wl, mei_chen_wechat,
                   "AES filing shows EAR99. Do not mention Chengdu end user in email.",
                   "2024-09-12T18:03:00+08:00", uid),
    )
    link(msg_004, msg_004_m1, "Part_Of")
    link(msg_004, msg_004_m3, "Part_Of")
    link(msg_004_m1, wl_recruiter, "Sent_By")
    track(msg_004_m1, msg_004_m3)

    # MSG-005 Discord thread
    msg_005 = artifact_id("MSG-005")
    msg_005_m1 = uid("msg-005-01")
    msg_005_m3 = uid("msg-005-03")
    add(
        _message(msg_005_m1, "MSG-005 Kyle Marsh vault drop announcement",
                   discord_marsh, discord_marsh,
                   "Friday drop — Ukraine package, TS//SCI, don't share outside server",
                   "2025-01-14T23:08:00-05:00", uid),
        _message(msg_005_m3, "MSG-005 Kyle Marsh burn notice",
                   discord_marsh, discord_marsh,
                   "Delete everything if anyone asks. Burner only.",
                   "2025-02-02T08:44:00-05:00", uid),
        {
            "@id": msg_005,
            "@type": ["uco-observable:MessageThread", "uco-core:UcoObject"],
            "uco-core:name": "MSG-005 Discord #vault-leaks (Kyle Marsh)",
            "uco-core:objectMarking": [{"@id": ts_marking}],
        },
    )
    link(msg_005_m1, msg_005, "Part_Of")
    link(msg_005_m3, msg_005, "Part_Of")
    link(discord_ndi, msg_005, "Part_Of")
    link(msg_005, art_004, "Contained_Within")
    track(msg_005, msg_005_m1, msg_005_m3)

    # MSG-006 additional sextortion messages + CAC layer-2 interpretation
    msg_006_m2 = uid("msg-006-02")
    msg_006_m3 = uid("msg-006-03")
    j1_streamvault = uid("acc-j1-streamvault")
    add({
        "@id": j1_streamvault,
        "@type": [
            "uco-observable:DigitalAccount",
            "uco-observable:ObservableObject",
            "uco-core:UcoObject",
        ],
        "uco-core:name": "Juvenile J-1 StreamVault account (synthetic handle)",
        "uco-core:description": "ICAC undercover persona messaging account for J-1.",
        "uco-core:hasFacet": [{
            "@id": uid("acc-j1-streamvault-facet"),
            "@type": "uco-observable:AccountFacet",
            "uco-observable:accountIdentifier": "j1_undercover_ak",
        }],
    })
    link(juvenile_j1, j1_streamvault, "Has_Account")
    add(
        _message(msg_006_m2, "MSG-006 J-1 Cash App compliance",
                   j1_streamvault, streamvault_nova,
                   "I opened the Cash App like you said. Account routing 041215663.",
                   "2025-08-20T06:12:00-08:00", uid),
        _message(msg_006_m3, "MSG-006 NovaBlade payment promise",
                   streamvault_nova, j1_streamvault,
                   "Good. You'll receive $500 tonight. Delete our chat.",
                   "2025-08-20T06:14:00-08:00", uid),
    )
    msg_006_thread = artifact_id("MSG-006")
    add({
        "@id": msg_006_thread,
        "@type": ["uco-observable:MessageThread", "uco-core:UcoObject"],
        "uco-core:name": "MSG-006 ICAC grooming / sextortion thread (J-1 ↔ NovaBlade)",
        "uco-core:objectMarking": [{"@id": cac_marking}, {"@id": juvenile_marking}],
    })
    for mid in (msg_006, msg_006_m2, msg_006_m3):
        link(mid, msg_006_thread, "Part_Of")
    financial_sextortion = uid("cac-financial-sextortion-incident")
    threat_disclose = uid("cac-threat-disclose")
    coercion_demand = uid("cac-coercion-demand")
    add(
        {
            "@id": financial_sextortion,
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": "Financial sextortion scheme — Juvenile J-1 (Layer 2 interpretation)",
            "uco-core:description": (
                "CAC Layer-2 interpretation over MSG-006 thread: financial coercion "
                "via StreamVault with Cash App mule routing."
            ),
            "uco-action:performer": {"@id": novablade},
            "uco-action:object": [{"@id": msg_006}, {"@id": msg_006_m2}, {"@id": msg_006_m3}],
        },
        {
            "@id": threat_disclose,
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": "Threat to disclose edited images to school group",
            "uco-action:performer": {"@id": novablade},
            "uco-action:object": [{"@id": msg_006}],
        },
        {
            "@id": coercion_demand,
            "@type": ["uco-action:Action", "uco-core:UcoObject"],
            "uco-core:name": "Coercion demand — additional images or public disclosure",
            "uco-action:performer": {"@id": novablade},
            "uco-action:object": [{"@id": msg_006_m3}],
        },
    )
    link(financial_sextortion, grooming, "Related_To")
    apply_marking(financial_sextortion, cac_marking, juvenile_marking)
    track(j1_streamvault, msg_006_m2, msg_006_m3, msg_006_thread, financial_sextortion, threat_disclose, coercion_demand)

    # EMAIL-003 FinCEN SAR escalation
    email_003 = artifact_id("EMAIL-003")
    email_from_003 = uid("email-003-from")
    email_to_003 = uid("email-003-to")
    add(
        {
            "@id": email_from_003,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "sar-liaison@fincen.gov",
            "uco-core:hasFacet": [{
                "@id": uid("email-003-from-facet"),
                "@type": "uco-observable:EmailAddressFacet",
                "uco-observable:addressValue": "sar-liaison@fincen.gov",
            }],
        },
        {
            "@id": email_to_003,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "pga-taskforce@fbi.gov",
            "uco-core:hasFacet": [{
                "@id": uid("email-003-to-facet"),
                "@type": "uco-observable:EmailAddressFacet",
                "uco-observable:addressValue": "pga-taskforce@fbi.gov",
            }],
        },
        {
            "@id": email_003,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "EMAIL-003 FinCEN SAR escalation (internal FBI)",
            "uco-core:objectMarking": [{"@id": fincen_marking}],
            "uco-core:hasFacet": [{
                "@id": uid("email-003-facet"),
                "@type": "uco-observable:EmailMessageFacet",
                "uco-observable:from": {"@id": email_from_003},
                "uco-observable:to": [{"@id": email_to_003}],
                "uco-observable:subject": "SAR cluster reference FIN-2022-PGA-4412",
                "uco-observable:sentTime": lit("xsd:dateTime", "2022-11-03T09:00:00-05:00"),
            }],
        },
    )
    link(email_003, art_008, "Related_To")
    track(email_003)

    # ------------------------------------------------------------------
    # Filesystem artifacts FS-002..FS-007 (FS-001 and FS-004/FS-008 canonical in main builder)
    # ------------------------------------------------------------------
    fs_002 = artifact_id("FS-002")
    fs_003 = artifact_id("FS-003")
    fs_005 = artifact_id("FS-005")
    fs_006 = artifact_id("FS-006")
    fs_007 = artifact_id("FS-007")
    fs_004 = reg_key
    fs_008 = img_0042
    add(
        _file_obs(fs_002, "FS-002 Keel iPhone logical extraction tree",
                  "keel-iphone-UFED.zip tree root", uid),
        _file_obs(fs_003, "FS-003 Carved seed-backup.txt (Victim-7)",
                  "/Users/victim7/Documents/Crypto/seed-backup.txt (carved)", uid, deleted=True),
        _file_obs(fs_005, "FS-005 SQLite WhatsApp contact query (Keel)",
                  "sms.db ZTEXT Hammond query — 3 rows", uid),
        _file_obs(fs_006, "FS-006 APFS filesystem events (Victim-7 MacBook)",
                  "fseventsd log — AnyDesk install/delete timeline (APFS equivalent)", uid),
        _file_obs(fs_007, "FS-007 bulk_extractor nested path",
                  "bulk_extractor/zip/carved/seed-backup.txt", uid),
    )
    link(fs_001, fs_002, "Related_To")
    link(fs_002, art_001_image, "Contained_Within")
    link(fs_003, art_002, "Derived_From")
    link(fs_005, art_001_image, "Contained_Within")
    link(fs_006, art_002, "Contained_Within")
    link(fs_007, fs_003, "Derived_From")
    link(fs_003, evt_003, "Related_To")
    track(fs_002, fs_003, fs_004, fs_005, fs_006, fs_007, fs_008)

    # ------------------------------------------------------------------
    # NET-001 flow summary + NET-002 AnyDesk session
    # ------------------------------------------------------------------
    net_001 = artifact_id("NET-001")
    net_002 = artifact_id("NET-002")
    src_ip_c2 = uid("net-src-ip-c2")
    dst_ip_c2 = uid("net-dst-ip-c2")
    conn_c2 = uid("net-conn-c2")
    dns_gate_c2 = uid("net-dns-gate-c2")
    pcap_analysis = uid("ia-net-001-pcap-analysis")
    add(
        {
            "@id": src_ip_c2,
            "@type": ["uco-observable:IPAddress", "uco-core:UcoObject"],
            "uco-core:name": "10.44.12.88 (Apex Semi internal)",
            "uco-core:hasFacet": [{
                "@id": uid("net-src-c2-facet"),
                "@type": "uco-observable:IPAddressFacet",
                "uco-observable:addressValue": "10.44.12.88",
            }],
        },
        {
            "@id": dst_ip_c2,
            "@type": ["uco-observable:IPAddress", "uco-core:UcoObject"],
            "uco-core:name": "198.51.100.44 (gate-c2.darknet.invalid resolved)",
            "uco-core:hasFacet": [{
                "@id": uid("net-dst-c2-facet"),
                "@type": "uco-observable:IPAddressFacet",
                "uco-observable:addressValue": "198.51.100.44",
            }],
        },
        {
            "@id": conn_c2,
            "@type": ["uco-observable:NetworkConnection", "uco-core:UcoObject"],
            "uco-core:name": "NET-001 TLS flow to gate-c2.darknet.invalid",
            "uco-core:hasFacet": [{
                "@id": uid("net-conn-c2-facet"),
                "@type": "uco-observable:NetworkConnectionFacet",
                "uco-observable:sourcePort": lit("xsd:integer", 52444),
                "uco-observable:destinationPort": lit("xsd:integer", 443),
            }],
        },
        {
            "@id": dns_gate_c2,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "DNS query gate-c2.darknet.invalid → 198.51.100.44",
        },
        {
            "@id": net_001,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "NET-001 PCAP flow summary (TLS C2 + DNS + S3 exfil)",
            "uco-core:description": "Derived flow summary from ART-003 apex-semi-20241103.pcap.",
        },
        {
            "@id": net_002,
            "@type": ["uco-observable:NetworkConnection", "uco-core:UcoObject"],
            "uco-core:name": "NET-002 AnyDesk TCP/6568 session (Victim-7)",
            "uco-core:description": "Client 198.51.100.44:44102 → 192.168.1.44:6568; linked EVT-003.",
            "uco-core:hasFacet": [{
                "@id": uid("net-002-facet"),
                "@type": "uco-observable:NetworkConnectionFacet",
                "uco-observable:destinationPort": lit("xsd:integer", 6568),
            }],
        },
        {
            "@id": pcap_analysis,
            "@type": "case-investigation:InvestigativeAction",
            "uco-core:name": "Wireshark examination of ART-003 PCAP (NET-001 summary)",
            "uco-action:object": [{"@id": art_003}],
            "uco-action:result": [{"@id": conn_c2}, {"@id": dns_gate_c2}],
            "uco-action:startTime": lit("xsd:dateTime", "2024-11-09T09:00:00-05:00"),
        },
    )
    link(conn_c2, src_ip_c2, "Related_To")
    link(conn_c2, dst_ip_c2, "Related_To")
    link(conn_c2, net_001, "Part_Of")
    link(dns_gate_c2, net_001, "Part_Of")
    g.append(rel(net_001, art_003, "Derived_From",
                 description="Flow summary derived from ART-003 PCAP capture"))
    link(net_002, evt_003, "Related_To")
    track(net_001, net_002, conn_c2, dns_gate_c2, pcap_analysis)

    # ------------------------------------------------------------------
    # PROC-001 .. PROC-010
    # ------------------------------------------------------------------
    cti_ioc_report = uid("cti-ioc-report")
    proc_009_action = uid("proc-009-acquisition")
    add({
        "@id": cti_ioc_report,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "GateRunner CTI IOC report (PROC-008 output)",
        "uco-core:objectMarking": [{"@id": malware_marking}],
    })
    add({
        "@id": proc_009_action,
        "@type": [
            "solveit-core:SolveitInvestigativeAction",
            "case-investigation:InvestigativeAction",
            "uco-core:UcoObject",
        ],
        "uco-core:name": "PROC-009 — Juvenile J-1 partial logical acquisition",
        "uco-core:description": "DFT-1048 chat-only scope; partial iOS gap documented.",
        "uco-action:object": [{"@id": art_006}],
        "uco-action:result": [{"@id": art_006_image}],
        "solveit-core:usedTechnique": [{"@id": SOLVEIT_DATA + "techniqueDFT-1019"}],
    })
    authorize_action(
        proc_009_action,
        juvenile_ce_auth,
        note="ICAC CE warrant — chat-only partial logical acquisition (DFT-1048)",
    )
    track(cti_ioc_report, proc_009_action)

    inline_tools: dict[str, str] = {
        uid("tool-cpa-769"): "Cellebrite Physical Analyzer 7.69",
        uid("tool-autopsy-421"): "Autopsy 4.21.0",
        uid("tool-xways-21"): "X-Ways Forensics 21.0",
        uid("tool-axiom-74"): "Magnet AXIOM 7.4",
        uid("tool-wireshark-42"): "Wireshark 4.2",
        uid("tool-ghidra-11"): "Ghidra 11 (REMnux 2024 air-gap)",
        uid("tool-ufed-782"): "Cellebrite UFED 7.82",
    }
    for tool_id, tool_name in inline_tools.items():
        add({
            "@id": tool_id,
            "@type": ["uco-tool:ConfiguredTool", "uco-core:UcoObject"],
            "uco-core:name": tool_name,
        })

    proc_specs = [
        ("PROC-001", "2022-04-05", "Cellebrite UFED 7.69 examination", ufed_tool,
         [art_001], [art_001_image], ["DFT-1019", "DFT-1042"], solveit_keel),
        ("PROC-002", "2022-04-06", "Cellebrite Physical Analyzer analysis", uid("tool-cpa-769"),
         [art_001_image], [msg_001_thread, fs_008], ["DFT-1052", "DFT-1054"], None),
        ("PROC-003", "2024-08-20", "FTK Imager + Tableau acquisition", ctx["ftk_imager"],
         [ctx["art_002_source_ssd"]], [art_002], ["DFT-1002", "DFT-1012", "DFT-1025"], coc_002_imaging),
        ("PROC-004", "2024-08-21", "Autopsy filesystem + carve examination", uid("tool-autopsy-421"),
         [art_002], [fs_001, fs_003], ["DFT-1061", "DFT-1064", "DFT-1052"], None),
        ("PROC-005", "2024-08-21", "X-Ways dual-tool hash verification", uid("tool-xways-21"),
         [art_002], [ctx["hash_verify_result"]], ["DFT-1042"], ctx["solveit_v7_verify"]),
        ("PROC-006", "2024-08-22", "Magnet AXIOM AnyDesk timeline", uid("tool-axiom-74"),
         [art_002], [evt_003, net_002], ["DFT-1069", "DFT-1056"], None),
        ("PROC-007", "2024-11-09", "Wireshark PCAP examination", uid("tool-wireshark-42"),
         [art_003], [conn_c2], ["DFT-1017"], pcap_analysis),
        ("PROC-008", "2025-03-14", "REMnux + Ghidra malware RE", uid("tool-ghidra-11"),
         [gatehelper], [cti_ioc_report], ["DFT-1054", "DFT-1057"], None),
        ("PROC-009", "2025-08-22", "Cellebrite UFED partial J-1 acquisition", uid("tool-ufed-782"),
         [art_006], [art_006_image], ["DFT-1019"], proc_009_action),
        ("PROC-010", "2025-09-01", "Chainalysis crypto trace", ctx["chainalysis_tool"],
         [mlar_csv], [ctx["crypto_trace_report"]], [], crypto_trace_action),
    ]
    for spec in proc_specs:
        pid, date, name, tool, objects, results, dfts, existing = spec
        proc_id = artifact_id(pid)
        if existing:
            for node in g:
                if node.get("@id") == existing:
                    node["uco-core:name"] = f"{pid} — {node.get('uco-core:name', name)}"
                    track(existing)
                    break
            continue
        action_types = ["case-investigation:InvestigativeAction", "uco-core:UcoObject"]
        if dfts:
            action_types = [
                "solveit-core:SolveitInvestigativeAction",
                "case-investigation:InvestigativeAction",
                "uco-core:UcoObject",
            ]
        action = {
            "@id": proc_id,
            "@type": action_types,
            "uco-core:name": f"{pid} — {name}",
            "uco-action:startTime": lit("xsd:dateTime", f"{date}T09:00:00-05:00"),
            "uco-action:instrument": {"@id": tool} if isinstance(tool, str) else tool,
            "uco-action:object": [{"@id": o} for o in objects],
            "uco-action:result": [{"@id": r} for r in results],
        }
        if dfts:
            action["solveit-core:usedTechnique"] = [
                {"@id": SOLVEIT_DATA + f"technique{d}"} for d in dfts
            ]
        add(action)
        track(proc_id)

    # ------------------------------------------------------------------
    # COC-003, COC-004, expanded COC-005
    # ------------------------------------------------------------------
    rule41_apex = uid("auth-rule41-apex-pcap")
    add({
        "@id": rule41_apex,
        "@type": "case-investigation:Authorization",
        "uco-core:name": "Rule 41 search warrant — Apex Semi PCAP (ART-003)",
        "uco-core:description": "Warrant paragraph 14 PCAP mirror and FBI copy receipt scope.",
    })
    register_auth(apex_consent)
    register_auth(rule41_apex)
    register_auth(discord_lp)

    hash_tool = uid("tool-sha256-art-003")
    art_003_hash_result = uid("art-003-hash-verify-result")
    wireshark_tool = uid("tool-wireshark-coc-003")
    apex_soc = uid("person-apex-soc-analyst")
    fbi_pcap_custodian = uid("person-fbi-pcap-custodian")
    add(
        {
            "@id": hash_tool,
            "@type": ["uco-tool:ConfiguredTool", "uco-core:UcoObject"],
            "uco-core:name": "SHA-256 integrity verifier (ART-003)",
        },
        {
            "@id": wireshark_tool,
            "@type": ["uco-tool:ConfiguredTool", "uco-core:UcoObject"],
            "uco-core:name": "Wireshark 4.2",
        },
        {
            "@id": apex_soc,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "Apex Semi SOC analyst (corporate preservation)",
        },
        {
            "@id": fbi_pcap_custodian,
            "@type": ["uco-identity:Person", "uco-core:UcoObject"],
            "uco-core:name": "FBI cyber liaison (ART-003 receipt)",
        },
        {
            "@id": art_003_hash_result,
            "@type": ["solveit-observable:HashVerificationResult", "uco-core:UcoObject"],
            "uco-core:name": "ART-003 PCAP SHA-256 verification result",
        },
    )
    coc_003_specs = [
        ("coc-003-preservation", "Corporate preservation Apex PCAP", "2024-11-06T06:00:00-05:00",
         apex_soc, apex_consent, [], []),
        ("coc-003-receipt", "FBI copy receipt ART-003", "2024-11-08T10:00:00-05:00",
         fbi_pcap_custodian, rule41_apex, [], []),
        ("coc-003-hash", "Integrity hash ART-003 PCAP", "2024-11-08T11:30:00-05:00",
         examiner_v7, apex_consent, [hash_tool], [art_003_hash_result]),
        ("coc-003-exam", "Wireshark examination NET-001", "2024-11-09T09:00:00-05:00",
         examiner_v7, apex_consent, [wireshark_tool], [pcap_analysis]),
    ]
    coc_003_ids: list[str] = []
    for label, name, start, performer, auth, tools, results in coc_003_specs:
        aid = uid(label)
        coc_003_ids.append(aid)
        action = {
            "@id": aid,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": f"COC-003 — {name}",
            "uco-action:startTime": lit("xsd:dateTime", start),
            "uco-action:performer": {"@id": performer},
            "uco-action:object": [{"@id": art_003}],
        }
        if tools:
            action["uco-action:instrument"] = [{"@id": t} for t in tools]
        if results:
            action["uco-action:result"] = [{"@id": r} for r in results]
        add(action)
        authorize_action(aid, auth)
        track(aid)

    prov_coc_003 = uid("prov-coc-003-pcap")
    add({
        "@id": prov_coc_003,
        "@type": "case-investigation:ProvenanceRecord",
        "uco-core:name": "COC-003 — ART-003 PCAP provenance",
        "uco-core:object": [{"@id": art_003}] + [{"@id": i} for i in coc_003_ids],
    })
    track(prov_coc_003)

    coc_004_physical = uid("coc-004-physical-scif")
    coc_004_digital = uid("coc-004-digital-export")
    prov_coc_004_phys = uid("prov-coc-004-physical")
    prov_coc_004_dig = uid("prov-coc-004-digital")
    add(
        {
            "@id": coc_004_physical,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "COC-004 — SCIF physical printout custody (ART-004)",
            "uco-action:performer": {"@id": kyle_marsh},
            "uco-action:object": [{"@id": discord_ndi}],
            "uco-action:startTime": lit("xsd:dateTime", "2025-01-15T08:00:00-05:00"),
        },
        {
            "@id": coc_004_digital,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "COC-004 — Discord logical export custody (ART-004)",
            "uco-action:performer": {"@id": kyle_marsh},
            "uco-action:object": [{"@id": art_004}],
            "uco-action:startTime": lit("xsd:dateTime", "2025-01-15T09:30:00-05:00"),
        },
        {
            "@id": prov_coc_004_phys,
            "@type": "case-investigation:ProvenanceRecord",
            "uco-core:name": "prov-coc-004-physical (SCIF printouts)",
            "uco-core:object": [{"@id": discord_ndi}, {"@id": coc_004_physical}],
        },
        {
            "@id": prov_coc_004_dig,
            "@type": "case-investigation:ProvenanceRecord",
            "uco-core:name": "prov-coc-004-digital (Discord export)",
            "uco-core:object": [{"@id": art_004}, {"@id": coc_004_digital}],
        },
    )
    authorize_action(coc_004_physical, discord_lp)
    authorize_action(coc_004_digital, discord_lp)
    track(coc_004_physical, coc_004_digital, prov_coc_004_phys, prov_coc_004_dig)

    # Expand COC-005 with device + acquisition
    for node in g:
        if node.get("@id") == prov_coc_005:
            node["uco-core:object"] = [
                {"@id": art_006},
                {"@id": art_006_image},
                {"@id": proc_009_action},
                {"@id": grooming},
            ]
            break

    # ------------------------------------------------------------------
    # AI-003 GateRunner classification + AI-004 voice analytics
    # ------------------------------------------------------------------
    ai_003 = artifact_id("AI-003")
    ai_004 = artifact_id("AI-004")
    elastic_ml = uid("tool-elastic-gaterunner-v3")
    yara_tool = uid("tool-yara-sagerunex")
    yara_result = uid("yara-gatehelper-match")
    malware_class_facet = uid("ai-003-classification-facet")
    malware_class_result = uid("ai-003-classification-result")
    voice_result = uid("ai-004-speaker-diarization")
    voice_tool = uid("tool-nuance-forensics-voice")
    add(
        {
            "@id": elastic_ml,
            "@type": "uco-tool:ConfiguredTool",
            "uco-core:name": "Elastic ML gate-runner-v3",
        },
        {
            "@id": yara_tool,
            "@type": "uco-tool:ConfiguredTool",
            "uco-core:name": "YARA Sagerunex_ruleset_2025",
        },
        {
            "@id": malware_class_facet,
            "@type": ["uco-analysis:ArtifactClassificationResultFacet", "uco-core:Facet"],
            "uco-analysis:classification": [{
                "@id": uid("ai-003-malware-class-entry"),
                "@type": "uco-analysis:ArtifactClassification",
                "uco-analysis:class": ["Malware.Family.GateRunner"],
            }],
        },
        {
            "@id": malware_class_result,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "GateRunner family classification result (0.94)",
            "uco-core:hasFacet": [{"@id": malware_class_facet}],
        },
        {
            "@id": yara_result,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "YARA 47/47 rule match on gatehelper.dll",
        },
        {
            "@id": ai_003,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "AI-003 GateRunner malware classification",
            "uco-action:instrument": [{"@id": elastic_ml}, {"@id": yara_tool}],
            "uco-action:object": [{"@id": gatehelper}],
            "uco-action:result": [{"@id": malware_class_result}, {"@id": yara_result}],
        },
        {
            "@id": voice_result,
            "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
            "uco-core:name": "CALL-003 speaker diarization labels (King K vs Keel)",
            "uco-core:description": "Synthetic speaker match score 0.82.",
        },
        {
            "@id": voice_tool,
            "@type": "uco-tool:ConfiguredTool",
            "uco-core:name": "Nuance Forensics Voice Analyst 2.1",
        },
        {
            "@id": ai_004,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "AI-004 Title III voice analytics (CALL-003)",
            "uco-action:performer": {"@id": ctx["examiner_keel"]},
            "uco-action:instrument": [{"@id": voice_tool}],
            "uco-action:object": [{"@id": call_003}],
            "uco-action:result": [{"@id": voice_result}],
            "uco-action:actionStatus": "Success",
            "uco-action:startTime": lit("xsd:dateTime", "2022-04-05T14:30:00-05:00"),
            "uco-action:endTime": lit("xsd:dateTime", "2022-04-05T15:10:00-05:00"),
        },
    )
    g.append(rel(malware_class_result, gatehelper, "Derived_From"))
    g.append(rel(yara_result, gatehelper, "Derived_From"))
    g.append(rel(voice_result, call_003, "Derived_From"))
    track(ai_003, ai_004, malware_class_result, yara_result, voice_result)

    ai_001_confirm = uid("ia-ai-001-human-confirm")
    ai_001_confirm_result = uid("ai-001-human-confirm-result")
    add(
        {
            "@id": ai_001_confirm_result,
            "@type": ["uco-core:UcoObject", "cacontology-detection:DetectionResult"],
            "uco-core:name": "ICAC analyst confirmation — PhotoDNA cluster confirmed",
            "uco-core:description": "Analyst certainty: high — confirmed CSAM-adjacent grooming set.",
        },
        {
            "@id": ai_001_confirm,
            "@type": ["case-investigation:InvestigativeAction", "uco-core:UcoObject"],
            "uco-core:name": "ICAC human confirmation — PhotoDNA hits (AI-001 step 2)",
            "uco-action:object": [{"@id": photodna_detection}],
            "uco-action:result": [{"@id": ai_001_confirm_result}],
        },
    )
    track(ai_001_confirm, ai_001_confirm_result)

    img_0038 = uid("img-0038-clip-rank2")
    img_0011 = uid("img-0011-clip-rank3")
    g.append(rel(img_0038, art_001_image, "Selected_From",
                 description="CLIP rank-2 from Keel DCIM folder"))
    g.append(rel(img_0011, art_001_image, "Selected_From",
                 description="CLIP rank-3 from Keel DCIM folder"))

    # CRYPTO-002 label for extended peel chain export
    crypto_002_export = artifact_id("CRYPTO-002")
    add({
        "@id": crypto_002_export,
        "@type": ["uco-observable:ObservableObject", "uco-core:UcoObject"],
        "uco-core:name": "CRYPTO-002 extended peel-chain export (chain-88421.csv)",
        "uco-core:objectMarking": [{"@id": fincen_marking}],
        "uco-core:hasFacet": [{
            "@id": uid("crypto-002-file-facet"),
            "@type": "uco-observable:FileFacet",
            "uco-observable:fileName": "chain-88421.csv",
            "uco-observable:extension": "csv",
        }],
    })
    link(crypto_002_export, ctx["crypto_trace_report"], "Related_To")
    track(crypto_002_export)

    for node in g:
        if node.get("@id") == grouping:
            node["uco-core:object"] = [{"@id": i} for i in sub_inv_ids]
            break

    sub_inv_object_map: dict[str, list[str]] = {
        inv_elder: [art_001, art_001_image, loc_003, instrument_edla, charge_edla, artifact_id("MSG-001")],
        inv_rico: [
            art_002, mlar_csv, crypto_victim_wallet, instrument_ddc, charge_rico,
            enterprise, artifact_id("MSG-002"),
        ],
        inv_insider: [
            email_001, msg_004, mei_chen, instrument_ndca_insider, charge_ndca_insider, loc_007,
        ],
        inv_export: [email_002, ctx["wei_zhang"], instrument_ndca_export, charge_ndca_export],
        inv_classified: [
            art_004, discord_ndi, kyle_marsh, artifact_id("MSG-005"),
            evt_007, loc_008, instrument_dmass, charge_dmass,
        ],
        inv_cac: [
            art_005, art_006, art_006_image, artifact_id("MSG-006"), grooming,
            evt_008, loc_010, instrument_alaska, charge_alaska,
        ],
        inv_cti: [art_003, artifact_id("NET-001"), gatehelper, evt_005, artifact_id("AI-003")],
    }
    for iid, oids in sub_inv_object_map.items():
        for node in g:
            if node.get("@id") == iid:
                node["uco-core:object"] = [{"@id": o} for o in oids]
                break

    return added


def _message(
    mid: str,
    name: str,
    from_id: str,
    to_id: str,
    text: str,
    sent: str,
    uid_fn: Callable[[str], str],
) -> dict:
    facet_id = uid_fn(f"{mid}-facet")
    return {
        "@id": mid,
        "@type": "uco-observable:Message",
        "uco-core:name": name,
        "uco-core:hasFacet": [{
            "@id": facet_id,
            "@type": "uco-observable:MessageFacet",
            "uco-observable:from": {"@id": from_id},
            "uco-observable:to": {"@id": to_id},
            "uco-observable:messageText": text,
            "uco-observable:sentTime": {"@type": "xsd:dateTime", "@value": sent},
        }],
    }


def _file_obs(fid: str, name: str, path: str, uid_fn: Callable[[str], str], *, deleted: bool = False) -> dict:
    desc = f"Path: {path}"
    if deleted:
        desc += " [DELETED — carved]"
    return {
        "@id": fid,
        "@type": ["uco-observable:File", "uco-core:UcoObject"],
        "uco-core:name": name,
        "uco-core:description": desc,
        "uco-core:hasFacet": [{
            "@id": uid_fn(f"{fid}-file-facet"),
            "@type": "uco-observable:FileFacet",
            "uco-observable:filePath": path,
        }],
    }
