# Weapons and Firearms Extension (`weap`)

Investigation-domain classes and properties for weapon evidence — firearms,
ammunition, and edged weapons recovered, used, or charged in criminal cases.
Replaces the earlier convention of typing weapons as bare
`uco-core:UcoObject` (dual-typed `gufo:FunctionalComplex`) with make, model,
caliber, and serial data buried in `uco-core:description`, which made
cross-case queries such as "all handguns with obliterated serials"
impossible.

## Contents

| File | Purpose |
|---|---|
| `weapons.ttl` | OWL T-Box: `weap:Weapon`, `weap:Firearm`, `weap:Handgun`, `weap:LongGun`, `weap:Rifle`, `weap:Shotgun`, `weap:CuttingWeapon`, `weap:Ammunition`; properties `make`, `model`, `caliber`, `serialNumber`, `serialNumberObliterated` |
| `weapons-shapes.ttl` | SHACL shapes (permissive: datatype/cardinality only, nothing required) |
| `weapons-profile-cco.ttl` | Bridge: subclass axioms into the [Common Core Ontologies](https://github.com/CommonCoreOntology/CommonCoreOntologies) Artifact Ontology weapon hierarchy (BFO 2020 mid-level; DoD/IC baseline; IEEE P3195.1) |
| `weapons-profile-gufo.ttl` | Bridge: `weap:Weapon rdfs:subClassOf gufo:FunctionalComplex` for [gUFO](https://nemo-ufes.github.io/gufo/)-profiled graphs |
| `weapons-exemplar.ttl` | A-Box exemplar (SIG Sauer P365 from *U.S. v. Lindell*, D.N.D. 3:25-cr-00005; rifle/pistol from *U.S. v. Perry & O'Dell*, W.D. Mo. 2:22-cr-04065) |

## Design

- Every class subclasses `uco-core:UcoObject`, so weapon instances
  participate natively in CASE/UCO graphs: `uco-core:Relationship`
  (`Possessed`, `Brandished`, `Seized`), `uco-action:Action`
  (`instrument`), `legalproc:ForfeitureOrder`, chain of custody.
- The class tree deliberately mirrors CCO's Artifact Ontology
  (Weapon > Projectile Launcher > Firearm > Hand Gun / Long Gun >
  Rifle / Shotgun; Portion of Ammunition as a Weapon). Alignments live in a
  separate bridge file per the
  [CDO profile pattern](https://cyberdomainontology.org/ontology/development/#profiles),
  so adopters are not forced to import CCO/BFO.
- Property names follow the NIEM justice-domain firearm representation
  (`nc:FirearmType` / `j:FirearmType`) for round-tripping with NIEM
  exchanges; definitions cite 18 U.S.C. § 921 where a statutory definition
  exists.
- Weapon *use* is modeled with Actions and Relationships, not properties —
  NIEM's `nc:WeaponUser` / `nc:WeaponInvolvedInActivity` correspond to a
  `uco-core:Relationship` and `uco-action:instrument` respectively.

## Usage

```python
gun = {
    "@id": uid("item-sig-p365"),
    "@type": "weap:Handgun",
    "uco-core:name": "SIG Sauer P365 9mm pistol",
    "weap:make": "SIG Sauer",
    "weap:model": "P365",
    "weap:caliber": "9mm",
}
```

Validate with the extension:

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/weapons/weapons.ttl \
  --ontology-graph extensions/weapons/weapons-shapes.ttl \
  --inference rdfs --allow-info graph.jsonld
```

or via the MCP tool: `validate_graph(path, extensions=["weapons"])`.

## Status

Local extension, not yet proposed upstream. Weapons sit outside UCO's cyber
scope but inside CASE's investigative scope; candidate for the CDO Community
Playground and eventually a CASE proposal. The `example.org` namespace is a
placeholder pending a community namespace decision (same convention as the
`cryptoinv` extension).
