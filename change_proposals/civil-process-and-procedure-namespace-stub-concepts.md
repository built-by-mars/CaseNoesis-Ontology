<!-- Change Proposal: Civil process and procedure namespace (stub concepts) -->
<!-- Target repository: CASE -->
<!-- Target release: 1.5.0 -->
<!-- Posted as: https://github.com/casework/CASE/issues/193 -->

_Change proposal written with the assistance of AI. The example graph and SPARQL queries below are CASE SHACL validated (see Pre-submission testing)._

# Target release

**Target**: CASE 1.5.0

This is the second of three companion proposals suggesting that CASE add small, jurisdiction-neutral **stub namespaces** for legal process and procedure — criminal, civil (this proposal), and corporate — so that application-domain ontologies can inherit shared legal-process concepts from CASE instead of each re-inventing them.

# Background

Digital investigations are deeply interrelated with **civil** legal process, yet CASE has no concepts for it. Common patterns with no CASE anchor today:

- **E-discovery**: a civil action triggers a litigation hold; forensic collections and productions respond to discovery requests. The entire EDRM workflow sits on top of investigative actions that CASE *can* represent, but the civil action, hold, and requests that motivate them cannot be expressed.
- **Civil enforcement**: regulators (FTC, SEC, data protection authorities) run investigations that end in civil complaints, injunctions, consent decrees, and civil judgments rather than criminal charges.
- **Civil asset forfeiture** proceeds *in rem* without any criminal charge.
- **Protective orders and injunctions** in exploitation, harassment, and IP-theft matters constrain how investigative evidence is handled and disclosed.
- **Private civil actions** (torts, breach of contract, class actions after data breaches) both consume investigation output and trigger new investigations.

`investigation:Authorization` covers "authoritative permission identified for investigative action" (warrants, consent), but a complaint, hold, discovery request, judgment, or settlement is not an authorization for investigative action — these are the surrounding civil process facts, and they currently have no home.

**What we achieve for whom and why it matters:** E-discovery platforms, corporate legal teams, regulators, and civil litigators gain standard CASE anchor points explaining *why* evidence is preserved, collected, and produced — enabling auditable, interoperable representations of preservation obligations and productions — while application-domain ontologies (e-discovery, regulatory enforcement, data protection) inherit and specialize the stubs.

