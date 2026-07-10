#!/usr/bin/env python3
"""Build a validated CASE/UCO graph for the Cisco Talos Lotus Blossom report.

Source (open-source cyber threat intelligence, not a legal case):
  "Lotus Blossom espionage group targets multiple industries with different
  versions of Sagerunex and hacking tools" — by Joey Chen, Cisco Talos,
  2025-02-27. https://blog.talosintelligence.com/lotus-blossom-espionage-group/

This exemplar models an APT/threat-intelligence report rather than acquired
digital evidence. It is the worked example behind
docs/recipes/cyber-threat-intelligence.md.

What is modeled
---------------
* The Talos report as a cyber observable (article) with its author (Joey
  Chen) and publisher (Cisco Talos), plus every in-article graphic captured
  as a RasterPicture observable with a SHA-256 hash and a description of what
  it depicts (the user asked that the graphics be captured because they carry
  details absent from the prose).
* Lotus Blossom as the threat actor. UCO has no dedicated ThreatActor class,
  so the group is a uco-identity:Organization; its aliases (Spring Dragon,
  Billbug, Thrip) are recorded, and every adversary behavior is a
  uco-action:Action whose performer is this Organization.
* The Sagerunex backdoor family (uco-tool:MaliciousTool) and its variants
  (Beta, original, Dropbox/Twitter, Zimbra) as File observables with the
  config-revealed artifacts (C2 endpoints, tokens, attacker host paths, debug
  log temp filenames), each with an existence interval from the Talos timeline
  graphic.
* The post-compromise toolkit: Chrome cookie stealer, Venom proxy, an
  adjust-privilege tool, a customized archiving tool, the "mtrain V1.01" HTran
  port relay, RAR, and Impacket.
* Registry-based persistence. This is the focal modeling question the user
  raised: UCO's registry coverage is *sufficient* for this data. The reg-add
  service-DLL persistence commands map cleanly onto
  uco-observable:WindowsRegistryKey + WindowsRegistryKeyFacet with embedded
  WindowsRegistryValue entries (name / data / dataType), where dataType uses
  the RegistryDatatypeVocab members reg_expand_sz and reg_dword, paired with
  uco-observable:WindowsService (startType service_auto_start from Start=2).
  No change proposal is required.
* Command-and-control infrastructure: legacy VPS IPs, a hardcoded HTTP proxy,
  and the third-party cloud C2 channels (Dropbox, Twitter/X, Zimbra webmail).
* Detection coverage: Snort SIDs and ClamAV signature names.

MITRE ATT&CK note: the Talos prose lists no ATT&CK technique IDs, but the
MITRE ATT&CK group page for Lotus Blossom (G0030) and the Sagerunex software
page (S1156) do. Twelve of those techniques are modeled here with the
uco-action:Technique *metaclass* exactly as defined in ucoProject/UCO PR #676
(Feature-Issue-666): each ATT&CK technique is itself an owl:Class that is a
subclass of uco-action:Action and carries uco-action:techniqueID (the
technique classes live in extensions/attack-technique/mitre-attack-catalog.ttl
under canonical ATT&CK IRIs), and a concrete behavior Action that exhibits a
technique is *typed with* that technique class (rdf:type) — the punning
pattern the PR intends, anchored by the new top-level uco-core:UcoType. Until
UCO 1.5.0 ships these terms, the local attack-technique extension declares
them (in their released uco-core:/uco-action: IRIs), loaded by the builder via
extensions=["attack-technique:full"]. See the recipe for the pattern.

All facts are drawn from the Talos article and its graphics. Uncertain OCR of
hexdump artifacts is flagged in the relevant description strings.
"""

from __future__ import annotations

import hashlib
import json
import struct
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "mcp_server"))

from graph_validator import validate_graph_file, validator_available  # noqa: E402

CASE_ID = "lotus-blossom-sagerunex-talos-2025"
NS = f"https://example.org/cti/{CASE_ID}/"
HERE = Path(__file__).resolve().parent
GRAPHICS_DIR = HERE / "graphics"
OUTPUT = HERE / "lotus-blossom-sagerunex.jsonld"

REPORT_URL = "https://blog.talosintelligence.com/lotus-blossom-espionage-group/"
REPORT_PUBLISHED = "2025-02-27T06:00:00-05:00"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def lit(dtype: str, value) -> dict:
    val = str(value).lower() if isinstance(value, bool) else str(value)
    return {"@type": dtype, "@value": val}


def rel(source: str, target: str, kind: str, directional: bool = True,
        tag: str | None = None, desc: str | None = None) -> dict:
    node = {
        "@id": uid(f"rel-{source}-{target}-{kind}"),
        "@type": "uco-core:Relationship",
        "uco-core:source": [{"@id": source}],
        "uco-core:target": [{"@id": target}],
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": lit("xsd:boolean", directional),
    }
    if tag:
        node["uco-core:tag"] = tag
    if desc:
        node["uco-core:description"] = desc
    return node


