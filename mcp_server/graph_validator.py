"""SHACL validation wrapper around the CASE Utilities ``case_validate`` CLI.

Gives MCP callers (AI agents, Link-Look, scripts) a bounded way to validate a
produced CASE/UCO graph file before it is submitted for human review. The
wrapper invokes the locally installed ``case_validate`` tool with an argument
array (no shell), parses its conformance report, and fails honestly with
typed errors when the validator or the graph file is unavailable.

This module never fabricates validation results: if ``case_validate`` is not
installed, callers receive ``validator_unavailable`` instead of a fake pass.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BUILT_VERSION = "case-1.4.0"

VALIDATOR_NAME = "case_validate"
SUPPORTED_GRAPH_EXTENSIONS = {".json", ".jsonld", ".json-ld", ".ttl", ".turtle"}
MAX_GRAPH_BYTES = 50 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 180

# Markers shared with Link-Look's graph_validation.rs parser so both sides of
# the roundtrip report the same conformance semantics.
_CONFORMS_KEY = "conforms"
_VIOLATION_MARKER = "Constraint Violation"
_WARNING_MARKER = "NonExistentCDOConceptWarning"


@dataclass(frozen=True)
class GraphValidationReport:
    """Structured, redaction-safe validation result."""

    conforms: bool | None
    warning_count: int
    violation_count: int
    exit_code: int
    validator_name: str
    safe_summary: str


def validator_available() -> bool:
    """Return True when the case_validate CLI is on PATH."""

    return shutil.which(VALIDATOR_NAME) is not None


def load_extension_ontology_paths(
    ext_name: str,
    *,
    mode: str = "subset",
    project_root: Path = PROJECT_ROOT,
) -> list[Path]:
    """Return ontology graph paths for an extension.

    mode ``subset`` uses ``extensions/<ext>/validation-subset.json`` when present
    (recommended for MCP / press-release KGs). mode ``full`` uses the extension
    manifest (all owl/shacl/bridge files).
    """

    ext_dir = project_root / "extensions" / ext_name
    paths: list[Path] = []
    if mode == "subset":
        subset_path = ext_dir / "validation-subset.json"
        if subset_path.exists():
            subset = json.loads(subset_path.read_text(encoding="utf-8"))
            for rel in subset.get("ontology_files", []):
                full = ext_dir / rel
                if full.exists():
                    paths.append(full)
            if paths:
                return paths
    manifest_path = ext_dir / "manifest.json"
    if not manifest_path.exists():
        return paths
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ("owl_files", "shacl_files", "bridge_files"):
        for rel_path in manifest.get(key, []):
            full_path = ext_dir / rel_path
            if full_path.exists():
                paths.append(full_path)
    return paths


def extension_ontology_args(
    extension_names: list[str] | None,
    project_root: Path = PROJECT_ROOT,
) -> list[str]:
    """Build case_validate flags for one or more extension manifests."""

    if not extension_names:
        return []
    args: list[str] = [
        "--built-version",
        DEFAULT_BUILT_VERSION,
        "--allow-info",
    ]
    used_subset = False
    for ext_name in extension_names:
        mode = "full" if ext_name.endswith(":full") else "subset"
        clean_name = ext_name.removesuffix(":full")
        rel_paths = load_extension_ontology_paths(
            clean_name, mode=mode, project_root=project_root
        )
        if mode == "subset" and rel_paths:
            used_subset = True
        for full_path in rel_paths:
            args.extend(["--ontology-graph", str(full_path)])
    if used_subset:
        pass  # subset modules are self-contained; skip rdfs inference
    else:
        args.extend(["--inference", "rdfs"])
    return args


def validate_graph_file(
    graph_path: str | Path,
    allow_warning: bool = True,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    extensions: list[str] | None = None,
    project_root: Path = PROJECT_ROOT,
) -> GraphValidationReport:
    """Validate a CASE/UCO graph file with the local case_validate tool.

    Raises ValueError with a typed message for every honest-failure path:
    ``validator_unavailable``, ``graph_missing``, ``unsupported_graph_extension``,
    ``graph_oversized``, ``validation_timeout``.
    """

    if not validator_available():
        raise ValueError("validator_unavailable")
    graph = Path(graph_path).expanduser().resolve()
    if not graph.exists() or not graph.is_file():
        raise ValueError("graph_missing")
    if graph.suffix.lower() not in SUPPORTED_GRAPH_EXTENSIONS:
        raise ValueError("unsupported_graph_extension")
    if graph.stat().st_size > MAX_GRAPH_BYTES:
        raise ValueError("graph_oversized")

    args = [VALIDATOR_NAME]
    if allow_warning:
        args.append("--allow-warning")
    extension_args = extension_ontology_args(extensions, project_root=project_root)
    if extension_args:
        args.extend(extension_args)
    elif extensions:
        args.extend(["--built-version", DEFAULT_BUILT_VERSION])
    args.append(str(graph))
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError("validation_timeout") from exc

    combined = f"{completed.stdout}\n{completed.stderr}"
    conforms = _parse_conforms(combined)
    violation_count = combined.count(_VIOLATION_MARKER)
    warning_count = combined.count(_WARNING_MARKER)
    exit_code = completed.returncode

    if exit_code == 0 and conforms is not False and violation_count == 0:
        if warning_count > 0:
            summary = (
                f"Graph conforms with {warning_count} validator warning(s); "
                "review warnings before relying on extension concepts."
            )
        elif extensions:
            mode_note = ""
            if any(not ext.endswith(":full") for ext in extensions):
                mode_note = " (validation-subset)"
            summary = (
                f"Graph conforms to CASE/UCO SHACL shapes with extension(s): "
                f"{', '.join(extensions)}.{mode_note}"
            )
        else:
            summary = "Graph conforms to CASE/UCO SHACL shapes."
    elif conforms is False or violation_count > 0:
        summary = (
            f"Graph does not conform: {violation_count} constraint violation(s). "
            "Fix the graph before submitting it for review."
        )
    else:
        summary = (
            "Validator could not produce a conformance result; "
            "the graph content may be malformed."
        )

    return GraphValidationReport(
        conforms=conforms,
        warning_count=warning_count,
        violation_count=violation_count,
        exit_code=exit_code,
        validator_name=VALIDATOR_NAME,
        safe_summary=summary,
    )


def report_to_dict(report: GraphValidationReport) -> dict[str, Any]:
    """Serialize a report into the MCP tool result shape."""

    return {
        "conforms": report.conforms,
        "warning_count": report.warning_count,
        "violation_count": report.violation_count,
        "exit_code": report.exit_code,
        "validator_name": report.validator_name,
        "safe_summary": report.safe_summary,
    }


def _parse_conforms(output: str) -> bool | None:
    for line in output.splitlines():
        key, sep, value = line.partition(":")
        if not sep or key.strip().lower() != _CONFORMS_KEY:
            continue
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    return None
