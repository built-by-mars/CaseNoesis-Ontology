#!/usr/bin/env python3
"""Execute recipe exemplar builders and optionally validate (#69).

Usage:
  python mcp_server/tools/run_recipe_examples.py --category upper-ontology
  python mcp_server/tools/run_recipe_examples.py --all --validate
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/recipes/recipe-execution.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def run_entry(entry: dict, *, validate: bool) -> dict:
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
    proc = subprocess.run(
        [sys.executable, str(builder)],
        cwd=str(builder.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        result["error"] = "builder_failed"
        result["stderr"] = proc.stderr[-2000:]
        return result
    output = ROOT / entry["output"]
    if not output.is_file():
        result["error"] = "output_missing"
        return result
    try:
        json.loads(output.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result["error"] = f"invalid_jsonld:{exc}"
        return result

    if validate and entry.get("profiles") is not None:
        sys.path.insert(0, str(ROOT / "mcp_server"))
        from graph_validator import validate_graph_file, validator_available

        if not validator_available():
            result["error"] = "validator_unavailable"
            return result
        report = validate_graph_file(
            output,
            project_root=ROOT,
            extensions=entry.get("extensions"),
            profiles=entry.get("profiles") or None,
            strict_concepts=bool(entry.get("strict_concepts", True)),
            allow_foundational_pair=bool(entry.get("allow_foundational_pair", False)),
        )
        result["conforms"] = report.conforms
        result["summary"] = report.safe_summary
        if report.conforms is not True:
            result["error"] = "validation_failed"
            return result

    result["ok"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", default="upper-ontology")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    args = parser.parse_args()

    manifest = load_manifest()
    entries = manifest["recipes"]
    if args.id:
        entries = [e for e in entries if e["id"] in args.id]
    elif not args.all:
        entries = [e for e in entries if e.get("category") == args.category]

    results = [run_entry(e, validate=args.validate) for e in entries]
    failed = [r for r in results if not r["ok"]]
    summary = {
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
    }
    print(json.dumps(summary, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
