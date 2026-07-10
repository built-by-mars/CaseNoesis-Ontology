<!-- Change Proposal: Criminal process and procedure namespace (stub concepts) -->
<!-- Target repository: CASE -->
<!-- Target release: 1.5.0 -->
<!-- Posted as: https://github.com/casework/CASE/issues/192 -->

_Change proposal written with the assistance of AI. The example graph and SPARQL queries below are CASE SHACL validated (see Pre-submission testing)._

# Target release

**Target**: CASE 1.5.0

This is the first of three companion proposals suggesting that CASE add small, jurisdiction-neutral **stub namespaces** for legal process and procedure — criminal (this proposal), civil, and corporate — so that application-domain ontologies can inherit shared legal-process concepts from CASE instead of each re-inventing them. The stubs are deliberately minimal: they exist to anchor inheritance and interoperability, and domain ontologies build them out.

# Background

CASE's `investigation:` namespace provides durable investigative primitives (`Investigation`, `InvestigativeAction`, `Authorization`, `ProvenanceRecord`, and roles such as `Investigator`, `Examiner`, `Attorney`, `Subject`). It has **no concepts for the substantive criminal legal process that investigations feed**: charges, pleas, proceedings, sentences, forfeiture, and restitution. These concepts are broadly applicable across criminal investigations globally, regardless of crime type or jurisdiction.

Because the concepts are missing, downstream application-domain ontologies are each re-inventing them:

