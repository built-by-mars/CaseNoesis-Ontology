# CaseNoesis-Ontology

A CASE/UCO-based ontology extending crime and offense modeling across multiple offense categories, built to support [CaseNoesis](https://github.com/built-by-mars/CaseNoesis)'s cross-domain case analysis.

## Origin

This project is forked from **[CASE-UCO-SDK](https://github.com/vulnmaster/CASE-UCO-SDK)** (v1.14.0 · CASE 1.4.0 · UCO 1.4.0), a multi-language data modeling library for building validated JSON-LD graphs for digital forensics and cyber-investigation workflows.

CASE-UCO-SDK was funded by [Project VIC International](https://www.projectvic.org), a nonprofit focused on building modern technologies to rescue children and aid thousands of law enforcement officers worldwide in finding victims of exploitation faster. 

## Inspiration

This ontology draws inspiration from the **[CAC Ontology](https://github.com/Project-VIC-International/CAC-Ontology)** (Crimes Against Children Ontology) — a 35+ module extension of CASE/UCO maintained by Project VIC International. CAC Ontology models the full lifecycle of a child-exploitation investigation as typed, related objects, including law enforcement organizations, legal processes, reporting, offender tradecraft, and digital forensics activities.

CaseNoesis-Ontology is **not a fork of CAC Ontology** and does not import its CSEA-specific classes directly. Instead, it generalizes the *pattern* CAC Ontology established and decomposes an offense into affordance, misuse event, and harm vector for use across offense types CAC Ontology was never designed to cover (fraud, cyber-enabled crime, trafficking, and others as the project develops).

## Where This Is Used

CaseNoesis-Ontology is the ontology layer for **[CaseNoesis](https://github.com/built-by-mars/CaseNoesis)**, which generalizes the affordance–misuse–harm framework developed in **["Affordances for Harm: How Offenders Misuse Platform Capabilities to Exploit Children, and Where to Intervene"](https://mrinaalr.github.io/website/Affordance%2C%20Misuse%2C%20Harm%2C%20Kill%20Chain.pdf)** beyond its original CSEA domain. CaseNoesis's ingestion pipeline maps case features into this ontology, emits validated RDF graphs, and builds a queryable knowledge graph for cross-offense-type pattern analysis — the same approach CaseLinker uses for CAC Ontology, applied at broader scope.

## Scope

- Core classes inherited from CASE/UCO (unmodified — no changes to upstream ontology sources)
- New domain-agnostic classes for affordance, misuse event, and harm vector modeling, generalized from the CAC Ontology pattern but decoupled from CSEA-specific semantics
- Multi-language typed bindings (Python, C#, Java, Rust) inherited from the CASE-UCO-SDK generator
- Supports CaseNoesis's ingestion pipeline directly; not intended as a standalone public ontology release at this stage

## Status

Early stage. Class structure for the generalized affordance/misuse/harm layer is under active revision. Core CASE/UCO classes and tooling (generator, CLI explorer, MCP server) are inherited as-is from upstream and unmodified.

## Documentation

Most SDK-level documentation (installation, usage, class discovery, AI-assisted development via MCP, ontology extension workflow) is inherited from CASE-UCO-SDK and still applies here — see the sections below in this repo for the full detail:

- Installation and basic usage (Python/C#/Java/Rust)
- Ontology extension workflow (`case-uco-generate scaffold`)
- Class discovery (CLI explorer, runtime introspection, `ONTOLOGY_REFERENCE.md`, `docs/MAPPING_GUIDE.md`)
- AI-assisted development via the included MCP server

New documentation specific to CaseNoesis's generalized affordance/misuse/harm classes will be added as that layer stabilizes.

## License

Apache-2.0, inherited from CASE-UCO-SDK. Original copyright, license terms, and the CASE/UCO ontology sources (themselves separately licensed — see [UCO](https://github.com/ucoProject/UCO) and [CASE](https://github.com/casework/CASE)) are retained per upstream requirements.