def image_dimensions(path: Path) -> tuple[int, int] | None:
    """Read (width, height) from a PNG or JPEG header without Pillow."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    if data[:2] == b"\xff\xd8":  # JPEG
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            i += 2 + seg_len
    return None


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# In-article graphics, in publication order. Each description records what the
# image depicts so the intelligence carried by the picture is preserved even
# though the picture itself is only referenced by hash.
GRAPHICS: list[tuple[str, str]] = [
    ("01-targeted-countries-map.jpeg",
     "Talos 'Targeted countries' map highlighting Vietnam, Hong Kong, "
     "Taiwan, and the Philippines as Lotus Blossom targets."),
    ("02-sagerunex-timeline.jpeg",
     "'Timeline of Sagerunex' Gantt chart: Beta/original ~2016-2021, "
     "Dropbox and Twitter version ~2018-2022, Zimbra version ~2019-2024."),
    ("03-cookie-stealer-code.png",
     "Decompiled get_cookies_from_chrome() of the Chrome cookie stealer; "
     "reads the Chrome 'Cookies' SQLite DB, decrypts values, and writes "
     "them to the temp file tmcok43.tmp."),
    ("04-venom-proxy-functions.png",
     "IDA function list of the Venom proxy agent "
     "(github_com_Dliv3_Venom_agent_dispatcher_* handlers: SyncCmd, "
     "ConnectCmd, DownloadCmd, UploadCmd, ShellCmd, Socks5Cmd, forwarding)."),
    ("05-adjust-privilege-code.png",
     "Decompiled adjust-privilege tool: usage 'pid image parameters', "
     "retrieves another process token to adjust privilege for a launch "
     "process."),
    ("06-archiving-tool-code.png",
     "Decompiled customized archiving tool with '[!] Compressed file not "
     "supported yet', '[!] Encrypted file not supported yet', and file-"
     "attribute parsing; compresses/encrypts stolen files and folders."),
    ("07-mtrain-portrelay-usage.png",
     "Cmder session showing 'mtrain.exe_f2370de517a032a27fcf3ba175e611a1b1a2b0ba "
     "-debug' printing 'MTrain V1.01' usage (-l/-t/-s ConnectPort/"
     "TransmissionHost/TransmissionPort); run from C:\\Users\\yyds\\Desktop."),
    ("08-attack-chain-diagram.jpeg",
     "Talos 'Attack chain' diagram: unknown vector -> initial compromised "
     "machine -> WMI lateral movement across the internal network -> tool "
     "sets (RAR, port relay, archiving, adjust-privilege, Venom, cookie "
     "stealer) -> Sagerunex data-exfiltrating machine -> C2 over VPS, "
     "Zimbra, Dropbox, and X (Twitter)."),
    ("09-sagerunex-debug-logfile-names.png",
     "Decompiled debug-log routines for the four Sagerunex variants showing "
     "the temp debug-log filenames each variant writes (e.g. TS_968T.tmp, "
     "TS_F856.tmp, DBGECD20.tmp, VDM_LOMT.tmp — OCR approximate)."),
    ("10-sagerunex-config-file-paths.png",
     "Decompiled config-path builders for the Sagerunex variants using "
     "SHGetSpecialFolderPath and CreateDirectory under Microsoft / Internet "
     "Explorer / Windows / Network folders, writing config filenames such as "
     "DMIX.DAT, GE_%X.dat, GED%X.CAB, DEP%X.CAB (OCR approximate)."),
    ("11-beta-config-hexdump.png",
     "Annotated hexdump of a Beta/original Sagerunex config: campaign code "
     "'WS1x321014'; C&C servers 103.234.97.19, 43.252.161.22, "
     "118.193.240.214, 103.232.223.117, 103.243.131.205; victim HTTP proxy "
     "192.168.240.18:8080 with proxy username/password."),
    ("12-beta-online-checkin-code.png",
     "Decompiled Beta online/beacon loop with debug strings 'Online fail - "
     "%d', 'Missing server config.', 'Online Fail! Wait for %d mins', 'Sleep "
     "- %d mins', and WaitForSingleObject waits."),
    ("13-beta-command-functions.png",
     "Decompiled Beta command dispatcher: Heart/Online check-ins then a "
     "command switch — host_Status, update_config, cmd_shell, "
     "Execute_Script, Read_file, create_file."),
    ("14-beta-infection-chain.jpeg",
     "Talos 'Beta version of Sagerunex' infection-chain diagram: shell runs "
     "the loader as a service, loader injects Sagerunex into memory; checks "
     "config file/system time/proxy/internet, drops/reads config, writes "
     "logs, connects to C2; commands host status, update config, cmd shell, "
     "read file, create file."),
    ("15-dropbox-twitter-command-code.png",
     "Decompiled Dropbox/Twitter variant: Twitter Tdle-from-id and Dropbox "
     "get-list/create-folder token handling, MAC-match and length checks, "
     "then command switch uploadFile / Set_config_info / test_token / cmd / "
     "read_file / create_file."),
    ("16-dropbox-twitter-config-hexdump.png",
     "Annotated hexdump of the Dropbox/Twitter config: Dropbox tokens, "
     "Twitter [ConsumerKey]/[ConsumerSecret]/[AccessToken]/[AccessTokenSecret]"
     "/[ScreenName] fields, and a possible attacker file path "
     "C:\\Users\\USER\\Documents\\dtj32\\dj32.dll."),
    ("17-dropbox-file-listing.png",
     "Dropbox API file listing extracted from one C2 account: JSON entries "
     "with client_modified/server_modified timestamps spanning 2018-07 "
     "through 2022-06, confirming the 2018-2022 activity window."),
    ("18-dropbox-twitter-infection-chain.jpeg",
     "Talos 'Dropbox & Twitter version of Sagerunex' infection-chain "
     "diagram, including the beacon response-ID logic (id<16 re-beacon, "
     "16-32 collect+execute, ==39 status check) and archive-and-send to "
     "Dropbox/Twitter."),
    ("19-zimbra-draft-request-code.png",
     "Decompiled Zimbra variant SaveDraftRequest building a Zimbra SOAP "
     "request with 'Cookie: ZM_TEST=true; ZM_AUTH_TOKEN=%s; "
     "JSESSIONID=%s', an X-Zimbra-Csrf-Token, and a draft mail carrying the "
     "encoded attachment."),
    ("20-zimbra-connection-command-code.png",
     "Decompiled Zimbra connection/command routine: builds the "
     "/service/home mailbox URL with ZM_AUTH_TOKEN, sends via a "
     "'Jakarta Commons-HttpClient/3.1' user agent, then a command switch — "
     "Send_back_log, Copy_Files, CmdShell, Read_Files, Create_Files."),
    ("21-zimbra-draft-mailbox.png",
     "Screenshot of a Zimbra (netvigator.com) 'Daily mail report' Drafts "
     "folder full of base64 draft bodies, each with a mail_report.rar "
     "attachment — the beacon/exfil channel."),
    ("22-zimbra-trash-mailbox.png",
     "Screenshot of the same Zimbra account's Trash folder with 'Daily mail "
     "report' drafts and mail_report.rar attachments — the command-result "
     "channel."),
    ("23-zimbra-infection-chain.jpeg",
     "Talos 'Zimbra webmail version of Sagerunex' infection-chain diagram: "
     "login for authToken, sync folders, save host info as mail_report.rar "
     "into the draft folder; commands host status, copy file, cmd shell, "
     "read file, create file, results saved to the trash folder."),
    ("24-cisco-coverage-matrix.png",
     "Cisco product coverage matrix (Secure Endpoint, Secure Email, Secure "
     "Firewall/IPS, Secure Malware Analytics, Umbrella DNS/SIG, Secure Web "
     "Appliance) for this threat."),
]

# reg-add service-DLL persistence commands from the 'Extended persistence'
# section. Each tuple: (service, key path, [(value name, datatype, data), ...]).
REGISTRY_PERSISTENCE = [
    ("tapisrv",
     r"HKLM\SYSTEM\CurrentControlSet\Services\tapisrv\Parameters",
     [("ServiceDll", "reg_expand_sz", r"c:\windows\tapisrv.dll")]),
    ("tapisrv",
     r"HKLM\SYSTEM\CurrentControlSet\Services\tapisrv",
     [("Start", "reg_dword", "2")]),
    ("swprv",
     r"HKLM\SYSTEM\CurrentControlSet\Services\swprv\Parameters",
     [("ServiceDll", "reg_expand_sz", r"c:\windows\swprv.dll"),
      ("ServiceDll", "reg_expand_sz", r"c:\windows\system32\swprv.dll")]),
    ("appmgmt",
     r"HKLM\SYSTEM\CurrentControlSet\Services\appmgmt\Parameters",
     [("ServiceDll", "reg_expand_sz", r"c:\windows\swprv.dll"),
      ("ServiceDll", "reg_expand_sz", r"c:\windows\system32\appmgmts.dll")]),
    ("appmgmt",
     r"HKLM\SYSTEM\CurrentControlSet\Services\appmgmt",
     [("Start", "reg_dword", "2")]),
]

# C2 endpoints recovered from the Beta/original config hexdump (graphic 11).
LEGACY_C2_IPS = [
    "103.234.97.19", "43.252.161.22", "118.193.240.214",
    "103.232.223.117", "103.243.131.205",
]

# Attacker-machine file paths revealed in the Dropbox/Twitter config.
ATTACKER_HOST_PATHS = [
    r"C:\Users\aa\Desktop\dpst.dll",
    r"C:\Users\3\Desktop\DT-1-64-G\msiscsii.dll",
    r"C:\Users\balabala\Desktop\swprve64.dll",
    r"C:\Users\test04\Desktop\a\dtsvc32.dll",
    r"C:\Users\USER\Documents\dtj32\dj32.dll",
]

# Campaign codes (IOCs section).
CAMPAIGN_CODES = [
    "st", "qaz", "test", "cmhk", "dtemp", "0305", "4007", "4007_new",
    "Jf_b64_t1", "Ber_64", "0817-svc64", "NSX32-0710", "Nsx32-0419",
    "NJX32-0710", "WS1x321014", "pccw-svc32", "CTMsx32-0712",
]

CLAMAV_SIGS = [
    "Win.Backdoor.Sagerunex-10041845-0", "Win.Tool.Mtrain-10041846-0",
    "Win.Tool.Ntfsdump-10041854-0", "Win.Backdoor.Sagerunex-10041857-0",
]
SNORT_SIDS = ["64511", "64510", "64509"]


def build_graph() -> dict:
    g: list[dict] = []

    # ------------------------------------------------------------------
    # Investigation container
    # ------------------------------------------------------------------
    investigation = uid("investigation")
    g.append({
        "@id": investigation,
        "@type": "case-investigation:Investigation",
        "uco-core:name": "Cisco Talos threat spotlight: Lotus Blossom / Sagerunex",
        "uco-core:description": (
            "Open-source cyber threat intelligence report by Cisco Talos "
            "(Joey Chen, 2025-02-27) analyzing cyber-espionage campaigns by "
            "the Lotus Blossom group (a.k.a. Spring Dragon, Billbug, Thrip), "
            "active since at least 2012, against government, manufacturing, "
            "telecommunications, and media targets in the Philippines, "
            "Vietnam, Hong Kong, and Taiwan. The group deploys the Sagerunex "
            "backdoor family (Beta/original, Dropbox/Twitter, and Zimbra "
            "variants) with persistence installed as service DLLs in the "
            "Windows registry, and a post-compromise toolkit (Chrome cookie "
            "stealer, Venom proxy, adjust-privilege tool, customized "
            "archiver, mtrain/HTran port relay, RAR, Impacket)."
        ),
        "case-investigation:focus": [
            "APT attribution", "Malware family analysis",
            "C2 infrastructure", "Registry persistence",
        ],
    })

    def add_org(label, name, desc, aliases=None):
        node = {
            "@id": uid(label),
            "@type": "uco-identity:Organization",
            "uco-core:name": name,
            "uco-core:description": desc,
        }
        if aliases:
            node["uco-core:tag"] = aliases
        g.append(node)
        return uid(label)

    def add_person(label, name, desc):
        g.append({
            "@id": uid(label),
            "@type": "uco-identity:Person",
            "uco-core:name": name,
            "uco-core:description": desc,
        })
        return uid(label)

    # ------------------------------------------------------------------
    # Report, author, publisher, and captured graphics
    # ------------------------------------------------------------------
    talos = add_org("org-talos", "Cisco Talos",
                    "Cisco Talos Intelligence Group; publisher of the report "
                    "and author of the detection coverage.")
    author = add_person("person-joey-chen", "Joey Chen",
                        "Cisco Talos researcher credited as author of the "
                        "Lotus Blossom / Sagerunex report.")
    report = uid("report")
    g.append({
        "@id": report,
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "Lotus Blossom espionage group targets multiple "
                         "industries with different versions of Sagerunex "
                         "and hacking tools",
        "uco-core:description": (
            "Cisco Talos blog post (threat spotlight, APT) authored by Joey "
            f"Chen and published by Cisco Talos on {REPORT_PUBLISHED[:10]}."
        ),
        "uco-core:hasFacet": [
            {
                "@id": uid("report-url-facet"),
                "@type": "uco-observable:URLFacet",
                "uco-observable:fullValue": REPORT_URL,
            },
        ],
    })
    g.append(rel(report, investigation, "part_of"))
    g.append(rel(author, report, "Authored_By", desc="Report author"))
    g.append(rel(talos, report, "Published_By", desc="Report publisher"))

    graphic_ids = []
    for fname, desc in GRAPHICS:
        path = GRAPHICS_DIR / fname
        if not path.exists():
            raise FileNotFoundError(f"missing graphic: {path}")
        label = f"graphic-{fname}"
        gid = uid(label)
        graphic_ids.append(gid)
        raster = {
            "@id": uid(f"{label}-raster-facet"),
            "@type": "uco-observable:RasterPictureFacet",
        }
        dims = image_dimensions(path)
        if dims:
            raster["uco-observable:pictureWidth"] = lit("xsd:integer", dims[0])
            raster["uco-observable:pictureHeight"] = lit("xsd:integer", dims[1])
        ext = path.suffix.lstrip(".").lower()
        raster["uco-observable:imageCompressionMethod"] = (
            "JPEG" if ext in ("jpg", "jpeg") else "PNG")
        g.append({
            "@id": gid,
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": fname,
            "uco-core:description": desc,
            "uco-core:hasFacet": [
                {
                    "@id": uid(f"{label}-file-facet"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": fname,
                    "uco-observable:extension": ext,
                    "uco-observable:sizeInBytes": lit(
                        "xsd:integer", path.stat().st_size),
                },
                raster,
                {
                    "@id": uid(f"{label}-hash-facet"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [{
                        "@id": uid(f"{label}-sha256"),
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": lit("xsd:hexBinary",
                                                   sha256_of(path)),
                    }],
                },
            ],
        })
        g.append(rel(gid, report, "Contained_Within", tag="graphic",
                     desc="Figure published in the Talos report"))

    # ------------------------------------------------------------------
    # Threat actor + predecessor tooling
    # ------------------------------------------------------------------
    lotus = add_org(
        "actor-lotus-blossom", "Lotus Blossom",
        "Cyber-espionage threat actor active since at least 2012; attributed "
        "by Talos with high confidence via exclusive use of the Sagerunex "
        "backdoor, consistent victimology, and TTPs. UCO has no dedicated "
        "ThreatActor class, so the group is modeled as an Organization.",
        aliases=["Spring Dragon", "Billbug", "Thrip"])
    g.append(rel(lotus, investigation, "Subject_Of"))

    evora = uid("tool-evora")
    g.append({
        "@id": evora,
        "@type": "uco-tool:MaliciousTool",
        "uco-core:name": "Evora",
        "uco-tool:toolType": "backdoor",
        "uco-core:description": "Older Billbug RAT; Sagerunex is assessed to "
                                "be an evolution of Evora.",
    })
    htran = uid("tool-htran")
    g.append({
        "@id": htran,
        "@type": "uco-tool:Tool",
        "uco-core:name": "HTran",
        "uco-tool:toolType": "port relay / proxy",
        "uco-core:description": "Public TCP connection-bouncing tool; the "
                                "actor's 'mtrain V1.01' is a modified HTran.",
    })

    # ------------------------------------------------------------------
    # Victimology: targeted regions and sectors
    # ------------------------------------------------------------------
    regions = {
        "Philippines": "loc-ph", "Vietnam": "loc-vn",
        "Hong Kong": "loc-hk", "Taiwan": "loc-tw",
    }
    for name, label in regions.items():
        g.append({
            "@id": uid(label),
            "@type": "uco-location:Location",
            "uco-core:name": name,
            "uco-core:hasFacet": [{
                "@id": uid(f"{label}-facet"),
                "@type": "uco-location:SimpleAddressFacet",
                "uco-location:country": name,
            }],
        })
        g.append(rel(lotus, uid(label), "Related_To", tag="targeting",
                     desc="Targeted region (Talos 'Targeted countries' map)"))

    sectors = ["government", "manufacturing", "telecommunications", "media"]
    victim_role = uid("victim-sectors")
    g.append({
        "@id": victim_role,
        "@type": "uco-victim:VictimTargeting",
        "uco-core:name": "Targeted sectors",
        "uco-core:description": (
            "Lotus Blossom targeted organizations in the following sectors: "
            + ", ".join(sectors) + "."),
        "uco-core:tag": sectors,
    })
    g.append(rel(lotus, victim_role, "Related_To", tag="targeting"))

    # ------------------------------------------------------------------
    # Sagerunex family + variants
    # ------------------------------------------------------------------
    sagerunex = uid("malware-sagerunex")
    g.append({
        "@id": sagerunex,
        "@type": "uco-tool:MaliciousTool",
        "uco-core:name": "Sagerunex",
        "uco-tool:toolType": "backdoor / RAT",
        "uco-core:description": (
            "Backdoor family used exclusively by Lotus Blossom since at least "
            "2016; a DLL-injected, in-memory RAT assessed to be an evolution "
            "of Evora. Loader has two patterns (embedded-and-encrypted "
            "payload with custom decryption; and a 'servicemain' variant that "
            "only runs as a service). Code obfuscated with VMProtect. All "
            "variants: search a temp debug-log file, verify a config file, "
            "run time-check logic, pause via WaitForSingleObject (300000 ms), "
            "and support web-proxy autodiscovery plus hardcoded proxy "
            "credentials before beaconing."),
    })
    g.append(rel(sagerunex, lotus, "Used_By", desc="Exclusive-use backdoor"))
    g.append(rel(sagerunex, evora, "Related_To", desc="Assessed evolution of Evora"))
    g.append(rel(lotus, evora, "Used"))
    g.append(rel(lotus, htran, "Used"))

    def add_variant(label, name, interval, desc, c2_target=None):
        g.append({
            "@id": uid(label),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-core:hasFacet": [{
                "@id": uid(f"{label}-file-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": f"{name} (Sagerunex variant)",
                "uco-observable:extension": "dll",
                "uco-observable:observableCreatedTime": lit(
                    "xsd:dateTime", interval[0]),
            }],
        })
        g.append(rel(uid(label), sagerunex, "Related_To",
                     desc="Member of the Sagerunex family"))
        g.append(rel(lotus, uid(label), "Used"))
        return uid(label)

    beta = add_variant(
        "variant-beta", "Sagerunex Beta version",
        ("2016-01-01T00:00:00Z", "2021-12-31T23:59:59Z"),
        "Beta variant with verbose debug strings (e.g. 'Online Fail! Wait "
        "for %d mins'); gathers hostname, MAC, and IP, queries public IP via "
        "api.ipaddress[.]com, encrypts and sends to a traditional VPS C2. "
        "Commands: host status, update config, cmd shell, read file, create "
        "file. Active ~2016-2021 (Talos timeline).")
    original = add_variant(
        "variant-original", "Sagerunex original version",
        ("2016-01-01T00:00:00Z", "2021-12-31T23:59:59Z"),
        "Original variant previously documented by other vendors; same code "
        "flow as the Beta version but with terse '0x00'-prefixed debug "
        "strings. Uses traditional VPS C2. Active ~2016-2021.")
    dropbox_var = add_variant(
        "variant-dropbox-twitter", "Sagerunex Dropbox/Twitter version",
        ("2018-01-01T00:00:00Z", "2022-12-31T23:59:59Z"),
        "Variant that tunnels C2 through the Dropbox and Twitter (X) APIs. "
        "Beacon response-ID logic: id<16 re-beacon; 16-32 collect host info "
        "and run paired commands; ==39 fetch queued data. Config embeds "
        "Dropbox tokens and Twitter ConsumerKey/ConsumerSecret/AccessToken/"
        "AccessTokenSecret/ScreenName. Predominantly active 2018-2022 and "
        "possibly still active.")
    zimbra_var = add_variant(
        "variant-zimbra", "Sagerunex Zimbra version",
        ("2019-01-01T00:00:00Z", "2024-12-31T23:59:59Z"),
        "Variant that uses the Zimbra open-source webmail API as its C2 "
        "channel: logs in for an auth token, saves encrypted host info as "
        "mail_report.rar attached to a Drafts-folder message (beacon/exfil), "
        "reads operator commands from mailbox content, and writes command "
        "results as mail_report.rar into the Trash folder. Active since 2019.")

    vmprotect = uid("tool-vmprotect")
    g.append({
        "@id": vmprotect,
        "@type": "uco-tool:Tool",
        "uco-core:name": "VMProtect",
        "uco-tool:toolType": "software protection / packer",
        "uco-core:description": "Commercial software-protection tool the actor "
                                "used to obfuscate Sagerunex against AV.",
    })
    g.append(rel(sagerunex, vmprotect, "Packed_By"))

    # Debug-log temp filenames (graphic 09) as artifacts of the family.
    for tmp in ["TS_968T.tmp", "TS_F856.tmp", "DBGECD20.tmp", "VDM_LOMT.tmp"]:
        lbl = f"debuglog-{tmp}"
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": tmp,
            "uco-core:description": "Sagerunex debug-log temp file written in "
                                    "the temp folder (OCR approximate).",
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": tmp,
                "uco-observable:extension": "tmp",
            }],
        })
        g.append(rel(sagerunex, uid(lbl), "Created", tag="artifact"))

    # Attacker-machine host paths revealed in config.
    for i, p in enumerate(ATTACKER_HOST_PATHS):
        lbl = f"attacker-path-{i}"
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": p,
            "uco-core:description": "Original build path revealed in the "
                                    "Dropbox/Twitter Sagerunex config; likely "
                                    "from the actor's machine.",
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:filePath": p,
            }],
        })
        g.append(rel(dropbox_var, uid(lbl), "Related_To", tag="attacker-artifact"))

    # ------------------------------------------------------------------
    # Post-compromise toolkit
    # ------------------------------------------------------------------
    def add_tool(label, name, tooltype, desc, malicious=True,
                 tool_hash=None, hash_method="SHA256"):
        node = {
            "@id": uid(label),
            "@type": "uco-tool:MaliciousTool" if malicious else "uco-tool:Tool",
            "uco-core:name": name,
            "uco-tool:toolType": tooltype,
            "uco-core:description": desc,
        }
        g.append(node)
        g.append(rel(lotus, uid(label), "Used"))
        if tool_hash:
            hlbl = f"{label}-file"
            g.append({
                "@id": uid(hlbl),
                "@type": "uco-observable:ObservableObject",
                "uco-core:name": name,
                "uco-core:hasFacet": [{
                    "@id": uid(f"{hlbl}-hash"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [{
                        "@id": uid(f"{hlbl}-hashval"),
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": hash_method,
                        "uco-types:hashValue": lit("xsd:hexBinary", tool_hash),
                    }],
                }],
            })
            g.append(rel(uid(label), uid(hlbl), "Characterized_By"))
        return uid(label)

    cookie = add_tool(
        "tool-cookie-stealer", "Chrome cookie stealer", "credential theft",
        "PyInstaller bundle of an open-source Chrome cookie stealer "
        "(get_cookies_from_chrome); reads the Chrome 'Cookies' SQLite DB, "
        "decrypts values, and writes them to the temp file tmcok43.tmp.")
    venom = add_tool(
        "tool-venom", "Venom proxy tool", "proxy / tunneling",
        "Go-based proxy tool for penetration testers "
        "(github.com/Dliv3/Venom), customized by the actor with a hardcoded "
        "destination IP per activity; used to bridge isolated machines to "
        "internet-accessible systems.")
    adjpriv = add_tool(
        "tool-adjust-privilege", "Adjust privilege tool", "privilege escalation",
        "Retrieves another process's token to adjust privileges for a launch "
        "process (usage: 'pid image parameters').")
    archiver = add_tool(
        "tool-archiver", "Customized archiving tool", "collection / staging",
        "Customized compress-and-encrypt tool that steals files or entire "
        "folders to a specific path with protection (e.g. Chrome and Firefox "
        "cookie folders).")
    mtrain = add_tool(
        "tool-mtrain", "mtrain V1.01", "port relay",
        "Modified HTran port-relay tool ('MTrain V1.01') that relays the "
        "victim connection out to the internet (modes -l/-t/-s). Sample "
        "filename in the Talos screenshot embeds a SHA-1: "
        "mtrain.exe_f2370de517a032a27fcf3ba175e611a1b1a2b0ba.",
        tool_hash="f2370de517a032a27fcf3ba175e611a1b1a2b0ba",
        hash_method="SHA1")
    rar = add_tool(
        "tool-rar", "RAR", "archiving", "Archive manager used to archive/zip "
        "files for exfiltration.", malicious=False)
    impacket = add_tool(
        "tool-impacket", "Impacket", "remote execution / lateral movement",
        "Used to execute remote processes and commands in the victim "
        "environment (lateral movement).", malicious=False)
    g.append(rel(mtrain, htran, "Related_To", desc="Modified from HTran"))

    # ------------------------------------------------------------------
    # Registry-based persistence (WindowsRegistryKey + WindowsService)
    # UCO registry coverage is sufficient for this data — no change proposal.
    # ------------------------------------------------------------------
    persistence_action = uid("action-persistence")
    service_ids: dict[str, str] = {}
    dll_ids: dict[str, str] = {}
    dll_family_linked: set[str] = set()

    def dll_observable(path: str) -> str:
        lbl = "dll-" + path.replace("\\", "-").replace(":", "").replace(" ", "")
        if lbl in dll_ids:
            return dll_ids[lbl]
        dll_ids[lbl] = uid(lbl)
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": path,
            "uco-core:description": "Sagerunex service DLL dropped on the "
                                    "victim and registered as a service DLL.",
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:FileFacet",
                "uco-observable:filePath": path,
                "uco-observable:fileName": path.rsplit("\\", 1)[-1],
                "uco-observable:extension": "dll",
            }],
        })
        return uid(lbl)

    for svc in {r[0] for r in REGISTRY_PERSISTENCE}:
        lbl = f"service-{svc}"
        service_ids[svc] = uid(lbl)
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": f"{svc} (hijacked service)",
            "uco-core:description": (
                f"Windows service '{svc}' abused for Sagerunex persistence; "
                "Start=2 configures automatic start (svchost service DLL "
                "loading)."),
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:WindowsServiceFacet",
                "uco-observable:serviceName": svc,
                "uco-observable:startType": "service_auto_start",
                "uco-observable:serviceType": "service_win32_share_process",
            }],
        })
        g.append(rel(uid(lbl), investigation, "part_of"))

    for i, (svc, key, values) in enumerate(REGISTRY_PERSISTENCE):
        lbl = f"regkey-{i}"
        reg_values = []
        for j, (vname, vtype, vdata) in enumerate(values):
            reg_values.append({
                "@id": uid(f"{lbl}-val-{j}"),
                "@type": "uco-observable:WindowsRegistryValue",
                "uco-core:name": vname,
                "uco-observable:data": vdata,
                "uco-observable:dataType": vtype,
            })
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:WindowsRegistryKey",
            "uco-core:name": key,
            "uco-core:description": (
                "Registry key written via 'reg add' to install/verify the "
                "Sagerunex backdoor as a service DLL."),
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:WindowsRegistryKeyFacet",
                "uco-observable:key": key,
                "uco-observable:registryValues": reg_values,
            }],
        })
        g.append(rel(uid(lbl), service_ids[svc], "Related_To", tag="persistence",
                     desc="Registry key configuring this service"))
        # Link ServiceDll values to the DLL file observables.
        for (vname, vtype, vdata) in values:
            if vname == "ServiceDll":
                d = dll_observable(vdata)
                g.append(rel(uid(lbl), d, "Related_To", tag="persistence",
                             desc="ServiceDll value points to this DLL"))
                # A single DLL path (e.g. c:\windows\swprv.dll) is reused across
                # more than one hijacked service, so guard the DLL->family edge
                # to avoid emitting a duplicate relationship @id.
                if d not in dll_family_linked:
                    dll_family_linked.add(d)
                    g.append(rel(d, sagerunex, "Related_To",
                                 desc="Service DLL is a Sagerunex payload"))

    reg_key_ids = [uid(f"regkey-{i}") for i in range(len(REGISTRY_PERSISTENCE))]
    g.append({
        "@id": persistence_action,
        "@type": "uco-action:Action",
        "uco-core:name": "Install Sagerunex as a service via the registry",
        "uco-core:description": (
            "Lotus Blossom ran 'reg add' commands to create ServiceDll and "
            "Start values under HKLM\\SYSTEM\\CurrentControlSet\\Services for "
            "tapisrv, swprv, and appmgmt, then 'reg query' to verify the "
            "backdoor runs as a service. This Action is additionally typed "
            "with the MITRE ATT&CK technique classes T1543.003 (Windows "
            "Service) and T1112 (Modify Registry) via the uco-action:Technique "
            "metaclass (ucoProject/UCO#676)."),
        "uco-action:performer": {"@id": lotus},
        "uco-action:object": [{"@id": rk} for rk in reg_key_ids],
        "uco-action:result": [{"@id": sid} for sid in service_ids.values()],
    })
    g.append(rel(persistence_action, investigation, "part_of"))

    # ------------------------------------------------------------------
    # Discovery + lateral movement + exfiltration actions
    # ------------------------------------------------------------------
    discovery = uid("action-discovery")
    g.append({
        "@id": discovery,
        "@type": "uco-action:Action",
        "uco-core:name": "Host and network discovery",
        "uco-core:description": (
            "Actor ran net, tasklist, quser, ipconfig, netstat, and dir to "
            "enumerate user accounts, directories, processes, and network "
            "configuration; assessed internet reachability and, when "
            "restricted, used the target proxy or the Venom tool. Tools were "
            "frequently staged in the world-readable public\\pictures folder."),
        "uco-action:performer": {"@id": lotus},
        "uco-action:instrument": [{"@id": venom}],
    })
    lateral = uid("action-lateral")
    g.append({
        "@id": lateral,
        "@type": "uco-action:Action",
        "uco-core:name": "Lateral movement via WMI/Impacket",
        "uco-core:description": (
            "Actor used Impacket (and WMI, per the attack-chain diagram) to "
            "execute remote processes and commands and move laterally across "
            "the internal network toward a data-exfiltrating host."),
        "uco-action:performer": {"@id": lotus},
        "uco-action:instrument": [{"@id": impacket}],
    })
    for a in (discovery, lateral):
        g.append(rel(a, investigation, "part_of"))

    # ------------------------------------------------------------------
    # C2 infrastructure
    # ------------------------------------------------------------------
    def ip_observable(ip: str, desc: str) -> str:
        lbl = "ip-" + ip.replace(".", "-")
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": ip,
            "uco-core:description": desc,
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:IPv4AddressFacet",
                "uco-observable:addressValue": ip,
            }],
        })
        return uid(lbl)

    for ip in LEGACY_C2_IPS:
        c2 = ip_observable(ip, "Legacy VPS command-and-control server from the "
                               "Beta/original Sagerunex config (graphic 11).")
        # These IPs were recovered only from the Beta/original config hexdump.
        # Per Talos, the later cloud variants (Dropbox/Twitter, Zimbra) moved
        # off the traditional VPS C2 entirely, so the VPS IPs attach to the
        # Beta and original variants only — not the Dropbox/Twitter variant.
        g.append(rel(beta, c2, "Connected_To", tag="c2",
                     desc="Traditional VPS C2 (Beta variant)"))
        g.append(rel(original, c2, "Connected_To", tag="c2",
                     desc="Traditional VPS C2 (original variant)"))

    proxy = ip_observable(
        "192.168.240.18",
        "Hardcoded victim HTTP proxy (192.168.240.18:8080) with proxy "
        "username/password embedded in the Sagerunex config (graphic 11).")
    g.append(rel(beta, proxy, "Connected_To", tag="proxy"))

    public_ip_svc = uid("svc-ipaddress-com")
    g.append({
        "@id": public_ip_svc,
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "api.ipaddress[.]com",
        "uco-core:description": "Public-IP lookup service queried by the Beta "
                                "variant to learn the victim's external IP.",
        "uco-core:hasFacet": [{
            "@id": uid("svc-ipaddress-com-facet"),
            "@type": "uco-observable:DomainNameFacet",
            "uco-observable:value": "api.ipaddress.com",
        }],
    })
    g.append(rel(beta, public_ip_svc, "Connected_To", tag="recon"))

    # Third-party cloud C2 channels
    cloud_c2 = {
        "c2-dropbox": ("Dropbox", "dropbox.com",
                       "Dropbox API used as a C2 tunnel; config embeds Dropbox "
                       "tokens. File listing spans 2018-07..2022-06 (graphic 17)."),
        "c2-twitter": ("Twitter / X", "twitter.com",
                       "Twitter (X) API used as a C2 tunnel; config embeds "
                       "ConsumerKey/ConsumerSecret/AccessToken/"
                       "AccessTokenSecret/ScreenName."),
        "c2-zimbra": ("Zimbra webmail", "netvigator.com",
                      "Zimbra webmail (observed netvigator.com mailboxes) used "
                      "as a C2 channel; host info and command results saved as "
                      "mail_report.rar in Drafts and Trash folders."),
    }
    cloud_ids = {}
    for lbl, (name, domain, desc) in cloud_c2.items():
        cloud_ids[lbl] = uid(lbl)
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-core:hasFacet": [{
                "@id": uid(f"{lbl}-facet"),
                "@type": "uco-observable:DomainNameFacet",
                "uco-observable:value": domain,
            }],
        })
    g.append(rel(dropbox_var, cloud_ids["c2-dropbox"], "Connected_To", tag="c2"))
    g.append(rel(dropbox_var, cloud_ids["c2-twitter"], "Connected_To", tag="c2"))
    g.append(rel(zimbra_var, cloud_ids["c2-zimbra"], "Connected_To", tag="c2"))

    # mail_report.rar exfil artifact
    mailrar = uid("artifact-mail-report-rar")
    g.append({
        "@id": mailrar,
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "mail_report.rar",
        "uco-core:description": "Encrypted RAR of collected host information "
                                "attached to Zimbra draft (beacon/exfil) and "
                                "trash (command result) messages.",
        "uco-core:hasFacet": [{
            "@id": uid("artifact-mail-report-rar-facet"),
            "@type": "uco-observable:FileFacet",
            "uco-observable:fileName": "mail_report.rar",
            "uco-observable:extension": "rar",
        }],
    })
    g.append(rel(zimbra_var, mailrar, "Created", tag="exfil"))
    g.append(rel(mailrar, cloud_ids["c2-zimbra"], "Uploaded_To", tag="exfil"))

    exfil = uid("action-exfil")
    g.append({
        "@id": exfil,
        "@type": "uco-action:Action",
        "uco-core:name": "Collection and exfiltration over third-party cloud",
        "uco-core:description": (
            "Sagerunex collects host information, encrypts/archives it, and "
            "exfiltrates over Dropbox, Twitter/X, or Zimbra webmail to evade "
            "detection by blending with legitimate cloud traffic."),
        "uco-action:performer": {"@id": lotus},
        "uco-action:instrument": [{"@id": archiver}, {"@id": rar}],
        "uco-action:object": [{"@id": zimbra_var}, {"@id": dropbox_var}],
        "uco-action:result": [{"@id": mailrar}],
    })
    g.append(rel(exfil, investigation, "part_of"))

    # ------------------------------------------------------------------
    # MITRE ATT&CK techniques (uco-action:Technique metaclass, UCO #676)
    #
    # ucoProject/UCO PR #676 (Feature-Issue-666) models uco-action:Technique
    # as a *metaclass* anchored by the new top-level uco-core:UcoType: "A
    # Technique instance is an owl:Class that is a subclass of
    # uco-action:Action." So each MITRE ATT&CK technique is itself an
    # owl:Class (subclass of Action) carrying uco-action:techniqueID, and a
    # concrete action that exhibits the technique is an *instance* of that
    # technique class. The technique classes are declared in
    # extensions/attack-technique/mitre-attack-catalog.ttl (canonical ATT&CK
    # IRIs); here we type each behavior Action with the technique class(es) it
    # exhibits — the faithful punning pattern, not a flat property carrier.
    #
    # The Talos prose lists no technique IDs; the mappings are from the MITRE
    # ATT&CK group page for Lotus Blossom (G0030) and Sagerunex (S1156).
    # ------------------------------------------------------------------
    def attack(tid: str) -> str:
        return f"https://attack.mitre.org/techniques/{tid}"

    def exhibit(action_id: str, tids: list[str]) -> None:
        """Add ATT&CK technique class IRIs to an existing Action's @type.

        Typing an Action instance with a technique class asserts the action is
        an instance of that class, which UCO #676 declares to be a subclass of
        uco-action:Action — the intended metaclass/punning representation.
        """
        for node in g:
            if node.get("@id") == action_id:
                cur = node["@type"]
                types = [cur] if isinstance(cur, str) else list(cur)
                for tid in tids:
                    iri = attack(tid)
                    if iri not in types:
                        types.append(iri)
                node["@type"] = types
                return
        raise KeyError(action_id)

    # Techniques exhibited by the four narrative behavior Actions.
    exhibit(persistence_action, ["T1543.003", "T1112"])
    exhibit(discovery, ["T1016"])
    exhibit(lateral, ["T1047"])
    exhibit(exfil, ["T1560.001", "T1041", "T1102.002"])

    # Behavior Actions for techniques without an existing narrative node. Each
    # is an instance of its ATT&CK technique class (hence an Action).
    extra_actions = [
        ("action-inject", "DLL injection of the Sagerunex backdoor",
         ["T1055.001"],
         "The Sagerunex loader injects the backdoor DLL into memory instead "
         "of running it from disk.", {"instrument": [sagerunex]}),
        ("action-obfuscate", "Obfuscate Sagerunex with VMProtect",
         ["T1027.002"],
         "The actor packs/obfuscates Sagerunex with VMProtect to hinder "
         "analysis and evade antivirus.",
         {"instrument": [vmprotect], "object": [sagerunex]}),
        ("action-proxy", "Internal proxying to reach the internet",
         ["T1090.001"],
         "The Venom proxy tool and the 'mtrain V1.01' HTran-derived port "
         "relay bridge isolated victim machines out to internet-accessible "
         "systems.", {"instrument": [venom, mtrain]}),
        ("action-webc2", "Command and control over web protocols",
         ["T1071.001"],
         "Sagerunex communicates with its C2 over HTTP/HTTPS web protocols.",
         {"instrument": [sagerunex]}),
        ("action-cookie-theft", "Steal Chrome session cookies", ["T1539"],
         "A Chrome cookie stealer reads and decrypts the Chrome 'Cookies' "
         "SQLite database to steal web session cookies.",
         {"instrument": [cookie]}),
    ]
    for lbl, name, tids, desc, links in extra_actions:
        node = {
            "@id": uid(lbl),
            "@type": ["uco-action:Action"] + [attack(t) for t in tids],
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-action:performer": {"@id": lotus},
        }
        if "instrument" in links:
            node["uco-action:instrument"] = [{"@id": x}
                                             for x in links["instrument"]]
        if "object" in links:
            node["uco-action:object"] = [{"@id": x} for x in links["object"]]
        g.append(node)
        g.append(rel(uid(lbl), investigation, "part_of"))

    # ------------------------------------------------------------------
    # Campaign codes (IOCs)
    # ------------------------------------------------------------------
    for code in CAMPAIGN_CODES:
        lbl = f"campaign-{code}"
        g.append({
            "@id": uid(lbl),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": code,
            "uco-core:description": "Lotus Blossom campaign code (Talos IOCs).",
        })
        g.append(rel(uid(lbl), lotus, "Related_To", tag="ioc"))

    # ------------------------------------------------------------------
    # Detection coverage
    # ------------------------------------------------------------------
    detection = uid("action-detection")
    g.append({
        "@id": detection,
        "@type": "uco-action:Action",
        "uco-core:name": "Cisco detection coverage",
        "uco-core:description": (
            "Talos-published detection: Snort SIDs " + ", ".join(SNORT_SIDS)
            + "; ClamAV signatures " + ", ".join(CLAMAV_SIGS)
            + ". Cisco Secure Endpoint/Email/Firewall/Malware Analytics, "
            "Umbrella, and Secure Web Appliance provide coverage."),
        "uco-action:performer": {"@id": talos},
        "uco-action:object": [{"@id": sagerunex}],
    })
    g.append(rel(detection, investigation, "part_of"))

    # Wire principal artifacts and actors into the investigation.
    for node in (sagerunex, beta, original, dropbox_var, zimbra_var,
                 cookie, venom, adjpriv, archiver, mtrain, rar, impacket):
        g.append(rel(node, investigation, "part_of"))

    return {
        "@context": {
            "kb": NS,
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "uco-victim": "https://ontology.unifiedcyberontology.org/uco/victim/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": g,
    }


def validate(path: Path) -> int:
    if not validator_available():
        print("case_validate not installed; skipping validation", file=sys.stderr)
        return 0
    report = validate_graph_file(
        path, project_root=ROOT, extensions=["attack-technique:full"])
    print(report.safe_summary)
    if report.undeclared_concepts:
        print("Undeclared concepts:", ", ".join(report.undeclared_concepts))
        print(report.concept_guidance)
    return 0 if report.conforms else 1


def main() -> int:
    payload = build_graph()
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Graph nodes: {len(payload['@graph'])}")
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
