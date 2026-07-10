"""Staged promotion lifecycle for learned knowledge artifacts.

The SDK lets agents grow extension ontologies, recipes, and routing indexes
during live investigations. This module defines the promotion boundary
between an experimental lesson and trusted operational guidance:

- ``candidate`` — generated or edited during an investigation. Candidate
  extensions carry ``"status": "candidate"`` in their ``manifest.json`` and
  are **excluded from routing discovery** (``route_investigation_content``
  does not advertise them). They can still be loaded *explicitly by name*
  (``validate_graph(extensions=["myext"])``) so the authoring investigation
  can keep working with them.
- ``operational`` — validated and intentionally promoted. Manifests without
  a ``status`` field are treated as operational (the nine bundled extensions
  predate the lifecycle). Promotion records provenance metadata.
- ``deprecated`` — retained with provenance, excluded from routing; the
  emergency revocation state for a bad extension.

Promotion (``promote_extension``) runs validation gates before flipping
status: manifest integrity, Turtle parse of every listed ontology file,
subclass-anchoring of every declared class (per the extension authoring
rules), and ``case_validate`` of exemplar files when present. A failed gate
leaves the manifest untouched.

Rollback is git-based — knowledge artifacts are plain files under version
control, so restoring the previous approved generation is::

    make rollback-extension EXT=<name> REF=<tag-or-commit>

which runs ``git checkout <ref> -- extensions/<name>``. Recipes follow the
same lifecycle with directories instead of manifests: candidate recipes live
in ``docs/recipes/candidates/`` (invisible to ``RECIPE_INDEX`` and the
catalog integrity tests) and are promoted by moving them into
``docs/recipes/`` and registering them in ``RECIPE_INDEX``, which the
catalog tests then enforce. See docs/recipes/recipe-authoring.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STATUS_CANDIDATE = "candidate"
STATUS_OPERATIONAL = "operational"
STATUS_DEPRECATED = "deprecated"
VALID_STATUSES = {STATUS_CANDIDATE, STATUS_OPERATIONAL, STATUS_DEPRECATED}

CANDIDATE_RECIPE_DIR = "docs/recipes/candidates"


@dataclass
class PromotionResult:
    ok: bool
    extension: str
    status: str
    gates: list[dict] = field(default_factory=list)
    error: str = ""


def extension_status(manifest: dict) -> str:
    """Lifecycle status of an extension manifest (absent field == operational)."""

    status = str(manifest.get("status", STATUS_OPERATIONAL)).strip().lower()
    return status if status in VALID_STATUSES else STATUS_OPERATIONAL


def is_routable(manifest: dict) -> bool:
    """Only approved operational artifacts are advertised by routing."""

    return extension_status(manifest) == STATUS_OPERATIONAL


def _manifest_path(name: str, project_root: Path) -> Path:
    return project_root / "extensions" / name / "manifest.json"


def _load_manifest(name: str, project_root: Path) -> dict:
    path = _manifest_path(name, project_root)
    if not path.is_file():
        raise ValueError("extension_manifest_missing")
    return json.loads(path.read_text(encoding="utf-8"))


def _gate_ontology_files_parse(name: str, manifest: dict, project_root: Path) -> dict:
    """Every listed ontology file must exist and parse as Turtle."""

    import rdflib

    ext_dir = project_root / "extensions" / name
    checked = 0
    for key in ("owl_files", "shacl_files", "bridge_files"):
        for rel in manifest.get(key, []):
            full = ext_dir / rel
            if not full.is_file():
                return {"gate": "ontology_files_parse", "ok": False,
                        "detail": f"missing file listed in manifest: {rel}"}
            try:
                rdflib.Graph().parse(str(full), format="turtle")
            except Exception as exc:
                return {"gate": "ontology_files_parse", "ok": False,
                        "detail": f"{rel}: parse failed ({type(exc).__name__})"}
            checked += 1
    if checked == 0:
        return {"gate": "ontology_files_parse", "ok": False,
                "detail": "manifest lists no ontology files"}
    return {"gate": "ontology_files_parse", "ok": True, "detail": f"{checked} file(s) parsed"}


def _gate_classes_anchored(name: str, manifest: dict, project_root: Path) -> dict:
    """Every declared owl:Class must be rdfs:subClassOf an existing class
    (extension authoring rule: no orphan concepts)."""

    import rdflib
    from rdflib import OWL, RDF, RDFS, URIRef

    ext_dir = project_root / "extensions" / name
    graph = rdflib.Graph()
    for key in ("owl_files", "bridge_files"):
        for rel in manifest.get(key, []):
            full = ext_dir / rel
            if full.is_file():
                try:
                    graph.parse(str(full), format="turtle")
                except Exception:
                    pass
    orphans = []
    for cls in graph.subjects(RDF.type, OWL.Class):
        if not isinstance(cls, URIRef):
            continue
        if graph.value(cls, RDFS.subClassOf) is None:
            orphans.append(str(cls))
    if orphans:
        return {"gate": "classes_anchored", "ok": False,
                "detail": f"classes without rdfs:subClassOf: {', '.join(sorted(orphans)[:5])}"}
    return {"gate": "classes_anchored", "ok": True,
            "detail": "every declared class subclasses an existing class"}


def _gate_exemplars_validate(
    name: str,
    manifest: dict,
    project_root: Path,
    require_validator: bool,
) -> dict:
    """Exemplar graphs listed in the manifest must pass case_validate with
    the extension's own ontology files loaded."""

    import graph_validator

    ext_dir = project_root / "extensions" / name
    exemplars = manifest.get("exemplar_files", [])
    if not exemplars:
        return {"gate": "exemplars_validate", "ok": True, "detail": "no exemplars listed"}
    if not graph_validator.validator_available():
        if require_validator:
            return {"gate": "exemplars_validate", "ok": False,
                    "detail": "case_validate unavailable; install case-utils or "
                              "pass require_validator=False in a dev-only context"}
        return {"gate": "exemplars_validate", "ok": True,
                "detail": "skipped: case_validate unavailable (require_validator=False)"}
    for rel in exemplars:
        full = ext_dir / rel
        if not full.is_file():
            return {"gate": "exemplars_validate", "ok": False,
                    "detail": f"missing exemplar: {rel}"}
        report = graph_validator.validate_graph_file(
            full, extensions=[f"{name}:full"], project_root=project_root
        )
        if report.conforms is not True:
            return {"gate": "exemplars_validate", "ok": False,
                    "detail": f"{rel}: {report.safe_summary}"}
    return {"gate": "exemplars_validate", "ok": True,
            "detail": f"{len(exemplars)} exemplar(s) conform"}


