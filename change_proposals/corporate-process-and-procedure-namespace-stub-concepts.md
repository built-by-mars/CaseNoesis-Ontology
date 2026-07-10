<!-- Change Proposal: Corporate process and procedure namespace (stub concepts) -->
<!-- Target repository: CASE -->
<!-- Target release: 1.5.0 -->
<!-- Posted as: https://github.com/casework/CASE/issues/194 -->

_Change proposal written with the assistance of AI. The example graph and SPARQL queries below are CASE SHACL validated (see Pre-submission testing)._

# Target release

**Target**: CASE 1.5.0

This is the third of three companion proposals suggesting that CASE add small, jurisdiction-neutral **stub namespaces** for legal process and procedure — criminal, civil, and corporate (this proposal) — so that application-domain ontologies can inherit shared legal-process concepts from CASE instead of each re-inventing them.

# Background

Corporate and internal investigations (fraud, misconduct, insider threat, incident response, e-discovery support, regulatory response) are run under **corporate mandates, policies, and governance decisions** rather than criminal-procedure law. CASE has no concepts for that surrounding process:

- The **internal mandate/authority** under which the investigation is opened (general counsel direction, board resolution, compliance program trigger). `investigation:Authorization` is defined around "authoritative permission identified for investigative action" and is typically read as legal-process instruments; an explicit corporate mandate stub removes the ambiguity for private-sector adopters.
- The **policy violation** being investigated — the corporate analogue of a criminal charge, asserted against internal policy rather than statute.
- The **disciplinary outcome** (termination, suspension, warning) — the corporate analogue of a sentence.
- The **referral** handing the matter to law enforcement or a regulator — the bridge from corporate process into the criminal/civil namespaces proposed in the companion issues.
- The **remediation actions** (revoke access, patch, retrain) that close out the matter.

