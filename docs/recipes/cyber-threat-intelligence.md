# Cyber Threat Intelligence and APT Reporting

> See [Recipe Index](INDEX.md) for all recipes.

Model an open-source cyber threat intelligence (CTI) report — a vendor
analysis (Cisco Talos, Mandiant, etc.) of a threat actor, its malware
families, its post-compromise toolkit, and its tactics, techniques, and
procedures (TTPs). This is fundamentally different from a single-incident
forensic case: the deliverable is *intelligence about an adversary*
distilled from many intrusions, not evidence acquired from one host or
capture. The distinctive modeling requirements are (1) **the report is the
primary artifact** — including its graphics, which routinely carry IOCs,
config dumps, and infection-chain detail that never appear in the prose;
(2) **the threat actor is an actor, not an observable** — UCO has no
`ThreatActor` class, so the group is a `uco-identity:Organization` whose
behaviors are `uco-action:Action` nodes; and (3) **malware families and
variants** are tools with a lineage and an activity timeline, distinct
from the individual samples that carry hashes.

Validated against `examples/cti/lotus_blossom_2025/` (Cisco Talos, "Lotus
Blossom espionage group targets multiple industries with different
versions of Sagerunex and hacking tools," Joey Chen, 2025-02-27).

**When to use this recipe**

- The source is a threat-intelligence report / threat spotlight / APT
  writeup attributing activity to a named group (Lotus Blossom, a.k.a.
  Spring Dragon / Billbug / Thrip; APT41; etc.)
- The content describes malware families and variants, C2 infrastructure
  (including third-party cloud C2 such as Dropbox, Twitter/X, or webmail),
  a post-compromise toolkit, registry/service persistence, victimology by
  sector and region, and IOCs (hashes, IPs, domains, campaign codes,
  Snort/ClamAV/YARA signatures)
- The report embeds graphics (timelines, maps, infection-chain diagrams,
  decompiled code, config hexdumps) that carry details absent from the text
- For a single intrusion with acquired packet capture or host evidence,
  use [network-investigation.md](network-investigation.md); for a
  delivery-chain narrative from a phishing email, use
  [spear-phishing.md](spear-phishing.md); for the analysis/attribution
  layer mechanics, use [analysis.md](analysis.md)

## Classes and properties

| Class | Role |
|---|---|
| `case-investigation:Investigation` | Report container; `focus` = attribution / malware / C2 / persistence |
| `uco-observable:ObservableObject` + `URLFacet` | The report itself (blog post) |
| `uco-identity:Person` / `Organization` | Report author and publisher (e.g., Joey Chen / Cisco Talos) |
| `uco-observable:ObservableObject` + `RasterPictureFacet` + `FileFacet` + `ContentDataFacet` | Each in-report graphic, captured by SHA-256 with a description of what it depicts |
| `uco-identity:Organization` | **The threat actor** (no `ThreatActor` class exists); aliases in `tag`/description |
| `uco-tool:MaliciousTool` | Malware family (backdoor/RAT) and offensive tools; `toolType` |
| `uco-tool:Tool` | Dual-use / legitimate tooling (RAR, Impacket, VMProtect, HTran) |
| `uco-observable:ObservableObject` + `FileFacet` | Malware samples/variants (with `observableCreatedTime` = activity-window start) and dropped DLLs |
| `uco-observable:WindowsRegistryKey` + `WindowsRegistryKeyFacet` + `WindowsRegistryValue` | Registry persistence (service-DLL install) |
| `uco-observable:WindowsService` + `WindowsServiceFacet` | The hijacked/created service (`startType`, `serviceType`) |
| `uco-observable:IPv4AddressFacet` / `DomainNameFacet` | C2 servers, proxies, cloud-C2 endpoints, recon services |
| `uco-location:Location` + `SimpleAddressFacet` | Targeted regions (victimology map) |
| `uco-victim:VictimTargeting` | Targeted sectors (a `Victim` role subclass) |
| `uco-action:Action` | Adversary behaviors: persistence, discovery, lateral movement, collection/exfil; also vendor detection coverage |

## Modeling patterns

### 1. The report and its graphics are first-class evidence

Model the blog post as an `ObservableObject` with a `URLFacet`, linked to
its author (`Person`) and publisher (`Organization`). Then capture **every
graphic** the report embeds. Threat reports put load-bearing detail into
images — a Gantt timeline of malware activity, a targeted-countries map,
infection-chain diagrams, decompiled code, and annotated config hexdumps
with C2 IPs and tokens. Download each image, hash it (SHA-256), and create
an `ObservableObject` with `FileFacet` + `RasterPictureFacet` +
`ContentDataFacet`, and — critically — a `uco-core:description` recording
*what the graphic shows*, so the intelligence survives even though the
pixels are only referenced by hash. Link each graphic to the report with
`Contained_Within` tagged `graphic`.

### 2. The threat actor is an Organization; its behaviors are Actions

UCO has no dedicated ThreatActor/IntrusionSet class, so model the group as
a `uco-identity:Organization`. Record its aliases (Spring Dragon, Billbug,
Thrip) in `tag` and the description, and its "active since 2012" attribution
narrative in the description. Every adversary behavior is a
`uco-action:Action` whose `performer` is this Organization — this keeps the
actor as the grammatical subject of the intrusion and lets a reader answer
"what did the actor do?" from graph structure. Attribution evidence
(exclusive malware use, victimology, TTP overlap) belongs in the
`Investigation`/actor descriptions.

### 3. Malware families vs. variants vs. samples

Distinguish three levels:

- **Family** (`uco-tool:MaliciousTool`, e.g. Sagerunex): the named
  backdoor lineage, its `toolType`, injection method, and shared behaviors;
  link to its predecessor with `Related_To` ("assessed evolution of Evora").
- **Variant** (`ObservableObject` + `FileFacet`): each distinct version
  (Beta, original, Dropbox/Twitter, Zimbra), with its activity window as
  `observableCreatedTime` (read from the report's timeline graphic) and its
  distinguishing C2 mechanism in the description; `Related_To` the family.
- **Sample**: an individual binary carrying a hash — attach a
  `ContentDataFacet` when the report gives one.

Record the actor's `Used` relationship to the family and to each variant.

### 4. Registry-based persistence is fully covered by core UCO

`reg add` service-DLL persistence maps cleanly onto core UCO — **no
extension or change proposal is required**. For each key, create a
`uco-observable:WindowsRegistryKey` whose `WindowsRegistryKeyFacet` carries
the `key` path and one embedded `WindowsRegistryValue` per value. On each
`WindowsRegistryValue` set `uco-core:name` (the value name, e.g.
`ServiceDll` / `Start`), `uco-observable:data` (the data, e.g.
`c:\windows\tapisrv.dll` / `2`), and `uco-observable:dataType` using a
`RegistryDatatypeVocab` member (`reg_expand_sz`, `reg_dword`, `reg_sz`,
`reg_binary`, `reg_multi_sz`, `reg_qword`, …). Pair the key with a
`uco-observable:WindowsService` (`WindowsServiceFacet.serviceName`,
`startType` = `service_auto_start` when `Start=2`, `serviceType`), and
relate the `ServiceDll` value's key to the dropped DLL `ObservableObject`.
Wrap the whole thing in a single persistence `uco-action:Action`
(`performer` = actor, `object` = the keys, `result` = the services).

> **Note on the value name property.** `WindowsRegistryValue` is a
> `UcoInherentCharacterizationThing`, and its name is `uco-core:name` — not
> `uco-observable:name` (which does not exist and will fail strict concept
> coverage). This is the single most common validation slip when modeling
> registry values.

### 5. MITRE ATT&CK techniques → the `uco-action:Technique` metaclass

`uco-action:Technique` is a **metaclass**, not an ordinary class, as defined
in [ucoProject/UCO PR #676](https://github.com/ucoProject/UCO/pull/676)
(resolving [issue #666](https://github.com/ucoProject/UCO/issues/666), UCO
1.5.0). Its exact wording: *"A technique is a class of actions joined by some
common characteristics. `uco-action:Technique` itself is a metaclass. A
Technique instance is an `owl:Class` that is a subclass of
`uco-action:Action`."* The PR also adds a top-level `uco-core:UcoType` (disjoint
from `uco-core:UcoThing`) to anchor the metaclass hierarchy, and one property,
`uco-action:techniqueID` (Literal-valued, used only on Techniques). It does
**not** add `techniqueFramework` / `techniqueTactic` / `techniquePlatform` —
those appeared only in the issue's early draft and are not in the merged model.

So model techniques with **punning**, in two layers:

- **The technique is a class.** Declare each ATT&CK technique as an
  `owl:Class` that is `a uco-action:Technique` and `rdfs:subClassOf
  uco-action:Action`, carrying `uco-action:techniqueID` (e.g. `T1543.003`).
  Keep these in an ontology/catalog graph, not the data graph — the local
  [`attack-technique`](../../extensions/attack-technique/) extension ships a
  partial MITRE ATT&CK catalog (`mitre-attack-catalog.ttl`) under the
  canonical `https://attack.mitre.org/techniques/<id>` IRIs. Tactic/platform
  context goes in each class's `rdfs:comment` (the merged UCO model keeps the
  general class minimal).
- **A concrete action exhibits the technique.** Type the behavior
  `uco-action:Action` instance *with the technique class* (add the technique
  IRI to its `@type`). Because the technique class is a subclass of
  `uco-action:Action`, the action instance is still a valid Action; the extra
  type asserts which technique it exhibits. Do **not** create a separate
  Technique instance per action or link with a `Uses_Technique` relationship —
  the punning `rdf:type` edge *is* the association.

Sourcing matters: a report that lists no ATT&CK IDs in its prose (this Talos
post does not) is usually still mapped on the corresponding MITRE ATT&CK
**group** and **software** pages — for Lotus Blossom, group
[G0030](https://attack.mitre.org/groups/G0030/) and Sagerunex software S1156.
Enrich from those high-confidence mappings (e.g. T1543.003 Windows Service,
T1112 Modify Registry, T1055.001 DLL Injection, T1027.002 Software Packing,
T1090.001 Internal Proxy, T1102.002 Web Service, T1560.001 Archive via
Utility, T1041 Exfil over C2). Validate with the extension **and RDFS
inference** (the metaclass constraints resolve under inference):
`validate_graph(path, extensions=["attack-technique:full"])`. Reuse the
`attack-technique` catalog IRIs rather than minting your own technique class,
so the model stays forward-compatible with UCO 1.5.0.

### 6. Third-party cloud C2 is still C2

New variants tunnel C2 through legitimate services (Dropbox, Twitter/X,
Zimbra webmail) to blend with normal traffic. Model each channel as an
`ObservableObject` with a `DomainNameFacet`, and connect the variant to it
with a `Connected_To` relationship tagged `c2`. Keep legacy VPS C2 IPs
(`IPv4AddressFacet`) and hardcoded proxies distinct, tagged `c2` / `proxy`.
Model exfil artifacts (e.g. `mail_report.rar` saved to Zimbra draft/trash
folders) as observables `Created` by the variant and `Uploaded_To` the
cloud channel.

### 7. Victimology: regions and sectors

Model targeted regions (from the report's map graphic) as
`uco-location:Location` + `SimpleAddressFacet.country`, related to the actor
with a `targeting`-tagged edge. Model targeted sectors as a
`uco-victim:VictimTargeting` node (a `Victim` role subclass) — put the
sector list in the description and `tag`; there is no `targetSector`
property, so do not invent one.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Dropping the report's graphics because they are "just images" | Capture each as a hashed `RasterPicture` observable with a description of the IOCs/diagram it carries |
| Modeling the threat actor as an `ObservableObject` or a `Tool` | The actor is a `uco-identity:Organization`; its behaviors are `uco-action:Action` nodes with the actor as `performer` |
| `uco-observable:name` on a `WindowsRegistryValue` | Use `uco-core:name`; the value's data/type are `uco-observable:data` / `uco-observable:dataType` |
| Free-text registry data type (`REG_EXPAND_SZ`) | Use `RegistryDatatypeVocab` members (`reg_expand_sz`, `reg_dword`, …) |
| Inventing a bespoke Technique/Malware/ThreatActor class | Actor → Organization; malware → MaliciousTool; ATT&CK techniques → the `uco-action:Technique` metaclass (UCO #676) via the `attack-technique` catalog — reuse the canonical ATT&CK IRIs, don't mint your own |
| Modeling a technique as a plain instance node (`x a uco-action:Technique` with `techniqueTactic`/`techniquePlatform`) | `uco-action:Technique` is a **metaclass**: a technique is an `owl:Class` (`a uco-action:Technique`, `rdfs:subClassOf uco-action:Action`) with `uco-action:techniqueID`; the merged PR has no framework/tactic/platform properties |
| Linking an action to its technique with a `Uses_Technique` relationship | Type the action instance *with the technique class* (`rdf:type`); the punning type edge is the association — no relationship node |
| Dropping ATT&CK techniques because the report's prose omits IDs | Enrich from the MITRE ATT&CK group (G0030) and software (S1156) pages |
| Collapsing family, variant, and sample into one node | Family = `MaliciousTool`; variants/samples = `ObservableObject` + `FileFacet`/`ContentDataFacet`, `Related_To` the family |
| Treating cloud C2 (Dropbox/Twitter/Zimbra) as benign | It is a C2 channel — `Connected_To` tagged `c2`, with exfil artifacts `Uploaded_To` it |

## Checklist

1. Fetch the report; capture the prose and **download every graphic**.
   View each image and write a description of what it depicts (timelines,
   maps, infection chains, decompiled code, config hexdumps with IOCs).
2. Create the `Investigation`; model the report `ObservableObject`
   (`URLFacet`), its author and publisher, and one hashed `RasterPicture`
   observable per graphic linked `Contained_Within` the report.
3. Model the threat actor as an `Organization` with aliases; wire it
   `Subject_Of` the investigation. Add predecessor tooling and lineage.
4. Model the malware family (`MaliciousTool`) and each variant
   (`ObservableObject` + `FileFacet`, activity window in
   `observableCreatedTime`); record `Used` edges from the actor; add
   config-revealed artifacts (attacker host paths, debug-log temp files).
5. Model the post-compromise toolkit (`MaliciousTool` / `Tool`) with
   `toolType` and hashes where given.
6. Model registry/service persistence with `WindowsRegistryKey` +
   `WindowsRegistryValue` (name via `uco-core:name`, `dataType` via
   `RegistryDatatypeVocab`) and `WindowsService`; wrap in a persistence
   `Action`.
7. Model C2 (legacy VPS IPs, proxies, and cloud channels) and exfil
   artifacts; model discovery / lateral-movement / exfil `Action`s. Keep
   pre-cloud VPS C2 scoped to the variants that used it — do not attach a
   variant's config-derived infrastructure to later variants that moved off
   it.
8. Add ATT&CK techniques with the `uco-action:Technique` metaclass (from the
   report and the MITRE group/software pages): declare each technique as an
   `owl:Class` (subclass of `uco-action:Action`, with `techniqueID`) in the
   `attack-technique` catalog, and type each exhibiting behavior `Action`
   *with* that technique class. Add IOCs (campaign codes, signatures) and
   vendor detection coverage.
9. Validate: `validate_graph(path, extensions=["attack-technique:full"])`
   (strict concept coverage) plus `case_validate --built-version case-1.4.0
   --ontology-graph extensions/attack-technique/attack-technique.ttl
   --ontology-graph extensions/attack-technique/attack-technique-shapes.ttl
   --ontology-graph extensions/attack-technique/mitre-attack-catalog.ttl
   --inference rdfs --allow-info`; `Conforms: True` before presenting.

## Validated exemplar

`examples/cti/lotus_blossom_2025/build_lotus_blossom_sagerunex.py` — the
Cisco Talos Lotus Blossom / Sagerunex report: the blog post and its 24
graphics captured by hash, Lotus Blossom as an `Organization` (aliases
Spring Dragon / Billbug / Thrip), the Sagerunex `MaliciousTool` family with
Beta/original/Dropbox-Twitter/Zimbra variants on their timeline windows, the
post-compromise toolkit (Chrome cookie stealer, Venom proxy,
adjust-privilege, archiver, mtrain/HTran port relay, RAR, Impacket),
registry service-DLL persistence for `tapisrv`/`swprv`/`appmgmt` with
`WindowsService` pairing, legacy VPS + Dropbox/Twitter/Zimbra cloud C2,
victimology (Philippines/Vietnam/Hong Kong/Taiwan; government/manufacturing/
telecom/media), campaign-code IOCs, Snort/ClamAV coverage, and twelve MITRE
ATT&CK techniques (G0030/S1156 mappings) modeled with the
`uco-action:Technique` metaclass — each technique an `owl:Class` in the
`attack-technique` catalog and typed onto the behavior `Action` that exhibits
it. 246 nodes; passes `case_validate` (with RDFS inference) and strict concept
coverage — all registry data against core UCO (which covers it natively) and
the technique metaclass/classes against the local `attack-technique` extension
(the [UCO #676](https://github.com/ucoProject/UCO/pull/676)
forward-implementation).

## Related

- [network-investigation.md](network-investigation.md) — single-incident network forensics with acquired pcap (contrast: one capture, not adversary intelligence)
- [spear-phishing.md](spear-phishing.md) — delivery-chain attack narrative from a phishing email
- [analysis.md](analysis.md) — the attribution/analysis layer with confidence-scored classifications
- [network-artifacts.md](network-artifacts.md) — IPs, domains, and URLs as observables
- [forensic-tool.md](forensic-tool.md) — modeling tools and their configured runs
