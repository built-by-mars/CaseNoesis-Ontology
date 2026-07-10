# Controlled Substances Extension (`drug`)

Investigation-domain class and properties for seized or charged quantities
of controlled substances. Replaces the earlier convention of typing drug
evidence as bare `uco-core:UcoObject` with substance, schedule, mass, and
purity buried in `uco-core:description`, which made cross-case queries such
as "all Schedule II seizures over 500 g" impossible.

## Contents

| File | Purpose |
|---|---|
| `drugs.ttl` | OWL T-Box: `drug:ControlledSubstance`; properties `substance` (ChEBI IRI reference), `substanceName`, `csaSchedule`, `substanceForm`, `mass`, `massUnit`, `purity`, `purityBasis`, `quantityDescription` |
| `drugs-shapes.ttl` | SHACL shapes (permissive: datatype/node-kind/cardinality only, nothing required) |
| `drugs-profile-gufo.ttl` | Bridge: `drug:ControlledSubstance rdfs:subClassOf gufo:Quantity` for [gUFO](https://nemo-ufes.github.io/gufo/)-profiled graphs |
| `drugs-exemplar.ttl` | A-Box exemplar (meth-mixture conspiracy quantity from *U.S. v. Lindell*, D.N.D. 3:25-cr-00005) |

## Design

- **Portion, not kind.** `drug:ControlledSubstance` is the concrete seized
  or charged quantity of matter (the bag of methamphetamine), subclassing
  `uco-core:UcoObject` so it participates natively in Relationships,
  Actions, forfeiture orders, and chain of custody. In gUFO terms it is a
  `gufo:Quantity` (amount of matter) — not `gufo:FunctionalComplex`, which
  fits artifacts like weapons and vehicles.
- **Chemical identity is delegated to
  [ChEBI](https://obofoundry.org/ontology/chebi.html)** (OBO Foundry,
  CC-BY, BFO-compatible) via the `drug:substance` IRI reference:
  methamphetamine `CHEBI_6809`, fentanyl `CHEBI_119915`, cocaine
  `CHEBI_27958`, heroin `CHEBI_27808`. Per the realist analysis behind the
  OBO [Drug Ontology (DrOn)](https://obofoundry.org/ontology/dron), the
  portion is *linked to*, not *typed by*, the molecule class. For diverted
  pharmaceutical products (tablets, NDC codes), reference DrOn classes the
  same way.
- **Regulation is local.** No open ontology covers CSA scheduling or the
  Sentencing Guidelines mixture-vs-actual distinction, so `csaSchedule` and
  `purityBasis` carry them as open-vocabulary properties with statutory
  citations (21 U.S.C. §§ 802, 812, 841(b); USSG § 2D1.1).

## Usage

```python
meth = {
    "@id": uid("item-meth-mixture"),
    "@type": "drug:ControlledSubstance",
    "uco-core:name": "Methamphetamine mixture (Count 2 conspiracy)",
    "drug:substance": {"@id": "http://purl.obolibrary.org/obo/CHEBI_6809"},
    "drug:csaSchedule": "II",
    "drug:mass": 500,
    "drug:massUnit": "g",
    "drug:purityBasis": "mixture",
    "drug:quantityDescription": "500 grams or more of a mixture and "
        "substance containing a detectable amount of methamphetamine",
}
```

Validate with the extension:

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/drugs/drugs.ttl \
  --ontology-graph extensions/drugs/drugs-shapes.ttl \
  --inference rdfs --allow-info graph.jsonld
```

or via the MCP tool: `validate_graph(path, extensions=["drugs"])`.

## Status

Local extension, not yet proposed upstream. Drug evidence sits outside
UCO's cyber scope but inside CASE's investigative scope; candidate for the
CDO Community Playground and eventually a CASE proposal. The `example.org`
namespace is a placeholder pending a community namespace decision (same
convention as the `cryptoinv` extension).
