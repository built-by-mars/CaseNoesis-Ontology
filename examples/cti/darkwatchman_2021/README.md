# DarkWatchman — Prevailion PACT CTI exemplar

Worked, validated CASE/UCO graph for an **open-source cyber threat
intelligence (CTI) report** emphasizing fileless registry-buffered
persistence and DGA C2. Companion exemplar to Lotus Blossom / Sagerunex under
[`docs/recipes/cyber-threat-intelligence.md`](../../../docs/recipes/cyber-threat-intelligence.md).

**Source:** Matt Stafford and Sherman Smith, "DarkWatchman: A new evolution
in fileless techniques," Prevailion Adversarial Counterintelligence Team
(PACT), 14 December 2021.
<https://www.prevailion.com/darkwatchman-new-fileless-techniques/>

**Archival capture used for graphics:**
<https://web.archive.org/web/20220629230035/https://www.prevailion.com/darkwatchman-new-fileless-techniques/>

## Contents

| File | What it is |
|---|---|
| `build_darkwatchman.py` | `CASEGraph` public-graph builder (`serializer_mode=casegraph_raw`; `upsert_node` / `write_streaming`) |
| `darkwatchman-prevailion.jsonld` | The validated graph |
| `build-manifest.json` | Sidecar hashes for builder, recipe, and output (not domain subjects) |
| `graphics/` | Ten in-report figures from the Wayback capture (Figures 1–8, 12, 19) |

Figures 9–11, 13–18, and 20 appear as inline code blocks in the HTML (not
separate image assets in this Wayback capture); their intelligence is modeled
from the report prose.

## Run

```bash
PYTHONPATH=python:mcp_server python examples/cti/darkwatchman_2021/build_darkwatchman.py
```

Validation uses the public SDK API:

```python
from case_uco.validation import validate_graph_file
validate_graph_file(path, extensions=["attack-technique:full"])
```

Critic sessions should use `serializer_mode="typed_sdk"` (or `auto`).

## What it demonstrates

- Typed CASEGraph emission (`upsert_node` / `create_relationship` / `add_type` /
  `write_streaming`) plus `case_uco.validation.validate_graph_file`
- Epistemic layers: source material, observables, observed behavior,
  capabilities, analytic assessments, detection patterns
- Unattributed activity as `Grouping` + `Annotation`/`ConfidenceFacet`
- Nested `ContextualCompilation` members under the Investigation
- ATT&CK punning via `add_type` with separate mapping-provenance Annotations
  (modeler enrichment; T1041 vs T1105; T1036.008 post-dated note)
- VT submission times as `Event`, not `FileFacet.observableCreatedTime`
- Keylogger `Contained_Within` SFX without a published digest
