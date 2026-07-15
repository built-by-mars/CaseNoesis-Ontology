# Trajectories extension — validation log

Date: 2026-07-14  
Branch: `main`  
Status: `candidate`

True green paths below. Upper shapes (`sh-time`, `sh-prov-o`, optional `sh-gufo`) load via the SDK profile bundle when `profiles` is set — not via ad-hoc TTL alone.

---

## Primary: SDK `case_uco.validation` (strict coverage)

Public API since v1.22.1 (`python/case_uco/validation/`). The
`mcp_server/graph_validator` module remains a thin re-export for MCP/critic
compatibility, but extension docs should import the package.

```bash
export PATH="$PWD/.venv/bin:$PATH"
export PYTHONPATH="$PWD/python${PYTHONPATH:+:$PYTHONPATH}"
python3 <<'PY'
from case_uco.validation import validate_graph_file

def check(path, profiles=("time", "prov-o")):
    r = validate_graph_file(
        path,
        extensions=["trajectories"],
        profiles=list(profiles),
        strict_concepts=True,
        force_rdfs_inference=True,
    )
    stages = dict(r.stage_status)
    print(path.split("/")[-1], "conforms=", r.conforms,
          "coverage=", stages.get("coverage_conformance"),
          "shacl=", stages.get("shacl_conformance"),
          "viol=", r.violation_count)

for p in (
    "extensions/trajectories/trajectories-exemplar.ttl",
    "extensions/trajectories/trajectories-elder-fraud-exemplar.ttl",
):
    check(p)
    check(p, profiles=("time", "prov-o", "gufo"))

check("extensions/trajectories/trajectories-invalid-exemplar.ttl")
PY
```

### Recorded results (re-verified 2026-07-15 on v1.22.4 / `2028ba9`)

| Artifact | profiles | Conforms | coverage | SHACL | notes |
|---|---|---|---|---|---|
| `trajectories-exemplar.ttl` | time, prov-o | **True** | ok | conforms | evidence `@id`s from snapchat-grooming-cybertip |
| `trajectories-exemplar.ttl` | time, prov-o, gufo | **True** | ok | conforms | loads `trajectories-profile-gufo.ttl` + `sh-gufo.ttl` |
| `trajectories-elder-fraud-exemplar.ttl` | time, prov-o | **True** | ok | conforms | evidence `@id`s from EDLA elder-fraud graph |
| `trajectories-elder-fraud-exemplar.ttl` | time, prov-o, gufo | **True** | ok | conforms | |
| `trajectories-invalid-exemplar.ttl` | time, prov-o | **False** | ok | nonconformant | 10 violations (firewall / missing props) |

Invalid exemplar expected messages include:

- `Every PhaseAssertion MUST cite >=1 evidence node via prov:wasDerivedFrom.`
- Missing `assertsState` / `atInterval` / `sequenceIndex` on dual-typed model
- Missing `uco-core:ConfidenceFacet` via `hasFacet`
- `traj:StateMachineModel is an INFERRED analytic artifact.`

Without `profiles=['time','prov-o']`, coverage fails closed on `profile_not_selected` for `time:*` / `prov:*` even if SHACL alone would pass.

---

## Critic: deterministic pass (offline)

```bash
export PATH="$PWD/.venv/bin:$PATH"
python3 <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "mcp_server")
from critic.models import CriticArtifactRequest
from critic.deterministic import analyze_artifact

for label, path in [
    ("cac", "extensions/trajectories/trajectories-exemplar.ttl"),
    ("elder", "extensions/trajectories/trajectories-elder-fraud-exemplar.ttl"),
]:
    req = CriticArtifactRequest(
        graph_path=str(Path(path).resolve()),
        critic_scope="graph",
        extensions=["trajectories"],
        profiles=["time", "prov-o"],
        force_rdfs_inference=True,
    )
    review = analyze_artifact(req)
    print(label, "status=", review.status,
          "findings=", len(review.deterministic_findings or []))
PY
```

### Recorded results

| Exemplar | status | deterministic findings |
|---|---|---|
| CAC grooming | `deterministic_clean` | `[]` |
| Elder-fraud | `deterministic_clean` | `[]` |

---

## Secondary: `case_validate` CLI (caveat)

```bash
.venv/bin/case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/trajectories/trajectories.ttl \
  --ontology-graph extensions/trajectories/trajectories-shapes.ttl \
  --ontology-graph ontology/upper/time.ttl \
  --ontology-graph ontology/upper/prov-o.ttl \
  --inference rdfs --allow-info \
  extensions/trajectories/<exemplar>.ttl
```

**What this loads**

| Layer | Loaded? |
|---|---|
| traj OWL + SHACL | Yes (`--ontology-graph`) |
| UCO/CASE shapes | Yes (`--built-version case-1.4.0`) |
| `ontology/upper/shapes/sh-time.ttl`, `sh-prov-o.ttl` | **No** |
| Strict concept coverage / profile selection | **No** |

Use the SDK primary path above for PR-grade “green.” CLI alone can report SHACL conformant while the SDK still fails coverage.

---

## Mutations (a–d) against updated CAC exemplar

Mutations written under `/tmp`, validated with the same CLI base as above (`rdfs` ON). All must fail.

| Mutation | Change | Result |
|---|---|---|
| (a) | Drop `prov:wasDerivedFrom` on first `PhaseAssertion` | Conforms **False** — missing evidence provenance |
| (b) | Drop `uco-core:hasFacet` ConfidenceFacet link | Conforms **False** — missing ConfidenceFacet |
| (c) | Dual-type `StateMachineModel` as also `PhaseAssertion` | Conforms **False** — firewall / missing required props |
| (d) | `Trajectory hasPhaseAssertion` → a `TransitionEstimate` | Conforms **False** — `sh:class` on hasPhaseAssertion |

---

## Focus-node non-vacuity (updated exemplars)

| Shape target | CAC | Elder | Invalid |
|---|---|---|---|
| PhaseAssertion | 4 | 4 | 2 |
| Trajectory | 1 | 1 | 1 |
| Transition | 3 | 3 | 1 |
| StateMachineModel | 1 | 1 | 1 |
| TransitionEstimate | 3 | 2 | 1 |

All nonzero on the valid exemplars.

---

## Deferred

- Language bindings under `packages/case-uco-trajectories/`
- Competency SPARQL queries (optional promote gate)
- Init of `ontology/aeo/ontology` (AEO documented as plug-in only in README)
