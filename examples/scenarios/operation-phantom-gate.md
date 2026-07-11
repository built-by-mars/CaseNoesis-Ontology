# Operation PHANTOM GATE — Composite Cyber Investigation Scenario

**Tier:** T0 (synthetic)  
**Investigation ID:** `INV-2026-PGA-001`  
**Purpose:** Exercise the CASE/UCO MCP server across core UCO, extension ontologies, SOLVE-IT method modeling, chain of custody, data-handling requirements, AI/ML pipelines, and the full recipe catalog.

Grounded in validated exemplars under `examples/pacer/`, `examples/cti/lotus_blossom_2025/`, and `examples/solveit/`. All person names, phone numbers, wallet addresses, and serial numbers below are **fabricated** for testing.

---

## Table of contents

1. [Executive summary](#executive-summary)
2. [Phase timeline](#phase-timeline)
3. [Organizations and roles](#organizations-and-roles)
4. [Data handling requirements](#data-handling-requirements)
5. [Cyber artifact catalog](#cyber-artifact-catalog)
6. [Chain of custody](#chain-of-custody)
7. [Digital forensics processing log](#digital-forensics-processing-log)
8. [AI/ML analysis pipeline results](#aiml-analysis-pipeline-results)
9. [Events and authentication logs](#events-and-authentication-logs)
10. [Locations](#locations)
11. [SOLVE-IT examination plan](#solve-it-examination-plan)
12. [Legal process](#legal-process)
13. [Extension bundles and MCP exercise matrix](#extension-bundles-and-mcp-exercise-matrix)
14. [Grounding in processed exemplars](#grounding-in-processed-exemplars)

---

## Executive summary

From **April 2022 through March 2026**, FBI Cyber Division, USSS, HSI, SEC, ICAC Task Forces, and Europol investigate the **Phantom Gate Alliance (PGA)** — an association-in-fact criminal enterprise that:

- Operated Treasury/IRS impersonation elder-fraud call centers with U.S. couriers
- Evolved into cryptocurrency social engineering, remote-access theft, and home invasions for hardware wallets
- Laundered proceeds via peel chains, no-KYC exchanges, and Monero chain-hopping
- Recruited insiders at U.S. technology and defense firms for trade-secret theft and export-control evasion
- Deployed APT-style malware (GateRunner, a Sagerunex-variant) against victim enterprises
- Recruited juvenile money mules via sextortion
- Used physical enforcement (weapons, controlled substances) at safehouses

**Lead cases:** `1:26-cr-00417-CKK` (D.D.C., RICO), `2:26-cr-00115-ILRL` (E.D. La., couriers), `3:26-cr-00141-VC` (N.D. Cal., insider), `3:26-cr-00446-WHA` (N.D. Cal., export), `1:26-cr-10159-IT` (D. Mass., classified leaks), `3:26-cr-00029-SLG` (D. Alaska, CAC).

---

## Phase timeline

| Phase | Period | Trigger | Recipes / extensions |
|-------|--------|---------|----------------------|
| 0 — Intelligence fusion | 2022-Q4 | FinCEN SAR cluster + NCMEC CyberTip | CTI, `cybertip-ncmec-workflow`, `accounts` |
| 1 — Elder fraud sting | 2023-Q1–Q2 | Controlled delivery, Louisiana | `elder-fraud-impersonation`, `call-log`, `cell-site`, `legalproc` |
| 2 — Crypto escalation | 2023-Q3–2024-Q2 | $47M theft + NM home invasion | `spear-phishing`, `network-investigation`, `fraud-crypto-laundering`, `rico`, `cryptoinv` |
| 3 — Enterprise mapping | 2024-Q3 | Second superseding indictment | `racketeering-enterprise`, `legal-process-modeling` |
| 4 — Insider / export | 2024-Q4–2025-Q2 | Corporate tip + border arrest | `insider-threat-trade-secrets`, `export-control-sanctions` |
| 5 — APT / CTI | 2025-Q1–Q3 | EDR alert + Talos-style report | `cyber-threat-intelligence`, `attack-technique` |
| 6 — CAC sextortion | 2025-Q2–2026-Q1 | ICAC undercover + CyberTip | CAC recipe set, `cac:full` |
| 7 — Takedown / sentencing | 2026-Q1–Q2 | Coordinated arrests | `solve-it`, `chain-of-custody`, `weapons-drug-evidence`, sentencing |

---

## Organizations and roles

### Criminal enterprise

**Phantom Gate Alliance (PGA)** — `rico:RacketeeringEnterprise`, `enterpriseType: association-in-fact`.

| Role (`rico:EnterpriseRole`) | Key persons (synthetic) |
|------------------------------|-------------------------|
| Call-center operator | Raj "King K" Mehta (unindicted, India) |
| Target identifier | COCONSPIRATOR T.I. |
| Voice social engineer | Victor Lam |
| Database hacker | COCONSPIRATOR M.F. |
| Residential burglar | Desmond R. |
| Money launderer | Ferro, Tangeman |
| Insider recruiter | COCONSPIRATOR W.L. |
| APT operator | COCONSPIRATOR A.P. |
| Juvenile recruiter | alias "NovaBlade" |

### Law enforcement

FBI Cyber (lead), USSS San Francisco FO, HSI New Orleans, ICAC multi-state, SEC, Europol EC3, NCMEC, corporate SOC (Apex Semi).

---

## Data handling requirements

Model these as `InvestigativeAction` constraints, `ProvenanceRecord` notes, `uco-marking:MarkingDefinition` / `objectMarking`, and `legalproc:Authorization` scope fields. Every derived artifact inherits handling from its source.

### Global investigation policy

| Requirement ID | Category | Rule | CASE/UCO modeling |
|----------------|----------|------|-------------------|
| DH-PGA-001 | CJIS | All criminal justice information at rest in FBI CJIS-compliant enclave; no cloud sync outside FedRAMP High boundary | `Authorization` description; lab `Location` |
| DH-PGA-002 | Need-to-know | Cross-district sharing only via MLAT or joint-task-force MOU with named recipients | `Relationship` custodian transfers; MLAT `InvestigativeAction` |
| DH-PGA-003 | Minimization | Third-party victim PII redacted in discovery exports; full content retained in prosecutor vault | SOLVE-IT DFT-1046 redaction action |
| DH-PGA-004 | Retention | Master forensic images retained 7 years post-final appeal or case closure | `ProvenanceRecord` + storage action |
| DH-PGA-005 | Derivative integrity | Every derived artifact (timeline, AI hit, wallet cluster) must `Derived_From` source with hash | `Relationship` kind `Derived_From` |
| DH-PGA-006 | Dual custody | Classified-adjacent NDI printouts: physical + digital custody chains separated | Two `ProvenanceRecord` nodes per `chain-of-custody.md` |
| DH-PGA-008 | FINCEN SAR | Bank Secrecy Act SAR/MLAR cluster data; no public filing attachment without FinCEN authorization | `FINCEN-SAR-PROTECTED` marking on MLAR source files |

### Per-artifact handling matrix

| Artifact ID | Sensitivity | Marking | Storage | Access | Special handling |
|-------------|-------------|---------|---------|--------|------------------|
| ART-001 Keel iPhone extraction | CJIS / LE sensitive | `LEO-SENSITIVE` (StatementMarking) | FBI NOLA evidence locker L-14 | ICAC + HSI only | Faraday at seizure; airplane mode before transport |
| ART-002 Victim-7 E01 image | CJIS + victim PII | `LEO-SENSITIVE` | DCFO digital vault DV-2024-881 | Named examiners only | FileVault key from victim interview — document provenance |
| ART-003 Apex Semi PCAP | Corporate confidential + CJIS | `COMPANY-CONFIDENTIAL` + `LEO-SENSITIVE` | Apex consent hold + FBI copy | Apex SOC + FBI | 72-hour capture window per warrant paragraph 14 |
| ART-004 Marsh Discord export | USG NDI | `TOP SECRET//SCI` on charged items | SCIF-adjacent secure room SR-3 | NS Division + FBI WFO | No internet-connected examination workstation |
| ART-005 StreamVault CyberTip bundle | CAC / CSAM-adjacent | `CAC-RESTRICTED` | NCMEC secure pipeline + ICAC | ICAC task force | PhotoDNA hits — no local thumbnail cache on analyst laptops |
| ART-006 Juvenile J-1 device image | CAC + juvenile privacy | `CAC-RESTRICTED` + `JUVENILE-PRIVACY` | ICAC isolated lab | Named UC + prosecutor | DFT-1048 partial processing — chat only, no unrelated media carve |
| ART-007 GateRunner malware sample | Malware — live | `MALWARE-LIVE` | Air-gapped VM host AG-07 | Malware RE team | No outbound network; hash-only sharing to CTI partners |
| ART-008 Blockchain MLAR CSV | Financial intelligence | `FINCEN-SAR-PROTECTED` | USSS crypto lab | USSS + AUSA | Exchange return — no public filing attachment |

### Marking definitions (sample)

```json
{
  "@id": "kb:marking-leo-sensitive",
  "@type": ["marking:MarkingDefinition", "uco-core:UcoObject"],
  "uco-core:name": "Law enforcement sensitive — PGA task force",
  "marking:definitionType": "statement",
  "marking:definition": [{"@id": "kb:marking-leo-sensitive-stmt"}]
}
{
  "@id": "kb:marking-leo-sensitive-stmt",
  "@type": "marking:StatementMarking",
  "marking:statement": "LAW ENFORCEMENT SENSITIVE — PGA JTF. Unauthorized disclosure subject to 5 U.S.C. § 552(b)(7)."
}
```

Apply via `uco-core:objectMarking` on observables, images, and exports — not only in free-text descriptions.

ProvenanceRecord and Investigation groupings use `uco-core:object` (from `ContextualCompilation`), not a case-investigation-specific object property.

---

## Cyber artifact catalog

Each entry includes an **artifact ID**, modeling hints, and **source-fidelity snippets** suitable for MCP ingestion (`process_document_file` text blocks, `route_investigation_content`, or direct graph construction).

### Phone calls

#### CALL-001 — Spoofed Treasury call to Victim A (elder fraud)

| Field | Value |
|-------|-------|
| Artifact ID | CALL-001 |
| Exhibit | GX-14 (E.D. La.) |
| Modeling | `ObservableObject` + `CallFacet`; `PhoneAccount` for endpoints |
| Recipe | `elder-fraud-impersonation`, `call-log` |

```
Direction:     incoming
To:            +1-985-555-0142 (Victim A mobile, Hammond LA)
From (CID):    +1-202-555-0199 (spoofed; displays "US Treasury")
Start:         2022-04-04T09:17:23-05:00
Duration:      00:47:12
Recording:     None (victim handset; detective observed live)
Transcript excerpt (Victim A statement, Det. D'Amato present):
  CALLER: "This is Special Agent Morrison, United States Treasury. Your
           name appeared in a narcotics forfeiture case in Miami."
  VICTIM A: "I don't know anything about Miami."
  CALLER: "We need to secure your funds. Purchase Green Dot cards today..."
```

#### CALL-002 — Lam cold-call to Victim-7 (crypto social engineering)

| Field | Value |
|-------|-------|
| Artifact ID | CALL-002 |
| Date | 2024-08-18T14:22:00-04:00 |
| Modeling | `CallFacet` + linked `Person` (Lam) + `Account` (VoIP burner) |

```
From account:  voip:+1-786-555-0133 (TextNow, alias "CoinShield Security")
To:            +1-202-555-0881 (Victim-7)
Duration:      00:31:44
Summary:       Caller claimed unauthorized login from Singapore; instructed
               Victim-7 to install AnyDesk and "verify wallet ownership."
Linked SMS:    MSG-003 (follow-up AnyDesk link)
```

#### CALL-003 — Title III intercept (King K → Keel dispatch)

| Field | Value |
|-------|-------|
| Artifact ID | CALL-003 |
| Authorization | Title III order 2:22-mj-00062-DM, ¶¶ 8–12 |
| Modeling | `CallFacet` + `Authorization` + `InvestigativeAction` (intercept) |

```
Date:          2022-03-29T16:05:11-05:00
From:          +91-98-5555-0144 (India; King K alias line)
To:            +1-504-555-0177 (Keel courier phone)
Transcript:
  KING K: "Package ready Hammond. Victim A confirmed ten thousand cash.
           Blue Camry, lot behind Shell on Highway 190."
  KEEL: "Copy. En route."
Cell-site:     TOWER-004 (Keel phone at handoff — see LOC-003)
```

---

### Text / messaging chains

#### MSG-001 — Courier dispatch thread (Keel iPhone, iMessage)

| Field | Value |
|-------|-------|
| Artifact ID | MSG-001 |
| Source device | ART-001 (`keel-iphone-UFED.zip`) |
| Modeling | `MessageThread` / `ThreadItem` or individual `Message` + `MessageFacet` |
| Recipe | `threaded-messaging`, `sms-and-contacts` |

```
Thread ID:     iMessage;+1-504-555-0177;+1-646-555-0191
Alias:         "King K" (+1-646-555-0191)

[2022-04-03 19:44:02 CDT] King K → Keel
  "Confirm tomorrow 10am. Victim A Hammond. Cash only. No cards."

[2022-04-04 08:12:33 CDT] Keel → King K
  [Attachment: IMG-004 package confirmation photo, see FS-008]

[2022-04-04 10:31:07 CDT] King K → Keel
  "Tangipahoa Sheriff on scene. ABORT. Destroy phone if you can."

[2022-04-04 10:31:19 CDT] Keel → King K
  "Already in custody."
```

#### MSG-002 — Pig-butchering Telegram (Victim-7 ↔ "Coach Elena")

| Field | Value |
|-------|-------|
| Artifact ID | MSG-002 |
| Platform | Telegram @coach_elena_pga (account ACC-007) |
| Recipe | `fraud-crypto-laundering`, `threaded-messaging` |

```
[2024-06-12 11:03 UTC] Coach Elena:
  "Your ETH staking pool matured. Reinvest through ApexVault Pro for 12% APY."

[2024-07-01 09:17 UTC] Victim-7:
  "Transferred 15 ETH to the wallet you sent."

[2024-07-15 14:55 UTC] Coach Elena:
  "Compliance hold — verify identity with exchange security team." 
  → triggers CALL-002 social-engineering escalation
```

#### MSG-003 — AnyDesk link SMS to Victim-7

```
[2024-08-18 14:58:33 EDT] +1-786-555-0133 → +1-202-555-0881
  "CoinShield: secure remote verification required. Install:
   https://anydesk.com/en/downloads (Session ID 1 234 567 890)"
```

#### MSG-004 — WeChat insider recruitment (Mei Chen ↔ COCONSPIRATOR W.L.)

| Field | Value |
|-------|-------|
| Artifact ID | MSG-004 |
| Exhibit | GX-22 (N.D. Cal., English translation certified) |
| Recipe | `insider-threat-trade-secrets` |

```
[2024-09-03 22:41 CST] W.L.:
  "Jade Horizon needs wafer scriber maintenance logs. USB is fine."

[2024-09-05 07:12 CST] Mei Chen:
  "Copied DTX-150 calibration folder to personal iCloud. Delete after read."

[2024-09-12 18:03 CST] W.L.:
  "AES filing shows EAR99. Do not mention Chengdu end user in email."
```

#### MSG-005 — Discord #vault-leaks (Kyle Marsh)

| Field | Value |
|-------|-------|
| Artifact ID | MSG-005 |
| Handling | DH-PGA-004 / ART-004 TS//SCI markings on attachments |
| Recipe | `espionage-classified-disclosure` |

```
[2025-01-14 23:08 EST] k_marsh_gaming:
  "Friday drop — Ukraine package, TS//SCI, don't share outside server"

[2025-01-14 23:09 EST] k_marsh_gaming:
  [Attachment: IMG-NDI-001.jpg — photograph of printed TS//SCI slides]

[2025-02-02 08:44 EST] k_marsh_gaming:
  "Delete everything if anyone asks. Burner only."
```

#### MSG-006 — ICAC grooming / sextortion (Juvenile J-1 ↔ NovaBlade)

| Field | Value |
|-------|-------|
| Artifact ID | MSG-006 |
| Handling | ART-006 juvenile privacy; DFT-1048 scope |
| Recipe | `cac-grooming-chat-modeling`, `cac-sextortion-coercion` |

```
[2025-08-19 21:33 AKDT] NovaBlade (StreamVault @novablade_884):
  "Send another or I post the edited pics to your school group."

[2025-08-20 06:12 AKDT] J-1:
  "I opened the Cash App like you said. Account routing 041215663."

[2025-08-20 06:14 AKDT] NovaBlade:
  "Good. You'll receive $500 tonight. Delete our chat."
```

---

### Email artifacts

#### EMAIL-001 — Spear-phish to Apex Semi (Mei Chen mailbox)

| Field | Value |
|-------|-------|
| Artifact ID | EMAIL-001 |
| Source | `Mei_Chen_MacBook/mail/V6/.../Messages/88421.emlx` |
| Recipe | `starter-email-export`, `spear-phishing` |

```
Message-ID: <a7f3c2@mail-security-apexsemi.net>
Date: Thu, 12 Sep 2024 09:01:22 -0700
From: IT Security <security-review@apexsemi-mail.net>  [SPF: FAIL]
To: mei.chen@apexsemi.com
Subject: Mandatory credential rotation — action by EOD
MIME: multipart/mixed
  Body: "Click to validate Okta session: https://apexsemi-mail.net/validate"
  Attachment: security_policy.pdf (SHA-256: a1b2c3... — macro-enabled, benign lure)
X-Originating-IP: 185.220.101.44 (Tor exit — see EVT-006)
```

#### EMAIL-002 — False AES/EEI filing notification (export control)

```
From: freight@jadehorizon-import.com
To: wei.zhang@jadehorizon-import.com
Date: 2024-03-18 14:22:00 -0400
Subject: RE: DTX-150 shipment — AES confirmation 20240318-88421
Body: "Consignee: JHI Nanjing. Commodity: EAR99 replacement parts.
       End user same as consignee. No Entity List parties."
True end user (investigation finding): GaStone Chengdu (Entity List 2014)
```

#### EMAIL-003 — FinCEN SAR escalation (internal FBI)

```
From: sar-liaison@fincen.gov (via secure portal)
To: pga-taskforce@fbi.gov
Date: 2022-11-03
Subject: SAR cluster reference FIN-2022-PGA-4412
Body: "Three SARs reference peel-chain deposits to account ending ...8841
       linked to Green Dot mule activity. Attach: sar_cluster_4412.csv"
Handling: DH-PGA-008 FINCEN-SAR-PROTECTED
```

---

### Accounts and identity linking

| Account ID | Platform | Identifier | Linked person | Linked accounts | Recipe |
|------------|----------|------------|---------------|-----------------|--------|
| ACC-001 | Mobile | +1-504-555-0177 (Keel) | Darius Keel | ACC-003 iCloud | `accounts`, `mobile-device-sim` |
| ACC-002 | Mobile | +1-646-555-0191 ("King K") | Raj Mehta (attributed) | CALL-003, MSG-001 | `call-log` |
| ACC-003 | Apple ID | keel.darius@icloud.com | Keel | ACC-001 device | `accounts` |
| ACC-004 | Telegram | @coach_elena_pga | COCONSPIRATOR T.I. | ACC-009 wallet | `fraud-crypto-laundering` |
| ACC-005 | AnyDesk | Session 1234567890 / Victim-7 | Victim-7 | EVT-003 RDP | `event`, `network-artifacts` |
| ACC-006 | Binance | UID 8847129033 (MLAR return) | Unknown mule | CRYPTO-001 | `cryptoinv` |
| ACC-007 | Ethereum | 0x7a3F...9c2D (Victim-7 hot wallet) | Victim-7 | CRYPTO-001 peel chain | `cryptoinv` |
| ACC-008 | Discord | k_marsh_gaming#8842 | Kyle Marsh | MSG-005 | `espionage-classified-disclosure` |
| ACC-009 | StreamVault | @novablade_884 | NovaBlade | MSG-006, CYBERTIP-001 | `cybertip-ncmec-workflow` |
| ACC-010 | WeChat | wxid_wl88421 | COCONSPIRATOR W.L. | MSG-004 | `insider-threat-trade-secrets` |

**Cross-platform correlation action:** InvestigativeAction `identity-correlation-pga-2025-q3` linked ACC-004, ACC-006, ACC-007 via USSS wallet clustering and ACC-001 call logs to ACC-002.

---

### File system artifacts

#### FS-001 — Victim-7 MacBook APFS layout (post-imaging)

| Field | Value |
|-------|-------|
| Source | ART-002 `evidence-2024-001.E01` |
| Recipe | `starter-filesystem-report`, `partitions`, `file-system` |

```
Volume:        APFS Container disk3 — 1 TB Samsung SSD
Partition:     disk3s1 — Macintosh HD — APFS encrypted (FileVault)
Key unlock:    Recovery key from victim statement 2024-08-20 (DH-PGA-002)

Notable paths (allocated):
  /Users/victim7/Downloads/AnyDesk.exe
    Size: 3,421,952 bytes
    Created: 2024-08-18 14:59:01 EDT
    Modified: 2024-08-18 14:59:01 EDT
    SHA-256: 8f14e45f...ceea167a

  /Users/victim7/Library/Logs/AnyDesk/ad.trace
    Contains session 1234567890 inbound connection 2024-08-18 15:02–15:47 EDT
    Remote IP logged: 198.51.100.44 (Lam VPN exit)

  /Users/victim7/Documents/Crypto/seed-backup.txt  [DELETED — see FS-003]
```

#### FS-002 — Keel iPhone logical extraction tree

```
Source: ART-001 Cellebrite UFED 7.69 logical
  private/var/mobile/Library/SMS/chat.db
    → MSG-001 thread export
  private/var/mobile/Media/DCIM/100APPLE/IMG_0042.JPG
    → FS-008 package confirmation photo
  private/var/mobile/Containers/Data/Application/.../Telegram/logs
    → partial; encryption limited (iOS 15 gap — SOLVE-IT residual risk)
```

#### FS-003 — Carved deleted file (Victim-7)

| Recipe | `file-recovery`, `file-fragments` |
|--------|-----------------------------------|

```
Carver:        Autopsy 4.21.0 + PhotoRec (dual-tool verify)
Offset:        0x3A8F1200 (unallocated APFS block)
Fragment:      seed-backup.txt (partial — 412 of ~890 bytes recovered)
Content excerpt: "... word11: canvas ... word12: ... [truncated]"
RecoveredObjectFacet: recoverability = "partial"
```

#### FS-004 — Apex Semi EDR — GateRunner persistence

| Recipe | `cyber-threat-intelligence`, registry native UCO |

```
Path: C:\Windows\System32\svchost.dll  [SIDeload — see CTI track]
Registry (from EDR export):
  HKLM\SYSTEM\CurrentControlSet\Services\tapisrv
    ImagePath: %SystemRoot%\System32\svchost.exe -k LocalService -p -s TapiSrv
    Parameters\ServiceDll: C:\ProgramData\Microsoft\Network\gatehelper.dll
  Datatype: reg_expand_sz (RegistryDatatypeVocab)
Associated service: tapisrv, Start=2 (service_auto_start)
```

#### FS-005 — SQLite WhatsApp (synthetic parallel on Keel contact)

```
File: ChatStorage.sqlite (from associated Android contact of co-conspirator)
Table: ZWAMESSAGE — 1,204 rows
Query artifact: SELECT ZFROMJID, ZTOJID, ZTEXT, ZMESSAGEDATE
  WHERE ZTEXT LIKE '%Hammond%' → 3 rows matching MSG-001 dates
Recipe: database-records
```

#### FS-006 — APFS filesystem events (Victim-7)

| Recipe | `file-system` (APFS fseventsd equivalent) |

```
Journal: $J:/Users/victim7/
Reason flags (structured Dictionary):
  2024-08-18T15:01:22-04:00  FILE_CREATE  AnyDesk.exe
  2024-08-18T15:47:33-04:00  DATA_OVERWRITE  seed-backup.txt
  2024-08-18T15:47:34-04:00  FILE_DELETE  seed-backup.txt
```

#### FS-007 — Bulk_extractor nested path

| Recipe | `bulk-extractor-path` |

```
Source scan: evidence-2024-001.E01
Feature file: email.txt
  Offset 884210944 → ZIP local header → email_frag_001
  Containment: E01 → APFS partition → Users/victim7/AppData.zip → mail/invite.eml
  Extracted invite.eml contains C2 domain gate-c2.darknet.invalid
```

#### FS-008 — Package confirmation photo (EXIF)

| Recipe | `exif-data` |

```
File: IMG_0042.JPG (Keel iPhone)
SHA-256: 4d5e6f...a1b2c3
Dimensions: 4032×3024
EXIF:
  DateTimeOriginal: 2022:04:04 08:11:58
  GPS: 30.5042° N, 90.4621° W (LOC-003 handoff lot — corroborates cell-site)
  Device: iPhone 13 Pro
```

---

### Network artifacts

#### NET-001 — PCAP summary (Apex Semi)

| Field | Value |
|-------|-------|
| File | `apex-semi-20241103.pcap` (ART-003) |
| SHA-256 | `c9d8e7f6a5b4...` |
| Window | 2024-11-03T00:00:00Z – 2024-11-06T00:00:00Z |
| Recipe | `network-investigation`, `network-artifacts` |

```
Flows (selected):
  10.44.12.88:52444 → 185.220.101.44:443  TLS SNI gate-c2.darknet.invalid  847 MB
  10.44.12.88:52444 → 149.154.167.41:443   Telegram API                  12 MB
  10.44.12.88:52444 → 52.84.100.12:443     AWS S3 ap-southeast-1          2.1 GB exfil

DNS:
  Query: gate-c2.darknet.invalid A → 198.51.100.44
  Query: dropbox.com A → (legitimate — GateRunner Dropbox C2 channel, CTI pattern)
```

#### NET-002 — AnyDesk session (Victim-7)

```
Protocol:      TCP/6568 (AnyDesk)
Client:        198.51.100.44:44102 (Lam VPN)
Server:        192.168.1.44:6568 (Victim-7 MacBook, home LAN)
Duration:      2024-08-18T15:02:11 – 15:47:28 EDT
Bytes:         1.2 GB outbound (screen stream + file transfer)
Linked event:  EVT-003
```

---

### Cryptocurrency artifacts

#### CRYPTO-001 — Peel chain (Victim-7 theft)

| Recipe | `fraud-crypto-laundering`, `cryptoinv` |

```
Theft tx:      2024-08-18 19:52:11 UTC
From:          0x7a3F...9c2D (ACC-007)
To:            0x9b1C...4f8A (PGA pass-through)
Amount:        12,441 ETH (~$47,093,000 USD spot)

Peel chain (Chainalysis export chain-88421.csv):
  Hop 1: 0x9b1C...4f8A → 0x2d8E...1a3B  (0.5 ETH peel)
  Hop 2: ... → Thorswap router 0x3a1... 
  Hop 3: USDT → eXch.io deposit 0x8f4...
  Hop 4: chain-hopping to Monero (txid redacted in MLAR)
launderingTechnique: peel-chain, chain-hopping-to-monero, crypto-to-cash
VASP: Thorswap, eXch (no-KYC flagged)
Forfeiture addresses: C1 0xTbdForfeit1..., C2 0xTbdForfeit2...
```

---

### CTI / malware artifacts

See `examples/cti/lotus_blossom_2025/` pattern. GateRunner = Sagerunex-variant.

| Artifact | Type | ATT&CK (attack-technique) |
|----------|------|---------------------------|
| gatehelper.dll | `MaliciousTool` | T1543.003, T1112 |
| Chrome cookie stealer | `MaliciousTool` | T1539 |
| mail_report.rar exfil | `FileFacet` | T1560.001, T1041 |
| 24 Talos-style report graphics | `RasterPicture` + SHA-256 | — |

---

## Chain of custody

One `InvestigativeAction` per transition; separate physical and digital provenance records per `docs/recipes/chain-of-custody.md`.

### COC-001 — Keel iPhone 13 Pro (ART-001)

**Exhibit:** E.D. La. 1-A  
**ProvenanceRecord:** `prov-art-001-physical`, `prov-art-001-digital`

| Step | Date/time (CDT) | Action | Performer | Location | Object | Seal / notes |
|------|-----------------|--------|-----------|----------|--------|--------------|
| 1 | 2022-04-04T10:35:00 | Collection/seizure | Det. B. Fontenot, TPSO | LOC-003 Tangipahoa sting | iPhone 13 Pro SN F2LD88421 | Bag TPSO-2022-044-A, seal S-9912 intact |
| 2 | 2022-04-04T11:20:00 | Faraday placement | Det. Fontenot | TPSO evidence room | Same | DFT-1010 — airplane mode confirmed |
| 3 | 2022-04-04T14:00:00 | Custody release | Det. Fontenot | TPSO → HSI | Bag TPSO-2022-044-A | Seal S-9912 intact |
| 4 | 2022-04-04T16:30:00 | Custody receipt | SA Rebecca Holt, HSI | HSI NOLA | Same | Seal verified |
| 5 | 2022-04-05T09:00:00 | Logical extraction | DF Examiner J. Price | HSI lab | → `keel-iphone-UFED.zip` | Tool: Cellebrite UFED 7.69 |
| 6 | 2022-04-05T11:45:00 | Hash verify | Examiner Price | HSI lab | UFED zip SHA-256 `e3b0c44...` | DFT-1042; matches UFED report |
| 7 | 2022-04-05T12:00:00 | Evidence storage | Evidence custodian | FBI NOLA locker L-14 | Physical device + digital copy | DH-PGA-001 |

### COC-002 — Victim-7 MacBook SSD image (ART-002)

**Exhibit:** D.D.C. GX-101  
**ProvenanceRecord:** `prov-art-002-digital`

| Step | Date/time (EDT) | Action | Performer | Instrument | Result |
|------|-----------------|--------|-----------|------------|--------|
| 1 | 2024-08-20T09:00:00 | Warrant execution | SA Dana Wu, FBI | — | MacBook Pro 16" SN C02Z88421 seized |
| 2 | 2024-08-20T10:15:00 | Write-blocked imaging | Examiner M. Okonkwo | Tableau TD3 + FTK Imager 4.7 | `evidence-2024-001.E01` |
| 3 | 2024-08-20T14:30:00 | Hash verify source vs image | Okonkwo | FTK Imager | SHA-256 match — `HashVerificationResult` |
| 4 | 2024-08-20T15:00:00 | Storage | DCFO digital vault | — | DV-2024-881; marking LEO-SENSITIVE |
| 5 | 2024-08-21T08:00:00 | Examination checkout | Okonkwo | Authorization SA Wu | Timeline + carving (FS-003) |
| 6 | 2024-08-22T17:00:00 | Re-seal / return to vault | Okonkwo | — | Working copy on examiner workstation WKS-884 |

### COC-003 — Apex Semi PCAP (ART-003)

| Step | Date/time | Action | Notes |
|------|-----------|--------|-------|
| 1 | 2024-11-06T06:00:00 | Corporate preservation | Apex Semi SOC — legal hold LH-2024-112 |
| 2 | 2024-11-08T10:00:00 | FBI copy receipt | Warrant ¶14; 72-hour mirror |
| 3 | 2024-11-08T11:30:00 | Integrity hash | SHA-256 `c9d8e7f6...` on `apex-semi-20241103.pcap` |
| 4 | 2024-11-09T09:00:00 | Examination | Wireshark 4.2 + NetworkMiner 2.8 — NET-001 summary |

### COC-004 — Classified Discord export (ART-004)

Dual chain: physical printouts (SCIF) + logical Discord JSON export.

| Step | Handling |
|------|----------|
| 1 | SCIF printer log → paper printouts → bag FBI-WFO-2025-NDI-04 |
| 2 | Discord LP warrant return → `discord_export_k_marsh.json` on air-gapped workstation |
| 3 | TS//SCI `objectMarking` applied before any prosecutor review |
| 4 | Redaction action (DFT-1046) before discovery to defense |

### COC-005 — Juvenile J-1 device (ART-006)

| Step | Requirement |
|------|-------------|
| 1 | ICAC CE warrant — device only, no cloud (minimization) |
| 2 | DFT-1048 — process `/data/data/com.streamvault.app/` and SMS only |
| 3 | Separate `ProvenanceRecord` — no joint storage with adult co-conspirator devices |
| 4 | Marking `JUVENILE-PRIVACY` on all derived reports |

---

## Digital forensics processing log

Structured processing steps for MCP `starter-tool-run`, `forensic-lifecycle`, and SOLVE-IT modeling.

| Proc ID | Date | Phase | Tool (version) | Input | Output | SOLVE-IT techniques | Status |
|---------|------|-------|----------------|-------|--------|---------------------|--------|
| PROC-001 | 2022-04-05 | Examination | Cellebrite UFED 7.69 | ART-001 device | `keel-iphone-UFED.zip` | DFT-1019, DFT-1042 | Success |
| PROC-002 | 2022-04-06 | Analysis | Cellebrite Physical Analyzer 7.69 | PROC-001 output | MSG-001 export, FS-008 | DFT-1052, DFT-1054 | Success |
| PROC-003 | 2024-08-20 | Acquisition | FTK Imager 4.7 + Tableau TD3 | Victim-7 SSD | ART-002 E01 | DFT-1002, DFT-1012, DFT-1025 | Success |
| PROC-004 | 2024-08-21 | Examination | Autopsy 4.21.0 | ART-002 | FS-001 listing, FS-003 carve | DFT-1061, DFT-1064, DFT-1052 | Partial (carve) |
| PROC-005 | 2024-08-21 | Verification | X-Ways 21.0 | ART-002 | Hash match confirmation | DFT-1042 (dual-tool) | Success |
| PROC-006 | 2024-08-22 | Analysis | Magnet AXIOM 7.4 | ART-002 | AnyDesk timeline EVT-003 | DFT-1069, DFT-1056 | Success |
| PROC-007 | 2024-11-09 | Examination | Wireshark 4.2 | ART-003 PCAP | NET-001 flow summary | DFT-1017 (capture already done) | Success |
| PROC-008 | 2025-03-14 | Malware RE | REMnux 2024 + Ghidra 11 | gatehelper.dll | CTI IOC report | DFT-1054, DFT-1057 | Success (air-gapped) |
| PROC-009 | 2025-08-22 | Acquisition | Cellebrite UFED 7.82 | J-1 device | Partial logical (ART-006) | DFT-1019 | Partial — iOS gap |
| PROC-010 | 2025-09-01 | Crypto trace | Chainalysis Reactor + TRM | CRYPTO-001 CSV | Wallet cluster graph | — (financial analysis) | Success |

Each row → `InvestigativeAction` with `instrument` (Tool/ConfiguredTool), `object`, `result`, `startTime`/`endTime`, optional `solveit-core:SolveitInvestigativeAction` overlay.

---

## AI/ML analysis pipeline results

Per `docs/recipes/ai-analysis-pipeline.md` — structured scores, not JSON blobs in descriptions.

### AI-001 — PhotoDNA hash match (StreamVault CyberTip)

| Step | Tool | Input | Output | Score |
|------|------|-------|--------|-------|
| 1 | PhotoDNA Cloud API v2 | CYBERTIP-001 image set (5 images) | HashMatchDetection | match confidence 0.997 |
| 2 | Human reviewer (ICAC) | Step 1 hits | Confirmed CSAM-adjacent grooming set | analyst certainty: high |

```json
{
  "@type": "InvestigativeAction",
  "uco-core:name": "PhotoDNA hash analysis — CyberTip 2025-88421",
  "uco-action:instrument": {"@id": "kb:tool-photodna-v2"},
  "uco-action:object": [{"@id": "kb:cybertip-001-image-set"}],
  "uco-action:result": [{"@id": "kb:detection-photodna-001"}]
}
```

`cacontology-detection:HashMatchDetection` with `confidenceScore: 0.997`.

### AI-002 — CLIP semantic image search (courier package photos)

| Step | Tool | Input | Output |
|------|------|-------|--------|
| 1 | CLIP ViT-B/32 (ConfiguredTool) | Keel DCIM folder (842 images) | Ranked matches |
| Query | — | "cash in envelope package confirmation" | — |

| Rank | File | Similarity | Selected |
|------|------|------------|----------|
| 1 | IMG_0042.JPG | 0.89 | Yes → FS-008, GX-14 |
| 2 | IMG_0038.JPG | 0.71 | No |
| 3 | IMG_0011.JPG | 0.68 | No |

Each result → `RasterPicture` + `ConfidenceFacet` + `Relationship` `Selected_From` input directory.

### AI-003 — Malware classification (GateRunner)

| Step | Tool | Output |
|------|------|--------|
| 1 | Elastic ML model `gate-runner-v3` | `ArtifactClassification`: `Malware.Family.GateRunner` confidence 0.94 |
| 2 | YARA scan `Sagerunex_ruleset_2025` | 47/47 rule match on gatehelper.dll |

`ArtifactClassificationResultFacet` on the DLL observable.

### AI-004 — Voice analytics (Title III sample — optional stretch)

| Step | Tool | Output |
|------|------|--------|
| 1 | Speaker diarization (synthetic) | CALL-003 speaker labels King K vs Keel — match score 0.82 |

---

## Events and authentication logs

Per `docs/recipes/event.md` — use `Event` + `Dictionary`/`DictionaryEntry` for structured attributes.

### EVT-001 — Green Dot card purchase (Victim A)

```
Event type:    FinancialTransaction
Start:         2022-04-04T11:45:00-05:00
Account:       Green Dot card ending 8842 (Victim A)
Dictionary entries:
  merchant:     Walgreens, Hammond LA
  amount USD:   500.00
  card_type:    prepaid
  triggered_by: CALL-001
Location:      LOC-002
```

### EVT-002 — Controlled delivery arrest trigger

```
Event type:    LawEnforcementOperation
Start:         2022-04-04T10:35:00-05:00
Actions:       surveillance → signal → arrest
Dictionary:
  operation_id: TPSO-CD-2022-044
  target:       Darius Keel
  victim:       Victim A (77)
```

### EVT-003 — AnyDesk remote session (Victim-7)

```
Event type:    RemoteAccessSession
Start:         2024-08-18T15:02:11-04:00
End:           2024-08-18T15:47:28-04:00
Account:       ACC-005 (session 1234567890)
Dictionary:
  software:     AnyDesk 8.0.8
  remote_ip:    198.51.100.44
  local_ip:     192.168.1.44
  bytes_out:    1288490188
  file_transfer: seed-backup.txt (see FS-003)
Linked:        CALL-002, MSG-003, NET-002
```

### EVT-004 — Wallet transfer (Victim-7 theft)

```
Event type:    CryptocurrencyTransfer
Start:         2024-08-18T19:52:11Z
Dictionary:
  chain:        Ethereum mainnet
  tx_hash:      0xabc884...def
  from:         0x7a3F...9c2D
  to:           0x9b1C...4f8A
  amount_eth:   12441.0
  usd_spot:     47093000
```

### EVT-005 — Apex Semi EDR alert (GateRunner)

```
Event type:    SecurityAlert
Start:         2024-11-03T02:14:33Z
Dictionary:
  edr_product:  CrowdStrike Falcon
  severity:     critical
  tactic:       Persistence
  technique:    T1543.003
  host:         apex-ws-88421.corp.apexsemi.com
  file:         C:\ProgramData\Microsoft\Network\gatehelper.dll
  sha256:       7f83b1657... (gatehelper.dll)
```

### EVT-006 — Spear-phish click (Mei Chen)

```
Event type:    Authentication
Start:         2024-09-12T09:04:18-07:00
Dictionary:
  method:       credential_phishing
  target_url:   https://apexsemi-mail.net/validate
  source_ip:    185.220.101.44
  user_agent:   Mozilla/5.0 (Macintosh; Mac OS X 10_15_7)
  mfa_bypassed: false
  outcome:      credentials_not_entered (user clicked, closed tab)
Linked:        EMAIL-001
```

### EVT-007 — SCIF badge swipe (Kyle Marsh)

```
Event type:    PhysicalAccess
Start:         2025-01-10T06:12:00-05:00
Dictionary:
  facility:     SCIF-NATGRD-884
  badge_id:     KM-4412
  reader:       NG-BASE-EAST-DOOR-3
  result:       granted
Linked:        espionage track — removal chain start
```

### EVT-008 — NCMEC CyberTip submission

```
Event type:    CyberTipReport
Start:         2025-08-19T18:02:00Z
Dictionary:
  cybertip_id: 2025-88421
  esp:          StreamVault
  reporter:     automated CSAM classifier
  ip_preservation: 185.220.101.55
Linked:        ACC-009, ART-005
```

---

## Locations

| Loc ID | Name | Address / coordinates | Role | Recipe |
|--------|------|----------------------|------|--------|
| LOC-001 | Victim A residence | 124 Oak Lane, Hammond, LA 70403 | Elder fraud victim | `location` |
| LOC-002 | Walgreens Hammond | 45000 Highway 190, Hammond, LA | Card purchase EVT-001 | `location` |
| LOC-003 | Tangipahoa sting lot | 30.5042°N, 90.4621°W (Shell rear lot) | Controlled delivery COC-001 | `elder-fraud` |
| LOC-004 | Victim-7 residence | 1800 Massachusetts Ave NW, Washington, DC | $47M theft | `location` |
| LOC-005 | Victim-4 residence | Albuquerque, NM (redacted street) | Home invasion attempt | `location` |
| LOC-006 | Lam Miami residence | 8841 Biscayne Blvd, Miami, FL | Obstruction — phone into bay | `location` |
| LOC-007 | Apex Semi HQ | San Jose, CA (campus) | Insider / EDR | `location` |
| LOC-008 | SCIF-NATGRD-884 | Otis ANGB, MA (not public) | Classified removal | `espionage` |
| LOC-009 | PGA Fargo safehouse | 884 1st Ave N, Fargo, ND | Weapons/drugs seizure | `weapons-drug-evidence` |
| LOC-010 | ICAC undercover meet | Anchorage, AK (park, synthetic) | CAC sting | `cac-icac-search-warrant-arrest` |

Cell-site **TOWER-004**: Sector 210°, 850 MHz — Keel phone at LOC-003, 2022-04-04T10:28:00 CDT (`cell-site` recipe).

---

## SOLVE-IT examination plan

Use MCP `plan_solveit_workflow` for each acquisition. Record `SolveitInvestigativeAction`, `WeaknessEvaluationSet`, and residual risk where mitigations were not applied.

| Phase | Workflow prompt | Key DFT | Residual risk if unmitigated |
|-------|-----------------|---------|------------------------------|
| Keel phone | "logical extract iPhone 13 Pro after controlled delivery arrest" | DFT-1010, DFT-1019, DFT-1042 | Remote wipe (DFW cloud sync) |
| Victim-7 SSD | "image FileVault MacBook with hardware write blocker" | DFT-1012, DFT-1002, DFT-1062 | Incomplete sector copy |
| J-1 device | "partial process juvenile phone chats only" | DFT-1048, DFT-1019 | Over-collection of juvenile data |
| PCAP | "analyze 72-hour warrant PCAP for C2" | DFT-1017, DFT-1056 | Clock skew vs EDR |
| Malware | "examine live malware sample air-gapped" | DFT-1054, DFT-1057 | Accidental outbound beacon |

---

## Legal process

### Charging instruments

| Court | Case | Charges (summary) |
|-------|------|-------------------|
| E.D. La. | 2:26-cr-00115 | § 1349 wire fraud conspiracy (couriers) |
| D.D.C. | 1:26-cr-00417 | § 1962(d) RICO; § 1349; § 1956(h); § 1512(c) |
| N.D. Cal. | 3:26-cr-00141 | § 1832 / § 1831 (Mei Chen) |
| N.D. Cal. | 3:26-cr-00446 | IEEPA / false AES (Wei Zhang) |
| D. Mass. | 1:26-cr-10159 | § 793(e) ×6 (Kyle Marsh) |
| D. Alaska | 3:26-cr-00029 | § 2422(b), production-related (CAC wing) |

### Authorizations

Title III (CALL-003), Rule 41 searches (COC-001, COC-002, ICAC CE), MLAT Romania VPS, corporate consent (Apex Semi), NCMEC preservation (StreamVault), Discord LP (Marsh).

---

## Extension bundles and MCP exercise matrix

### Per-phase validation bundles

```text
Phase 1:  legalproc
Phase 2:  legalproc, rico, cryptoinv
Phase 3:  legalproc, rico
Phase 4:  legalproc (+ uco-marking for export/espionage tracks)
Phase 5:  attack-technique
Phase 6:  cac (+ legalproc)
Phase 7:  solveit, weapons, drugs, toolcap
Always:   chain-of-custody, ai-analysis-pipeline, event, location recipes (core)
```

### MCP tool prompts

| Tool | Input |
|------|-------|
| `route_investigation_content` | Full narrative or artifact sections above |
| `route_cac_content` | MSG-006, CYBERTIP-001, ART-005 |
| `guide_mapping` | "elder fraud courier iPhone + cell-site", "AnyDesk crypto theft timeline", "GateRunner registry persistence" |
| `plan_solveit_workflow` | Each SOLVE-IT row |
| `process_document_file` | Synthetic PACER PDFs when available |
| `validate_graph` | Cumulative extensions per phase |

### Artifact ID → recipe quick reference

| IDs | Recipes |
|-----|---------|
| CALL-*, MSG-*, ACC-* | `call-log`, `threaded-messaging`, `sms-and-contacts`, `accounts` |
| EMAIL-* | `starter-email-export`, `spear-phishing` |
| FS-* | `file-system`, `file-recovery`, `database-records`, `usn-journal`, `bulk-extractor-path`, `exif-data` |
| NET-*, EVT-003 | `network-investigation`, `event` |
| CRYPTO-* | `fraud-crypto-laundering`, `cryptoinv` |
| COC-* | `chain-of-custody`, `forensic-lifecycle` |
| AI-* | `ai-analysis-pipeline`, `analysis` |
| DH-* | `espionage-classified-disclosure` (markings), SOLVE-IT DFT-1046 |
| CTI / FS-004 | `cyber-threat-intelligence`, `attack-technique` |

---

## Grounding in processed exemplars

| Scenario element | Exemplar |
|------------------|----------|
| RICO enterprise, crypto, obstruction | `examples/pacer/ddc_2024_cr_00417/` |
| Elder fraud, calls, couriers | `examples/pacer/edla_2022_cr_00115/` |
| Crypto laundering plea pattern | `examples/pacer/doj_crypto_2023_239/` |
| Insider WeChat, jury verdict | `examples/pacer/ndca_2024_cr_00141/` |
| Export control, Entity List | `examples/pacer/ndca_2020_cr_00446/` |
| Classified Discord, TS markings | `examples/pacer/dma_2023_cr_10159/` |
| APT / ATT&CK CTI | `examples/cti/lotus_blossom_2025/` |
| SOLVE-IT acquisition | `examples/solveit/` |
| Weapons + drugs | `examples/pacer/ndnd_2025_cr_00005/` |
| ICAC / trial CAC | `examples/pacer/anchorage_pd_2022_004/` |

---

## Sample combined ingestion block

Use this single block to stress-test MCP routing:

> On 2022-04-04, Victim A (77, Hammond LA) received CALL-001 from a spoofed "US Treasury" line. Det. D'Amato observed the call live. Keel arrived at LOC-003 for a cash pickup; TPSO executed a controlled delivery (EVT-002) and seized his iPhone (COC-001, ART-001). iMessage thread MSG-001 shows dispatch from "King K" (+1-646-555-0191). Title III intercept CALL-003 captured the India dispatch line. Package photo IMG_0042.JPG (FS-008) GPS-corroborates the handoff. PhotoDNA pipeline AI-001 and CLIP semantic search AI-002 ranked the confirmation photo at 0.89 similarity (89/100 scale).
>
> On 2024-08-18, Victim-7 in Washington DC received CALL-002 and MSG-003, installed AnyDesk (FS-001), and underwent remote session EVT-003 from 198.51.100.44. Seed file seed-backup.txt was deleted (FS-006 APFS filesystem events) and partially carved (FS-003). $47M in ETH moved per CRYPTO-001. SSD image ART-002 was acquired under COC-002 with FileVault key provenance documented under DH-PGA-002.
>
> Apex Semi EDR fired EVT-005 on gatehelper.dll (FS-004). PCAP ART-003 (NET-001) showed 2.1 GB S3 exfil. GateRunner maps to ATT&CK T1543.003, T1539 via attack-technique extension.
>
> NCMEC CyberTip 2025-88421 (EVT-008) from StreamVault led to MSG-006 sextortion of Juvenile J-1 with JUVENILE-PRIVACY handling (COC-005, DH-PGA-006). Discord export ART-004 carries TS//SCI markings on NDI printouts. Fargo safehouse LOC-009 yielded SIG Sauer P365 and 482g methamphetamine mixture.

---

*Rebuild graph:* `python examples/scenarios/build_phantom_gate_scenario.py` → `operation-phantom-gate.jsonld`