**Relationship to CASE 1.5.0 work:** [CASE #178](https://github.com/casework/CASE/issues/178) adds `CorporateInvestigator`, `RegulatoryInvestigator`, `InsuranceInvestigator`, `PrivateInvestigator`, and `CivilSocietyInvestigator` roles — the investigator types whose work is dominated by civil (not criminal) process. Those roles have no civil process objects to attach their work to. [CASE #189](https://github.com/casework/CASE/issues/189) proposes process meta-model scaffolds (LE and corporate); its gates and milestones need civil process facts (holds, discovery deadlines) to reference.

**Design principles** (shared with the criminal and corporate companion proposals): stubs only; jurisdiction-neutral with open vocabularies; a separate namespace (suggested: `https://ontology.caseontology.org/case/civil/`, prefix `civil`) so adopters import only what they need.

# Requirements

## Requirement 1

Define a new CASE namespace for civil process and procedure concepts (suggested IRI: `https://ontology.caseontology.org/case/civil/`).

## Requirement 2

Define the following stub classes, each a subclass of `uco-core:UcoObject`:

| Class | Definition (summary) |
|---|---|
| `CivilAction` | A legal proceeding in which a party seeks a civil remedy (damages, injunction, declaratory relief) rather than criminal punishment. Property: `causeOfAction` (xsd:string open vocabulary, e.g. `negligence`, `breach-of-contract`, `statutory-violation`, `in-rem-forfeiture`). |
| `CivilProceeding` | A formal event in a civil matter before a tribunal (hearing, deposition, trial, appeal). Property: `proceedingType` (xsd:string open vocabulary). |
| `LegalHold` | A preservation obligation requiring a party to retain information relevant to reasonably anticipated or pending litigation or regulatory action. |
| `DiscoveryRequest` | A formal demand in a civil matter for information, documents, or testimony (interrogatories, requests for production, subpoenas duces tecum). Property: `discoveryType` (xsd:string open vocabulary). |
| `CivilJudgment` | A tribunal's final determination of the parties' rights and obligations in a civil matter, including injunctions and consent decrees. Property: `judgmentType` (xsd:string open vocabulary, e.g. `money-judgment`, `injunction`, `consent-decree`, `declaratory`, `dismissal`). |
| `Settlement` | A voluntary resolution of a civil dispute between parties, with or without tribunal approval. |

## Requirement 3

Define one object property `concernsCivilAction` (range: `CivilAction`) linking holds, discovery requests, proceedings, judgments, and settlements to the civil matter they belong to. Party roles (plaintiff, defendant/respondent) reuse the existing `uco-role:Role` pattern and `uco-core:Relationship`; no new role classes are proposed here (they could later join the #178 role work).

# Risk / Benefit analysis

## Benefits

1. **Closes the e-discovery gap** — the single largest commercial use of digital forensics has no CASE representation of the obligations (hold, discovery request) that drive it. This directly serves the corporate scaffold envisioned in [CASE #189](https://github.com/casework/CASE/issues/189).
2. **Covers regulator and civil-investigator workflows** — the new 1.5.0 investigator roles (regulatory, corporate, insurance, private) predominantly produce civil outcomes.
3. **Globally applicable** — civil claims, preservation duties, discovery/disclosure, judgments, and settlements exist across common-law and civil-law systems; stubs carry no jurisdictional commitments.
4. **Auditability** — a production or preservation action can point at the hold or request that legally justified it, complementing `ProvenanceRecord` chains.
5. **Cheap to maintain** — six classes, four datatype properties, one object property.

## Risks

- **Overlap concern with `investigation:Authorization`**: a discovery subpoena can *authorize* collection. Mitigation: where an instrument authorizes investigative action, it may additionally be modeled as an `Authorization`; the civil stubs capture the instrument's role in the civil matter. Documentation should show the dual-typing pattern.
- **Scope creep** toward full litigation ontologies (LKIF, LegalRuleML, EDRM reference models). Mitigation: stubs only; domain ontologies specialize.
- **Common-law bias in naming** (e.g., "discovery"). Mitigation: definitional comments are drafted functionally (demand for information in a civil matter) so disclosure-based systems fit; the committee may prefer more neutral labels.
- The submitter is unaware of other risks.

# Competencies demonstrated

## Competency 1

**Scenario**: After a data breach investigation, the breached company faces a class action. A litigation hold obligates preservation of the investigation's forensic corpus; a request for production seeks the incident timeline and forensic images; the company produces derived reports; the matter ends in a court-approved settlement. The CASE graph must show which investigative evidence was preserved and produced under which civil obligations.

### Competency Question 1.1

Which preservation and discovery obligations attach to the civil action, and what investigative evidence do they cover?

#### Result 1.1

| Instrument | Civil action | Covered evidence |
|---|---|---|
| Litigation hold 2026-LH-014 | Doe v. Example Corp. | Breach investigation forensic corpus |
| Request for production No. 3 | Doe v. Example Corp. | Incident timeline and forensic images |

### Competency Question 1.2

How was the civil action resolved?

#### Result 1.2

| Civil action | Resolution |
|---|---|
| Doe v. Example Corp. | Court-approved settlement |

### Draft SPARQL

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/civil/>

SELECT ?instrument ?instrumentName ?actionName
WHERE {
    ?instrument proposed:concernsCivilAction ?action ;
                uco-core:name ?instrumentName .
    ?action uco-core:name ?actionName .
    { ?instrument a proposed:LegalHold } UNION { ?instrument a proposed:DiscoveryRequest }
}

# ---

PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/civil/>

SELECT ?actionName ?resolutionName
WHERE {
    ?resolution proposed:concernsCivilAction ?action ;
                uco-core:name ?resolutionName .
    ?action uco-core:name ?actionName .
    { ?resolution a proposed:Settlement } UNION { ?resolution a proposed:CivilJudgment }
}
```

# Example instance data

The example graph is also available as a standalone file (`change_proposals/civil-process-and-procedure-namespace-stub-concepts.jsonld`) for validation and SPARQL testing. I am fine with my examples being transcribed and credited.

```json
{
  "@context": {
    "kb": "http://example.org/kb/",
    "proposed": "http://example.org/ontology/proposed/civil/",
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:investigation-1",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "Example Corp. data breach investigation"
    },
    {
      "@id": "kb:forensic-corpus-1",
      "@type": "uco-observable:ObservableObject",
      "uco-core:name": "Breach investigation forensic corpus"
    },
    {
      "@id": "kb:civil-action-1",
      "@type": "proposed:CivilAction",
      "uco-core:name": "Doe v. Example Corp.",
      "proposed:causeOfAction": "negligence"
    },
    {
      "@id": "kb:legal-hold-1",
      "@type": "proposed:LegalHold",
      "uco-core:name": "Litigation hold 2026-LH-014",
      "proposed:concernsCivilAction": { "@id": "kb:civil-action-1" }
    },
    {
      "@id": "kb:discovery-request-1",
      "@type": "proposed:DiscoveryRequest",
      "uco-core:name": "Request for production No. 3",
      "proposed:discoveryType": "request-for-production",
      "proposed:concernsCivilAction": { "@id": "kb:civil-action-1" }
    },
    {
      "@id": "kb:deposition-1",
      "@type": "proposed:CivilProceeding",
      "uco-core:name": "Deposition of incident response lead",
      "proposed:proceedingType": "deposition",
      "proposed:concernsCivilAction": { "@id": "kb:civil-action-1" }
    },
    {
      "@id": "kb:settlement-1",
      "@type": "proposed:Settlement",
      "uco-core:name": "Court-approved class settlement",
      "proposed:concernsCivilAction": { "@id": "kb:civil-action-1" }
    },
    {
      "@id": "kb:rel-hold-preserves-corpus",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:legal-hold-1" },
      "uco-core:target": { "@id": "kb:forensic-corpus-1" },
      "uco-core:kindOfRelationship": "Preserves",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-request-seeks-corpus",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:discovery-request-1" },
      "uco-core:target": { "@id": "kb:forensic-corpus-1" },
      "uco-core:kindOfRelationship": "Seeks_Production_Of",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-action-arises-from-investigation",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:civil-action-1" },
      "uco-core:target": { "@id": "kb:investigation-1" },
      "uco-core:kindOfRelationship": "Arises_From",
      "uco-core:isDirectional": true
    }
  ]
}
```

# Solution suggestion

Draft Turtle stubs (namespace and naming subject to committee preference): six `owl:Class` declarations subclassing `uco-core:UcoObject` (`CivilAction`, `CivilProceeding`, `LegalHold`, `DiscoveryRequest`, `CivilJudgment`, `Settlement`), datatype properties `causeOfAction`, `proceedingType`, `discoveryType`, `judgmentType` (all `xsd:string` open vocabularies), and object property `concernsCivilAction`, with permissive SHACL shapes. See the criminal companion proposal for the full Turtle pattern; the civil file is identical in style.

Domain ontologies then specialize, e.g. an e-discovery ontology declaring `ediscovery:PreservationNotice rdfs:subClassOf civil:LegalHold`.

# Related proposals and references

| Reference | Relevance |
|---|---|
| [CASE #189](https://github.com/casework/CASE/issues/189) — Process meta-model / business rules namespaces | Companion: #189's corporate/LE workflow scaffolds need civil process facts (holds, discovery deadlines) as gate/milestone referents. |
| [CASE #178](https://github.com/casework/CASE/issues/178) / [#183](https://github.com/casework/CASE/issues/183) — Investigator subclasses (1.5.0) | Corporate, regulatory, insurance, private, and civil-society investigator roles produce civil outcomes that need these stubs. |
| [CASE #187](https://github.com/casework/CASE/issues/187) — Analyst role | Same release train. |
| [CASE #146](https://github.com/casework/CASE/issues/146) — InvestigativeAction/ProvenanceRecord | Productions responding to discovery requests keep their provenance chains; the stubs add the *why*. |
| Companion proposals | [CASE #192](https://github.com/casework/CASE/issues/192) — Criminal process and procedure namespace; [CASE #194](https://github.com/casework/CASE/issues/194) — Corporate process and procedure namespace. |
| [EDRM](https://edrm.net/) | Industry reference model for e-discovery whose stages (preservation, collection, production) motivate `LegalHold`/`DiscoveryRequest`. Cited for motivation only; no EDRM dependency proposed. |

# Pre-submission testing

## SPARQL query testing

| Query | Tested | Expected results match | Notes |
|-------|--------|----------------------|-------|
| CQ 1.1 — obligations attached to the civil action | Yes | Yes | 2 results: litigation hold + request for production |
| CQ 1.2 — resolution of the civil action | Yes | Yes | 1 result: court-approved settlement |

## Graph validation

```
$ make test-proposal PROPOSAL=civil-process-and-procedure-namespace-stub-concepts
case_validate --built-version case-1.4.0 --inference rdfs --allow-info \
  --ontology-graph change_proposals/civil-process-and-procedure-namespace-stub-concepts.ttl \
  change_proposals/civil-process-and-procedure-namespace-stub-concepts.jsonld
Validation Report
Conforms: True
```

## Unresolved issues

- Namespace IRI, class naming, and whether party roles (plaintiff/respondent) should join the #178 role hierarchy are committee decisions; the example data uses a `proposed:` placeholder namespace.
- Human-readable IRIs are used in the example for readability; production data should use UUID-based IRIs.
