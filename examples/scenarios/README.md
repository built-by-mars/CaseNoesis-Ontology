# Investigation Scenarios

**Fictitious stress-test narratives** for exercising the CASE/UCO MCP server,
recipe catalog, and extension ontologies end-to-end. Each scenario is
**Tier T0 (fully synthetic)** — all identifiers, persons, and evidence are
invented for SDK/MCP evaluation, not real investigative data. Scenarios are
structurally grounded in validated exemplars under `examples/pacer/`,
`examples/cti/`, and `examples/solveit/` to show how the SDK models complex
investigations **adjacent to, in, and through the cyber domain**.

| Scenario | File | Builder | Grounded exemplars |
|----------|------|---------|-------------------|
| Operation PHANTOM GATE | [operation-phantom-gate.md](operation-phantom-gate.md) | [build_phantom_gate_scenario.py](build_phantom_gate_scenario.py) → [operation-phantom-gate.jsonld](operation-phantom-gate.jsonld) (452 nodes; long-tail via [phantom_gate_longtail.py](phantom_gate_longtail.py); gates in [phantom_gate_acceptance.py](phantom_gate_acceptance.py)) | RICO/crypto (`ddc_2024`), elder fraud (`edla_2022`), insider/export (`ndca_2024`, `ndca_2020`), espionage (`dma_2023`), CTI (`lotus_blossom_2025`), CAC (ICAC), weapons/drugs (`ndnd_2025`), SOLVE-IT (`solveit/`) |

Coverage contract: [phantom_gate_coverage.json](phantom_gate_coverage.json) — checked by [check_phantom_gate_coverage.py](check_phantom_gate_coverage.py). SDK round-trip: [build_phantom_gate_typed.py](build_phantom_gate_typed.py).

## Agent workflow

1. Read the scenario markdown for the active phase.
2. Feed narrative excerpts or artifact snippets to MCP: `route_investigation_content`, `route_cac_content`, `guide_mapping`, `plan_solveit_workflow`.
3. Build Layer 2–3 graphs with the SDK (`python examples/scenarios/build_phantom_gate_scenario.py` produces [operation-phantom-gate.jsonld](operation-phantom-gate.jsonld)).
4. Optional fidelity gates: `python examples/scenarios/check_phantom_gate_coverage.py` and `python examples/scenarios/build_phantom_gate_typed.py`.
5. Validate with `validate_graph` using the extension bundle listed for that phase in the scenario doc.
6. Do not report success until `Conforms: True`.
