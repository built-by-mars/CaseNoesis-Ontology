"""Closed-world concept coverage checking for CASE/UCO/extension graphs.

SHACL validation only evaluates shapes whose target classes exist, so a graph
that types nodes with classes (or uses properties) that no supported ontology
declares can pass ``case_validate`` silently. This module closes that gap:
every class and property IRI used by a submitted graph must be declared in
the CASE/UCO core ontologies or in a supported extension ontology, otherwise
the graph is rejected with guidance to draft a change proposal or add the
concept to an extension ontology.

Once an extension ontology (or the upstream ontology) declares the concept,
the same graph passes without further changes — the declared-term set is
recomputed from the ontology files on disk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Namespaces whose terms are governed outside this SDK (W3C standards and
# vocabularies imported by the supported ontologies). Terms in these
# namespaces are never reported as undeclared.
STANDARD_NAMESPACE_PREFIXES: tuple[str, ...] = (
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/2001/XMLSchema#",
    "http://www.w3.org/ns/shacl#",
    "http://www.w3.org/2004/02/skos/core#",
    "http://purl.org/dc/terms/",
    "http://purl.org/dc/elements/1.1/",
    # W3C Web Annotation Data Model (https://www.w3.org/TR/annotation-model/),
    # used by document-annotation sidecar graphs.
    "http://www.w3.org/ns/oa#",
)

# Namespaces of external/upper ontologies that UCO maintains alignment
# profiles for, published by the CDO project as CDO-Shapes-* repositories
# (https://github.com/Cyber-Domain-Ontology). Because a UCO profile exists,
# graphs may use these ontologies' terms directly; strict concept coverage
# never reports them as undeclared. Discover the profiles with the
# get_uco_profiles() MCP tool. See docs/recipes/extensions.md.
UCO_PROFILE_NAMESPACE_PREFIXES: tuple[str, ...] = (
    # CDO-Shapes-BFO — Basic Formal Ontology 2020 (top-level)
    "http://purl.obolibrary.org/obo/BFO_",
    # CDO-Shapes-gufo — gentle Unified Foundational Ontology (top-level)
    "http://purl.org/nemo/gufo#",
    # CDO-Shapes-PROV-O — W3C Provenance Ontology
    "http://www.w3.org/ns/prov#",
    # CDO-Shapes-Time — W3C OWL-Time
    "http://www.w3.org/2006/time#",
    # CDO-Shapes-GeoSPARQL — OGC GeoSPARQL 1.1 (core + Simple Features geometries)
    "http://www.opengis.net/ont/geosparql#",
    "http://www.opengis.net/ont/sf#",
    # CDO-Shapes-FOAF — Friend-of-a-Friend
    "http://xmlns.com/foaf/0.1/",
    # CDO-Shapes-ORG — W3C Organization Ontology
    "http://www.w3.org/ns/org#",
    # CDO-Shapes-PROF — W3C Profiles Vocabulary
    "http://www.w3.org/ns/dx/prof/",
    # CDO-Shapes-SKOS and CDO-Shapes-OWL namespaces are already covered by
    # STANDARD_NAMESPACE_PREFIXES above.
)

CORE_ONTOLOGY_GLOBS: tuple[str, ...] = (
    "ontology/UCO/ontology/uco/*/*.ttl",
    "ontology/CASE/ontology/*/*.ttl",
)

GUIDANCE = (
    "Undeclared classes/properties found. Every term must be declared in "
    "CASE/UCO or a supported extension ontology before the graph can be "
    "accepted. Options: (1) draft an upstream change proposal — run "
    "check_existing_proposals(concept) then draft_change_proposal(...) per "
    "docs/recipes/change-proposal.md; (2) create or update an extension "
    "ontology declaring the terms (docs/recipes/extensions.md) and register "
    "it in the extension manifest / validation subset; (3) if the concept "
    "exists in an external/upper ontology, check get_uco_profiles() — terms "
    "from ontologies with a UCO profile (BFO, gUFO, PROV-O, OWL-Time, "
    "GeoSPARQL, FOAF, ORG) are accepted directly. Re-run validate_graph "
    "afterwards — the check passes as soon as the concept is declared."
)


@dataclass(frozen=True)
class ConceptCoverageReport:
    """Result of a closed-world concept coverage check."""

    ok: bool
    undeclared_classes: tuple[str, ...] = ()
    undeclared_properties: tuple[str, ...] = ()
    checked_class_count: int = 0
    checked_property_count: int = 0
    guidance: str = field(default="")

    @property
    def undeclared_total(self) -> int:
        return len(self.undeclared_classes) + len(self.undeclared_properties)


_DECLARED_CACHE: dict[tuple[str, tuple[str, ...]], frozenset[str]] = {}


def _core_ontology_paths(project_root: Path) -> list[Path]:
    paths: list[Path] = []
    for pattern in CORE_ONTOLOGY_GLOBS:
        for path in sorted(project_root.glob(pattern)):
            if "master" in path.parts or "dependencies" in path.parts:
                continue
            paths.append(path)
    return paths


def _extension_ontology_paths(project_root: Path, extensions: list[str]) -> list[Path]:
    # Import here to avoid a cycle at module load time.
    from graph_validator import load_extension_ontology_paths

    paths: list[Path] = []
    for ext_name in extensions:
        clean_name = ext_name.removesuffix(":full")
        # Full manifest, not subset: a concept declared in any module of a
        # supported extension counts as declared.
        paths.extend(
            load_extension_ontology_paths(clean_name, mode="full", project_root=project_root)
        )
    return paths


def load_declared_terms(
    project_root: Path = PROJECT_ROOT,
    extensions: list[str] | None = None,
) -> frozenset[str]:
    """Return every IRI declared (used as a subject) in supported ontologies.

    Any URIRef subject in an ontology file counts as declared — class,
    property, named individual, or shape. Parse failures in individual files
    are skipped (some extension files use cross-file prefixes).
    """

    key = (str(project_root), tuple(sorted(extensions or [])))
    cached = _DECLARED_CACHE.get(key)
    if cached is not None:
        return cached

    import rdflib
    from rdflib import URIRef

    declared: set[str] = set()
    paths = _core_ontology_paths(project_root)
    paths.extend(_extension_ontology_paths(project_root, extensions or []))
    for path in paths:
        graph = rdflib.Graph()
        try:
            graph.parse(str(path), format="turtle")
        except Exception:
            continue
        for subject in graph.subjects():
            if isinstance(subject, URIRef):
                declared.add(str(subject))
    result = frozenset(declared)
    _DECLARED_CACHE[key] = result
    return result


def _is_standard(iri: str) -> bool:
    return iri.startswith(STANDARD_NAMESPACE_PREFIXES) or iri.startswith(
        UCO_PROFILE_NAMESPACE_PREFIXES
    )


def check_graph_concepts(
    graph_path: str | Path,
    project_root: Path = PROJECT_ROOT,
    extensions: list[str] | None = None,
) -> ConceptCoverageReport:
    """Check that every class and property in a graph file is declared.

    Classes are the URIRef objects of ``rdf:type`` triples; properties are
    all predicates. Instance IRIs (kb:, urn:uuid:, …) never appear in either
    position, so no instance-namespace whitelist is needed.
    """

    import rdflib
    from rdflib import RDF, URIRef

    graph = rdflib.Graph()
    path = Path(graph_path)
    fmt = "json-ld" if path.suffix.lower() in {".json", ".jsonld", ".json-ld"} else "turtle"
    graph.parse(str(path), format=fmt)

    used_classes = {
        str(obj)
        for obj in graph.objects(predicate=RDF.type)
        if isinstance(obj, URIRef)
    }
    used_properties = {str(pred) for pred in graph.predicates()}

    declared = load_declared_terms(project_root=project_root, extensions=extensions)

    undeclared_classes = sorted(
        iri for iri in used_classes if not _is_standard(iri) and iri not in declared
    )
    undeclared_properties = sorted(
        iri
        for iri in used_properties
        if not _is_standard(iri) and iri not in declared
    )

    ok = not undeclared_classes and not undeclared_properties
    return ConceptCoverageReport(
        ok=ok,
        undeclared_classes=tuple(undeclared_classes),
        undeclared_properties=tuple(undeclared_properties),
        checked_class_count=len(used_classes),
        checked_property_count=len(used_properties),
        guidance="" if ok else GUIDANCE,
    )


def coverage_report_to_dict(report: ConceptCoverageReport) -> dict:
    """Serialize a coverage report into the MCP tool result shape."""

    payload: dict = {
        "ok": report.ok,
        "checked_class_count": report.checked_class_count,
        "checked_property_count": report.checked_property_count,
    }
    if not report.ok:
        payload["undeclared_classes"] = list(report.undeclared_classes)
        payload["undeclared_properties"] = list(report.undeclared_properties)
        payload["guidance"] = report.guidance
    return payload
