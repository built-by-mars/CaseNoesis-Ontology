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
    undeclared_concepts: tuple[str, ...] = ()
    concept_guidance: str = ""
    unknown_upper_ontology_terms: tuple[str, ...] = ()
    role_mismatches: tuple[tuple[str, str, str], ...] = ()


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


def resolve_extension_dependencies(
    extension_names: list[str],
    project_root: Path = PROJECT_ROOT,
) -> list[str]:
    """Expand an extension list with manifest ``depends_on`` entries.

    An extension whose exemplars/graphs reuse another extension's terms (e.g.
    ``rico`` builds on ``legalproc``) declares ``"depends_on": [...]`` in its
    manifest; callers then only need to name the top-level extension. The
    ``:full`` suffix on a requested name is preserved; dependencies load in
    their default (subset-preferred) mode. Cycles are tolerated.
    """

    resolved: list[str] = []
    seen: set[str] = set()
    queue = list(extension_names)
    while queue:
        name = queue.pop(0)
        clean = name.removesuffix(":full")
        if clean in seen:
            continue
        seen.add(clean)
        resolved.append(name)
        manifest_path = project_root / "extensions" / clean / "manifest.json"
        if manifest_path.is_file():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for dep in manifest.get("depends_on", []):
                if dep not in seen:
                    queue.append(dep)
    return resolved


def extension_has_validation_subset(ext_name: str, project_root: Path = PROJECT_ROOT) -> bool:
    """Return True when an extension publishes a validation-subset manifest."""

    return (project_root / "extensions" / ext_name / "validation-subset.json").is_file()


def extension_ontology_args(
    extension_names: list[str] | None,
    project_root: Path = PROJECT_ROOT,
) -> list[str]:
    """Build case_validate flags for one or more extension manifests."""

    if not extension_names:
        return []
    extension_names = resolve_extension_dependencies(extension_names, project_root)
    args: list[str] = [
        "--built-version",
        DEFAULT_BUILT_VERSION,
        "--allow-info",
    ]
    used_subset = False
    for ext_name in extension_names:
        mode = "full" if ext_name.endswith(":full") else "subset"
        clean_name = ext_name.removesuffix(":full")
        if mode == "subset" and extension_has_validation_subset(clean_name, project_root):
            used_subset = True
        rel_paths = load_extension_ontology_paths(
            clean_name, mode=mode, project_root=project_root
        )
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
    strict_concepts: bool = True,
) -> GraphValidationReport:
    """Validate a CASE/UCO graph file with the local case_validate tool.

    When ``strict_concepts`` is True (the default), the SHACL pass is followed
    by a closed-world concept coverage check: every class and property IRI in
    the graph must be declared in CASE/UCO or a supported extension ontology.
    Undeclared concepts force ``conforms=False`` with guidance to draft a
    change proposal or add the concept to an extension ontology.

    Raises ValueError with a typed message for every honest-failure path:
    ``validator_unavailable``, ``graph_missing``, ``unsupported_graph_extension``,
    ``graph_oversized``, ``validation_timeout``.
    """

    if not validator_available():
        raise ValueError("validator_unavailable")
    # Deployment filesystem policy: graph reads must stay inside configured
    # read roots (typed error "source_outside_read_roots" when violated).
    import workspace_policy

    graph = workspace_policy.check_read_path(graph_path, include_write_roots=True)
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

    undeclared: tuple[str, ...] = ()
    concept_guidance = ""
    unknown_upper: tuple[str, ...] = ()
    role_mismatches: tuple[tuple[str, str, str], ...] = ()
    if strict_concepts:
        try:
            from concept_coverage import check_graph_concepts

            coverage = check_graph_concepts(
                graph, project_root=project_root, extensions=extensions
            )
        except Exception as exc:  # honest failure: never fake coverage
            conforms = None
            summary = (
                f"{summary} Additionally, the concept coverage check could "
                f"not run ({type(exc).__name__}); treat the result as "
                "unverified."
            )
        else:
            if not coverage.ok:
                undeclared = coverage.undeclared_classes + coverage.undeclared_properties
                unknown_upper = coverage.unknown_upper_ontology_terms
                role_mismatches = coverage.role_mismatches
                concept_guidance = coverage.guidance
                shacl_passed = conforms is not False and violation_count == 0
                conforms = False
                parts: list[str] = []
                if undeclared:
                    shown = ", ".join(undeclared[:8])
                    more = f" (+{len(undeclared) - 8} more)" if len(undeclared) > 8 else ""
                    parts.append(
                        f"Graph uses {len(undeclared)} class/property term(s) not declared "
                        f"in CASE/UCO or supported extension ontologies: {shown}{more}."
                    )
                if unknown_upper:
                    shown = ", ".join(unknown_upper[:8])
                    parts.append(
                        f"Graph uses {len(unknown_upper)} term(s) inside profiled "
                        f"upper-ontology namespaces that the pinned ontology releases "
                        f"do not declare: {shown}."
                    )
                if role_mismatches:
                    shown = "; ".join(
                        f"{iri} (declared as {declared_role}, used as {used_as})"
                        for iri, declared_role, used_as in role_mismatches[:4]
                    )
                    parts.append(
                        f"Graph uses {len(role_mismatches)} declared term(s) in the "
                        f"wrong RDF role: {shown}."
                    )
                parts.append(
                    "Draft a change proposal or add the concept(s) to an extension "
                    "ontology, then re-validate."
                )
                concept_summary = " ".join(parts)
                summary = concept_summary if shacl_passed else f"{summary} {concept_summary}"

    return GraphValidationReport(
        conforms=conforms,
        warning_count=warning_count,
        violation_count=violation_count,
        exit_code=exit_code,
        validator_name=VALIDATOR_NAME,
        safe_summary=summary,
        undeclared_concepts=undeclared,
        concept_guidance=concept_guidance,
        unknown_upper_ontology_terms=unknown_upper,
        role_mismatches=role_mismatches,
    )


def report_to_dict(report: GraphValidationReport) -> dict[str, Any]:
    """Serialize a report into the MCP tool result shape."""

    payload = {
        "conforms": report.conforms,
        "warning_count": report.warning_count,
        "violation_count": report.violation_count,
        "exit_code": report.exit_code,
        "validator_name": report.validator_name,
        "safe_summary": report.safe_summary,
    }
    if report.undeclared_concepts:
        payload["undeclared_concepts"] = list(report.undeclared_concepts)
    if report.unknown_upper_ontology_terms:
        payload["unknown_upper_ontology_terms"] = list(
            report.unknown_upper_ontology_terms
        )
    if report.role_mismatches:
        payload["role_mismatches"] = [
            {"iri": iri, "declared_role": declared_role, "used_as": used_as}
            for iri, declared_role, used_as in report.role_mismatches
        ]
    if report.concept_guidance:
        payload["concept_guidance"] = report.concept_guidance
    return payload


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
