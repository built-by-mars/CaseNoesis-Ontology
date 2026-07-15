#!/usr/bin/env python3
"""Build a CASE/UCO graph for the Prevailion DarkWatchman CTI report.

Source: Matt Stafford & Sherman Smith, "DarkWatchman: A new evolution in
fileless techniques," Prevailion PACT, 2021-12-14.
  https://www.prevailion.com/darkwatchman-new-fileless-techniques/
  Wayback: https://web.archive.org/web/20220629230035/...

CASEGraph public-graph exemplar (critic serializer_mode=casegraph_raw):
uses create_relationship/add_type/write_streaming with upsert_node property
maps (not generated-dataclass create() throughout). Preserves epistemology:

* Unattributed activity → uco-core:Grouping + Annotation (not Organization)
* Observed vs capability vs hypothesis are separated
* Contained_Within kept even without published digests
* VT submission times are Events, not FileFacet.observableCreatedTime
* Builder/recipe hashes live in build-manifest.json, not the domain graph
* ATT&CK punning via add_type + mapping-provenance Annotations

Companion to docs/recipes/cyber-threat-intelligence.md.
"""

from __future__ import annotations

import hashlib
import json
import struct
import uuid
from pathlib import Path

from case_uco import CASEGraph
from case_uco.validation import validate_graph_file, validator_available

ROOT = Path(__file__).resolve().parents[3]

CASE_ID = "darkwatchman-prevailion-2021"
NS = f"https://example.org/cti/{CASE_ID}/"
HERE = Path(__file__).resolve().parent
GRAPHICS_DIR = HERE / "graphics"
OUTPUT = HERE / "darkwatchman-prevailion.jsonld"
MANIFEST = HERE / "build-manifest.json"

REPORT_URL = "https://www.prevailion.com/darkwatchman-new-fileless-techniques/"
REPORT_WAYBACK = (
    "https://web.archive.org/web/20220629230035/"
    "https://www.prevailion.com/darkwatchman-new-fileless-techniques/"
)
REPORT_PUBLISHED = "2021-12-14T12:00:00Z"
JS_RAT_SHA256 = (
    "ee9cd9a5ac70f7b55b52c02f54fd53186c294a940b2502bbe427d847dde83c85"
)


def uid(label: str) -> str:
    return f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'{CASE_ID}:{label}')}"


def lit(dtype: str, value) -> dict:
    val = str(value).lower() if isinstance(value, bool) else str(value)
    return {"@type": dtype, "@value": val}


def rel(source: str, target: str, kind: str, *, tag: str | None = None,
        desc: str | None = None, assertion: str | None = None) -> dict:
    aid = assertion or f"rel-{source}-{target}-{kind}-{tag or 'none'}"
    node = {
        "@id": uid(aid),
        "@type": "uco-core:Relationship",
        "uco-core:source": [{"@id": source}],
        "uco-core:target": [{"@id": target}],
        "uco-core:kindOfRelationship": kind,
        "uco-core:isDirectional": lit("xsd:boolean", True),
    }
    if tag:
        node["uco-core:tag"] = tag
    if desc:
        node["uco-core:description"] = desc
    return node


def image_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    return None


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


GRAPHICS: list[tuple[str, str]] = [
    ("01-figure-1.png",
     "Figure 1 — spoofed email headers: From/Reply-To/Return-Path "
     "mail@ponyexpress.ru; Date 2021-11-15 06:18:39 +0300."),
    ("02-figure-2.png",
     "Figure 2 — true sender: Hop 1 rentbikespb.ru / 45.156.27.245 blacklisted."),
    ("03-figure-3.png",
     "Figure 3 — Relay Information: rentbikespb.ru → jino.ru ESMTPS "
     "2021-11-15 03:48:51 UTC."),
    ("04-figure-4.png",
     "Figure 4 — Outlook Pony Express lure with ZIP attachment "
     "Накладная №12-6317-3621.zip (ANY.RUN)."),
    ("05-figure-5.png",
     "Figure 5 — Forum victim post: NOD blocked bfdb1290.top / 91.208.206.44."),
    ("06-figure-6.png",
     "Figure 6 — Forum reply: attachment was a hidden-extension .exe."),
    ("07-figure-7.png",
     "Figure 7 — Forum reply: payload found in registry, would not uninstall."),
    ("08-figure-8.png",
     "Figure 8 — WinRAR SFX contains 134121811.js and 2204722946; "
     "Setup=134121811.js \"%sfxname%\", Path=%TEMP%."),
    ("09-figure-12-scheduled-task.png",
     "Figure 12 — Task Scheduler: GUID task 26b799fa-… at logon of "
     "DESKTOP-JGLLJLD\\admin."),
    ("10-figure-19-keylogger-powershell.png",
     "Figure 19 — Base64 PowerShell decode of registry-stored C# keylogger."),
]

SAMPLES: list[tuple[str, str, str]] = [
    ("409839f9c8327eff6208aeca4f7113f5a0abdfa97f266f404b14f9fa6ab1432f",
     "Накладная №12-6317-3621.exe", "2021-11-12T12:31:12Z"),
    ("27c4e9f01e5142a021329163b074f0692a9b4e832e0b53a5e31d364fdbbcdef8",
     "Накладная №12-6317-3621.zip", "2021-11-12T20:49:52Z"),
    ("74c85df7a1f1af78fde252e52d0bfbdec75a626f613f080bd3ca8e3feee34ce5",
     "RAR SFX shell [0]", "2021-11-15T01:28:57Z"),
    ("671ede00b5be118bab9238386fd3f7502ffa21f678d8f509b181d4a819524525",
     "Уведомление об окончании срока бесплатного хранения.msg",
     "2021-11-15T05:28:07Z"),
]

# Seeded DGA list from Figure 17 / code. Only a subset is observed live.
DGA_SEEDS = [
    "bfdb1290.top", "a3698d83.top", "3a60dc39.top", "4d67ecaf.top",
    "d303790c.top", "a404499a.top", "3d0d1820.top", "4a0a28b6.top",
    "dab53527.top", "adb205b1.top",
]
OBSERVED_C2 = {
    "bfdb1290.top": "91.208.206.44",
    "a3698d83.top": "185.177.59.174",
    "3a60dc39.top": "185.177.59.174",
}

