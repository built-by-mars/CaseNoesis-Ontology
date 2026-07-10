# Racketeering and Criminal Enterprise Extension (`rico`)

Investigation-domain classes and properties for racketeering (RICO)
prosecutions: the charged **enterprise** — including association-in-fact
enterprises that are not legal entities — the **functional roles** members
serve within it, and the statutory **predicate categories** of racketeering
activity enumerated in a RICO count. Replaces the earlier convention of
describing the enterprise in a plain `uco-identity:Organization` description
string, which made cross-case queries such as "all association-in-fact
enterprises whose predicates include § 1343 wire fraud" impossible.

## Contents

| File | Purpose |
|---|---|
| `rico.ttl` | OWL T-Box: `rico:RacketeeringEnterprise`, `rico:EnterpriseRole`; properties `enterpriseType`, `roleFunction`, `predicateStatute` |
| `rico-shapes.ttl` | SHACL shapes (permissive: datatype/node-kind/cardinality; `enterpriseType` and `roleFunction` required on their classes) |
| `rico-exemplar.ttl` | A-Box exemplar (the "SE Enterprise" from *U.S. v. Lam et al.*, D.D.C. 1:24-cr-00417-CKK) |

## Design

- **The enterprise is an Organization.** 18 U.S.C. § 1961(4) defines
  "enterprise" to include legal entities *and* "any union or group of
  individuals associated in fact although not a legal entity."
  `rico:RacketeeringEnterprise` subclasses `uco-identity:Organization`
  ("a grouping of people organized for a purpose"), which accommodates
  both branches; `rico:enterpriseType` records which branch is charged
  (`legal-entity` / `association-in-fact`). *Boyle v. United States*, 556
  U.S. 938 (2009) requires only purpose, relationships, and longevity for
  an association-in-fact — carried as ordinary UCO descriptions,
  `Member_Of` relationships, and existence intervals.
- **Roles are role nodes, not prose.** RICO indictments allege a division
  of labor (organizers, callers, money launderers, residential burglars,
  database hackers). `rico:EnterpriseRole` subclasses `uco-role:Role`;
  persons link to roles with `Has_Role` relationships and roles to the
  enterprise with `Role_Within`, so several persons can share a function
  and one person can hold several.
- **Predicates are queryable.** `rico:predicateStatute` (repeatable,
  domain-free string) records each statutory category of racketeering
  activity (18 U.S.C. § 1961(1)) enumerated in the count — attach it to
  the RICO `legalproc:CriminalCharge` node. The pattern requirement
  (two acts within ten years, § 1961(5)) stays in the charge description.
- **Everything else is reused.** Charges, pleas, verdicts, sentences, and
  forfeiture come from the `legalproc` extension (CASE issue #192 stubs);
  virtual-asset observables from `cryptoinv` (UCO issue #675); firearms
  from `weapons`. This extension adds only what racketeering needs beyond
  them.

## Usage

```python
enterprise = {
    "@id": uid("org-se-enterprise"),
    "@type": ["rico:RacketeeringEnterprise", "uco-identity:Organization"],
    "uco-core:name": "The Social Engineering Enterprise (SE Enterprise)",
    "rico:enterpriseType": "association-in-fact",
}
role = {
    "@id": uid("role-money-launderer"),
    "@type": ["rico:EnterpriseRole", "uco-role:Role"],
    "rico:roleFunction": "money-launderer",
}
rico_count = {
    "@id": uid("charge-lam-count1ss"),
    "@type": "legalproc:CriminalCharge",
    "legalproc:statuteCitation": "18 U.S.C. § 1962(d)",
    "legalproc:offenseForm": "conspiracy",
    "rico:predicateStatute": [
        "18 U.S.C. § 1343 (wire fraud)",
        "18 U.S.C. § 1956 (laundering of monetary instruments)",
    ],
}
```

Validate with the extension (plus `legalproc` for the charge classes):

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/rico/rico.ttl \
  --ontology-graph extensions/rico/rico-shapes.ttl \
  --ontology-graph extensions/legalproc/legalproc.ttl \
  --ontology-graph extensions/legalproc/legalproc-shapes.ttl \
  --inference rdfs --allow-info graph.jsonld
```

or via the MCP tool: `validate_graph(path, extensions=["rico", "legalproc"])`.

## Status

Local extension, not yet proposed upstream. Racketeering enterprises sit
inside CASE's investigative scope; candidate for the CDO Community
Playground and a CASE change proposal (see
`change_proposals/racketeering-enterprise-and-enterprise-roles.md`). The
`example.org` namespace is a placeholder pending a community namespace
decision (same convention as the `cryptoinv`, `drugs`, and `weapons`
extensions).
