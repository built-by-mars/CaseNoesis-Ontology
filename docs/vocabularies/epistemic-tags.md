# Epistemic tag vocabulary (controlled)

Controlled `uco-core:tag` values for CASE/UCO CTI and investigation graphs.
Machine-readable source: [`epistemic-tags.json`](epistemic-tags.json).

These are **recommended string tags**, not OWL individuals. Graphs remain
SHACL-valid if they use other tags; recipes and the critic treat members of
this vocabulary as first-class signals (especially hash-availability tags).

## Stance (`epistemic:*`)

| Tag | Use when |
|-----|----------|
| `epistemic:observed` | Source documents observed / repeatedly executed behavior |
| `epistemic:reported` | Vendor/report states a fact the modeler did not re-observe |
| `epistemic:capability` | Code capability or conditional path (not an observed Action) |
| `epistemic:assessment` | Classification / motive / nature assessment |
| `epistemic:hypothesis` | Explicit hypothesis (pair with verbal confidence) |
| `epistemic:enrichment` | Modeler enrichment (ATT&CK, etc.) |
| `epistemic:unattributed` | Activity cluster without a justified Organization |
| `epistemic:source-contradiction` | Preserve an internal source contradiction |

## Verbal confidence

| Tag | Use when |
|-----|----------|
| `confidence:low-verbal` | Low verbal confidence |
| `confidence:moderate-verbal` | Moderate (“appears”, “likely”) |
| `confidence:high-verbal` | High verbal confidence without a numeric facet |

Prefer these over invented `ConfidenceFacet` numbers unless the source
publishes a score or a cited normalization policy exists.

## Hash / bytes honesty

| Tag | Critic effect |
|-----|---------------|
| `hash-status:not-published` | Medium `CRIT-H-DERIVED-NO-HASH` (with `cti-report` or alone) |
| `source-bytes:not-acquired` | Same — bytes never acquired |
| `content:not-reproduced` | Known-to-exist object with omitted payload |

Do **not** invent digests or weaken `Contained_Within` merely to silence the critic.

## ATT&CK mapping provenance

| Tag | Use when |
|-----|----------|
| `att&ck-mapping` | Technique mapping present |
| `mapping-source:case-uco-modeler` | Mapping authored by the exemplar modeler |
| `post-dated-technique` | Technique post-dates the report |

See also: [`docs/recipes/cyber-threat-intelligence.md`](../recipes/cyber-threat-intelligence.md).