# Observed / schema registry entries. Omit b and r (never set).
REG_OBSERVED = [
    ("0", "1", "Installation flag (observed value 1 = installed)"),
    ("1", None, "Base64 PowerShell that compiles/runs the C# keylogger "
     "(content not reproduced; stored under <uid>1)"),
    ("a", None, "Keylogger buffer (keystrokes + clipboard)"),
    ("c", None, "Current C2 server domain for the day"),
    ("h", None, "clear_browsers_history flag"),
    ("j", None, "JavaScript snippet to evaluate"),
    ("m", None, "Keylogger mutex"),
    ("p", None, "collect_user_profile flag"),
    ("s", None, "Stop keylogger flag"),
    ("t", None, "Reconnect timeout"),
    ("v", None, "Autorun JavaScript snippet storage"),
    ("z", None, "Stop RAT flag"),
]


def build_graph() -> CASEGraph:
    graph = CASEGraph()

    def add(node: dict) -> str:
        nid = node["@id"]
        types = node.pop("@type")
        node.pop("@id", None)
        graph.upsert_node(nid, types=types, properties=node)
        return nid

    def link(source: str, target: str, kind: str, *, tag: str | None = None,
             desc: str | None = None, assertion: str | None = None) -> str:
        props = {}
        if tag:
            props["uco-core:tag"] = tag
        rel = graph.create_relationship(
            source, target, kind,
            assertion_id=uid(assertion or f"rel-{source}-{target}-{kind}-{tag or 'none'}"),
            description=desc,
            properties=props or None,
        )
        return rel["@id"]

    def refs(ids: list[str]) -> list[dict[str, str]]:
        return [{"@id": item} for item in dict.fromkeys(ids)]

    def report_reference(context: str) -> dict:
        # Full-context UUIDv5 avoids collisions when long section locators share a prefix.
        return {
            "@id": uid(f"ref:{context}"),
            "@type": "uco-core:ExternalReference",
            "uco-core:referenceURL": lit("xsd:anyURI", REPORT_WAYBACK),
            "uco-core:definingContext": context,
        }

    def mitre_reference(tid: str) -> dict:
        url = f"https://attack.mitre.org/techniques/{tid}"
        return {
            "@id": uid(f"ref:mitre-attack:{tid}"),
            "@type": "uco-core:ExternalReference",
            "uco-core:referenceURL": lit("xsd:anyURI", url),
            "uco-core:definingContext": (
                f"MITRE ATT&CK technique {tid} "
                "(mapping enrichment; ATT&CK release pinned by attack-technique catalog)"
            ),
        }

    attack_mapping_ids: list[str] = []

    def compilation(label: str, name: str, desc: str, members: list[str],
                    *, kind: str = "uco-core:ContextualCompilation") -> str:
        return add({
            "@id": uid(label),
            "@type": kind,
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-core:object": refs(members),
        })

    def analytic(label: str, statement: str, *, confidence_tag: str | None,
                 tags: list[str], about: list[str], source_ctx: str) -> str:
        all_tags = list(tags)
        if confidence_tag:
            all_tags.append(confidence_tag)
        return add({
            "@id": uid(label),
            "@type": "uco-core:Annotation",
            "uco-core:name": label.replace("-", " "),
            "uco-core:description": statement,
            "uco-core:statement": statement,
            "uco-core:tag": all_tags,
            "uco-core:object": refs(about),
            "uco-core:externalReference": [report_reference(source_ctx)],
        })

    def annotation(label: str, statement: str, about: list[str],
                   tags: list[str] | None = None,
                   source_ctx: str = "Prevailion DarkWatchman report") -> str:
        node = {
            "@id": uid(label),
            "@type": "uco-core:Annotation",
            "uco-core:name": label.replace("-", " "),
            "uco-core:statement": statement,
            "uco-core:description": statement,
            "uco-core:object": refs(about),
            "uco-core:externalReference": [report_reference(source_ctx)],
        }
        if tags:
            node["uco-core:tag"] = tags
        return add(node)

    # ------------------------------------------------------------------
    # Source material
    # ------------------------------------------------------------------
    prevailion = add({
        "@id": uid("org-prevailion"),
        "@type": "uco-identity:Organization",
        "uco-core:name": "Prevailion",
        "uco-core:description": "Publisher; Adversarial Counterintelligence Team (PACT).",
    })
    author_matt = add({
        "@id": uid("person-matt-stafford"),
        "@type": "uco-identity:Person",
        "uco-core:name": "Matt Stafford",
        "uco-core:description": "Prevailion PACT analyst; co-author.",
    })
    author_sherman = add({
        "@id": uid("person-sherman-smith"),
        "@type": "uco-identity:Person",
        "uco-core:name": "Sherman Smith",
        "uco-core:description": "Prevailion PACT analyst; co-author.",
    })
    report = add({
        "@id": uid("report"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "DarkWatchman: A new evolution in fileless techniques.",
        "uco-core:description": (
            f"Prevailion PACT blog post published {REPORT_PUBLISHED[:10]}. "
            f"Live URL {REPORT_URL}; archival capture {REPORT_WAYBACK}. "
            "Authors: Matt Stafford and Sherman Smith. Attribution of the "
            "operators was not possible per the report's closing analysis."
        ),
        "uco-core:hasFacet": [{
            "@id": uid("report-url-facet"),
            "@type": "uco-observable:URLFacet",
            "uco-observable:fullValue": REPORT_URL,
        }],
        "uco-core:externalReference": [{
            "@id": uid("report-wayback-ref"),
            "@type": "uco-core:ExternalReference",
            "uco-core:referenceURL": lit("xsd:anyURI", REPORT_WAYBACK),
            "uco-core:definingContext": "Internet Archive Wayback Machine capture",
        }],
    })
    ann_authorship = annotation(
        "ann-authorship",
        "Report authored by Matt Stafford and Sherman Smith; published by Prevailion PACT.",
        [report, author_matt, author_sherman, prevailion],
        tags=["provenance:publication"],
    )

    graphic_ids = []
    for fname, desc in GRAPHICS:
        path = GRAPHICS_DIR / fname
        if not path.exists():
            raise FileNotFoundError(path)
        label = f"graphic-{fname}"
        gid = uid(label)
        graphic_ids.append(gid)
        raster: dict = {
            "@id": uid(f"{label}-raster"),
            "@type": "uco-observable:RasterPictureFacet",
            "uco-observable:imageCompressionMethod": "PNG",
        }
        dims = image_dimensions(path)
        if dims:
            raster["uco-observable:pictureWidth"] = lit("xsd:integer", dims[0])
            raster["uco-observable:pictureHeight"] = lit("xsd:integer", dims[1])
        add({
            "@id": gid,
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": fname,
            "uco-core:description": desc,
            "uco-core:hasFacet": [
                {
                    "@id": uid(f"{label}-file"),
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": fname,
                    "uco-observable:extension": "png",
                    "uco-observable:sizeInBytes": lit(
                        "xsd:integer", path.stat().st_size),
                },
                raster,
                {
                    "@id": uid(f"{label}-hash"),
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [{
                        "@id": uid(f"{label}-sha256"),
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": lit(
                            "xsd:hexBinary", sha256_of(path)),
                    }],
                },
            ],
        })
        link(gid, report, "Contained_Within", tag="graphic")

    # ------------------------------------------------------------------
    # Unattributed activity cluster (NOT an Organization)
    # ------------------------------------------------------------------
    cluster = add({
        "@id": uid("grouping-darkwatchman-activity"),
        "@type": "uco-core:Grouping",
        "uco-core:name": "DarkWatchman activity cluster",
        "uco-core:context": [
            "Unattributed DarkWatchman activity analyzed by Prevailion PACT. "
            "Local analytic grouping — not a named attributed organization."
        ],
        "uco-core:description": (
            "Activity cluster for DarkWatchman reporting. PACT stated "
            "attribution was not possible. Do not treat this Grouping as an "
            "action performer."
        ),
        "uco-core:tag": ["epistemic:unattributed", "activity-cluster"],
    })

    # ------------------------------------------------------------------
    # Malware family + file instances
    # ------------------------------------------------------------------
    dw_family = add({
        "@id": uid("malware-darkwatchman"),
        "@type": "uco-tool:MaliciousTool",
        "uco-core:name": "DarkWatchman",
        "uco-tool:toolType": "fileless JavaScript RAT + C# keylogger",
        "uco-core:description": (
            "JavaScript RAT (~32 KB) with C# keylogger (~8.5 KB compiled) "
            "storing state under HKCU\\Software\\Microsoft\\Windows\\DWM\\, "
            "DGA C2 (.top / Netlab360 tordwm), remote update, LOLbins."
        ),
        "uco-core:tag": ["malware-family"],
    })

    def file_obs(label: str, name: str, desc: str, *,
                 path: str | None = None, size: int | None = None,
                 digest: str | None = None, ext: str | None = None) -> str:
        facets: list[dict] = [{
            "@id": uid(f"{label}-file"),
            "@type": "uco-observable:FileFacet",
            "uco-observable:fileName": name,
        }]
        if path:
            facets[0]["uco-observable:filePath"] = path
        if ext:
            facets[0]["uco-observable:extension"] = ext
        if size is not None:
            facets[0]["uco-observable:sizeInBytes"] = lit("xsd:integer", size)
        if digest:
            facets.append({
                "@id": uid(f"{label}-hash"),
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:hash": [{
                    "@id": uid(f"{label}-sha256"),
                    "@type": "uco-types:Hash",
                    "uco-types:hashMethod": "SHA256",
                    "uco-types:hashValue": lit("xsd:hexBinary", digest),
                }],
            })
        return add({
            "@id": uid(label),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-core:hasFacet": facets,
        })

    js_temp = file_obs(
        "file-js-temp", "134121811.js",
        "JS RAT instance dropped to %TEMP% by the WinRAR SFX (Figure 8).",
        path=r"%TEMP%\134121811.js", size=32641, digest=JS_RAT_SHA256, ext="js")
    js_installed = file_obs(
        "file-js-localappdata", "<uid>0.js",
        "Installed JS RAT path under %%LOCALAPPDATA%%\\<uid>0.js after move "
        "(Shell.NameSpace(28)). Same content hash as 134121811.js.",
        path=r"%LOCALAPPDATA%\<uid>0.js", size=32641, digest=JS_RAT_SHA256,
        ext="js")
    # Distinct filesystem instances of the same JS content; linked by install
    # Action (object=TEMP, result=LocalAppData), not a Parent_Of edge.

    keylogger = file_obs(
        "file-keylogger-hex", "2204722946",
        "XOR-obfuscated keylogger hex inside the SFX. No standalone SHA-256 "
        "published in the report timeline; size 44424 bytes (Figure 8).",
        size=44424)
    graph.set_property(keylogger, "uco-core:tag", [
        "hash-status:not-published", "source-bytes:not-acquired",
        "epistemic:reported",
    ])

    # ------------------------------------------------------------------
    # Delivery chain
    # ------------------------------------------------------------------
    spoof_addr = add({
        "@id": uid("email-spoof-from"),
        "@type": "uco-observable:EmailAddress",
        "uco-core:name": "mail@ponyexpress.ru",
        "uco-core:hasFacet": [{
            "@id": uid("email-spoof-from-facet"),
            "@type": "uco-observable:EmailAddressFacet",
            "uco-observable:addressValue": "mail@ponyexpress.ru",
        }],
    })
    smtp_host = add({
        "@id": uid("domain-smtp-rentbikespb"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "smtp.rentbikespb.ru",
        "uco-core:description": "True SMTP host in Received header.",
        "uco-core:hasFacet": [{
            "@id": uid("domain-smtp-rentbikespb-facet"),
            "@type": "uco-observable:DomainNameFacet",
            "uco-observable:value": "smtp.rentbikespb.ru",
        }],
    })
    rentbike = add({
        "@id": uid("domain-rentbikespb"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "rentbikespb.ru",
        "uco-core:description": "Registrable true-sender domain; parked at mail.ru "
                                "outside brief operational window.",
        "uco-core:hasFacet": [{
            "@id": uid("domain-rentbikespb-facet"),
            "@type": "uco-observable:DomainNameFacet",
            "uco-observable:value": "rentbikespb.ru",
        }],
    })
    pony = add({
        "@id": uid("domain-ponyexpress"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "ponyexpress.ru",
        "uco-core:description": "Impersonated legitimate courier domain.",
        "uco-core:hasFacet": [{
            "@id": uid("domain-ponyexpress-facet"),
            "@type": "uco-observable:DomainNameFacet",
            "uco-observable:value": "ponyexpress.ru",
        }],
    })
    ip_send = add({
        "@id": uid("ip-45-156-27-245"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "45.156.27.245",
        "uco-core:description": "Operational SMTP sending IP for rentbikespb.ru.",
        "uco-core:hasFacet": [{
            "@id": uid("ip-45-156-27-245-facet"),
            "@type": "uco-observable:IPv4AddressFacet",
            "uco-observable:addressValue": "45.156.27.245",
        }],
    })
    ip_park = add({
        "@id": uid("ip-94-100-180-200"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "94.100.180.200",
        "uco-core:description": "mail.ru parking target for rentbikespb.ru "
                                "before/after operational use.",
        "uco-core:hasFacet": [{
            "@id": uid("ip-94-100-180-200-facet"),
            "@type": "uco-observable:IPv4AddressFacet",
            "uco-observable:addressValue": "94.100.180.200",
        }],
    })
    link(smtp_host, ip_send, "Resolved_To", tag="operational-mail",
                     desc="Campaign window resolution")
    link(rentbike, ip_park, "Resolved_To", tag="parking",
                     desc="Pre/post-operational parking at mail.ru")
    link(smtp_host, rentbike, "FQDN_Of",
                     desc="smtp host under rentbikespb.ru")

    email_msg = add({
        "@id": uid("email-lure"),
        "@type": "uco-observable:EmailMessage",
        "uco-core:name": "Уведомление об окончании срока бесплатного хранения",
        "uco-core:description": (
            "Spearphishing lure spoofed as PONY EXPRESS. True sender evidenced "
            "by Received-from smtp.rentbikespb.ru [45.156.27.245]."
        ),
        "uco-core:hasFacet": [{
            "@id": uid("email-lure-facet"),
            "@type": "uco-observable:EmailMessageFacet",
            "uco-observable:subject": (
                "Уведомление об окончании срока бесплатного хранения"),
            "uco-observable:sentTime": lit(
                "xsd:dateTime", "2021-11-15T06:18:39+03:00"),
            "uco-observable:from": {"@id": spoof_addr},
            "uco-observable:receivedLines": [
                "Received: from rentbikespb.ru (smtp.rentbikespb.ru "
                "[45.156.27.245])"
            ],
            "uco-observable:body": (
                "Machine-translated lure: free storage for consignment "
                "#12-6317-3621 expires 2021-11-16; attachment is a scanned "
                "consignment note; contact +7-495-937-77-77."
            ),
        }],
    })

    sample_ids: dict[str, str] = {}
    vt_event_ids: list[str] = []
    for digest, fname, when in SAMPLES:
        lbl = f"sample-{digest[:12]}"
        sample_ids[digest] = file_obs(
            lbl, fname,
            f"VirusTotal-linked sample from the Prevailion timeline "
            f"(submission Event at {when}).",
            digest=digest,
            ext=fname.rsplit(".", 1)[-1] if "." in fname else None,
        )
        vt_event_ids.append(add({
            "@id": uid(f"event-vt-{digest[:12]}"),
            "@type": "uco-core:Event",
            "uco-core:name": f"VirusTotal submission of {fname}",
            "uco-core:eventType": ["virus-total-submission", "first-observed"],
            "uco-core:startTime": [lit("xsd:dateTime", when)],
            "uco-core:eventContext": [{"@id": sample_ids[digest]}],
            "uco-core:description": (
                "Timestamp is a VirusTotal submission/observation time from "
                "the report timeline — not an intrinsic file creation time."
            ),
            "uco-core:tag": ["epistemic:reported", "timestamp:submitted"],
        }))

    zip_id = sample_ids[
        "27c4e9f01e5142a021329163b074f0692a9b4e832e0b53a5e31d364fdbbcdef8"]
    exe_id = sample_ids[
        "409839f9c8327eff6208aeca4f7113f5a0abdfa97f266f404b14f9fa6ab1432f"]
    link(zip_id, email_msg, "Contained_Within", tag="attachment")
    link(email_msg, zip_id, "Had_Attachment")
    link(exe_id, zip_id, "Contained_Within")
    link(js_temp, exe_id, "Contained_Within",
                     desc="JS RAT inside WinRAR SFX (Figure 8)")
    link(keylogger, exe_id, "Contained_Within",
                     desc="Keylogger hex inside WinRAR SFX (Figure 8); "
                          "no published standalone digest")
    link(js_temp, js_installed, "Moved_To", tag="install-path",
         desc="Report: JS moved from %TEMP% to %LOCALAPPDATA%\\<uid>0.js")
    msg_id = sample_ids[
        "671ede00b5be118bab9238386fd3f7502ffa21f678d8f509b181d4a819524525"]
    link(email_msg, msg_id, "Contained_Within", tag="msg-representation",
         desc="EmailMessage represented by hashed .msg timeline sample")

    a_family = analytic(
        "analytic-family-classification",
        "Samples and components are classified as the DarkWatchman malware "
        "family based on Prevailion dynamic analysis and reverse engineering.",
        confidence_tag="confidence:high-verbal",
        tags=["epistemic:assessment", "classification"],
        about=[dw_family, js_temp, keylogger, exe_id],
        source_ctx="Section: Malware analysis / sample classification",
    )

    # ------------------------------------------------------------------
    # Registry + scheduled task
    # ------------------------------------------------------------------
    reg_root = r"HKCU\Software\Microsoft\Windows\DWM"
    # Concrete observed state only; schema semantics → Configuration.
    reg_key = add({
        "@id": uid("regkey-dwm"),
        "@type": "uco-observable:WindowsRegistryKey",
        "uco-core:name": reg_root,
        "uco-core:description": (
            "DarkWatchman configuration hive path. Observed install-flag value "
            "modeled below; code-derived parameter semantics are ConfigurationEntries."
        ),
        "uco-core:hasFacet": [{
            "@id": uid("regkey-dwm-facet"),
            "@type": "uco-observable:WindowsRegistryKeyFacet",
            "uco-observable:key": reg_root,
            "uco-observable:registryValues": [
                {
                    "@id": uid("regkey-dwm:value:0"),
                    "@type": "uco-observable:WindowsRegistryValue",
                    "uco-core:name": "<uid>0",
                    "uco-observable:dataType": "reg_sz",
                    "uco-observable:data": "1",
                },
                {
                    # Known to exist from the report; payload not reproduced here.
                    "@id": uid("regkey-dwm:value:1"),
                    "@type": "uco-observable:WindowsRegistryValue",
                    "uco-core:name": "<uid>1",
                    "uco-observable:dataType": "reg_sz",
                    "uco-core:tag": ["content:not-reproduced", "epistemic:observed"],
                    "uco-core:description": (
                        "Observed registry value holding Base64 PowerShell that "
                        "compiles/runs the C# keylogger; data omitted (not reproduced)."
                    ),
                },
            ],
        }],
    })
    reg_schema_entries = []
    for suffix, data, purpose in REG_OBSERVED:
        entry = {
            "@id": uid(f"regkey-dwm:config-entry:{suffix}"),
            "@type": "uco-configuration:ConfigurationEntry",
            "uco-configuration:itemName": f"<uid>{suffix}",
            "uco-configuration:itemType": "registry-value-name-template",
            "uco-configuration:itemDescription": purpose,
        }
        if data is not None:
            entry["uco-configuration:itemValue"] = [data]
        reg_schema_entries.append(entry)
    reg_schema = add({
        "@id": uid("config-dwm-registry-schema"),
        "@type": "uco-configuration:Configuration",
        "uco-core:name": "DarkWatchman registry schema",
        "uco-core:description": (
            "Code-derived parameter semantics under HKCU\\Software\\Microsoft\\"
            "Windows\\DWM\\. uid+b and uid+r are referenced in code but never set."
        ),
        "uco-core:tag": ["epistemic:reported", "malware-configuration"],
        "uco-configuration:configurationEntry": reg_schema_entries,
        "uco-core:externalReference": [
            report_reference("Section: Registry / configuration table")],
    })

    wscript = file_obs(
        "tool-wscript", "wscript.exe",
        "Windows Script Host used to launch the installed JS RAT.",
        path=r"%SystemRoot%\System32\wscript.exe", ext="exe")
    task = add({
        "@id": uid("task-persistence"),
        "@type": "uco-observable:WindowsTask",
        "uco-core:name": "26b799fa-… (partial GUID prefix; DarkWatchman logon task)",
        "uco-core:description": (
            "Scheduled task with partial GUID-like name from Figure 12 "
            "(26b799fa-…). Logon trigger; runs wscript on installed JS. "
            "Account DESKTOP-JGLLJLD\\admin is an ANY.RUN analysis-environment "
            "account, not a confirmed victim identity."
        ),
        "uco-core:tag": ["partial-task-id", "analysis-environment-account"],
        "uco-core:hasFacet": [{
            "@id": uid("task-persistence-facet"),
            "@type": "uco-observable:WindowsTaskFacet",
            "uco-observable:imageName": "wscript.exe",
            "uco-observable:parameters": '"%LOCALAPPDATA%\\<uid>0.js"',
            "uco-observable:application": {"@id": wscript},
            "uco-observable:taskComment": "At log on persistence for DarkWatchman",
            "uco-observable:triggerList": [{
                "@id": uid("task-persistence-trigger"),
                "@type": "uco-observable:TriggerType",
                "uco-observable:triggerType": "TASK_TRIGGER_LOGON",
                "uco-observable:isEnabled": lit("xsd:boolean", True),
            }],
            "uco-observable:actionList": [{
                "@id": uid("task-persistence-action"),
                "@type": "uco-observable:TaskActionType",
                "uco-observable:actionType": "TASK_ACTION_EXEC",
                "uco-observable:iExecAction": {
                    "@id": uid("task-persistence-iexec"),
                    "@type": "uco-observable:IExecActionType",
                    "uco-observable:execProgramPath": r"%SystemRoot%\System32\wscript.exe",
                    "uco-observable:execArguments": '"%LOCALAPPDATA%\\<uid>0.js"',
                },
            }],
        }],
    })

    # ------------------------------------------------------------------
    # Infrastructure — candidates vs observed C2
    # ------------------------------------------------------------------
    domain_ids: dict[str, str] = {}
    for d in DGA_SEEDS:
        observed = d in OBSERVED_C2
        domain_ids[d] = add({
            "@id": uid("domain-" + d.replace(".", "-")),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": d,
            "uco-core:description": (
                "Observed live C2 domain from Prevailion analysis."
                if observed else
                "Seeded DGA candidate domain from malware configuration "
                "(Figure 17 / code); not asserted as observed traffic here."
            ),
            "uco-core:tag": (
                ["c2", "epistemic:observed"] if observed
                else ["dga-candidate", "epistemic:reported"]
            ),
            "uco-core:hasFacet": [{
                "@id": uid(f"domain-{d}-facet"),
                "@type": "uco-observable:DomainNameFacet",
                "uco-observable:value": d,
            }],
        })
    dga_entries = [{
        "@id": uid(f"dga-config-entry-{d.replace('.', '-')}"),
        "@type": "uco-configuration:ConfigurationEntry",
        "uco-configuration:itemName": d,
        "uco-configuration:itemType": "dga-seed-domain",
        "uco-configuration:itemDescription": (
            "Observed live C2 seed" if d in OBSERVED_C2
            else "Seeded DGA candidate (not asserted as observed traffic)"
        ),
        "uco-configuration:itemObject": [{"@id": domain_ids[d]}],
    } for d in DGA_SEEDS]
    dga_config = add({
        "@id": uid("config-dga-seed-set"),
        "@type": "uco-configuration:Configuration",
        "uco-core:name": "DarkWatchman DGA seed set",
        "uco-core:description": (
            "All ten seeded .top domains from Figure 17 / code. Candidate "
            "membership is separate from observed resolution/connection."
        ),
        "uco-core:tag": ["epistemic:reported", "dga-configuration"],
        "uco-configuration:configurationEntry": dga_entries,
        "uco-core:externalReference": [
            report_reference("Figure 17 / DGA seed list")],
    })

    # Direct configuration → malware-family links for consumer queries.
    cfg_tool_reg = add({
        "@id": uid("configured-tool-registry"),
        "@type": "uco-tool:ConfiguredTool",
        "uco-core:name": "DarkWatchman (registry configuration)",
        "uco-core:description": (
            "ConfiguredTool view of DarkWatchman using the HKCU\\…\\DWM registry schema."
        ),
        "uco-configuration:isConfigurationOf": {"@id": dw_family},
        "uco-configuration:usesConfiguration": {"@id": reg_schema},
        "uco-core:tag": ["malware-configuration"],
    })
    cfg_tool_dga = add({
        "@id": uid("configured-tool-dga"),
        "@type": "uco-tool:ConfiguredTool",
        "uco-core:name": "DarkWatchman (DGA configuration)",
        "uco-core:description": (
            "ConfiguredTool view of DarkWatchman using the seeded DGA domain set."
        ),
        "uco-configuration:isConfigurationOf": {"@id": dw_family},
        "uco-configuration:usesConfiguration": {"@id": dga_config},
        "uco-core:tag": ["dga-configuration"],
    })

    c2_ips: dict[str, str] = {}
    for ip in sorted(set(OBSERVED_C2.values())):
        c2_ips[ip] = add({
            "@id": uid("ip-" + ip.replace(".", "-")),
            "@type": "uco-observable:ObservableObject",
            "uco-core:name": ip,
            "uco-core:description": "Observed C2 hosting IP from Prevailion report.",
            "uco-core:hasFacet": [{
                "@id": uid(f"ip-{ip}-facet"),
                "@type": "uco-observable:IPv4AddressFacet",
                "uco-observable:addressValue": ip,
            }],
        })
    for d, ip in OBSERVED_C2.items():
        link(js_installed, domain_ids[d], "Connected_To", tag="c2",
                         desc="Observed C2 from persistent installed instance")
        link(domain_ids[d], c2_ips[ip], "Resolved_To", tag="c2",
                         desc="Reported resolution during analysis window")

    ann_dga_contradiction = annotation(
        "ann-dga-length-contradiction",
        "Source contradiction: algorithm section describes 8-character DGA "
        "labels; detection section says 7-character alphanumeric domains. "
        "Code-derived 8-character interpretation has stronger support.",
        [dw_family, domain_ids["bfdb1290.top"]],
        tags=["epistemic:source-contradiction"],
        source_ctx="Algorithm section vs Detection Opportunities",
    )
    ann_fileless = annotation(
        "ann-fileless-characterization",
        "Vendor characterization (executive summary): malware 'never writes "
        "anything to disk'. Detailed installation section contradicts this by "
        "moving the JS file to LocalAppData. Graph models the detailed "
        "mechanics; this annotation preserves the stronger executive claim "
        "as sourced characterization, not an unqualified fact.",
        [dw_family, js_installed, report],
        tags=["epistemic:reported", "epistemic:source-contradiction"],
        source_ctx="Executive summary vs installation section",
    )

    # ------------------------------------------------------------------
    # Capabilities (NOT observed Action occurrences)
    # ------------------------------------------------------------------
    caps = compilation(
        "grouping-capabilities",
        "DarkWatchman capability model",
        "Capabilities / Notable Functionality from the report — code abilities, "
        "not individually observed historical occurrences.",
        [],
        kind="uco-core:Grouping",
    )
    # fill members after annotations created
    cap_wmi = annotation(
        "cap-wmi",
        "Capability: execute miscellaneous commands via WMI.",
        [dw_family],
        tags=["epistemic:capability", "att&ck-enrichment:T1047"],
        source_ctx="Section: Capabilities / Notable Functionality",
    )
    cap_shadow = annotation(
        "cap-shadow",
        "Capability: if admin, delete shadow copies via "
        "'vssadmin.exe Delete Shadows /All /Quiet' (conditional path).",
        [dw_family],
        tags=["epistemic:capability", "att&ck-enrichment:T1490"],
        source_ctx="Section: Capabilities / Notable Functionality",
    )
    cap_upload = annotation(
        "cap-upload",
        "Capability: upload/exfiltrate files from victim to C2 (outbound).",
        [dw_family],
        tags=["epistemic:capability", "att&ck-enrichment:T1041"],
        source_ctx="Section: Capabilities / Notable Functionality",
    )
    cap_ingress = annotation(
        "cap-ingress",
        "Capability: remote update of RAT/keylogger and ingress tool transfer "
        "(C2-to-victim; T1105).",
        [dw_family],
        tags=["epistemic:capability", "att&ck-enrichment:T1105"],
        source_ctx="Section: Capabilities / Notable Functionality",
    )
    graph.set_property(caps, "uco-core:object", refs(
        [cap_wmi, cap_shadow, cap_upload, cap_ingress]))
    graph.set_property(caps, "uco-core:context", ["malware-capability-model"])

    # ------------------------------------------------------------------
    # Observed / reported Actions (no Organization performer)
    # ------------------------------------------------------------------
    def attack(tid: str) -> str:
        return f"https://attack.mitre.org/techniques/{tid}"

    def action(label: str, name: str, desc: str, tids: list[str], *,
               tags: list[str], instrument=None, obj=None, result=None,
               performer=None) -> str:
        aid = uid(label)
        props: dict = {
            "uco-core:name": name,
            "uco-core:description": desc,
            "uco-core:tag": list(tags),
        }
        if performer:
            props["uco-action:performer"] = {"@id": performer}
        if instrument:
            props["uco-action:instrument"] = [{"@id": x} for x in instrument]
        if obj:
            props["uco-action:object"] = [{"@id": x} for x in obj]
        if result:
            props["uco-action:result"] = [{"@id": x} for x in result]
        graph.upsert_node(aid, types="uco-action:Action", properties=props)
        for tid in tids:
            graph.add_type(aid, attack(tid))
        mid = annotation(
            f"ann-attack-{label}",
            (
                "CASE/UCO modeler enrichment using MITRE ATT&CK technique IRIs; "
                "not vendor-asserted identifiers in the 2021 Prevailion prose. "
                f"Techniques: {', '.join(tids)}. Technique URLs: "
                + ", ".join(attack(t) for t in tids)
                + ". Mapping date: 2026-07-14; mapping author: CASE/UCO SDK exemplar."
            ),
            [aid],
            tags=["att&ck-mapping", "epistemic:enrichment",
                  "mapping-source:case-uco-modeler"],
            source_ctx=f"Section: behavior supporting {', '.join(tids)}",
        )
        # Structured report + one MITRE ExternalReference per technique.
        graph.set_property(
            mid,
            "uco-core:externalReference",
            [
                report_reference(f"Section: behavior supporting {', '.join(tids)}"),
                *[mitre_reference(t) for t in tids],
            ],
        )
        attack_mapping_ids.append(mid)
        if label == "action-user-exec":
            graph.add_type(aid, attack("T1036.008"))
            mid2 = annotation(
                "ann-attack-T1036-008-enrichment",
                "T1036.008 (Masquerade File Type) added as present-day modeler "
                "enrichment; technique was created after the 2021 report. "
                f"URL: {attack('T1036.008')}.",
                [aid],
                tags=["att&ck-mapping", "epistemic:enrichment",
                      "mapping-source:case-uco-modeler", "post-dated-technique"],
                source_ctx="Section: SFX masquerade / document icon (T1036.008)",
            )
            graph.set_property(
                mid2,
                "uco-core:externalReference",
                [
                    report_reference(
                        "Section: SFX masquerade / document icon (T1036.008)"
                    ),
                    mitre_reference("T1036.008"),
                ],
            )
            attack_mapping_ids.append(mid2)
        return aid

    a_phish = action(
        "action-spearphish",
        "Deliver Pony Express spearphishing lure",
        "Spoofed ponyexpress.ru email from smtp.rentbikespb.ru with ZIP attachment.",
        ["T1566.001"],
        tags=["epistemic:reported"],
        instrument=[email_msg],
        result=[zip_id],
    )
    a_user = action(
        "action-user-exec",
        "Victim opens masqueraded invoice SFX",
        "Recipient opened the attached archive; SFX used a document icon and "
        "hidden extensions (forum corroboration). Performer omitted: the victim "
        "executed the file; operators are not the grammatical performer.",
        ["T1204.002", "T1036"],
        tags=["epistemic:reported"],
        obj=[exe_id],
        result=[js_temp, keylogger],
    )
    a_js = action(
        "action-js-exec",
        "Execute DarkWatchman JavaScript RAT via wscript",
        "SFX Setup runs 134121811.js with wscript.",
        ["T1059.007"],
        tags=["epistemic:reported"],
        instrument=[wscript],
        obj=[js_temp],
    )
    a_install = action(
        "action-install",
        "Install fileless registry config, move JS, create scheduled task",
        "Moves JS to LocalAppData as <uid>0.js, writes keylogger Base64 into "
        f"{reg_root}\\<uid>1, sets <uid>0=1, creates logon scheduled task.",
        ["T1053.005", "T1112"],
        tags=["epistemic:reported"],
        instrument=[js_temp],
        obj=[js_temp, keylogger, reg_key],
        result=[js_installed, task, reg_key],
    )
    a_decode = action(
        "action-decode-keylogger",
        "XOR/Base64 decode and CSC-compile keylogger",
        "Un-XOR 2204722946 into Base64 PowerShell under <uid>1; CSC compiles "
        "and runs the C# keylogger at RAT startup.",
        ["T1140", "T1059.001"],
        tags=["epistemic:reported"],
        instrument=[js_installed],
        obj=[keylogger],
        result=[reg_key],
    )
    a_keylog = action(
        "action-keylog",
        "Capture keystrokes and clipboard via registry buffer",
        "Keylogger hooks WH_KEYBOARD_LL; buffer in registry <uid>a; JS RAT "
        "scrapes/clears buffer before C2 transmission.",
        ["T1056.001", "T1115"],
        tags=["epistemic:reported"],
        instrument=[keylogger, js_installed],
        obj=[reg_key],
    )
    a_dga = action(
        "action-dga",
        "Resolve C2 via Domain Generation Algorithm",
        "Builds up to 510 domains/day; probes https://<label>.top/index.php. "
        "Netlab360 tracks as tordwm.",
        ["T1568.002", "T1071.001"],
        tags=["epistemic:reported"],
        instrument=[js_installed],
        obj=[domain_ids[d] for d in OBSERVED_C2],
    )
    a_discovery = action(
        "action-discovery",
        "Collect host profile and security products",
        "srv_send_info / collect_user_profile gather OS, AV, browser histories, "
        "smartcard PnP drivers (reported operating behavior).",
        ["T1082", "T1518.001"],
        tags=["epistemic:reported"],
        instrument=[js_installed],
    )
    keylog_buffer = add({
        "@id": uid("content-keylog-buffer"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "Keylog buffer",
        "uco-core:description": (
            "Logical content: keystrokes + clipboard buffered under registry "
            "<uid>a before HTTPS C2 transmission."
        ),
        "uco-core:tag": ["exfil-content", "epistemic:reported"],
    })
    host_profile = add({
        "@id": uid("content-host-profile"),
        "@type": "uco-observable:ObservableObject",
        "uco-core:name": "Host profile collection",
        "uco-core:description": (
            "Logical content: OS/AV/browser-history/smartcard profile gathered "
            "by srv_send_info / collect_user_profile."
        ),
        "uco-core:tag": ["exfil-content", "epistemic:reported"],
    })
    a_exfil = action(
        "action-c2-exfil",
        "Exfiltrate keylogs and host data over HTTPS C2",
        "WinHttpRequest.5.1 POST with forged IE11 UA (rv:11.1); body carries "
        "host profile and keylog buffer over the C2 channel. C2 domains are "
        "participants via Connected_To, not the Action object.",
        ["T1071.001", "T1041"],
        tags=["epistemic:reported"],
        instrument=[js_installed],
        obj=[keylog_buffer, host_profile],
    )

    # Analytic assessments (unattributed)
    a_attr = analytic(
        "analytic-attribution-impossible",
        "PACT: attribution of DarkWatchman was not possible.",
        confidence_tag=None,
        tags=["epistemic:assessment"],
        about=[cluster, report],
        source_ctx="Section: Closing Analysis",
    )
    a_criminal = analytic(
        "analytic-appears-criminal",
        "PACT: DarkWatchman appears to be used by criminal actors "
        "(Russian-language lures/code comments; mail servers in Russia).",
        confidence_tag="confidence:appears-verbal",
        tags=["epistemic:assessment"],
        about=[cluster, dw_family],
        source_ctx="Section: Closing Analysis",
    )
    a_access = analytic(
        "analytic-initial-access",
        "PACT assesses with moderate confidence that DarkWatchman is an "
        "initial-access tool for ransomware groups or affiliates.",
        confidence_tag="confidence:moderate-verbal",
        tags=["epistemic:assessment"],
        about=[cluster, dw_family],
        source_ctx="Section: Closing Analysis",
    )
    a_ransom = analytic(
        "analytic-ransomware-hypothesis",
        "Hypothesis (not confirmed): ransomware operators could provide "
        "DarkWatchman to affiliates for foothold and C2 under operator control.",
        confidence_tag="confidence:hypothesis-verbal",
        tags=["epistemic:hypothesis"],
        about=[cluster, dw_family],
        source_ctx="Section: Closing Analysis",
    )

    # Detection patterns (LogicalPattern + provenance Annotation)
    pat_reg = add({
        "@id": uid("pattern-registry-template"),
        "@type": "uco-pattern:LogicalPattern",
        "uco-core:name": "DarkWatchman DWM registry name template",
        "uco-core:description": (
            "Anomalous keys under HKCU\\Software\\Microsoft\\Windows\\DWM\\ "
            "with 8-character uid + 1-character suffix."
        ),
        # CASE 1.4.0 types patternExpression as pattern:PatternExpression.
        # Avoid backslashes in the literal — pyshacl SPARQL message formatting
        # crashes on '\\' in replacement strings.
        "uco-pattern:patternExpression": lit(
            "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression",
            "HKCU/Software/Microsoft/Windows/DWM/[0-9a-f]{8}[a-z]",
        ),
        "uco-core:tag": ["detection-pattern", "epistemic:reported"],
    })
    pat_ua = add({
        "@id": uid("pattern-user-agent"),
        "@type": "uco-pattern:LogicalPattern",
        "uco-core:name": "DarkWatchman forged IE11 UA",
        "uco-core:description": "Incorrect IE11 UA string using rv:11.1.",
        "uco-pattern:patternExpression": lit(
            "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression",
            "User-Agent contains 'rv:11.1'",
        ),
        "uco-core:tag": ["detection-pattern", "epistemic:reported"],
    })
    pat_http = add({
        "@id": uid("pattern-http-8xx"),
        "@type": "uco-pattern:LogicalPattern",
        "uco-core:name": "DarkWatchman HTTP 8xx C2 commands",
        "uco-core:description": "Abnormal HTTP status codes 820–835 as C2 commands.",
        "uco-pattern:patternExpression": lit(
            "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression",
            "HTTP status in 820..835",
        ),
        "uco-core:tag": ["detection-pattern", "epistemic:reported"],
    })
    det_reg = annotation(
        "detect-registry-template",
        "Detection opportunity: DWM registry name template (see LogicalPattern).",
        [pat_reg, reg_key],
        tags=["detection-pattern", "epistemic:reported"],
        source_ctx="Section: Detection Opportunities",
    )
    det_ua = annotation(
        "detect-user-agent",
        "Detection opportunity: forged IE11 UA with rv:11.1 (see LogicalPattern).",
        [pat_ua, js_installed],
        tags=["detection-pattern", "epistemic:reported"],
        source_ctx="Section: Detection Opportunities",
    )
    det_http = annotation(
        "detect-http-8xx",
        "Detection opportunity: HTTP 8xx C2 command channel (see LogicalPattern).",
        [pat_http, js_installed],
        tags=["detection-pattern", "epistemic:reported"],
        source_ctx="Section: Detection Opportunities",
    )

    # ------------------------------------------------------------------
    # Nested compilations → Investigation
    # ------------------------------------------------------------------
    actions = [
        a_phish, a_user, a_js, a_install, a_decode, a_keylog, a_dga,
        a_discovery, a_exfil,
    ]
    graph.set_property(cluster, "uco-core:object", refs([
        dw_family, *actions, js_temp, js_installed, keylogger, exe_id, zip_id,
        *domain_ids.values(), a_family, a_attr, a_criminal, a_access, a_ransom,
        caps, reg_key, task, dga_config, reg_schema,
    ]))
    src_comp = compilation(
        "comp-source", "Source material",
        "Report, authors, publisher, and in-report graphics.",
        [report, prevailion, author_matt, author_sherman, ann_authorship,
         *graphic_ids],
    )
    deliv_comp = compilation(
        "comp-delivery", "Delivery chain",
        "Email lure, samples, SFX contents, VT submission Events, and "
        "delivery Actions.",
        list(dict.fromkeys([
            email_msg, spoof_addr, smtp_host, rentbike, pony, ip_send, ip_park,
            zip_id, exe_id, js_temp, keylogger, a_phish, a_user, a_js,
            *sample_ids.values(), *vt_event_ids,
        ])),
    )
    mal_comp = compilation(
        "comp-malware", "Malware behavior and persistence",
        "Family, file instances, registry, task, and operating Actions.",
        [dw_family, js_installed, reg_key, reg_schema, cfg_tool_reg, task,
         wscript, caps, keylog_buffer, host_profile, a_install, a_decode,
         a_keylog, a_dga, a_discovery, a_exfil],
    )
    infra_comp = compilation(
        "comp-infra", "Infrastructure",
        "Observed C2, DGA candidates/config, and mail infrastructure.",
        [*domain_ids.values(), *c2_ips.values(), smtp_host, rentbike,
         ip_send, ip_park, dga_config, cfg_tool_dga, ann_dga_contradiction],
    )
    analytic_comp = compilation(
        "comp-analytic", "Analytic assessments",
        "Unattributed cluster and PACT/modeler analytic assertions.",
        [cluster, a_attr, a_criminal, a_access, a_ransom, a_family,
         ann_fileless],
    )
    detect_comp = compilation(
        "comp-detection", "Detection patterns",
        "LogicalPatterns plus provenance Annotations.",
        [pat_reg, pat_ua, pat_http, det_reg, det_ua, det_http],
    )
    attack_comp = compilation(
        "comp-attack-mappings", "ATT&CK mappings and enrichment",
        "Modeler ATT&CK mapping Annotations attached to observed Actions.",
        attack_mapping_ids,
    )

    investigation = add({
        "@id": uid("investigation"),
        "@type": "case-investigation:Investigation",
        "uco-core:name": "Prevailion CTI: DarkWatchman fileless RAT",
        "uco-core:description": (
            "Open-source CTI graph for Prevailion PACT's DarkWatchman report. "
            "Unattributed activity cluster; epistemic layers separate observed "
            "behavior, capabilities, and hypotheses. Built with CASEGraph "
            "public upsert APIs (critic serializer_mode=casegraph_raw)."
        ),
        "case-investigation:focus": [
            "Malware family analysis",
            "Fileless registry persistence",
            "DGA C2 infrastructure",
            "Spearphishing delivery",
            "Epistemic modeling of unattributed CTI",
        ],
        "uco-core:object": refs([
            src_comp, deliv_comp, mal_comp, infra_comp, analytic_comp,
            detect_comp, attack_comp,
        ]),
    })
    _ = actions, investigation
    return graph


def write_manifest() -> None:
    recipe = ROOT / "docs" / "recipes" / "cyber-threat-intelligence.md"
    payload = {
        "schema_version": "1.1",
        "note": (
            "Build/critic provenance sidecar — these paths are NOT domain "
            "subjects of the CTI investigation graph."
        ),
        "artifacts": [
            {
                "role": "builder_source",
                "path": str((HERE / "build_darkwatchman.py").relative_to(ROOT)),
                "sha256": sha256_of(HERE / "build_darkwatchman.py"),
            },
            {
                "role": "modeling_guidance",
                "path": str(recipe.relative_to(ROOT)),
                "sha256": sha256_of(recipe),
            },
            {
                "role": "output_artifact",
                "path": str(OUTPUT.relative_to(ROOT)),
                "sha256": sha256_of(OUTPUT),
            },
        ],
        # Back-compat keys for older critic clients
        "builder": {
            "path": str((HERE / "build_darkwatchman.py").relative_to(ROOT)),
            "sha256": sha256_of(HERE / "build_darkwatchman.py"),
            "role": "builder_source",
        },
        "recipe": {
            "path": str(recipe.relative_to(ROOT)),
            "sha256": sha256_of(recipe),
            "role": "modeling_guidance",
        },
        "output": {
            "path": str(OUTPUT.relative_to(ROOT)),
            "sha256": sha256_of(OUTPUT),
            "role": "output_artifact",
        },
    }
    MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST}")


def validate(path: Path) -> int:
    import sys
    if not validator_available():
        print("case_validate not installed; refusing to claim success",
              file=sys.stderr)
        return 2
    report = validate_graph_file(
        path, project_root=ROOT, extensions=["attack-technique:full"])
    print(report.safe_summary)
    if report.undeclared_concepts:
        print("Undeclared concepts:", ", ".join(report.undeclared_concepts))
        print(report.concept_guidance)
    return 0 if report.conforms else 1


def main() -> int:
    graph = build_graph()
    graph.write_streaming(str(OUTPUT), atomic=True)
    print(f"Wrote {OUTPUT}")
    print(f"Graph nodes: {len(graph)}")
    write_manifest()
    return validate(OUTPUT)


if __name__ == "__main__":
    raise SystemExit(main())
