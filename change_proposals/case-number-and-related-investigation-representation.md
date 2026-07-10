<!-- Change Proposal: Case number and related-investigation representation -->
<!-- Target repository: CASE -->
<!-- Target release: 1.5.0 -->
<!-- Appended as a comment to: https://github.com/casework/CASE/issues/191#issuecomment-4926701151 -->

_Change proposal written with the assistance of AI in response to the question opening this issue. The example graph and SPARQL queries below are CASE SHACL validated (see Pre-submission testing)._

# Target release

**Target**: CASE 1.5.0

# Background

The question opening this issue — what does "Case number" from a typical imaging tool map to? — currently has no good answer, and the gap is deeper than one property:

1. **No case number property.** `investigation:Investigation` has `investigationForm`, `investigationStatus`, and `focus`, but no identifier property. Adjacent terms don't fit: `investigation:exhibitNumber` identifies evidence items, not cases; `uco-core:name` is a display name, not an identifier; `uco-identity:IdentifierFacet` is scoped to identities ("uniquely and specifically identifies an entity" within `identity:Identity`); `uco-core:externalIdentifier` has the right semantics ("an identifier for some information defined external to the UCO context") but is generic, undiscoverable, and not associated with `Investigation` in any shape or documentation — which is why tool authors end up asking this question.

2. **No mechanism for relating investigations that carry different case numbers.** Real matters routinely span organizations, each of which opens its own case. A concrete ICAC example:

   - A technology platform's trust & safety team opens internal case `TS-2026-88041`,
   - files a **NCMEC CyberTipline** report, which receives report ID `CT-2026-1234567`,
   - NCMEC routes it to a state ICAC task force, which opens case `ICAC-AK-2026-0113`,
   - the task force refers it to a local police department, which opens case `2026-004567`,
   - local police seize an encrypted smartphone and submit it to the state crime laboratory, which opens lab case `SCDL-26-0892`.

   Five organizations, five case numbers, one investigative continuum. Today CASE cannot express that these cases are related, in what way, or in what direction — so a graph assembled from all five organizations' records (exactly the cross-tool interchange CASE exists for) cannot be traversed from CyberTip to lab report.

The same pattern appears far beyond ICAC: incident response cases escalating to regulator cases, corporate internal investigations referred to law enforcement, task-force cases spawning per-defendant prosecutions, lab submissions, and mutual legal assistance requests between jurisdictions.