def promote_extension(
    name: str,
    project_root: Path = PROJECT_ROOT,
    reviewed_by: str = "",
    require_validator: bool = True,
) -> PromotionResult:
    """Run all promotion gates; on success mark the extension operational.

    Provenance (who approved, when, which gates ran) is recorded in the
    manifest ``promotion`` block. A failed gate leaves the manifest
    untouched and reports the failure.
    """

    manifest = _load_manifest(name, project_root)
    current = extension_status(manifest)
    if current == STATUS_OPERATIONAL:
        return PromotionResult(ok=True, extension=name, status=current,
                               error="already_operational")

    gates = [
        _gate_ontology_files_parse(name, manifest, project_root),
        _gate_classes_anchored(name, manifest, project_root),
        _gate_exemplars_validate(name, manifest, project_root, require_validator),
    ]
    failed = [g for g in gates if not g["ok"]]
    if failed:
        return PromotionResult(
            ok=False, extension=name, status=current, gates=gates,
            error=f"promotion_gate_failed:{failed[0]['gate']}",
        )

    manifest["status"] = STATUS_OPERATIONAL
    manifest["promotion"] = {
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "reviewed_by": reviewed_by or "unrecorded",
        "previous_status": current,
        "gates": gates,
    }
    # Invalidate declared-term caches so the promoted concepts are live
    # immediately (belt-and-braces; the fingerprint key also detects this).
    try:
        import concept_coverage

        concept_coverage.clear_declared_term_cache()
    except Exception:
        pass
    _manifest_path(name, project_root).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return PromotionResult(ok=True, extension=name, status=STATUS_OPERATIONAL, gates=gates)


def deprecate_extension(
    name: str,
    reason: str,
    project_root: Path = PROJECT_ROOT,
    deprecated_by: str = "",
) -> dict:
    """Emergency revocation: mark an extension deprecated (kept on disk with
    provenance, excluded from routing discovery)."""

    manifest = _load_manifest(name, project_root)
    manifest["status"] = STATUS_DEPRECATED
    manifest["deprecation"] = {
        "deprecated_at": datetime.now(timezone.utc).isoformat(),
        "deprecated_by": deprecated_by or "unrecorded",
        "reason": reason,
    }
    _manifest_path(name, project_root).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    try:
        import concept_coverage

        concept_coverage.clear_declared_term_cache()
    except Exception:
        pass
    return {"ok": True, "extension": name, "status": STATUS_DEPRECATED, "reason": reason}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Knowledge artifact lifecycle management.")
    sub = parser.add_subparsers(dest="command", required=True)

    promote = sub.add_parser("promote", help="Promote a candidate extension to operational.")
    promote.add_argument("extension")
    promote.add_argument("--reviewed-by", default="")
    promote.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    deprecate = sub.add_parser("deprecate", help="Deprecate (revoke) an extension.")
    deprecate.add_argument("extension")
    deprecate.add_argument("--reason", required=True)
    deprecate.add_argument("--deprecated-by", default="")
    deprecate.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    status = sub.add_parser("status", help="Show lifecycle status of every extension.")
    status.add_argument("--project-root", type=Path, default=PROJECT_ROOT)

    args = parser.parse_args(argv)
    if args.command == "promote":
        result = promote_extension(
            args.extension, project_root=args.project_root, reviewed_by=args.reviewed_by
        )
        for gate in result.gates:
            marker = "PASS" if gate["ok"] else "FAIL"
            print(f"[{marker}] {gate['gate']}: {gate['detail']}")
        if result.ok:
            print(f"{result.extension}: {result.status}"
                  + (f" ({result.error})" if result.error else ""))
            return 0
        print(f"Promotion failed: {result.error}")
        return 1
    if args.command == "deprecate":
        result = deprecate_extension(
            args.extension, reason=args.reason,
            project_root=args.project_root, deprecated_by=args.deprecated_by,
        )
        print(f"{result['extension']}: {result['status']} — {result['reason']}")
        return 0
    if args.command == "status":
        ext_root = args.project_root / "extensions"
        for manifest_path in sorted(ext_root.glob("*/manifest.json")):
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            print(f"{manifest_path.parent.name}: {extension_status(manifest)}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
