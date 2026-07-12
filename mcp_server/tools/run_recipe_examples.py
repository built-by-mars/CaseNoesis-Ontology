#!/usr/bin/env python3
"""Execute recipe exemplar builders and optionally validate (#69).

Builders run in isolated temporary directories with a subprocess timeout.
Outputs are RDF-parsed (JSON-LD/Turtle via RDFLib) before validation.
When ``--validate`` is set, ``case_validate`` must be available (fail-closed).

Usage:
  python mcp_server/tools/run_recipe_examples.py --category upper-ontology
  python mcp_server/tools/run_recipe_examples.py --all --validate
  python mcp_server/tools/run_recipe_examples.py --all --validate --report /tmp/report.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/recipes/recipe-execution.json"
DEFAULT_TIMEOUT_SECONDS = 120


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _rdf_parse(path: Path) -> None:
    """Parse graph as RDF; raise ValueError on failure."""
    import rdflib

    g = rdflib.Graph()
    suffix = path.suffix.lower()
    if suffix in {".json", ".jsonld", ".json-ld"}:
        fmt = "json-ld"
    elif suffix in {".ttl", ".turtle"}:
        fmt = "turtle"
    else:
        raise ValueError(f"unsupported_graph_extension:{suffix}")
    g.parse(str(path), format=fmt)
    if len(g) == 0:
        raise ValueError("empty_rdf_graph")


def _run_competency_queries(graph_path: Path, queries: list[dict]) -> list[dict]:
    """Run SPARQL SELECT queries and compare to expected bindings."""
    import rdflib

    g = rdflib.Graph()
    fmt = "json-ld" if graph_path.suffix.lower() in {".json", ".jsonld", ".json-ld"} else "turtle"
    g.parse(str(graph_path), format=fmt)
    outcomes: list[dict] = []
    for spec in queries:
        qpath = ROOT / spec["query"]
        if not qpath.is_file():
            outcomes.append({"query": spec["query"], "ok": False, "error": "query_missing"})
            continue
        sparql = qpath.read_text(encoding="utf-8")
        rows = list(g.query(sparql))
        expected = spec.get("expected_count")
        min_count = spec.get("min_count")
        ok = True
        detail: dict = {"query": spec["query"], "actual_count": len(rows)}
        if expected is not None and len(rows) != int(expected):
            ok = False
            detail["error"] = f"expected_count:{expected}"
        if min_count is not None and len(rows) < int(min_count):
            ok = False
            detail["error"] = f"min_count:{min_count}"
        detail["ok"] = ok
        outcomes.append(detail)
    return outcomes


def run_entry(
    entry: dict,
    *,
    validate: bool,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    keep_generated: bool = False,
) -> dict:
    result = {
        "id": entry["id"],
        "ok": False,
        "builder": entry.get("builder"),
        "output": entry.get("output"),
    }
    builder = ROOT / entry["builder"]
    if not builder.is_file():
        result["error"] = "builder_missing"
        return result

    import os

    output_name = Path(entry["output"]).name
    with tempfile.TemporaryDirectory(prefix=f"recipe-{entry['id']}-") as tmp:
        tmp_dir = Path(tmp)
        tmp_builder = tmp_dir / builder.name
        shutil.copy2(builder, tmp_builder)
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{ROOT / 'python'}:{ROOT / 'mcp_server'}" + (
            f":{env['PYTHONPATH']}" if env.get("PYTHONPATH") else ""
        )
        try:
            proc = subprocess.run(
                [sys.executable, str(tmp_builder)],
                cwd=str(tmp_dir),
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds,
                env=env,
            )
        except subprocess.TimeoutExpired:
            result["error"] = "builder_timeout"
            return result
        if proc.returncode != 0:
            result["error"] = "builder_failed"
            result["stderr"] = (proc.stderr or "")[-2000:]
            return result
        tmp_output = tmp_dir / output_name
        if not tmp_output.is_file():
            # Some builders may write under a nested name matching OUTPUT basename only
            candidates = list(tmp_dir.rglob(output_name))
            if not candidates:
                result["error"] = "output_missing"
                result["stdout"] = (proc.stdout or "")[-1000:]
                return result
            tmp_output = candidates[0]
        try:
            _rdf_parse(tmp_output)
        except Exception as exc:
            result["error"] = f"rdf_parse_failed:{exc}"
            return result

        if keep_generated:
            dest = ROOT / entry["output"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_output, dest)
            result["committed_output"] = str(dest)

        if not validate:
            result["ok"] = True
            return result

        if entry.get("profiles") is None and not entry.get("extensions"):
            result["error"] = "validation_profiles_required"
            return result

        sys.path.insert(0, str(ROOT / "mcp_server"))
        from graph_validator import validate_graph_file, validator_available

        if not validator_available():
            result["error"] = "validator_unavailable"
            return result

        report = validate_graph_file(
            tmp_output,
            project_root=ROOT,
            extensions=entry.get("extensions"),
            profiles=entry.get("profiles") or None,
            strict_concepts=bool(entry.get("strict_concepts", True)),
            allow_foundational_pair=bool(entry.get("allow_foundational_pair", False)),
        )
        result["conforms"] = report.conforms
        result["verification_status"] = report.verification_status
        result["summary"] = report.safe_summary
        result["bundle_fingerprint"] = report.bundle_fingerprint
        result["selected_profiles"] = list(report.selected_profiles)
        if report.conforms is not True:
            result["error"] = "validation_failed"
            return result
        if report.verification_status != "complete":
            result["error"] = f"verification_incomplete:{report.verification_status}"
            return result

        for invalid_path in entry.get("expect_invalid") or []:
            invalid_file = ROOT / invalid_path
            if not invalid_file.is_file():
                result["error"] = f"expect_invalid_missing:{invalid_path}"
                return result
            try:
                _rdf_parse(invalid_file)
            except Exception as exc:
                result["error"] = f"expect_invalid_rdf_parse_failed:{exc}"
                return result
            invalid_report = validate_graph_file(
                invalid_file,
                project_root=ROOT,
                extensions=entry.get("extensions"),
                profiles=entry.get("profiles") or None,
                strict_concepts=bool(entry.get("strict_concepts", True)),
                allow_foundational_pair=bool(entry.get("allow_foundational_pair", False)),
            )
            if invalid_report.conforms is True:
                result["error"] = f"expect_invalid_conforms:{invalid_path}"
                return result
            result.setdefault("expect_invalid_results", []).append(
                {
                    "path": invalid_path,
                    "conforms": invalid_report.conforms,
                    "verification_status": invalid_report.verification_status,
                }
            )

        competency = entry.get("competency_queries") or []
        if competency:
            outcomes = _run_competency_queries(tmp_output, competency)
            result["competency_queries"] = outcomes
            if any(not o.get("ok") for o in outcomes):
                result["error"] = "competency_query_failed"
                return result

    result["ok"] = True
    return result


def run_manifest_entries(
    entries: list[dict],
    *,
    validate: bool,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    keep_generated: bool = False,
) -> dict:
    results = [
        run_entry(
            e,
            validate=validate,
            timeout_seconds=timeout_seconds,
            keep_generated=keep_generated,
        )
        for e in entries
    ]
    failed = [r for r in results if not r["ok"]]
    return {
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
    }


def entries_for_recipe_slug(slug: str) -> list[dict]:
    """Return execution-manifest entries whose recipe path matches ``slug``."""
    manifest = load_manifest()
    needle = f"{slug}.md"
    return [
        e
        for e in manifest["recipes"]
        if Path(e.get("recipe", "")).name == needle or e.get("id") == slug
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", default="upper-ontology")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument(
        "--keep-generated",
        action="store_true",
        help="Copy builder output back into the repository tree after a successful run.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Write machine-readable JSON report to this path.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    entries = manifest["recipes"]
    if args.id:
        entries = [e for e in entries if e["id"] in args.id]
    elif not args.all:
        entries = [e for e in entries if e.get("category") == args.category]

    try:
        summary = run_manifest_entries(
            entries,
            validate=args.validate,
            timeout_seconds=args.timeout,
            keep_generated=args.keep_generated,
        )
    except subprocess.TimeoutExpired as exc:
        print(json.dumps({"error": "builder_timeout", "detail": str(exc)}, indent=2))
        return 1

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