**What we achieve for whom and why it matters:** Tool authors get a direct, documented answer for the ubiquitous "Case number" field; investigators and analysts get a standard way to stitch multi-agency case chains into one traversable graph; and application-domain ontologies (CAC Ontology and others) inherit both concepts from CASE instead of minting their own — the CAC Ontology has already had to propose a local `cacontology:caseNumber` ([CAC-Ontology #41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41)) precisely because CASE offers no term to inherit.

**Relationship to other proposals:** This complements the three legal process and procedure namespace proposals ([#192](https://github.com/casework/CASE/issues/192) criminal, [#193](https://github.com/casework/CASE/issues/193) civil, [#194](https://github.com/casework/CASE/issues/194) corporate): case numbers identify matters in all three arenas (police case numbers, court dockets, corporate matter numbers), and a [#194](https://github.com/casework/CASE/issues/194) `Referral` handing a corporate matter to law enforcement is exactly the event that produces a *related investigation with a new case number*. It is orthogonal to [#138](https://github.com/casework/CASE/issues/138) (Investigation as Event specialization) and to [#189](https://github.com/casework/CASE/issues/189) (process meta-model), both of which would benefit from — but do not conflict with — these terms. [UCO #554](https://github.com/ucoProject/UCO/issues/554) (work ticket concept) covers the analogous ticket-number pattern for help-desk workflows and could align with the same `externalIdentifier` grounding.

# Requirements

## Requirement 1 — `investigation:caseIdentifier`

Add a datatype property to the `investigation:` namespace:

- **Name**: `caseIdentifier` (suggested; `caseNumber` is the colloquial term but many systems issue non-numeric identifiers)
- `rdfs:subPropertyOf uco-core:externalIdentifier` — inheriting UCO's identifier semantics: the value is assigned by a case-management authority external to the graph
- Domain: `investigation:Investigation` (via SHACL property shape on the `Investigation` shape; multiple values permitted, since one organization may assign several identifiers to one case)
- Range: `xsd:string`

This directly answers the mapping table in the opening comment:

| Imaging tool field | CASE/UCO term |
|---|---|
| Case number | **`investigation:caseIdentifier`** (proposed) on the `investigation:Investigation` node |
| Description | `uco-core:description` |
| Evidence number | `investigation:exhibitNumber` |
| Examiner name | `uco-core:name` on the `investigation:Examiner` role / identity |
| Notes | `uco-observable:Note` |

## Requirement 2 — Related-investigation representation

Standardize how investigations with different case identifiers are related, using the existing `uco-core:Relationship` machinery rather than new object properties:

- Document (and optionally subclass) the pattern: a `uco-core:Relationship` whose `source` and `target` are `investigation:Investigation` nodes.
- Recommend an **open vocabulary** for `uco-core:kindOfRelationship` between investigations, e.g.: `Referred_To` (matter handed to another organization), `Escalated_To`, `Spawned` (parent case opens child case, e.g. per-defendant prosecutions), `Merged_Into`, `Parallel_To` (concurrent related cases), `Evidence_Submitted_To` (lab submission), `Successor_Of`.
- Optionally, add `investigation:InvestigationRelationship rdfs:subClassOf uco-core:Relationship` with SHACL constraining `source`/`target` to `investigation:Investigation`, so tools can *find* inter-case links without inspecting every Relationship. The committee may prefer the documentation-only variant; either resolves the gap. The example below uses the typed subclass.

## Requirement 3 — Non-prescriptive and inheritable

Both terms carry no workflow or jurisdictional commitments. Application-domain ontologies specialize them, e.g. `cacontology:caseNumber rdfs:subPropertyOf investigation:caseIdentifier` (re-parenting the [CAC-Ontology #41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41) proposal), or a lab-domain ontology declaring `lab:SubmissionRelationship rdfs:subClassOf investigation:InvestigationRelationship`.

# Risk / Benefit analysis

## Benefits

1. **Answers a real, recurring tool-mapping question** — the imaging-tool field prompting this issue is present in essentially every acquisition and case-management tool (FTK Imager, Cellebrite, Magnet AXIOM, lab LIMS).
2. **Multi-agency traversal** — one SPARQL query walks the CyberTip-to-lab chain across five organizations' graphs.
3. **Grounded in existing UCO semantics** — `caseIdentifier` refines `uco-core:externalIdentifier`; relating investigations reuses `uco-core:Relationship`. Minimal new surface area.
4. **Stops downstream forking** — CAC-Ontology #41 already had to propose `caseNumber` locally for want of a CASE parent; other domain ontologies will follow.
5. **Composes with the 1.5.0 agenda** — investigator roles (#178/#183/#187), legal process namespaces (#192–#194), and the #189 process meta-model all produce or consume case identifiers and inter-case links.

## Risks

- **Naming**: `caseIdentifier` vs `caseNumber`. Mitigation: committee choice; a `skos:altLabel "case number"` preserves findability either way.
- **Property proliferation on `Investigation`**: one property, subproperty of an existing core term — minimal.
- **Vocabulary drift** in `kindOfRelationship` values between investigations. Mitigation: publish the recommended values as a semi-open vocabulary (the same approach as `InvestigationFormVocab`), leaving room for domain values.
- **Overlap concern with `uco-identity:IdentifierFacet`**: that facet identifies *identities*; a case identifier identifies a *compilation of investigative context*. Documentation should state the distinction (it is the very confusion the opening comment raises).
- The submitter is unaware of other risks.

# Competencies demonstrated

## Competency 1

**Scenario**: The five-organization ICAC chain above: platform trust & safety case `TS-2026-88041` → NCMEC CyberTip `CT-2026-1234567` → state ICAC task force case `ICAC-AK-2026-0113` → local police case `2026-004567` → state lab case `SCDL-26-0892` (encrypted phone submission).

### Competency Question 1.1

Given the local police case number `2026-004567`, what related cases exist across all organizations, with what case identifiers, and how are they related?

#### Result 1.1

| Case | Identifier | Relation to chain |
|---|---|---|
| Platform T&S internal investigation | TS-2026-88041 | Referred_To NCMEC CyberTip intake |
| NCMEC CyberTipline report handling | CT-2026-1234567 | Referred_To state ICAC task force case |
| State ICAC task force case | ICAC-AK-2026-0113 | Referred_To local police case |
| Local police case | 2026-004567 | Evidence_Submitted_To state lab case |
| State lab examination case | SCDL-26-0892 | (terminal node) |

### Competency Question 1.2

Which investigations in the graph carry which case identifiers (the imaging-tool "Case number" lookup)?

#### Result 1.2

All five investigations return their `caseIdentifier` values in one query, regardless of which organization's tooling produced each subgraph.

### Draft SPARQL

```sparql
PREFIX investigation: <https://ontology.caseontology.org/case/investigation/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/investigation/>

SELECT ?sourceCase ?kind ?targetCase
WHERE {
    ?rel a proposed:InvestigationRelationship ;
         uco-core:source ?src ;
         uco-core:target ?tgt ;
         uco-core:kindOfRelationship ?kind .
    ?src proposed:caseIdentifier ?sourceCase .
    ?tgt proposed:caseIdentifier ?targetCase .
}

# ---

PREFIX investigation: <https://ontology.caseontology.org/case/investigation/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/investigation/>

SELECT ?investigationName ?caseId
WHERE {
    ?inv a investigation:Investigation ;
         uco-core:name ?investigationName ;
         proposed:caseIdentifier ?caseId .
}
```

# Example instance data

The example graph is available as a standalone file (`change_proposals/case-number-and-related-investigation-representation.jsonld`) for validation and SPARQL testing. Proposed terms use a `proposed:` placeholder namespace pending committee decisions. I am fine with my examples being transcribed and credited.

```json
{
  "@context": {
    "kb": "http://example.org/kb/",
    "proposed": "http://example.org/ontology/proposed/investigation/",
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:investigation-platform-ts",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "Platform trust & safety internal investigation",
      "proposed:caseIdentifier": "TS-2026-88041"
    },
    {
      "@id": "kb:investigation-ncmec-cybertip",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "NCMEC CyberTipline report handling",
      "proposed:caseIdentifier": "CT-2026-1234567"
    },
    {
      "@id": "kb:investigation-state-icac",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "State ICAC task force case",
      "proposed:caseIdentifier": "ICAC-AK-2026-0113"
    },
    {
      "@id": "kb:investigation-local-pd",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "Local police department case",
      "proposed:caseIdentifier": "2026-004567"
    },
    {
      "@id": "kb:investigation-state-lab",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "State crime laboratory examination (encrypted smartphone)",
      "proposed:caseIdentifier": "SCDL-26-0892"
    },
    {
      "@id": "kb:rel-ts-to-ncmec",
      "@type": "proposed:InvestigationRelationship",
      "uco-core:source": { "@id": "kb:investigation-platform-ts" },
      "uco-core:target": { "@id": "kb:investigation-ncmec-cybertip" },
      "uco-core:kindOfRelationship": "Referred_To",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-ncmec-to-icac",
      "@type": "proposed:InvestigationRelationship",
      "uco-core:source": { "@id": "kb:investigation-ncmec-cybertip" },
      "uco-core:target": { "@id": "kb:investigation-state-icac" },
      "uco-core:kindOfRelationship": "Referred_To",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-icac-to-local",
      "@type": "proposed:InvestigationRelationship",
      "uco-core:source": { "@id": "kb:investigation-state-icac" },
      "uco-core:target": { "@id": "kb:investigation-local-pd" },
      "uco-core:kindOfRelationship": "Referred_To",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-local-to-lab",
      "@type": "proposed:InvestigationRelationship",
      "uco-core:source": { "@id": "kb:investigation-local-pd" },
      "uco-core:target": { "@id": "kb:investigation-state-lab" },
      "uco-core:kindOfRelationship": "Evidence_Submitted_To",
      "uco-core:isDirectional": true
    }
  ]
}
```

# Solution suggestion

```turtle
@prefix investigation: <https://ontology.caseontology.org/case/investigation/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

investigation:caseIdentifier
    a owl:DatatypeProperty ;
    rdfs:subPropertyOf uco-core:externalIdentifier ;
    rdfs:label "caseIdentifier"@en ;
    skos:altLabel "case number"@en ;
    rdfs:comment "An identifier assigned to an investigation by the organization or case-management authority conducting or tracking it, e.g. a police case number, CyberTipline report ID, laboratory submission number, or court docket number. An investigation may carry multiple case identifiers. Distinct organizations investigating related matters each assign their own case identifiers; relate such investigations with an InvestigationRelationship."@en ;
    rdfs:range xsd:string .

investigation:InvestigationRelationship
    a owl:Class ;
    rdfs:subClassOf uco-core:Relationship ;
    rdfs:label "InvestigationRelationship"@en ;
    rdfs:comment "An investigation relationship is a grouping of characteristics unique to an assertion of an association between two investigations, typically conducted by different organizations under different case identifiers. Recommended kindOfRelationship values (open vocabulary): 'Referred_To', 'Escalated_To', 'Spawned', 'Merged_Into', 'Parallel_To', 'Evidence_Submitted_To', 'Successor_Of'."@en .
```

Plus a SHACL property shape adding `caseIdentifier` to the `investigation:Investigation` node shape, and `sh:class investigation:Investigation` constraints on `uco-core:source`/`uco-core:target` of `InvestigationRelationship`. If the committee prefers not to add the subclass, Requirement 2 can be met with documentation of the plain `uco-core:Relationship` pattern; `caseIdentifier` (Requirement 1) stands alone either way.

# Related proposals and references

| Reference | Relevance |
|---|---|
| This issue ([CASE #191](https://github.com/casework/CASE/issues/191)) | The tool-mapping gap this proposal fills. |
| [CAC-Ontology #41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41) | CAC had to propose a local `caseNumber` (as `rdfs:subPropertyOf uco-core:externalIdentifier`) for want of a CASE parent; it would re-parent to `investigation:caseIdentifier`. |
| [CASE #192](https://github.com/casework/CASE/issues/192) / [#193](https://github.com/casework/CASE/issues/193) / [#194](https://github.com/casework/CASE/issues/194) — legal process namespace stubs | Criminal dockets, civil actions, and corporate matters all carry case identifiers; a #194 `Referral` produces a related investigation with a new case number. |
| [CASE #189](https://github.com/casework/CASE/issues/189) — process meta-model | Workflow runs and gates operate within cases identified and chained by these terms. |
| [CASE #178](https://github.com/casework/CASE/issues/178) / [#183](https://github.com/casework/CASE/issues/183) / [#187](https://github.com/casework/CASE/issues/187) — roles | Different investigator roles sit at different links of the case chain (T&S analyst, LE investigator, lab examiner). |
| [CASE #138](https://github.com/casework/CASE/issues/138) — Investigation as Event | Orthogonal; no conflict with either superclass decision. |
| [UCO #554](https://github.com/ucoProject/UCO/issues/554) — Work ticket concept | The analogous ticket-number pattern; both ground in `uco-core:externalIdentifier`. |
| [NCMEC CyberTipline](https://www.missingkids.org/gethelpnow/cybertipline) | Real-world referral pipeline motivating the multi-organization scenario. |

# Pre-submission testing

## SPARQL query testing

| Query | Tested | Expected results match | Notes |
|-------|--------|----------------------|-------|
| CQ 1.1 — case chain with identifiers and relation kinds | Yes | Yes | 4 results: TS→CyberTip→ICAC→local PD (Referred_To ×3), local PD→lab (Evidence_Submitted_To) |
| CQ 1.2 — caseIdentifier lookup per investigation | Yes | Yes | 5 results, one per organization |

## Graph validation

```
$ make test-proposal PROPOSAL=case-number-and-related-investigation-representation
case_validate --built-version case-1.4.0 --inference rdfs --allow-info \
  --ontology-graph change_proposals/case-number-and-related-investigation-representation.ttl \
  change_proposals/case-number-and-related-investigation-representation.jsonld
Validation Report
Conforms: True
```

## Unresolved issues

- `caseIdentifier` vs `caseNumber` naming, and typed-subclass vs documentation-only for Requirement 2, are committee decisions; the example uses a `proposed:` placeholder namespace.
- Whether the recommended inter-investigation `kindOfRelationship` values should become a formal semi-open vocabulary (like `InvestigationFormVocab`) is left to committee preference.
- Human-readable IRIs are used in the example for readability; production data should use UUID-based IRIs.
