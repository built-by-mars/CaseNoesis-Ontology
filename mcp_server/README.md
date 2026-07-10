# CASE/UCO MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that gives AI coding assistants programmatic access to the CASE/UCO ontology. Instead of reading thousands of lines of documentation, your AI agent can call tools like `search_classes("mobile")` to find the right types for your forensic scenario.

## Setup

### 1. Install FastMCP

```bash
pip install fastmcp
```

If you're using a virtual environment (recommended):

```bash
source .venv/bin/activate
pip install fastmcp
```

### 2. Restart Cursor

The `.cursor/mcp.json` configuration is already included in the repository. After installing FastMCP, restart Cursor to activate the MCP server.

### 3. Verify

Open Cursor's MCP panel (Settings > Tools & MCP) and confirm the "case-uco" server shows as connected. You can also test from the command line:

```bash
cd /path/to/CASE-UCO-SDK
fastmcp dev mcp_server/server.py
```

## Available Tools

| Tool | Arguments | Description |
|------|-----------|-------------|
| `search_classes` | `query: str` | Find classes by keyword match on name or description |
| `get_class_details` | `name: str` | Full property table for a specific class |
| `find_classes_for_domain` | `domain: str` | Map a forensic task to the right classes |
| `list_all_facets` | (none) | All Facet classes for the ObservableObject pattern |
| `get_recipe` | `scenario: str` | Find a code recipe for a forensic workflow |
| `get_recipes` | `scenario: str, limit?: int, include_content?: bool` | Find multiple ranked recipes for multi-domain scenarios |
| `route_investigation_content` | `content_text?, source_path?, max_families?` | Classify ANY submission by investigation family (CAC, violent crime, financial/crypto, court filings, intrusion, mobile, email, filesystem, civil, corporate) and return recipes, extensions, namespaces, CDO upper-ontology profiles — or the extension-gap workflow for unseen data types |
| `route_cac_content` | `content_text?, source_path?, output_format?, include_recipe_content?, max_recipes?` | Detect CAC domains in submitted content and return multiple CAC recipes plus validation guidance |
| `list_all_vocabs` | (none) | All vocabulary/enum types with members |
| `process_document_file` | `source_path, output_path, file_kind?, upload_id?, progress_output?` | Process a supported local synthetic document (receipt image, PDF, Office, CSV/table) into bounded CASE/UCO-shaped JSON-LD |
| `validate_graph` | `graph_path: str, allow_warning?: bool, extensions?: list[str]` | Run `case_validate` against JSON-LD/Turtle; `extensions=['cac']` uses the press-release subset; `extensions=['cac:full']` uses the full manifest |

## Available Resources

| URI | Description |
|-----|-------------|
| `case-uco://domains` | All forensic domain categories with descriptions |
| `case-uco://modules` | All ontology modules |
| `case-uco://patterns` | Core modeling patterns with code examples |

## How AI Agents Use This

When you describe a forensic scenario in natural language, the AI agent:

1. Calls `route_investigation_content` to classify the submission (investigation family → recipes, extensions, namespaces, upper-ontology profiles)
2. Calls `find_classes_for_domain` or `search_classes` to identify relevant types
3. Calls `get_class_details` on each type to see its properties
4. For CAC content, calls `route_cac_content` to get multiple matching recipes and validation guidance
5. Optionally calls `get_recipe` or `get_recipes` to find code examples
6. Writes correct SDK code using the exact class names and property names
7. Calls `validate_graph` with the matching `extensions=[...]` on the finished graph — strict concept coverage rejects undeclared terms and routes the agent to the change-proposal / extension workflow

This is much faster and more accurate than the agent reading markdown documentation.

## Workflow for Hermes and Link-Look (any investigation type)

End-to-end pattern for warrant returns, legal filings, case files, press
releases, and investigator notes — including data types the server has
never seen:

1. **Extract** — `process_document_file(source_path="case.pdf", output_path="extract.jsonld")` for PDFs/images, or pass plain text directly.
2. **Classify** — `route_investigation_content(content_text=<clean narrative excerpt>)` detects the investigation family (CAC, violent crime/terrorism, financial/crypto, court filings, network intrusion, mobile/device, email, filesystem, civil e-discovery, corporate/internal) and returns per-family recipes, the extension ontologies to enable, core namespaces, and applicable CDO upper-ontology profiles. If nothing matches, it returns `extension_gap_guidance` — the search → proposal → local-extension workflow for previously unseen data.
3. **Compose, don't split** — when several families match (real cases are often CAC + violent crime + fraud at once), build ONE graph composing every matched family's recipes with the union of their extensions (`docs/recipes/cross-domain-extensions.md`).
4. **Go deeper than the anchors** — family recipes cover the domain-interpretation layer; use `get_recipes(scenario)` for ranked matches across the full 60+ recipe catalog and `guide_mapping(evidence_source)` for each evidence type actually in hand (devices, files, messages, call logs, locations, EXIF, databases, ...).
5. **Deep-route CAC** — for CAC content, `route_cac_content(...)` adds per-domain CAC recipes and modeling checklists (steps below).
6. **Grow the catalog (self-improvement loop)** — when an agent has to work out a pattern no recipe covers, it writes one; when a live case proves an existing recipe wrong, incomplete, or invisible to routing, the agent improves that recipe (or its index keywords) in place. `docs/recipes/recipe-authoring.md` defines both paths: structure, grounding rules (validated exemplar, strict concept coverage, cyber vs. non-cyber typing), re-validation before publishing, and registration in `INDEX.md` + `RECIPE_INDEX` (+ a router family when warranted). Investigators are mostly non-technical — the recipe catalog is where the automation accumulates its modeling judgment — and because every recipe is grounded in public CASE/UCO/CAC releases, published extensions, and CDO-profiled upper ontologies, the knowledge models it produces can be shared with outside parties who can validate and reuse them independently.

