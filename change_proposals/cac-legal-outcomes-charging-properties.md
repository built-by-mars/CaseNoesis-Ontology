<!-- Change Proposal: Declare widely-used charging and sentencing properties in cacontology-legal-outcomes -->
<!-- Target repository: CAC-Ontology (Project-VIC-International/CAC-Ontology) -->
<!-- Drafted by the CASE/UCO SDK on behalf of Project VIC International -->
<!-- Posted as: https://github.com/Project-VIC-International/CAC-Ontology/issues/40 -->

# Summary

Declare the charging/sentencing properties that CAC knowledge graphs already use heavily but that
`cacontology-legal-outcomes.ttl` never declares: `chargedWith`, `statuteCitation`,
`sentenceDurationMonths`, `phaseStatus`, and a per-count ordinal (`countNumber`), plus an alignment
decision for `FederalProsecution`, which graphs cite in the `legal-outcomes` namespace but which is
declared only in `cacontology-usa-federal-law.ttl`.

These terms currently validate "by accident": SHACL validators only check shapes for declared
target classes, so undeclared properties in the `cacontology-legal-outcomes` namespace pass
silently. The CASE/UCO SDK is adding a strict concept-coverage check that fails any graph using a
class or property not declared in a supported ontology, which makes declaring these terms upstream
(or in an extension) a prerequisite for continued validation of real case graphs.

# Evidence of use

Usage counts across the CAC-Ontology repository's own `examples_knowledge_graphs/*.ttl` and the
CASE/UCO SDK's validated PACER exemplar corpus (4 federal cases: D. Alaska `3:20-cr-00029-SLG-MMS`,
E.D. Cal. `1:20-cr-00252-JLT-BAM`, E.D. Wis. `1:25-cr-00069-WCG`, USSS complaint):

| Term (legal-outcomes ns) | Upstream example files | SDK exemplar cases | Declared today? |
|---|---|---|---|
| `chargedWith` | 7 occurrences (+4 as `cacontology:chargedWith`) | 4 | No |
| `chargeCount` | 14 occurrences | 4 | No (referenced by `ConvictionRecordShape` only) |
| `statuteCitation` | 0 | 4 | No |
| `sentenceDurationMonths` | 2 | 2 | No |
| `phaseStatus` | 0 | 4 | Only as `cacontology-asset-forfeiture:phaseStatus` |
| `FederalProsecution` | 1 | 3 | Only as `cacontology-usa-federal:FederalProsecution` |
| `jurisdiction` | 2 (+8 in other module namespaces) | covered by companion core proposal | No |

# Requirements

## Requirement 1: `chargedWith` (ObjectProperty)

```turtle
cacontology-legal-outcomes:chargedWith rdf:type owl:ObjectProperty ;
    rdfs:label "charged with"@en ;
    rdfs:comment "Links a person (or investigation subject role) to a criminal charge filed against them. A person may face multiple charges; in multi-defendant indictments each defendant links only to the counts naming them. Complements the existing hasCharge property, which links a LegalProceeding to its charges. See Fed. R. Crim. P. 7 (https://www.law.cornell.edu/rules/frcrmp/rule_7) for the charging-instrument context."@en ;
    rdfs:domain uco-identity:Person ;
    rdfs:range cacontology-legal-outcomes:CriminalCharge .
```

This is the single most load-bearing edge in federal prosecution graphs — every defendant→count
matrix in the upstream Brooklyn examples and all four SDK PACER exemplars uses it.

## Requirement 2: `statuteCitation` (DatatypeProperty)

```turtle
cacontology-legal-outcomes:statuteCitation rdf:type owl:DatatypeProperty ;
    rdfs:label "statute citation"@en ;
    rdfs:comment "The statutory citation for a criminal charge, e.g. '18 U.S.C. §§ 2251(a), (e)'. United States Code citations follow the conventions of the Office of the Law Revision Counsel (https://uscode.house.gov/)."@en ;
    rdfs:domain cacontology-legal-outcomes:CriminalCharge ;
    rdfs:range xsd:string .
```

## Requirement 3: resolve the `chargeCount` semantics collision, add `countNumber`

`cacontology-legal-outcomes-shapes.ttl` (`ConvictionRecordShape`) constrains `chargeCount` as the
**total number of charges** on a conviction record (`sh:minInclusive 1; sh:maxInclusive 100`).
Example graphs, however, use `chargeCount` on individual `FederalCharge` nodes as the **ordinal
count number** ("Count 3"). These are different concepts sharing one IRI.