[CASE #178](https://github.com/casework/CASE/issues/178) adds a `CorporateInvestigator` role for exactly these investigations, and [CASE #189](https://github.com/casework/CASE/issues/189) proposes a **CASE-Process-Corporate** workflow scaffold with "internal mandate/authority, legal hold & preservation, HR/Legal decision gates, regulatory/referral decisions, remediation linkage as abstract milestones." Those gates and milestones need substantive objects to reference — this proposal supplies them. Legal hold and preservation are covered by the civil companion proposal (`LegalHold` serves both litigation and internal-investigation preservation).

**What we achieve for whom and why it matters:** Corporate security, HR/legal, DFIR, and insider-threat teams — plus vendors building case-management tooling on CASE — gain standard anchor points for mandate, violation, outcome, referral, and remediation, making internal investigation records auditable and portable (e.g., when a matter is referred to law enforcement, the corporate graph hands off cleanly to criminal-process concepts).

**Design principles** (shared with the criminal and civil companion proposals): stubs only; jurisdiction- and policy-neutral with open vocabularies; a separate namespace (suggested: `https://ontology.caseontology.org/case/corporate/`, prefix `corporate`) so adopters import only what they need.

# Requirements

## Requirement 1

Define a new CASE namespace for corporate process and procedure concepts (suggested IRI: `https://ontology.caseontology.org/case/corporate/`).

## Requirement 2

Define the following stub classes:

| Class | Parent | Definition (summary) |
|---|---|---|
| `CorporateInvestigationMandate` | `uco-core:UcoObject` | The internal authority under which a corporate investigation is opened (e.g., general counsel direction, board resolution, compliance-program trigger). Property: `mandateSource` (xsd:string open vocabulary, e.g. `general-counsel`, `board`, `compliance-program`, `hr`). |
| `PolicyViolation` | `uco-core:UcoObject` | An asserted breach of an internal policy, code of conduct, or contractual obligation identified by an investigation. Property: `policyCitation` (xsd:string — identifier of the policy provision). |
| `DisciplinaryOutcome` | `uco-core:UcoObject` | An employment or membership consequence resulting from an investigation. Property: `outcomeType` (xsd:string open vocabulary, e.g. `termination`, `suspension`, `written-warning`, `training`, `no-action`). |
| `Referral` | `uco-core:UcoObject` | The formal handoff of an investigated matter to an external authority (law enforcement, regulator, prosecutor). Property: `referralType` (xsd:string open vocabulary, e.g. `law-enforcement`, `regulator`, `prosecutor`). |
| `RemediationAction` | `uco-action:Action` | An action taken to correct or mitigate the condition identified by the investigation (access revocation, patching, control changes, retraining). |

## Requirement 3

Define one object property `concernsViolation` (range: `PolicyViolation`) linking outcomes, referrals, and remediation actions to the violation they respond to. Linkage of the mandate to the `investigation:Investigation`, and of a `Referral` to the resulting criminal/civil matter, uses existing `uco-core:Relationship` patterns (and the companion criminal/civil stubs when adopted).

# Risk / Benefit analysis

## Benefits

1. **Completes the 1.5.0 corporate story** — `CorporateInvestigator` ([#178](https://github.com/casework/CASE/issues/178)) plus the CASE-Process-Corporate scaffold ([#189](https://github.com/casework/CASE/issues/189)) currently have no substantive objects for mandates, violations, outcomes, referrals, or remediation.
2. **Cross-sector handoff** — a `Referral` node is the explicit bridge from a corporate matter into criminal or civil process, so a single graph can trace insider-threat conduct from internal detection through prosecution.
3. **Auditability and defensibility** — corporate investigations increasingly require documented mandate and proportionality (e.g., works-council and privacy regimes); an explicit mandate object anchors that record.
4. **Globally applicable** — mandates, policy violations, disciplinary outcomes, referrals, and remediation exist in private-sector investigations worldwide.
5. **Cheap to maintain** — five classes, four datatype properties, one object property.

## Risks

- **Boundary with #189's process meta-model**: gates/assignments/statuses belong to #189, not here. Mitigation: this namespace holds substantive facts only; the proposals are drafted to compose, not overlap.
- **Boundary with `investigation:Authorization`**: where a mandate legally authorizes specific investigative actions, dual-typing or a `Relationship` to an `Authorization` remains available; documentation should show the pattern.
- **HR/privacy sensitivity** — disciplinary data is personal data. Mitigation: the stubs prescribe no personal attributes; adopters apply their data-protection controls (and UCO marking vocabularies) as usual.
- The submitter is unaware of other risks.

# Competencies demonstrated

## Competency 1

**Scenario**: A corporate security team investigates insider data exfiltration. The investigation is opened under a general-counsel mandate; it substantiates a violation of the acceptable-use policy; the employee is terminated; the matter is referred to law enforcement; and remediation revokes the employee's access and tightens DLP controls. The CASE graph of the forensic work must anchor all five facts.

### Competency Question 1.1

Under what mandate was the investigation conducted, and what policy violations did it substantiate?

#### Result 1.1

| Mandate | Violation |
|---|---|
| General counsel mandate GC-2026-011 | Acceptable Use Policy § 4.2 (unauthorized data transfer) |

### Competency Question 1.2

What outcomes, referrals, and remediation followed from the substantiated violation?

#### Result 1.2

| Response | Type |
|---|---|
| Employment terminated | DisciplinaryOutcome (termination) |
| Referral to law enforcement | Referral (law-enforcement) |
| Access revocation and DLP rule tightening | RemediationAction |

### Draft SPARQL

```sparql
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/corporate/>

SELECT ?mandateName ?violationName ?policy
WHERE {
    ?mandate a proposed:CorporateInvestigationMandate ;
             uco-core:name ?mandateName .
    ?violation a proposed:PolicyViolation ;
               uco-core:name ?violationName ;
               proposed:policyCitation ?policy .
}

# ---

PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX proposed: <http://example.org/ontology/proposed/corporate/>

SELECT ?responseName ?responseType
WHERE {
    ?response proposed:concernsViolation ?violation ;
              uco-core:name ?responseName ;
              a ?responseType .
    FILTER (?responseType IN (proposed:DisciplinaryOutcome, proposed:Referral, proposed:RemediationAction))
}
```

# Example instance data

The example graph is also available as a standalone file (`change_proposals/corporate-process-and-procedure-namespace-stub-concepts.jsonld`) for validation and SPARQL testing. I am fine with my examples being transcribed and credited.

```json
{
  "@context": {
    "kb": "http://example.org/kb/",
    "proposed": "http://example.org/ontology/proposed/corporate/",
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "kb:investigation-1",
      "@type": "case-investigation:Investigation",
      "uco-core:name": "Insider data exfiltration investigation 2026-INV-007"
    },
    {
      "@id": "kb:mandate-1",
      "@type": "proposed:CorporateInvestigationMandate",
      "uco-core:name": "General counsel mandate GC-2026-011",
      "proposed:mandateSource": "general-counsel"
    },
    {
      "@id": "kb:violation-1",
      "@type": "proposed:PolicyViolation",
      "uco-core:name": "Acceptable Use Policy § 4.2 (unauthorized data transfer)",
      "proposed:policyCitation": "AUP-4.2"
    },
    {
      "@id": "kb:outcome-1",
      "@type": "proposed:DisciplinaryOutcome",
      "uco-core:name": "Employment terminated",
      "proposed:outcomeType": "termination",
      "proposed:concernsViolation": { "@id": "kb:violation-1" }
    },
    {
      "@id": "kb:referral-1",
      "@type": "proposed:Referral",
      "uco-core:name": "Referral to law enforcement",
      "proposed:referralType": "law-enforcement",
      "proposed:concernsViolation": { "@id": "kb:violation-1" }
    },
    {
      "@id": "kb:remediation-1",
      "@type": "proposed:RemediationAction",
      "uco-core:name": "Access revocation and DLP rule tightening",
      "proposed:concernsViolation": { "@id": "kb:violation-1" }
    },
    {
      "@id": "kb:rel-mandate-authorizes-investigation",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:mandate-1" },
      "uco-core:target": { "@id": "kb:investigation-1" },
      "uco-core:kindOfRelationship": "Mandates",
      "uco-core:isDirectional": true
    },
    {
      "@id": "kb:rel-violation-found-by-investigation",
      "@type": "uco-core:Relationship",
      "uco-core:source": { "@id": "kb:violation-1" },
      "uco-core:target": { "@id": "kb:investigation-1" },
      "uco-core:kindOfRelationship": "Substantiated_By",
      "uco-core:isDirectional": true
    }
  ]
}
```

# Solution suggestion

Draft Turtle stubs (namespace and naming subject to committee preference): four `owl:Class` declarations subclassing `uco-core:UcoObject` (`CorporateInvestigationMandate`, `PolicyViolation`, `DisciplinaryOutcome`, `Referral`) and one subclassing `uco-action:Action` (`RemediationAction`), datatype properties `mandateSource`, `policyCitation`, `outcomeType`, `referralType` (`xsd:string` open vocabularies), and object property `concernsViolation`, with permissive SHACL shapes. See the criminal companion proposal for the full Turtle pattern.

Domain ontologies then specialize, e.g. an insider-threat ontology declaring `insider:DataExfiltrationViolation rdfs:subClassOf corporate:PolicyViolation`.

# Related proposals and references

| Reference | Relevance |
|---|---|
| [CASE #189](https://github.com/casework/CASE/issues/189) — Process meta-model / business rules namespaces | Companion: the CASE-Process-Corporate scaffold's gates and milestones reference the substantive objects proposed here. |
| [CASE #178](https://github.com/casework/CASE/issues/178) / [#183](https://github.com/casework/CASE/issues/183) — Investigator subclasses (1.5.0) | `CorporateInvestigator`'s work products (violations, outcomes, referrals) need these stubs. |
| [CASE #187](https://github.com/casework/CASE/issues/187) — Analyst role | Same release train. |
| [CASE #146](https://github.com/casework/CASE/issues/146) — InvestigativeAction/ProvenanceRecord | Corporate findings keep standard provenance chains; the stubs add mandate and disposition anchors. |
| Companion proposals | [CASE #192](https://github.com/casework/CASE/issues/192) — Criminal process and procedure namespace (referral target); [CASE #193](https://github.com/casework/CASE/issues/193) — Civil process and procedure namespace (`LegalHold` covers internal preservation). |
| [DOJ Justice Manual 9-28.000](https://www.justice.gov/jm/jm-9-28000-principles-federal-prosecution-business-organizations) | Principles of federal prosecution of business organizations — cited in #178 for the corporate investigator; motivates the referral bridge modeled here. |

# Pre-submission testing

## SPARQL query testing

| Query | Tested | Expected results match | Notes |
|-------|--------|----------------------|-------|
| CQ 1.1 — mandate and substantiated violations | Yes | Yes | 1 result: GC-2026-011 / AUP-4.2 |
| CQ 1.2 — outcomes, referrals, remediation | Yes | Yes | 3 results: termination, law-enforcement referral, remediation action |

## Graph validation

```
$ make test-proposal PROPOSAL=corporate-process-and-procedure-namespace-stub-concepts
case_validate --built-version case-1.4.0 --inference rdfs --allow-info \
  --ontology-graph change_proposals/corporate-process-and-procedure-namespace-stub-concepts.ttl \
  change_proposals/corporate-process-and-procedure-namespace-stub-concepts.jsonld
Validation Report
Conforms: True
```

## Unresolved issues

- Namespace IRI and class naming are committee decisions; the example data uses a `proposed:` placeholder namespace.
- Whether `CorporateInvestigationMandate` should instead be a subclass of `investigation:Authorization` is a design question for committee discussion (this draft keeps it a sibling to avoid implying legal-process semantics).
- Human-readable IRIs are used in the example for readability; production data should use UUID-based IRIs.