CAC-specific continuation:

1. **Route** — `route_cac_content(content_text=<clean narrative excerpt>)` returns multiple matched recipes (e.g. task force + warrant arrest + grooming + legal charges + CSAM purchasing).
2. **Build** — Agent reads returned recipe files and composes JSON-LD or TTL using CAC classes (`CASE_UCO_EXTENSIONS=cac`).
3. **Validate** — `validate_graph("output.jsonld", extensions=["cac"])` uses `extensions/cac/validation-subset.json` (recommended for press-release KGs). Use `extensions=["cac:full"]` only when the full CAC manifest SHACL is repaired upstream.

For non-CAC prosecutions (violent crime, terrorism, generic federal cases), build with the `legalproc` extension and validate with `extensions=["legalproc"]` — see `docs/recipes/legal-process-modeling.md` and the exemplar at `examples/pacer/wdmo_2022_cr_04065/`.

Example Hermes tool sequence for the Maryland ICAC Annapolis arrest press article:

```text
process_document_file(
  source_path="/path/to/Maryland_ICAC_Arrest_Test_PDF.pdf",
  output_path="/tmp/maryland-extract.jsonld",
)
route_cac_content(
  content_text="Maryland State Police Computer Crimes Unit and Maryland ICAC Task Force ...",
  output_format="jsonld",
  include_recipe_content=true,
  max_recipes=6,
)
# Agent builds graph using matched recipes and modeling_checklist
validate_graph(
  graph_path="examples/maryland-icac-annapolis-arrest-2025.jsonld",
  extensions=["cac"],
)
```

Noisy PDF extraction (navigation, ads, repeated URLs) lowers routing scores. When `route_cac_content` reports `extraction_quality.noisy_extraction: true`, summarize investigative facts into `content_text` before routing. Reference builder: `examples/build_maryland_icac_annapolis_arrest.py`.

## Running under Hermes Agent

The server runs unmodified under any MCP-native agent harness. For the
[Hermes Agent](https://github.com/NousResearch/hermes-agent) (Nous Research),
register it as a stdio MCP server in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  case-uco:
    command: "/home/cory/CASE-UCO-Libraries/.venv/bin/python"
    args: ["/home/cory/CASE-UCO-Libraries/mcp_server/server.py"]
    env:
      PYTHONPATH: "python:mcp_server"
      # CASE_UCO_EXTENSIONS: "cac,aeo,cryptoinv,legalproc"   # optional extension registries
```

Run `/reload-mcp` in Hermes after editing the config. All tools are then
discoverable by the agent alongside its built-in tools.

Law-enforcement deployment notes:

- The server is local-only (stdio); it performs no network calls at runtime.
  Egress posture is determined entirely by the agent's configured LLM
  provider — pair this server with a local model backend by default, and use
  commercial backends only in agency-approved, accredited environments.
  Hosting an MCP server inside an agent does not by itself satisfy CJIS or
  any other compliance obligation.
- `process_document_file` accepts bounded local files only and returns safe
  metadata; `validate_graph` requires the CASE Utilities `case_validate` CLI
  on PATH and never fabricates a passing result.
- Agents should call `validate_graph` on every produced graph before
  submitting it to downstream tools (e.g., Link-Look normalization review).

## Architecture

The server wraps the existing Python registry API (`case_uco.registry`) and a domain index (`domain_index.py`) that maps investigative tasks to classes.

```
mcp_server/
├── server.py          FastMCP server with tool and resource definitions
├── domain_index.py    Task-to-class mappings, domain categories, recipe index
├── requirements.txt   Python dependencies (fastmcp, pypdf)
└── README.md          This file
```

### Document processor extraction dependencies

`document_processor.py` detects optional extraction tooling at runtime and
fails with typed, actionable errors when it is missing — it never shows
undecodable bytes to a reviewer:

| Capability | Tooling | Failure code when absent |
|---|---|---|
| PDF text layer (preferred) | `pdftotext` (poppler-utils) | falls back to `pypdf` |
| PDF text layer (fallback) | `pypdf` (in `requirements.txt`) | falls back to gated literal-string scrape |
| Scanned/image-only PDF OCR | `pdftoppm` (poppler-utils) or `pypdf` page-image extraction, plus `tesseract` | `pdf_text_missing` |
| Subset-font PDF with no real extractor | — | `pdf_text_unreadable` |
| Image OCR (receipts/scans) | `tesseract` | `ocr_unavailable` |

On Debian/Ubuntu: `sudo apt install poppler-utils tesseract-ocr`. Rootless
alternative: `conda create -n link-look-ocr -c conda-forge tesseract poppler`
and symlink the binaries into a `PATH` directory (e.g. `~/.local/bin`). For
air-gapped deployments, mirror these packages with your offline bundle.

The server reads from `python/case_uco/_registry.json`, which is auto-generated by `case-uco-generate generate` and contains the full ontology schema.

## Troubleshooting

**Server not connecting:** Make sure `fastmcp` is installed in the Python environment that Cursor uses. If using a venv, the `.cursor/mcp.json` may need its command adjusted to point to the venv Python.

**"Registry not found" error:** Run `case-uco-generate generate` from the project root to produce the `_registry.json` file, or ensure the `python/case_uco/_registry.json` file exists.

**Testing outside Cursor:** You can run the server directly for debugging:

```bash
PYTHONPATH=python:mcp_server python mcp_server/server.py
```
