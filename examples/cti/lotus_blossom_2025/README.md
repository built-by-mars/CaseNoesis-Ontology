# Lotus Blossom / Sagerunex — Cisco Talos CTI exemplar

Worked, validated CASE/UCO graph for an **open-source cyber threat
intelligence (CTI) report** rather than acquired forensic evidence. It is
the exemplar behind [`docs/recipes/cyber-threat-intelligence.md`](../../../docs/recipes/cyber-threat-intelligence.md).

**Source:** Joey Chen, "Lotus Blossom espionage group targets multiple
industries with different versions of Sagerunex and hacking tools," Cisco
Talos, 2025-02-27.
<https://blog.talosintelligence.com/lotus-blossom-espionage-group/>

## Contents

| File | What it is |
|---|---|
| `build_lotus_blossom_sagerunex.py` | Builder that emits and validates the graph |
| `lotus-blossom-sagerunex.jsonld` | The validated graph (278 nodes) |
| `graphics/` | The 24 in-report figures, downloaded and renamed in reading order; each is captured in the graph as a hashed `RasterPicture` observable |

## Run

```bash
python examples/cti/lotus_blossom_2025/build_lotus_blossom_sagerunex.py
```

The builder computes each graphic's SHA-256 and dimensions at build time,
writes the JSON-LD, and runs `case_validate` plus the strict
concept-coverage check. Everything except the ATT&CK techniques validates
against **core UCO**; the `uco-action:Technique` metaclass, `uco-core:UcoType`,
and the technique classes validate against the local
[`attack-technique`](../../../extensions/attack-technique/) extension (the
forward-implementation of
[ucoProject/UCO PR #676](https://github.com/ucoProject/UCO/pull/676)), which
the builder loads as `extensions=["attack-technique:full"]` (RDFS inference
on).

## What it demonstrates

- **The report and its graphics as evidence.** The blog post is an
  `ObservableObject` (`URLFacet`) with its author (Joey Chen) and publisher
  (Cisco Talos); all 24 figures are hashed `RasterPicture` observables whose
  descriptions preserve the IOCs, timelines, infection chains, decompiled
  code, and config hexdumps the images carry (details absent from the prose).
- **Threat actor as an Organization.** Lotus Blossom (aliases Spring Dragon,
  Billbug, Thrip) is a `uco-identity:Organization` — UCO has no ThreatActor
  class — and its behaviors are `uco-action:Action` nodes.
- **Malware family, variants, and toolkit.** Sagerunex is a
  `uco-tool:MaliciousTool` family; the Beta/original, Dropbox-Twitter, and
  Zimbra variants are `ObservableObject`s on their timeline activity windows.
  The post-compromise toolkit (Chrome cookie stealer, Venom proxy,
  adjust-privilege, customized archiver, mtrain/HTran port relay, RAR,
  Impacket) is modeled with `toolType` and hashes where given.
- **Registry/service-DLL persistence — native UCO coverage.** The `reg add`
  commands for `tapisrv` / `swprv` / `appmgmt` map onto
  `WindowsRegistryKey` + `WindowsRegistryKeyFacet` with embedded
  `WindowsRegistryValue` (`uco-core:name` + `uco-observable:data` +
  `uco-observable:dataType` from `RegistryDatatypeVocab`: `reg_expand_sz`,
  `reg_dword`), paired with `WindowsService` (`startType` `service_auto_start`
  from `Start=2`). **No change proposal is needed** — UCO models registry
  data natively.
- **Third-party cloud C2.** Legacy VPS C2 IPs and a hardcoded proxy
  (`IPv4AddressFacet`) plus Dropbox, Twitter/X, and Zimbra webmail C2
  channels (`DomainNameFacet`), with `mail_report.rar` exfil artifacts.
- **Victimology and IOCs.** Targeted regions (Philippines, Vietnam, Hong
  Kong, Taiwan) as `Location`s, sectors as `VictimTargeting`, campaign-code
  IOCs, and Snort/ClamAV detection coverage.

## MITRE ATT&CK

The Talos prose carries **no** ATT&CK technique IDs, but the MITRE ATT&CK
group page [G0030](https://attack.mitre.org/groups/G0030/) and the Sagerunex
software page S1156 map this reporting to a set of techniques. The graph
models twelve of them (T1543.003, T1112, T1055.001, T1027.002, T1047,
T1090.001, T1102.002, T1071.001, T1560.001, T1041, T1016, T1539) using the
`uco-action:Technique` **metaclass** exactly as defined in
[ucoProject/UCO PR #676](https://github.com/ucoProject/UCO/pull/676)
(@ajnelson-nist, UCO 1.5.0). Per that PR, *"a Technique instance is an
`owl:Class` that is a subclass of `uco-action:Action`,"* anchored by the new
top-level `uco-core:UcoType`. So each ATT&CK technique is an `owl:Class`
(`a uco-action:Technique`, `rdfs:subClassOf uco-action:Action`, with
`uco-action:techniqueID`) declared in the
[`attack-technique`](../../../extensions/attack-technique/) extension's
`mitre-attack-catalog.ttl` under its canonical
`https://attack.mitre.org/techniques/<id>` IRI, and each behavior `Action`
that exhibits a technique is **typed with** that technique class (the punning
`rdf:type` edge is the association — there is no separate Technique instance
or relationship node). Until UCO 1.5.0 ships, the extension declares these
terms in their released `uco-core:` / `uco-action:` IRIs, so this exemplar's
technique data survives the upstream release unchanged.

The nine behavior Actions and the techniques they carry:

| Action | ATT&CK technique(s) |
|---|---|
| Install Sagerunex as a service via the registry | T1543.003, T1112 |
| Host and network discovery | T1016 |
| Lateral movement via WMI/Impacket | T1047 |
| Collection and exfiltration over third-party cloud | T1560.001, T1041, T1102.002 |
| DLL injection of the Sagerunex backdoor | T1055.001 |
| Obfuscate Sagerunex with VMProtect | T1027.002 |
| Internal proxying to reach the internet | T1090.001 |
| Command and control over web protocols | T1071.001 |
| Steal Chrome session cookies | T1539 |

## Validation

```
Graph nodes: 246
Graph conforms to CASE/UCO SHACL shapes with extension(s): attack-technique:full.
Conforms: True                                  # case_validate + attack-technique ontology graphs (--inference rdfs)
```