- The **[CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology)** (Project VIC International) defines `CriminalCharge`, `CriminalSentence`, `ArraignmentProceeding`, `AppealProcess`, `DefendantRole`, and related classes in its `legal-outcomes` module (60 classes), plus `AssetForfeitureAction`, `ConsentOrder`, and `ForfeitureOutcome` in its `asset-forfeiture` module (34 classes), and `FederalProsecution` and statute-specific charge classes in its `usa-federal-law` module (40 classes). Related property proposals: [CAC-Ontology #40](https://github.com/Project-VIC-International/CAC-Ontology/issues/40) (charging properties), [CAC-Ontology #41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41) (case identification).
- The **[CASE-UCO SDK `cryptoinv` extension](https://github.com/vulnmaster/CASE-UCO-SDK)** (cryptocurrency/financial-crime investigations) independently defines `CriminalCharge`, `PleaAgreement`, `SentencingOutcome`, `ForfeitureOrder`, `RestitutionOrder`, and `AssetSeizureAction`, validated against the prosecution record of *United States v. Lichtenstein & Morgan*, No. 1:23-cr-00239-CKK (D.D.C.).
- **[SOLVE-IT](https://github.com/SOLVE-IT-DF)** notation needs have surfaced similar "classes that do not yet exist" pressure ([CASE #185](https://github.com/casework/CASE/issues/185)).

Two CASE/UCO domain ontologies defining `CriminalCharge` independently, with incompatible IRIs, is exactly the interoperability failure CASE exists to prevent. Cross-domain queries ("all charges across CAC and financial-crime graphs") are impossible today.

**What we achieve for whom and why it matters:** Application-domain ontology maintainers (CAC Ontology, financial crime, trafficking, terrorism, etc.) gain a shared inheritance point for criminal legal process concepts, and tool builders gain one query vocabulary for charges, pleas, sentences, and forfeiture across all criminal investigation domains — while CASE remains non-prescriptive about any jurisdiction's procedure.

**Relationship to CASE 1.5.0 work:** This complements — and does not overlap — [CASE #189](https://github.com/casework/CASE/issues/189) (process meta-model namespaces for workflow/business rules: templates, runs, gates, assignments). #189 models *how investigative work is run*; this proposal models *the substantive legal facts and instruments* the work produces or responds to. It likewise complements the new investigator roles targeted for 1.5.0 ([CASE #178](https://github.com/casework/CASE/issues/178), [#183](https://github.com/casework/CASE/issues/183), [#187](https://github.com/casework/CASE/issues/187)): a `LawEnforcementInvestigator`'s actions produce charges and sentences that currently have no home.

**Design principles (all three companion proposals):**

1. **Stubs only.** Each class carries a label, a definitional comment, and at most a few open-vocabulary properties. Domain ontologies specialize (e.g., `cacontology:FederalCharge rdfs:subClassOf case-criminal:CriminalCharge`).
2. **Jurisdiction-neutral.** No hardcoded phases, sequences, or jurisdiction-specific instruments. Open vocabularies (`xsd:string` with recommended values) rather than closed enumerations.
3. **Separate namespace.** A new namespace (suggested: `https://ontology.caseontology.org/case/criminal/`) rather than additions to `investigation:`, keeping the investigation primitives clean and letting adopters import only what they need.

# Requirements

## Requirement 1

Define a new CASE namespace for criminal process and procedure concepts (suggested IRI: `https://ontology.caseontology.org/case/criminal/`, prefix `criminal`), imported by but separate from `investigation:`.

## Requirement 2

Define the following stub classes, each a subclass of `uco-core:UcoObject`:

| Class | Definition (summary) |
|---|---|
| `CriminalCharge` | A formal accusation, stated as a count in a charging instrument, that a person committed a specific statutory offense. Properties: `statuteCitation` (xsd:string, 1..*), `countNumber` (xsd:nonNegativeInteger, 0..1). |
| `Plea` | A defendant's formal answer to a criminal charge. Property: `pleaType` (xsd:string open vocabulary; recommended: `guilty`, `not-guilty`, `nolo-contendere`). |
| `CriminalProceeding` | A formal event in a criminal case before a tribunal. Property: `proceedingType` (xsd:string open vocabulary; recommended: `arraignment`, `preliminary-hearing`, `trial`, `plea-hearing`, `sentencing-hearing`, `appeal`). |
| `Sentence` | A penalty recommended by a party or imposed by a tribunal upon conviction. Property: `sentenceStatus` (xsd:string open vocabulary; recommended: `recommended`, `imposed`, `vacated`). |
| `ForfeitureOrder` | An order (or pre-conviction allegation) requiring surrender to the state of property involved in or traceable to an offense. |
| `RestitutionOrder` | An order (or request) that an offender compensate victims for losses caused by the offense, monetarily or in kind. |

## Requirement 3

Define one object property `concernsCharge` (domain: `Plea`, `Sentence`, `CriminalProceeding`, `ForfeitureOrder`, `RestitutionOrder`; range: `CriminalCharge`) linking process instruments to the charges they concern. All other linkage (charge-to-subject, order-to-property, document provenance) uses existing `uco-core:Relationship` and `case-investigation:ProvenanceRecord` patterns — no new relationship vocabulary is proposed.

# Risk / Benefit analysis

## Benefits

1. **Stops concept forking already underway** — CAC Ontology and the SDK `cryptoinv` extension have both independently minted `CriminalCharge`; a CASE stub gives them a common parent before more domains (trafficking, terrorism, narcotics) fork again.
2. **Cross-domain querying** — one SPARQL vocabulary for charges, pleas, sentences, and forfeiture across every criminal investigation domain.
3. **Globally applicable** — charges, pleas, sentences, forfeiture, and restitution exist in essentially all criminal justice systems; stubs carry no jurisdictional commitments.
4. **Cheap to maintain** — six classes, five datatype properties, one object property; domain complexity lives in the domain ontologies.
5. **Complements 1.5.0 roles and #189 process meta-model** — roles say *who*, #189 says *how work is organized*, this namespace says *what legal facts resulted*.

## Risks

- **Scope creep** toward a full legal ontology (e.g., LKIF, LegalRuleML territory). Mitigation: stubs only; anything jurisdiction- or procedure-specific belongs in domain ontologies. The committee may wish to note the boundary explicitly in documentation.
- **Overlap concern with `investigation:Authorization`** — warrants and court orders authorizing investigative action remain `Authorization`; `ForfeitureOrder`/`RestitutionOrder` are case *outcomes*, not investigative authorizations. Documentation should state this distinction.
- **Naming/namespace choices** (`case/criminal/` vs. additions to `investigation:`) are committee decisions; this proposal only needs *some* stable inheritance point.
- The submitter is unaware of other risks.

# Competencies demonstrated

## Competency 1

**Scenario**: A federal prosecution record (PACER: information, plea agreement, statement of facts, sentencing memorandum) is modeled as a CASE knowledge graph. The defendant is charged with money laundering conspiracy (Count One, 18 U.S.C. § 1956(h)), pleads guilty under a plea agreement, receives a government sentencing recommendation of 60 months, and consents to a forfeiture money judgment with in-kind restitution to the victim exchange. (This mirrors *United States v. Lichtenstein & Morgan*, No. 1:23-cr-00239-CKK (D.D.C.), for which a validated exemplar graph exists in the CASE-UCO SDK.)

### Competency Question 1.1

What charges were filed in the case, under which statutes, and as which counts?

#### Result 1.1

| Charge | Statute | Count |
|---|---|---|
| Money Laundering Conspiracy | 18 U.S.C. § 1956(h) | 1 |

### Competency Question 1.2

For each charge, what plea was entered and what sentence was recommended or imposed?

#### Result 1.2

| Charge | Plea | Sentence status |
|---|---|---|
| Money Laundering Conspiracy | guilty | recommended |

### Draft SPARQL

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/criminal/>

SELECT ?chargeName ?statute ?count
WHERE {
    ?charge a proposed:CriminalCharge ;
            uco-core:name ?chargeName ;
            proposed:statuteCitation ?statute .
    OPTIONAL { ?charge proposed:countNumber ?count }
}

# ---

PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/criminal/>

SELECT ?chargeName ?pleaType ?sentenceStatus
WHERE {
    ?plea a proposed:Plea ;
          proposed:pleaType ?pleaType ;
          proposed:concernsCharge ?charge .
    ?charge uco-core:name ?chargeName .
    ?sentence a proposed:Sentence ;
              proposed:sentenceStatus ?sentenceStatus ;
              proposed:concernsCharge ?charge .
}
```

# Example instance data

The example graph is also available as a standalone file (`change_proposals/criminal-process-and-procedure-namespace-stub-concepts.jsonld`) for validation and SPARQL testing. I am fine with my examples being transcribed and credited.

```json
{
  "@context": {
    "kb": "http://example.org/kb/",
    "proposed": "http://example.org/ontology/proposed/criminal/",
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:investigation-1",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "U.S. v. Example Defendant (money laundering prosecution)"
    },
    {
      "@id": "kb:defendant-1",
      "@type": "uco-identity:Person",
      "uco-core:name": "Example Defendant"
    },
    {
      "@id": "kb:charge-count1",
      "@type": "proposed:CriminalCharge",
      "uco-core:name": "Count One: Money Laundering Conspiracy",
      "proposed:statuteCitation": "18 U.S.C. § 1956(h)",
      "proposed:countNumber": { "@type": "xsd:nonNegativeInteger", "@value": "1" }
    },
    {
      "@id": "kb:plea-1",
      "@type": "proposed:Plea",
      "uco-core:name": "Guilty plea to Count One",
      "proposed:pleaType": "guilty",
      "proposed:concernsCharge": { "@id": "kb:charge-count1" }
    },
    {
      "@id": "kb:proceeding-plea-hearing",
      "@type": "proposed:CriminalProceeding",
      "uco-core:name": "Plea hearing",
      "proposed:proceedingType": "plea-hearing",
      "proposed:concernsCharge": { "@id": "kb:charge-count1" }
    },
    {
      "@id": "kb:sentence-1",
      "@type": "proposed:Sentence",
      "uco-core:name": "Government sentencing recommendation: 60 months",
      "proposed:sentenceStatus": "recommended",
      "proposed:concernsCharge": { "@id": "kb:charge-count1" }
    },
    {
      "@id": "kb:forfeiture-1",
      "@type": "proposed:ForfeitureOrder",
      "uco-core:name": "Consent order of forfeiture with money judgment",
      "proposed:concernsCharge": { "@id": "kb:charge-count1" }
    },
    {
      "@id": "kb:restitution-1",
      "@type": "proposed:RestitutionOrder",
      "uco-core:name": "In-kind restitution of forfeited assets to victim",
      "proposed:concernsCharge": { "@id": "kb:charge-count1" }
    },
    {
      "@id": "kb:rel-charged-with",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:defendant-1" },
      "uco-core:target": { "@id": "kb:charge-count1" },
      "uco-core:kindOfRelationship": "Charged_With",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-charge-part-of-investigation",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:charge-count1" },
      "uco-core:target": { "@id": "kb:investigation-1" },
      "uco-core:kindOfRelationship": "part_of",
      "uco-core:isDirectional": true
    }
  ]
}
```

# Solution suggestion

Draft Turtle for the stub classes (namespace and naming subject to committee preference):

```turtle
@prefix criminal: <https://ontology.caseontology.org/case/criminal/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

criminal:CriminalCharge
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "CriminalCharge"@en ;
    rdfs:comment "A criminal charge is a formal accusation, stated as a count within a charging instrument, that a person committed a specific statutory offense."@en .

criminal:Plea
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "Plea"@en ;
    rdfs:comment "A plea is a defendant's formal answer to a criminal charge."@en .

criminal:CriminalProceeding
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "CriminalProceeding"@en ;
    rdfs:comment "A criminal proceeding is a formal event in a criminal case conducted before a tribunal."@en .

criminal:Sentence
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "Sentence"@en ;
    rdfs:comment "A sentence is a penalty recommended by a party or imposed by a tribunal upon conviction of a criminal charge."@en .

criminal:ForfeitureOrder
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "ForfeitureOrder"@en ;
    rdfs:comment "A forfeiture order is an order, or pre-conviction allegation, requiring surrender to the state of property involved in or traceable to an offense."@en .

criminal:RestitutionOrder
    a owl:Class ;
    rdfs:subClassOf uco-core:UcoObject ;
    rdfs:label "RestitutionOrder"@en ;
    rdfs:comment "A restitution order is an order or request that an offender compensate victims for losses caused by the offense, monetarily or in kind."@en .
```

Plus datatype properties `statuteCitation`, `countNumber`, `pleaType`, `proceedingType`, `sentenceStatus` and object property `concernsCharge`, with permissive SHACL shapes (open vocabularies as `xsd:string`; only `statuteCitation` required on `CriminalCharge`). Domain ontologies then declare e.g. `cacontology:FederalCharge rdfs:subClassOf criminal:CriminalCharge` and the SDK `cryptoinv` extension retires its local duplicates.

# Related proposals and references

| Reference | Relevance |
|---|---|
| [CASE #189](https://github.com/casework/CASE/issues/189) — Process meta-model / business rules namespaces | Companion: #189 models workflow structure (templates, runs, gates); this proposal models substantive legal facts. Both are needed for workflow applications. |
| [CASE #178](https://github.com/casework/CASE/issues/178) / [#183](https://github.com/casework/CASE/issues/183) — Investigator subclasses (1.5.0) | The `LawEnforcementInvestigator` role's work product (charges, sentences) needs these stubs to be representable. |
| [CASE #187](https://github.com/casework/CASE/issues/187) — Analyst role | Same release train; roles + legal process together complete the criminal investigation picture. |
| [CASE #185](https://github.com/casework/CASE/issues/185) — SOLVE-IT notation for classes that do not yet exist | Evidence of downstream demand for missing CASE classes. |
| [CASE #146](https://github.com/casework/CASE/issues/146) — InvestigativeAction/ProvenanceRecord | Charging and sentencing instruments derive from investigative actions; provenance patterns stay unchanged. |
| [UCO #675](https://github.com/ucoProject/UCO/issues/675) — Cryptocurrency address and transaction representation | The financial-crime prosecutions motivating that proposal also produced the duplicated legal-process classes cited here. |
| [CAC-Ontology #40](https://github.com/Project-VIC-International/CAC-Ontology/issues/40), [#41](https://github.com/Project-VIC-International/CAC-Ontology/issues/41) | CAC charging/case-identification property proposals that would instead specialize these CASE stubs. |
| Companion proposals | [CASE #193](https://github.com/casework/CASE/issues/193) — Civil process and procedure namespace; [CASE #194](https://github.com/casework/CASE/issues/194) — Corporate process and procedure namespace. |

# Pre-submission testing

## SPARQL query testing

| Query | Tested | Expected results match | Notes |
|-------|--------|----------------------|-------|
| CQ 1.1 — charges with statute and count | Yes | Yes | 1 result: Count One, 18 U.S.C. § 1956(h), count 1 |
| CQ 1.2 — plea and sentence status per charge | Yes | Yes | 1 result: guilty / recommended |

## Graph validation

```
$ make test-proposal PROPOSAL=criminal-process-and-procedure-namespace-stub-concepts
case_validate --built-version case-1.4.0 --inference rdfs --allow-info \
  --ontology-graph change_proposals/criminal-process-and-procedure-namespace-stub-concepts.ttl \
  change_proposals/criminal-process-and-procedure-namespace-stub-concepts.jsonld
Validation Report
Conforms: True
```

## Unresolved issues

- Namespace IRI and class naming are committee decisions; the example data uses a `proposed:` placeholder namespace.
- Human-readable IRIs are used in the example for readability; production data should use UUID-based IRIs (informational validator notes suppressed with `--allow-info`).
