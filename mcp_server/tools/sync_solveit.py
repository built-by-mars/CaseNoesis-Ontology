#!/usr/bin/env python3
"""Synchronize the bundled ``solveit`` extension with upstream SOLVE-IT.

SOLVE-IT (https://github.com/SOLVE-IT-DF/solve-it) is the digital forensics
knowledge base of objectives, techniques, weaknesses, and mitigations; its
companion repository (https://github.com/SOLVE-IT-DF/solve-it-ontology)
ships a CASE/UCO extension ontology and an hourly-compiled RDF knowledge
base (``docs/data/solve-it-kb.ttl``). Upstream releases move quickly, so the
SDK vendors *pinned* snapshots and this script is the one mechanism that
refreshes them:

1. Downloads the ontology module TTLs and the compiled knowledge base from
   ``solve-it-ontology`` at a pinned commit (or reads them from
   ``--source-dir`` for air-gapped rebuilds).
2. Regenerates ``solveit-technique-catalog.ttl`` — every SOLVE-IT technique
   punned as an ``owl:Class`` typed ``uco-action:Technique`` per the UCO
   1.5.0 metaclass pattern (ucoProject/UCO PR #676), matching the bundled
   MITRE ATT&CK catalog in ``extensions/attack-technique/``.
3. Rewrites the ``provenance`` block in ``ontology/solveit/manifest.json``
   (commit SHA, upstream release tag, ontology version, retrieval time).

Usage:
    python3 mcp_server/tools/sync_solveit.py --ontology-ref <sha-or-branch> \
        --release-tag v0.2026-06
    python3 mcp_server/tools/sync_solveit.py --skip-fetch   # regenerate only
    python3 mcp_server/tools/sync_solveit.py --source-dir /path/to/files

Run ``make eval-routing`` and the MCP test suite after syncing; a new
upstream snapshot can add techniques the recipe/routing layers should know
about.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "mcp_server"))
from extension_paths import extension_dir  # noqa: E402

EXT_DIR = extension_dir("solveit", PROJECT_ROOT)
CATALOG_FILE = "solveit-technique-catalog.ttl"
KB_FILE = "solve-it-kb.ttl"

ONTOLOGY_REPO = "SOLVE-IT-DF/solve-it-ontology"
KB_REPO = "SOLVE-IT-DF/solve-it"

# Ontology module files vendored verbatim from solve-it-ontology.
ONTOLOGY_FILES = [
    "solve_it_core.ttl",
    "solve_it_observable.ttl",
    "solve_it_observable_acquisition.ttl",
    "solve_it_observable_search.ttl",
    "solve_it_observable_timeline.ttl",
    "solve_it_observable_shapes.ttl",
    "solve_it_analysis.ttl",
    "solve_it_sqlite.ttl",
    "solve_it_tool_profile.ttl",
    "solve_it_weakness_assessment.ttl",
]

SOLVEIT_CORE = "https://ontology.solveit-df.org/solveit/core/"
SOLVEIT_DATA = "https://ontology.solveit-df.org/solveit/data/"
UCO_ACTION = "https://ontology.unifiedcyberontology.org/uco/action/"


def _fetch(url: str, timeout: int = 120) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "case-uco-sdk-sync"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _resolve_commit(ref: str) -> str:
    """Resolve a branch/tag/sha ref on solve-it-ontology to a commit SHA."""

    if len(ref) == 40 and all(c in "0123456789abcdef" for c in ref.lower()):
        return ref
    payload = json.loads(
        _fetch(f"https://api.github.com/repos/{ONTOLOGY_REPO}/commits/{ref}", timeout=30)
    )
    return payload["sha"]


def _latest_release_tag() -> str | None:
    try:
        payload = json.loads(
            _fetch(f"https://api.github.com/repos/{KB_REPO}/releases/latest", timeout=30)
        )
        return payload.get("tag_name")
    except Exception:
        return None


def fetch_upstream(commit: str) -> str:
    """Download ontology TTLs + compiled KB at ``commit`` into the extension."""

    base = f"https://raw.githubusercontent.com/{ONTOLOGY_REPO}/{commit}"
    for name in ONTOLOGY_FILES:
        (EXT_DIR / name).write_bytes(_fetch(f"{base}/{name}"))
        print(f"fetched {name}")
    (EXT_DIR / KB_FILE).write_bytes(_fetch(f"{base}/docs/data/{KB_FILE}"))
    print(f"fetched {KB_FILE}")
    version = _fetch(f"{base}/VERSION", timeout=30).decode("utf-8").strip()
    return version


def copy_from_source_dir(source_dir: Path) -> str:
    for name in ONTOLOGY_FILES + [KB_FILE]:
        src = source_dir / name
        if not src.is_file():
            raise SystemExit(f"missing {name} in --source-dir {source_dir}")
        shutil.copyfile(src, EXT_DIR / name)
    version_file = source_dir / "VERSION"
    return version_file.read_text(encoding="utf-8").strip() if version_file.is_file() else "unknown"


def _ttl_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def generate_technique_catalog() -> int:
    """Emit ``solveit-technique-catalog.ttl`` from the vendored KB.

    Each SOLVE-IT technique keeps its canonical knowledge-base IRI and is
    punned as an ``owl:Class`` typed ``uco-action:Technique`` subclassing
    ``uco-action:Action`` and carrying ``uco-action:techniqueID`` — the UCO
    1.5.0 metaclass pattern (PR #676), identical in shape to
    ``extensions/attack-technique/mitre-attack-catalog.ttl``. The punning is
    additive: the same IRIs remain ``solveit-core:Technique`` individuals in
    the knowledge base, so both modeling styles interoperate in one graph.
    """

    import rdflib
    from rdflib import RDF, RDFS, URIRef

    graph = rdflib.Graph()
    graph.parse(str(EXT_DIR / KB_FILE), format="turtle")

    technique_class = URIRef(SOLVEIT_CORE + "Technique")
    objective_class = URIRef(SOLVEIT_CORE + "Objective")
    technique_id = URIRef(SOLVEIT_CORE + "techniqueID")
    technique_name = URIRef(SOLVEIT_CORE + "techniqueName")
    includes_technique = URIRef(SOLVEIT_CORE + "includesTechnique")
    objective_name = URIRef(SOLVEIT_CORE + "objectiveName")

    # technique IRI -> objective names, for the catalog comments.
    objectives_of: dict[str, list[str]] = {}
    for objective in graph.subjects(RDF.type, objective_class):
        name_lit = graph.value(objective, objective_name)
        if name_lit is None:
            continue
        for tech in graph.objects(objective, includes_technique):
            objectives_of.setdefault(str(tech), []).append(str(name_lit))

    entries: list[tuple[str, str]] = []  # (technique id, turtle block)
    for tech in graph.subjects(RDF.type, technique_class):
        tid = graph.value(tech, technique_id)
        if tid is None:
            continue
        name_lit = graph.value(tech, technique_name)
        label = _ttl_escape(str(name_lit)) if name_lit else str(tid)
        objectives = sorted(set(objectives_of.get(str(tech), [])))
        comment = f"SOLVE-IT technique {tid}: {label}."
        if objectives:
            comment += " Objective(s): " + "; ".join(_ttl_escape(o) for o in objectives) + "."
        comment += " See https://solveit-df.org for weaknesses and mitigations."
        block = (
            f"<{tech}>\n"
            f"\ta owl:Class , action:Technique ;\n"
            f"\trdfs:subClassOf action:Action ;\n"
            f'\trdfs:label "{_ttl_escape(str(tid))}: {label}"@en ;\n'
            f'\trdfs:comment "{_ttl_escape(comment)}"@en ;\n'
            f'\taction:techniqueID "{_ttl_escape(str(tid))}" ;\n'
            f"\t.\n"
        )
        entries.append((str(tid), block))

    entries.sort(key=lambda item: item[0])
    header = (
        "# SOLVE-IT technique catalog — GENERATED FILE, do not edit by hand.\n"
        "# Regenerate with: python3 mcp_server/tools/sync_solveit.py --skip-fetch\n"
        "#\n"
        "# Every SOLVE-IT technique punned as an owl:Class typed\n"
        "# uco-action:Technique per the UCO 1.5.0 metaclass pattern\n"
        "# (ucoProject/UCO PR #676), forward-implemented by the bundled\n"
        "# attack-technique extension. IRIs are the canonical SOLVE-IT\n"
        "# knowledge-base IRIs, so the punned classes and the native\n"
        "# solveit-core:Technique individuals coexist in one graph.\n"
        "#\n"
        f"# Source: {SOLVEIT_DATA} (see manifest.json provenance block)\n"
        "\n"
        "@prefix action: <https://ontology.unifiedcyberontology.org/uco/action/> .\n"
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        "\n"
    )
    output = header + "\n".join(block for _, block in entries)
    (EXT_DIR / CATALOG_FILE).write_text(output, encoding="utf-8")

    # Round-trip check: the generated catalog must parse.
    rdflib.Graph().parse(str(EXT_DIR / CATALOG_FILE), format="turtle")
    print(f"generated {CATALOG_FILE}: {len(entries)} techniques")
    return len(entries)


def verify_vendored_files() -> dict[str, int]:
    """All vendored TTLs must parse; returns triple counts per file."""

    import rdflib

    counts: dict[str, int] = {}
    for name in ONTOLOGY_FILES + [KB_FILE, CATALOG_FILE]:
        graph = rdflib.Graph()
        graph.parse(str(EXT_DIR / name), format="turtle")
        counts[name] = len(graph)
    return counts


def update_manifest_provenance(
    commit: str | None,
    release_tag: str | None,
    ontology_version: str,
    technique_count: int,
) -> None:
    manifest_path = EXT_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    provenance = manifest.setdefault("provenance", {})
    if commit:
        provenance["ontology_repo"] = f"https://github.com/{ONTOLOGY_REPO}"
        provenance["ontology_commit"] = commit
    if release_tag:
        provenance["knowledge_base_repo"] = f"https://github.com/{KB_REPO}"
        provenance["knowledge_base_release"] = release_tag
    provenance["ontology_version"] = ontology_version
    provenance["technique_count"] = technique_count
    provenance["synced"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    provenance["sync_tool"] = "mcp_server/tools/sync_solveit.py"
    manifest["version"] = ontology_version
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"updated manifest provenance (ontology {ontology_version}, "
          f"{technique_count} techniques)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ontology-ref", default="main",
                        help="solve-it-ontology branch/tag/commit to vendor (default: main)")
    parser.add_argument("--release-tag", default=None,
                        help="SOLVE-IT knowledge-base release tag being targeted "
                             "(recorded in provenance; default: latest upstream release)")
    parser.add_argument("--source-dir", type=Path, default=None,
                        help="read upstream files from a local directory (air-gapped)")
    parser.add_argument("--skip-fetch", action="store_true",
                        help="regenerate the technique catalog and provenance from "
                             "already-vendored files without downloading")
    args = parser.parse_args(argv)

    EXT_DIR.mkdir(parents=True, exist_ok=True)

    commit: str | None = None
    release_tag = args.release_tag
    if args.source_dir:
        ontology_version = copy_from_source_dir(args.source_dir)
    elif args.skip_fetch:
        manifest = json.loads((EXT_DIR / "manifest.json").read_text(encoding="utf-8"))
        provenance = manifest.get("provenance", {})
        commit = provenance.get("ontology_commit")
        release_tag = release_tag or provenance.get("knowledge_base_release")
        ontology_version = provenance.get("ontology_version", manifest.get("version", "unknown"))
    else:
        commit = _resolve_commit(args.ontology_ref)
        print(f"pinned solve-it-ontology commit: {commit}")
        ontology_version = fetch_upstream(commit)
        if release_tag is None:
            release_tag = _latest_release_tag()

    technique_count = generate_technique_catalog()
    counts = verify_vendored_files()
    for name, triples in sorted(counts.items()):
        print(f"  {name}: {triples} triples")
    update_manifest_provenance(commit, release_tag, ontology_version, technique_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
