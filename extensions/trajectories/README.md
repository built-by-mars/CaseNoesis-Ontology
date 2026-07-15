# Trajectories Extension (`trajectories`)

Vocabulary-agnostic **state-machine** and **per-case trajectory** metamodel
for CASE/UCO investigation graphs. Status: **`candidate`**.

## Phase 1 gaps this fills

| Gap | What existed | What `traj` adds |
|---|---|---|
| (1) Typed state | Domain-fixed CAC/AEO phase *classes* | `traj:State` instances (optionally `skos:Concept`) |
| (2) Transition + trigger/guard | CAC `PhaseTransitionEvent` (investigation-only); referral triggers | `traj:Transition` with `fromState` / `toState` / `trigger` / optional `guard` |
| (3) Ordered case occupancy + interval + evidence + confidence | Timestamps + `ConfidenceFacet` + PROV available but not bundled | `traj:Trajectory` of `traj:PhaseAssertion` (owl-time + `prov:wasDerivedFrom` + `ConfidenceFacet`) |
| (4) Learned transition probabilities | Scalar `transitionLikelihood` on one CAC class; no model artifact | `traj:StateMachineModel` + `traj:TransitionEstimate` with `prov:wasGeneratedBy` |

It does **not** re-model CAC grooming taxonomy, RICO enterprises, kill-chains, or drugs/weapons content — only the trajectory machinery.

## Contents

| File | Purpose |
|---|---|
| `trajectories.ttl` | OWL T-Box |
| `trajectories-shapes.ttl` | SHACL observed≠inferred firewall |
| `trajectories-profile-gufo.ttl` | Optional gUFO bridge (`State rdf:type gufo:Phase` metaclass; `PhaseAssertion`⊆`gufo:Situation`) |
| `trajectories-exemplar.ttl` | CAC grooming trajectory + model |
| `trajectories-elder-fraud-exemplar.ttl` | Non-CAC elder-fraud trajectory (EDLA 2022-cr-00115) |
| `trajectories-invalid-exemplar.ttl` | Expected-invalid firewall fixture |

## Design choices

### Ordering idiom

`traj:sequenceIndex` (xsd:nonNegativeInteger) on each `PhaseAssertion`,
referenced from `Trajectory` via `hasPhaseAssertion`.

- Preferred over `rdf:List` (awkward in SHACL/SPARQL).
- Preferred over AEO `ArrayOfAction` (planned narrative actions, not
  observed occupancy).
- Complementary to CAC `EventSequence` (investigation events), not a
  replacement.

### Confidence

Reuse **`uco-core:ConfidenceFacet`** on the assertion via
`uco-core:hasFacet` — no `traj:confidence` mint. SHACL requires ≥1
`ConfidenceFacet` on every `PhaseAssertion`.

### Firewall (observed vs inferred)

- `PhaseAssertion` **owl:disjointWith** `StateMachineModel` /
  `TransitionEstimate`.
- Every `PhaseAssertion`: ≥1 `prov:wasDerivedFrom`, confidence facet,
  state, interval, sequence index.
- Every model / estimate: ≥1 `prov:wasGeneratedBy`.
- Trajectories reference **PhaseAssertions only**; models
  `traj:learnedFrom` trajectories (never the reverse).

### Mapping CAC `PhaseTransitionEvent` → `traj:Transition`

| CAC temporal | `traj` |
|---|---|
| `PhaseTransitionEvent` | `traj:Transition` (more general; not limited to investigation lifecycle) |
| `transitionsFrom` / `transitionsTo` | `fromState` / `toState` |
| begin/end timestamps on the event | Prefer intervals on **PhaseAssertions**; put trigger-time on the trigger Action if needed |
| Fixed investigation phases | Plug-in `traj:State` vocab (SKOS), not hard subclassing |

Keep using CAC temporal classes for **investigation** lifecycle; use `traj`
for **offense / engagement / fraud** occupancy histories and analytic models.

## Plug-in vocabulary pattern

Domain phases are **instances**, not T-Box dependencies:

```turtle
:InitialContact a traj:State , skos:Concept ;
    skos:inScheme :CACGroomingPhaseScheme ;
    skos:exactMatch <https://cacontology.projectvic.org/grooming#InitialContactPhase> .
```

No dependence on unmerged CAC PRs (#33 AffordanceMisuse, #39 ConditioningPhase).

### AEO CyberKillChain plug-in (do not modify AEO)

Wrap kill-chain phase actions the same way:

```turtle
:Reconnaissance a traj:State , skos:Concept ;
    skos:inScheme :AEOCyberKillChainScheme ;
    skos:exactMatch <https://ontology.adversaryengagement.org/ae/attack/…> ;
    uco-core:description "Corresponds to a CyberKillChain phase Action." .
```

`aeo:CyberKillChain` / `Storyline` remain for **planned** adversary-engagement
narratives; `traj:Trajectory` records **observed** occupancy.

## Validation

**Primary (SDK):** `from case_uco.validation import validate_graph_file`
(public API since v1.22.1) with `extensions=['trajectories']`,
`profiles=['time','prov-o']`, `strict_concepts=True`. That bundle loads
upper shapes `sh-time.ttl` / `sh-prov-o.ttl`. Add `'gufo'` to `profiles`
to load `trajectories-profile-gufo.ttl` + `sh-gufo.ttl`.

**Secondary (CLI):** `case_validate` with traj OWL/shapes plus upper
*ontology* TTL (`time.ttl` / `prov-o.ttl`) does **not** load upper
*shapes* or run concept coverage — do not treat CLI-alone SHACL green
as SDK green. See `VALIDATION.md` for exact commands and results.

Invalid exemplar must fail (observed≠inferred firewall).

## Status

Local candidate extension (`"status": "candidate"`). `example.org`
namespace matches rico/drugs/weapons placeholders pending a community IRI.
Language bindings (`packages/case-uco-trajectories`) are deferred.
