# Held-out routing evaluation (issue #58)

This directory contains the **external evaluation harness** for the hybrid
investigation router. It is deliberately separated from the development
artifacts:

| Layer | Location | Purpose | May be edited alongside router changes? |
|---|---|---|---|
| Unit tests | `mcp_server/tests/` | Correctness of individual functions | Yes |
| Development benchmark | `mcp_server/tests/test_routing_benchmark.py` | Calibrates thresholds during development | Yes |
| **Held-out evaluation** | `evaluation/routing/` | Measures transfer to unfamiliar investigator language | **No — governance-gated** |

## Why a held-out corpus

The synonym dictionary (`mcp_server/semantic_retrieval.py`) and the
development benchmark were written in the same repository and release, so
benchmark success partly measures dictionary coverage rather than true
transfer. The held-out corpus is evaluation data the router implementation
must not be tuned against.

The MCP server is always driven by *some* LLM agent — anything from a small
local model (e.g. Gemma-class, on closed Link-Look deployments) to a
frontier model. The deterministic router is the stage that must behave
identically regardless of which model calls it, which is exactly what this
harness measures: the corpus is evaluated **without any LLM in the loop**,
so results are reproducible across deployments and model choices, and a
weak local model gets the same routing quality as a frontier one.

## Governance rules

1. **Separation of authorship.** Corpus cases must be authored or reviewed
   by someone (or some agent session) that did not edit
   `SYNONYM_GROUPS` / family keyword lists in the same change. Corpus
   provenance records authorship per version.
2. **No co-modification.** CI fails any change that touches both the router
   implementation (`mcp_server/semantic_retrieval.py`,
   `mcp_server/investigation_router.py`) and the held-out corpus
   (`evaluation/routing/heldout-corpus-*.json`), unless the commit message
   carries the `[eval-governance-approved]` tag recording an explicit
   evaluation-governance review.
3. **Independent versioning.** Corpus files are versioned by their own
   `corpus_version` field, not by SDK release. Never rewrite a published
   version; add cases in a new version.
4. **Public-safe content only.** All cases are synthetic (Tier T0). No
   operational or sensitive investigative data may enter the corpus.

## Running

```bash
make eval-routing
# or directly:
python evaluation/routing/run_evaluation.py \
    --corpus evaluation/routing/heldout-corpus-v1.json \
    --report evaluation/routing/report.json
```

The harness exits non-zero when any documented minimum threshold fails
(thresholds live in the corpus file so they version with the data). The
report is machine-readable JSON: per-family precision/recall/F1,
multi-label exact and partial match, false-positive rate on hard negatives,
abstention accuracy on unseen domains, confidence calibration by band, and
regression against the deterministic keyword baseline.

Hidden-split note: this repository ships the v1 public split. Deployments
that need a truly hidden split (e.g. Project VIC acceptance testing) should
maintain it in a separate controlled repository and run this same harness
against it with `--corpus`; the harness never prints case text into CI logs
(only case ids), so threshold enforcement does not expose hidden content.