Proposed resolution:

```turtle
cacontology-legal-outcomes:chargeCount rdf:type owl:DatatypeProperty ;
    rdfs:label "charge count"@en ;
    rdfs:comment "The total number of criminal charges associated with a legal proceeding or conviction record."@en ;
    rdfs:range xsd:nonNegativeInteger .

cacontology-legal-outcomes:countNumber rdf:type owl:DatatypeProperty ;
    rdfs:label "count number"@en ;
    rdfs:comment "The ordinal count number a charge holds within its charging instrument (e.g. Count 3 of an indictment). See Fed. R. Crim. P. 7(c) (https://www.law.cornell.edu/rules/frcrmp/rule_7)."@en ;
    rdfs:domain cacontology-legal-outcomes:CriminalCharge ;
    rdfs:range xsd:nonNegativeInteger .
```

This dovetails with issue #36, which already requests the `ConvictionRecord` OWL class and its
shape-referenced properties (`convictionDate`, `convictionType`, `chargeCount`, `priorConvictions`).

## Requirement 4: `sentenceDurationMonths` (DatatypeProperty)

`sentenceDuration` exists with range `xsd:duration`, but every consuming graph found in the wild
records months as a plain integer (`240`). Analysts filtering "sentences over 120 months" get no
help from `xsd:duration` lexical forms in most tooling.

```turtle
cacontology-legal-outcomes:sentenceDurationMonths rdf:type owl:DatatypeProperty ;
    rdfs:label "sentence duration in months"@en ;
    rdfs:comment "Duration of a criminal sentence expressed as a whole number of months, as stated on the judgment (e.g. AO 245B, https://www.uscourts.gov/forms/criminal-judgment-forms/judgment-criminal-case-0). Convenience companion to sentenceDuration (xsd:duration) for direct numeric comparison."@en ;
    rdfs:domain cacontology-legal-outcomes:CriminalSentence ;
    rdfs:range xsd:integer .
```

## Requirement 5: `phaseStatus` at legal-outcomes (or cac-core) level

`phaseStatus` is declared only in `cacontology-asset-forfeiture.ttl`, but graphs need it on
pre-trial/trial/sentencing phases. Either re-declare in `cacontology-legal-outcomes` with domain
`cac-core:Phase`, or promote the asset-forfeiture declaration to `cac-core` and deprecate the
module-local copy.

```turtle
cacontology-legal-outcomes:phaseStatus rdf:type owl:DatatypeProperty ;
    rdfs:label "phase status"@en ;
    rdfs:comment "Status of a legal phase (e.g. 'judgment_entered', 'scheduled', 'concluded')."@en ;
    rdfs:range xsd:string .
```

## Requirement 6: `FederalProsecution` namespace alignment

`FederalProsecution` is declared in `cacontology-usa-federal-law.ttl`, but at least one upstream
example and three SDK exemplars type prosecution nodes as
`cacontology-legal-outcomes:FederalProsecution`. Either:

- (a) add `cacontology-legal-outcomes:FederalProsecution owl:equivalentClass cacontology-usa-federal:FederalProsecution`, or
- (b) document `cacontology-usa-federal:FederalProsecution` as canonical and fix the examples.

The SDK has migrated its newest exemplar to the `usa-federal` IRI and can migrate the rest; (b) is
the cleaner outcome if maintainers agree.

# Risk / benefit

- All additions are backward compatible: no existing triple becomes invalid.
- Declaring these terms turns silent-passing data into schema-checked data, and unblocks strict
  closed-world concept validation in downstream SDKs.
- The `chargeCount` split is the only item with migration impact; existing per-charge ordinal
  usage should move to `countNumber`.

# Pre-submission notes

- Companion proposal: "core case-identification properties" (caseNumber / jurisdiction /
  located_at / Subject / participatesInEvent), filed separately.
- Related open issues: #36 (ConvictionRecord class + shape-referenced properties),
  #37 (supervised-release special conditions, payment schedule), #34 (CriminalComplaint).
- Interim measure: the CASE/UCO SDK carries these declarations in a clearly-marked local pending
  extension (`extensions/cac/local/cacontology-sdk-pending.ttl`) that will be retired when this
  lands upstream.
