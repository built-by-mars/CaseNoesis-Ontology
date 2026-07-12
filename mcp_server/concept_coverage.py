"""Closed-world concept coverage checking for CASE/UCO/extension graphs.

SHACL validation only evaluates shapes whose target classes exist, so a graph
that types nodes with classes (or uses properties) that no supported ontology
declares can pass ``case_validate`` silently. This module closes that gap:
every class and property IRI used by a submitted graph must be declared in
the CASE/UCO core ontologies or in a supported extension ontology, otherwise
the graph is rejected with guidance to draft a change proposal or add the
concept to an extension ontology.

Three layers of checking:

1. **Declared-term membership** — every class/property must be declared in a
   supported ontology (core, extension, pinned upper-ontology registry, or a
   foundational W3C namespace).
2. **Exact upper-ontology terms** — profiled upper ontologies (BFO, gUFO,
   PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG, PROF) are validated against the
   pinned term registry (``upper_ontology_registry.json``) instead of
   whole-namespace acceptance, so fabricated terms inside a profiled
   namespace fail.
3. **RDF role awareness** — declarations are tracked by role (class,
   property, shape, individual). A declared class used as a predicate, or a
   declared property used as an ``rdf:type`` class, is reported as a role
   mismatch rather than silently accepted. OWL punning (e.g. the ATT&CK
   ``uco-action:Technique`` metaclass pattern where a term is both an
   ``owl:Class`` and an individual) is supported: any term declared as a
   class may be used as an ``rdf:type`` object.

Foundational W3C vocabulary policy: terms in RDF, RDFS, OWL, XSD, SHACL,
SKOS, Dublin Core, and Web Annotation namespaces are accepted by namespace
because they are governed by W3C specifications outside this SDK and are
imported wholesale by the supported ontologies.

Once an extension ontology (or the upstream ontology) declares the concept,
the same graph passes without further changes — the declared-term set is
recomputed whenever the ontology files on disk change (the cache key includes
a content fingerprint of every ontology file, so a term added, removed, or
renamed during the same server process is picked up on the next check).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPPER_ONTOLOGY_REGISTRY_PATH = Path(__file__).resolve().parent / "upper_ontology_registry.json"

# Namespaces whose terms are governed outside this SDK (W3C standards and
# vocabularies imported by the supported ontologies). Terms in these
# namespaces are never reported as undeclared. This is a deliberate,
# documented policy: these are foundational specification vocabularies, not
# domain ontologies, and the supported ontologies import them wholesale.
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
# graphs may use these ontologies' terms directly — but only *exact declared
# terms* from the pinned releases recorded in upper_ontology_registry.json.
# Fabricated terms inside these namespaces fail strict concept coverage.
# Discover the profiles with the get_uco_profiles() MCP tool. See
# docs/recipes/extensions.md. Regenerate the registry with
# mcp_server/tools/build_upper_ontology_registry.py.
# Map stable profile IDs to the namespace prefixes they authorize for
# profile-selective concept coverage (issue #68).
PROFILE_ID_TO_NAMESPACE_PREFIXES: dict[str, tuple[str, ...]] = {
    "bfo": ("http://purl.obolibrary.org/obo/BFO_",),
    "gufo": ("http://purl.org/nemo/gufo#",),
    "prov-o": ("http://www.w3.org/ns/prov#",),
    "time": ("http://www.w3.org/2006/time#",),
    "owl-time": ("http://www.w3.org/2006/time#",),
    "geosparql": (
        "http://www.opengis.net/ont/geosparql#",
        "http://www.opengis.net/ont/sf#",
    ),
    "foaf": ("http://xmlns.com/foaf/0.1/",),
    "org": ("http://www.w3.org/ns/org#",),
    "prof": ("http://www.w3.org/ns/dx/prof/",),
}

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
    "exists in an external/upper ontology, check get_uco_profiles() — exact "
    "declared terms from ontologies with a UCO profile (BFO, gUFO, PROV-O, "
    "OWL-Time, GeoSPARQL, FOAF, ORG, PROF) are accepted directly. Re-run "
    "validate_graph afterwards — the check passes as soon as the concept is "
    "declared."
)

UPPER_TERM_GUIDANCE = (
    "Terms flagged as unknown_upper_ontology_terms sit inside a profiled "
    "upper-ontology namespace (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, "
    "ORG, PROF) but are not declared by the pinned release of that ontology "
    "(see mcp_server/upper_ontology_registry.json for pinned versions). "
    "Check the ontology's specification for the correct term name; do not "
    "invent terms in external namespaces."
)

ROLE_MISMATCH_GUIDANCE = (
    "Terms flagged as role_mismatches are declared in a supported ontology "
    "but used in the wrong RDF position: a class cannot be used as a "
    "predicate, and a property cannot be the object of rdf:type. Punned "
    "class/individual terms (e.g. ATT&CK techniques via the "
    "uco-action:Technique metaclass) are supported — any declared owl:Class "
    "is valid as an rdf:type object."
)


@dataclass(frozen=True)
class ConceptCoverageReport:
    """Result of a closed-world concept coverage check.

    ``verification_status`` distinguishes a check that fully ran
    (``"complete"``) from one that could not perform a required stage
    (``"could_not_verify"``). Fail-closed policy: an inability to verify is
    never reported as a pass — when the pinned upper-ontology registry is
    missing or malformed and the graph uses profiled upper-ontology terms,
    the report is not ok and ``verification_errors`` names the failed stage.
    """

    ok: bool
    undeclared_classes: tuple[str, ...] = ()
    undeclared_properties: tuple[str, ...] = ()
    unknown_upper_ontology_terms: tuple[str, ...] = ()
    role_mismatches: tuple[tuple[str, str, str], ...] = ()  # (iri, declared_role, used_as)
    checked_class_count: int = 0
    checked_property_count: int = 0
    guidance: str = field(default="")
    verification_status: str = "complete"
    verification_errors: tuple[str, ...] = ()

    @property
    def undeclared_total(self) -> int:
        return (
            len(self.undeclared_classes)
            + len(self.undeclared_properties)
            + len(self.unknown_upper_ontology_terms)
            + len(self.role_mismatches)
        )


@dataclass(frozen=True)
class DeclaredTerms:
    """Declared ontology terms, tracked by RDF role.

    ``unknown_role`` holds subjects whose role could not be determined from
    the ontology files (annotation-only declarations, individuals, ontology
    metadata). They are accepted in any position for backward compatibility.
    """

    classes: frozenset[str]
    properties: frozenset[str]
    shapes: frozenset[str]
    unknown_role: frozenset[str]

    def __contains__(self, iri: str) -> bool:
        return (
            iri in self.classes
            or iri in self.properties
            or iri in self.shapes
            or iri in self.unknown_role
        )


_DECLARED_CACHE: dict[tuple, DeclaredTerms] = {}
_DECLARED_CACHE_MAX_ENTRIES = 16
_UPPER_REGISTRY_CACHE: dict[str, dict] = {}


def clear_declared_term_cache() -> None:
    """Drop every cached declared-term set.

    Ontology writes performed through supported tools (extension scaffolding,
    proposal-local declarations, package generation) may call this to force a
    reload, although the content-fingerprint cache key already detects file
    additions, removals, and modifications automatically.
    """

    _DECLARED_CACHE.clear()
    _UPPER_REGISTRY_CACHE.clear()


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
    from graph_validator import (
        load_extension_ontology_paths,
        resolve_extension_dependencies,
    )

    paths: list[Path] = []
    for ext_name in resolve_extension_dependencies(extensions, project_root):
        clean_name = ext_name.removesuffix(":full")
        # Full manifest, not subset: a concept declared in any module of a
        # supported extension counts as declared.
        paths.extend(
            load_extension_ontology_paths(clean_name, mode="full", project_root=project_root)
        )
    return paths


def _ontology_fingerprint(paths: list[Path]) -> str:
    """Cheap content fingerprint: path + mtime + size of every ontology file.

    Any file added, removed, renamed, or modified changes the fingerprint,
    which invalidates the declared-term cache entry without requiring an
    explicit clear. Stat calls keep repeated validation of unchanged graphs
    fast (no re-parsing).
    """

    hasher = hashlib.sha256()
    for path in paths:
        try:
            stat = path.stat()
        except OSError:
            hasher.update(f"{path}:missing;".encode())
            continue
        hasher.update(f"{path}:{stat.st_mtime_ns}:{stat.st_size};".encode())
    return hasher.hexdigest()


def load_declared_terms(
    project_root: Path = PROJECT_ROOT,
    extensions: list[str] | None = None,
) -> DeclaredTerms:
    """Return every IRI declared in supported ontologies, tracked by role.

    Roles are derived from explicit typing (``owl:Class``,
    ``owl:ObjectProperty``, ``sh:NodeShape``, …) plus structural inference
    (``rdfs:subClassOf`` subjects/objects are classes, ``rdfs:domain`` /
    ``rdfs:range`` subjects are properties, ``sh:targetClass`` objects are
    classes, ``sh:path`` IRIs are properties). Subjects whose role cannot be
    determined land in ``unknown_role`` and are accepted anywhere. Parse
    failures in individual files are skipped (some extension files use
    cross-file prefixes).

    Results are cached; the cache key includes a fingerprint of every
    ontology file (mtime + size), so ontology edits during a long-running
    server process are picked up automatically.
    """

    paths = _core_ontology_paths(project_root)
    paths.extend(_extension_ontology_paths(project_root, extensions or []))

    key = (
        str(project_root),
        tuple(sorted(extensions or [])),
        _ontology_fingerprint(paths),
    )
    cached = _DECLARED_CACHE.get(key)
    if cached is not None:
        return cached

    import rdflib
    from rdflib import OWL, RDF, RDFS, URIRef
    from rdflib.namespace import SH

    class_types = {OWL.Class, RDFS.Class}
    property_types = {
        OWL.ObjectProperty,
        OWL.DatatypeProperty,
        OWL.AnnotationProperty,
        OWL.FunctionalProperty,
        OWL.InverseFunctionalProperty,
        OWL.TransitiveProperty,
        OWL.SymmetricProperty,
        RDF.Property,
    }
    shape_types = {SH.NodeShape, SH.PropertyShape}

    classes: set[str] = set()
    properties: set[str] = set()
    shapes: set[str] = set()
    subjects_seen: set[str] = set()

    for path in paths:
        graph = rdflib.Graph()
        try:
            graph.parse(str(path), format="turtle")
        except Exception:
            continue

        for subject in graph.subjects():
            if isinstance(subject, URIRef):
                subjects_seen.add(str(subject))

        for subject, rdf_type in graph.subject_objects(RDF.type):
            if not isinstance(subject, URIRef):
                continue
            iri = str(subject)
            if rdf_type in class_types or rdf_type == RDFS.Datatype:
                classes.add(iri)
            elif rdf_type in property_types:
                properties.add(iri)
            elif rdf_type in shape_types:
                shapes.add(iri)

        # Structural role inference for terms declared without explicit typing.
        for subject in graph.subjects(RDFS.subClassOf):
            if isinstance(subject, URIRef):
                classes.add(str(subject))
        for obj in graph.objects(None, RDFS.subClassOf):
            if isinstance(obj, URIRef):
                classes.add(str(obj))
        for pred in (RDFS.subPropertyOf, RDFS.domain, RDFS.range):
            for subject in graph.subjects(pred):
                if isinstance(subject, URIRef):
                    properties.add(str(subject))
        for pred in (RDFS.domain, RDFS.range):
            for obj in graph.objects(None, pred):
                if isinstance(obj, URIRef):
                    classes.add(str(obj))
        for obj in graph.objects(None, SH.targetClass):
            if isinstance(obj, URIRef):
                classes.add(str(obj))
        for obj in graph.objects(None, SH.path):
            if isinstance(obj, URIRef):
                properties.add(str(obj))
        sh_class = URIRef("http://www.w3.org/ns/shacl#class")
        for obj in graph.objects(None, sh_class):
            if isinstance(obj, URIRef):
                classes.add(str(obj))

    # Punning support: a term declared as both class and property keeps both
    # roles. A shape IRI that is also a class (the CDO pattern where SHACL
    # shapes pun ontology classes) is primarily a class.
    shapes -= classes | properties
    unknown_role = subjects_seen - classes - properties - shapes

    result = DeclaredTerms(
        classes=frozenset(classes),
        properties=frozenset(properties),
        shapes=frozenset(shapes),
        unknown_role=frozenset(unknown_role),
    )
    if len(_DECLARED_CACHE) >= _DECLARED_CACHE_MAX_ENTRIES:
        _DECLARED_CACHE.pop(next(iter(_DECLARED_CACHE)))
    _DECLARED_CACHE[key] = result
    return result


def _load_upper_registry() -> tuple[dict | None, str | None]:
    """Load the pinned upper-ontology term registry (role-aware).

    Returns ``(registry, error)``. ``registry`` is ``{"classes": frozenset,
    "properties": frozenset, "individuals": frozenset, "datatypes":
    frozenset}`` unioned across all profiled ontologies. ``error`` is a typed
    code when the registry is unusable: ``upper_ontology_registry_missing``,
    ``upper_ontology_registry_malformed``, or
    ``upper_ontology_registry_provenance_invalid``.

    Fail-closed policy (issue #55): an unusable registry never degrades to
    whole-namespace acceptance. ``check_graph_concepts`` reports
    ``could_not_verify`` for any graph that uses profiled upper-ontology
    terms while the registry is unavailable.
    """

    if not UPPER_ONTOLOGY_REGISTRY_PATH.is_file():
        return None, "upper_ontology_registry_missing"
    try:
        stat = UPPER_ONTOLOGY_REGISTRY_PATH.stat()
    except OSError:
        return None, "upper_ontology_registry_missing"
    cache_key = f"{UPPER_ONTOLOGY_REGISTRY_PATH}:{stat.st_mtime_ns}:{stat.st_size}"
    cached = _UPPER_REGISTRY_CACHE.get(cache_key)
    if cached is not None:
        return cached, None
    try:
        raw = json.loads(UPPER_ONTOLOGY_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "upper_ontology_registry_malformed"
    ontologies = raw.get("ontologies")
    if not isinstance(ontologies, dict) or not ontologies:
        return None, "upper_ontology_registry_malformed"
    merged: dict[str, set[str]] = {
        "classes": set(),
        "properties": set(),
        "individuals": set(),
        "datatypes": set(),
    }
    for entry in ontologies.values():
        # Provenance requirement: every pinned ontology entry must record
        # where it came from and which release it pins.
        if not isinstance(entry, dict) or not entry.get("source_url") or not (
            entry.get("version_iri") or entry.get("version_info")
        ):
            return None, "upper_ontology_registry_provenance_invalid"
        for role in merged:
            merged[role].update(entry.get(role, []))
    if not any(merged.values()):
        return None, "upper_ontology_registry_malformed"
    result = {role: frozenset(values) for role, values in merged.items()}
    _UPPER_REGISTRY_CACHE.clear()  # single registry file; drop stale versions
    _UPPER_REGISTRY_CACHE[cache_key] = result
    return result, None


def _is_standard(iri: str) -> bool:
    """True for foundational W3C vocabulary accepted by namespace policy."""

    return iri.startswith(STANDARD_NAMESPACE_PREFIXES)


UCO_PROFILE_NAMESPACE_PREFIXES: tuple[str, ...] = tuple(
    sorted({prefix for prefixes in PROFILE_ID_TO_NAMESPACE_PREFIXES.values() for prefix in prefixes})
)


def _is_upper_namespace(iri: str) -> bool:
    return iri.startswith(UCO_PROFILE_NAMESPACE_PREFIXES)


def _selected_upper_prefixes(selected_profiles: list[str] | None) -> frozenset[str] | None:
    """Return allowed upper-namespace prefixes when profiles are selected.

    ``None`` means all profiled upper namespaces remain eligible (legacy
    behavior when no profile filter is supplied). An empty frozenset means
    profiles were selected but authorize no upper namespaces.
    """
    if selected_profiles is None:
        return None
    allowed: set[str] = set()
    for pid in selected_profiles:
        allowed.update(PROFILE_ID_TO_NAMESPACE_PREFIXES.get(pid, ()))
    return frozenset(allowed)


def _profile_for_upper_iri(iri: str) -> str | None:
    # Prefer canonical ids (time over owl-time alias) for diagnostics.
    preferred_order = (
        "bfo",
        "gufo",
        "prov-o",
        "time",
        "geosparql",
        "foaf",
        "org",
        "prof",
        "owl-time",
    )
    for pid in preferred_order:
        prefixes = PROFILE_ID_TO_NAMESPACE_PREFIXES.get(pid, ())
        if prefixes and iri.startswith(prefixes):
            return "time" if pid == "owl-time" else pid
    for pid, prefixes in PROFILE_ID_TO_NAMESPACE_PREFIXES.items():
        if iri.startswith(prefixes):
            return pid
    return None


def check_graph_concepts(
    graph_path: str | Path,
    project_root: Path = PROJECT_ROOT,
    extensions: list[str] | None = None,
    selected_profiles: list[str] | None = None,
) -> ConceptCoverageReport:
    """Check that every class and property in a graph file is declared.

    Classes are the URIRef objects of ``rdf:type`` triples; properties are
    all predicates. Instance IRIs (kb:, urn:uuid:, …) never appear in either
    position, so no instance-namespace whitelist is needed.

    When ``selected_profiles`` is provided, upper-ontology terms are accepted
    only from those profiles (and their declared namespace prefixes). A term
    from an unselected profile is reported as undeclared with guidance that
    the profile was not selected — not as an unknown registry term.
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
    upper, upper_error = _load_upper_registry()
    allowed_prefixes = _selected_upper_prefixes(selected_profiles)

    undeclared_classes: list[str] = []
    undeclared_properties: list[str] = []
    unknown_upper: set[str] = set()
    unselected_profile_terms: list[str] = []
    role_mismatches: list[tuple[str, str, str]] = []
    verification_errors: list[str] = []
    upper_terms_used = False

    def _handle_upper(iri: str, *, as_class: bool) -> bool:
        """Return True if the IRI was handled as an upper-ontology term."""
        nonlocal upper_terms_used
        if not _is_upper_namespace(iri):
            return False
        upper_terms_used = True
        if allowed_prefixes is not None and not iri.startswith(tuple(allowed_prefixes)):
            pid = _profile_for_upper_iri(iri) or "unknown"
            unselected_profile_terms.append(f"{iri} (profile_not_selected:{pid})")
            return True
        if upper is None:
            return True
        if as_class:
            if iri in upper["classes"] or iri in upper["datatypes"]:
                return True
            if iri in upper["properties"]:
                role_mismatches.append((iri, "upper-ontology property", "class (rdf:type object)"))
            else:
                unknown_upper.add(iri)
        else:
            if iri in upper["properties"]:
                return True
            if iri in upper["classes"]:
                role_mismatches.append((iri, "upper-ontology class", "property (predicate)"))
            else:
                unknown_upper.add(iri)
        return True

    for iri in sorted(used_classes):
        if _is_standard(iri):
            continue
        if _handle_upper(iri, as_class=True):
            continue
        if iri in declared.classes or iri in declared.unknown_role:
            continue
        if iri in declared.properties:
            role_mismatches.append((iri, "property", "class (rdf:type object)"))
        elif iri in declared.shapes:
            role_mismatches.append((iri, "SHACL shape", "class (rdf:type object)"))
        else:
            undeclared_classes.append(iri)

    for iri in sorted(used_properties):
        if _is_standard(iri):
            continue
        if _handle_upper(iri, as_class=False):
            continue
        if iri in declared.properties or iri in declared.unknown_role:
            continue
        if iri in declared.classes:
            role_mismatches.append((iri, "class", "property (predicate)"))
        elif iri in declared.shapes:
            role_mismatches.append((iri, "SHACL shape", "property (predicate)"))
        else:
            undeclared_properties.append(iri)

    if upper_terms_used and upper_error is not None and allowed_prefixes != frozenset():
        verification_errors.append(upper_error)

    ok = (
        not undeclared_classes
        and not undeclared_properties
        and not unknown_upper
        and not unselected_profile_terms
        and not role_mismatches
        and not verification_errors
    )
    guidance_parts: list[str] = []
    if undeclared_classes or undeclared_properties:
        guidance_parts.append(GUIDANCE)
    if unknown_upper:
        guidance_parts.append(UPPER_TERM_GUIDANCE)
    if unselected_profile_terms:
        guidance_parts.append(
            "Terms flagged as profile_not_selected are declared by a profiled "
            "upper ontology that was not included in this validation bundle. "
            "Add the required profile to profiles=[...] or remove the term."
        )
    if role_mismatches:
        guidance_parts.append(ROLE_MISMATCH_GUIDANCE)
    if verification_errors:
        guidance_parts.append(
            "A required verification stage could not run "
            f"({', '.join(verification_errors)}): the pinned upper-ontology "
            "term registry (mcp_server/upper_ontology_registry.json) is "
            "missing, malformed, or lacks release provenance while the graph "
            "uses profiled upper-ontology terms. Restore or regenerate the "
            "registry (mcp_server/tools/build_upper_ontology_registry.py); "
            "an unverifiable graph is never reported as conformant."
        )

    return ConceptCoverageReport(
        ok=ok,
        undeclared_classes=tuple(undeclared_classes) + tuple(unselected_profile_terms),
        undeclared_properties=tuple(undeclared_properties),
        unknown_upper_ontology_terms=tuple(sorted(unknown_upper)),
        role_mismatches=tuple(role_mismatches),
        checked_class_count=len(used_classes),
        checked_property_count=len(used_properties),
        guidance=" ".join(guidance_parts),
        verification_status="could_not_verify" if verification_errors else "complete",
        verification_errors=tuple(verification_errors),
    )


def coverage_report_to_dict(report: ConceptCoverageReport) -> dict:
    """Serialize a coverage report into the MCP tool result shape."""

    payload: dict = {
        "ok": report.ok,
        "checked_class_count": report.checked_class_count,
        "checked_property_count": report.checked_property_count,
        "verification_status": report.verification_status,
    }
    if not report.ok:
        payload["undeclared_classes"] = list(report.undeclared_classes)
        payload["undeclared_properties"] = list(report.undeclared_properties)
        if report.unknown_upper_ontology_terms:
            payload["unknown_upper_ontology_terms"] = list(
                report.unknown_upper_ontology_terms
            )
        if report.role_mismatches:
            payload["role_mismatches"] = [
                {"iri": iri, "declared_role": declared_role, "used_as": used_as}
                for iri, declared_role, used_as in report.role_mismatches
            ]
        if report.verification_errors:
            payload["verification_errors"] = list(report.verification_errors)
        payload["guidance"] = report.guidance
    return payload
