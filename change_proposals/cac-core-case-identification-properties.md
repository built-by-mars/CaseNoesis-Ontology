<!-- Change Proposal: Core case-identification properties aligned with UCO/CASE -->
<!-- Target repository: CAC-Ontology (Project-VIC-International/CAC-Ontology) -->
<!-- Drafted by the CASE/UCO SDK on behalf of Project VIC International -->
<!-- Posted as: https://github.com/Project-VIC-International/CAC-Ontology/issues/41 -->

# Summary

Declare (or align) the core-level case identification terms that CAC graphs already use but that
no CAC module declares: `caseNumber`, `jurisdiction`, `located_at`, `participatesInEvent`, and the
`Subject` class. Where UCO or CASE already provides the concept, this proposal inherits it
(subproperty / equivalent class) rather than minting an independent term.

# Alignment analysis (checked against UCO 1.x and CASE 1.x)

| CAC term in use | Existing UCO/CASE concept | Recommendation |
|---|---|---|
| `cacontology:caseNumber` | `uco-core:externalIdentifier` — "An identifier for some information defined external to the UCO context" (no domain restriction); canonical richer pattern is `uco-core:externalReference` → `uco-core:ExternalReference` | Declare as `rdfs:subPropertyOf uco-core:externalIdentifier` so consumers inherit UCO identifier semantics while keeping direct CAC queryability |
| `cacontology:Subject` | **`case-investigation:Subject` already exists** (`rdfs:subClassOf uco-role:Role`, "a role whose conduct is within the scope of an investigation") | Do **not** mint a new class. Either fix examples to use `case-investigation:Subject`, or declare `cacontology:Subject owl:equivalentClass case-investigation:Subject` in `cacontology-bridge-case.ttl` for continuity |
| `cacontology:jurisdiction` | No UCO/CASE equivalent (`uco-location:Location` is a place, not a legal authority scope) | Declare once at core level; deprecate the nine per-module variants |
| `cacontology:located_at` | UCO idiom is `uco-core:Relationship` with `kindOfRelationship "Located_At"`, or `uco-action:location` for Actions | Declare as ObjectProperty with range `uco-location:Location` for direct edges, documenting the Relationship alternative |
| `cacontology:participatesInEvent` | Referenced by `cacontology-core-shapes.ttl` SPARQL constraints but **never declared** in `cacontology-core.ttl` | Declare it — same declaration-gap class as `ConvictionRecord` (issue #36) |

# Evidence of use

- `caseNumber`: 5 upstream example files (`cacontology:caseNumber`, `cacontology-core:caseNumber`)
  and all 5 CASE/UCO SDK PACER/press exemplars.
- `jurisdiction`: 25 upstream example files across **nine** ad hoc namespaces
  (`cacontology-multi`, `cacontology-trafficking`, `cacontology-legal-outcomes`,
  `cacontology-impact`, `cacontology-taskforce`, `cacontology-international`,
  `cacontology-federal`, `cacontology-core`, `cacontology`). Only `cacontology-case:jurisdictionLevel`
  and count-style properties are actually declared.
- `Subject`: 5 upstream example files + 4 SDK exemplars type defendants
  `cacontology:Subject` even though `case-investigation:Subject` exists.
- `participatesInEvent`: 3 upstream example files; `cacontology-core-shapes.ttl` lines ~319–342
  constrain it, so shape-checked data cannot currently reference a declared property.
- `located_at`: 4 SDK exemplar cases (not yet in upstream examples).

# Requirements

## Requirement 1: `caseNumber`

```turtle
cacontology:caseNumber rdf:type owl:DatatypeProperty ;
    rdfs:subPropertyOf uco-core:externalIdentifier ;
    rdfs:label "case number"@en ;
    rdfs:comment "The docket or case number assigned to an investigation or prosecution by an external case-management authority, e.g. a federal ECF docket number such as '3:20-cr-00029-SLG-MMS' (see PACER, https://pacer.uscourts.gov/). Subproperty of uco-core:externalIdentifier: the identifier is defined external to the UCO context by the issuing court or agency."@en ;
    rdfs:domain cacontology:CACInvestigation ;
    rdfs:range xsd:string .
```

## Requirement 2: `jurisdiction`

```turtle
cacontology:jurisdiction rdf:type owl:DatatypeProperty ;
    rdfs:label "jurisdiction"@en ;
    rdfs:comment "The legal jurisdiction responsible for an investigation, prosecution, or legal outcome, e.g. 'District of Alaska'. For US federal courts see 28 U.S.C. ch. 5 (https://www.law.cornell.edu/uscode/text/28/part-I/chapter-5)."@en ;
    rdfs:range xsd:string .
```

Follow-up housekeeping: mark the per-module `jurisdiction` variants as
`rdfs:subPropertyOf cacontology:jurisdiction` or deprecate them.

## Requirement 3: `located_at`

```turtle
cacontology:located_at rdf:type owl:ObjectProperty ;
    rdfs:label "located at"@en ;
    rdfs:comment "Links an investigation, organization, or legal proceeding to the uco-location:Location where it is situated or seated (e.g. the district court location). For evidence observables prefer the UCO idiom: a uco-core:Relationship with kindOfRelationship 'Located_At'."@en ;
    rdfs:range uco-location:Location .
```

## Requirement 4: `Subject` alignment

Preferred: fix upstream examples to type investigation subjects with `case-investigation:Subject`
(exists today, `rdfs:subClassOf uco-role:Role`). If continuity with published graphs matters more,
add to `cacontology-bridge-case.ttl`:

```turtle
cacontology:Subject rdf:type owl:Class ;
    owl:equivalentClass case-investigation:Subject ;
    rdfs:subClassOf uco-role:Role ;
    rdfs:label "Subject"@en ;
    rdfs:comment "Role of a person whose conduct is within the scope of a CAC investigation. Equivalent to case-investigation:Subject (https://ontology.caseontology.org/case/investigation/Subject); provided for continuity with existing CAC graphs."@en .
```

## Requirement 5: `participatesInEvent`

```turtle
cacontology:participatesInEvent rdf:type owl:ObjectProperty ;
    rdfs:label "participates in event"@en ;
    rdfs:comment "Links a person or role to a cacontology:ChildSexualAbuseEvent (or subclass) in which they participate. Declared to back the existing SPARQL constraints in cacontology-core-shapes.ttl that already traverse this property."@en ;
    rdfs:range cacontology:ChildSexualAbuseEvent .
```

# Risk / benefit

- All additions are backward compatible; the `Subject` item only adds an alias or documentation.
- Consolidating `jurisdiction` removes nine-way namespace fragmentation that currently defeats
  cross-module queries.
- Declaring `participatesInEvent` closes a shapes-reference-undeclared-term gap identical to the
  `ConvictionRecord` gap tracked in issue #36.

# Pre-submission notes

- Companion proposal: "legal-outcomes charging and sentencing properties" (chargedWith,
  statuteCitation, countNumber, sentenceDurationMonths, phaseStatus, FederalProsecution), filed
  separately.
- Interim measure: the CASE/UCO SDK carries these declarations in a clearly-marked local pending
  extension (`ontology/cac/local/cacontology-sdk-pending.ttl`) that will be retired when this
  lands upstream.
