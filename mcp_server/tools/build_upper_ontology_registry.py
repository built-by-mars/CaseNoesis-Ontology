#!/usr/bin/env python3
"""Build the pinned upper-ontology term registry used by concept coverage.

Strict concept coverage historically accepted *any* IRI under a profiled
upper-ontology namespace (BFO, gUFO, PROV-O, OWL-Time, GeoSPARQL, FOAF, ORG,
PROF), which let fabricated terms such as ``prov:CompletelyImaginaryProperty``
pass validation. This script downloads pinned releases of each profiled
ontology, extracts the exact declared terms with their RDF roles (class,
property, individual, datatype), and writes a compact JSON registry to
``mcp_server/upper_ontology_registry.json``. The registry is committed to the
repository so validation works offline; re-run this script to refresh it when
a profiled ontology publishes a new supported release.

Usage:
    python3 mcp_server/tools/build_upper_ontology_registry.py
    python3 mcp_server/tools/build_upper_ontology_registry.py --source-dir /path/to/downloaded

With ``--source-dir`` the script reads previously downloaded ontology files
(named per the ``local_file`` field below) instead of fetching over HTTP,
which supports air-gapped rebuilds.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = PROJECT_ROOT / "mcp_server" / "upper_ontology_registry.json"

# Pinned sources for every ontology that UCO maintains a CDO-Shapes profile
# for. ``namespace_prefixes`` filters extracted terms so annotation vocabulary
# defined in the same file under other namespaces is not registered.
ONTOLOGY_SOURCES: dict[str, dict] = {
    "bfo": {
        "title": "Basic Formal Ontology (BFO) 2.0 / ISO 21838-2",
        "profile": "CDO-Shapes-BFO",
        "namespace_prefixes": ["http://purl.obolibrary.org/obo/BFO_"],
        "source_url": "http://purl.obolibrary.org/obo/bfo.owl",
        "local_file": "bfo.owl",
        "format": "xml",
    },
    "gufo": {
        "title": "gentle Unified Foundational Ontology (gUFO)",
        "profile": "CDO-Shapes-gufo",
        "namespace_prefixes": ["http://purl.org/nemo/gufo#"],
        "source_url": "https://nemo-ufes.github.io/gufo/gufo.ttl",
        "local_file": "gufo.ttl",
        "format": "turtle",
    },
    "prov-o": {
        "title": "W3C Provenance Ontology (PROV-O)",
        "profile": "CDO-Shapes-PROV-O",
        "namespace_prefixes": ["http://www.w3.org/ns/prov#"],
        "source_url": "http://www.w3.org/ns/prov-o.ttl",
        "local_file": "prov-o.ttl",
        "format": "turtle",
    },
    "owl-time": {
        "title": "W3C OWL-Time",
        "profile": "CDO-Shapes-Time",
        "namespace_prefixes": ["http://www.w3.org/2006/time#"],
        "source_url": "https://www.w3.org/2006/time.ttl",
        "local_file": "time.ttl",
        "format": "turtle",
    },
    "geosparql": {
        "title": "OGC GeoSPARQL 1.1 (core)",
        "profile": "CDO-Shapes-GeoSPARQL",
        "namespace_prefixes": ["http://www.opengis.net/ont/geosparql#"],
        "source_url": "https://opengeospatial.github.io/ogc-geosparql/geosparql11/geo.ttl",
        "local_file": "geo.ttl",
        "format": "turtle",
    },
    "geosparql-sf": {
        "title": "OGC Simple Features geometries (GeoSPARQL 1.1)",
        "profile": "CDO-Shapes-GeoSPARQL",
        "namespace_prefixes": ["http://www.opengis.net/ont/sf#"],
        "source_url": "https://opengeospatial.github.io/ogc-geosparql/geosparql11/sf_geometries.ttl",
        "local_file": "sf.ttl",
        "format": "turtle",
    },
    "foaf": {
        "title": "Friend of a Friend (FOAF) vocabulary",
        "profile": "CDO-Shapes-FOAF",
        "namespace_prefixes": ["http://xmlns.com/foaf/0.1/"],
        "source_url": "http://xmlns.com/foaf/spec/index.rdf",
        "local_file": "foaf.rdf",
        "format": "xml",
    },
    "org": {
        "title": "W3C Organization Ontology (ORG)",
        "profile": "CDO-Shapes-ORG",
        "namespace_prefixes": ["http://www.w3.org/ns/org#"],
        "source_url": "https://www.w3.org/ns/org.ttl",
        "local_file": "org.ttl",
        "format": "turtle",
    },
    "prof": {
        "title": "W3C Profiles Vocabulary (PROF)",
        "profile": "CDO-Shapes-PROF",
        "namespace_prefixes": ["http://www.w3.org/ns/dx/prof/"],
        "source_url": "https://www.w3.org/ns/dx/prof/",
        "local_file": "prof.ttl",
        "format": "turtle",
        "accept": "text/turtle",
    },
}


def _fetch(url: str, accept: str | None) -> bytes:
    request = urllib.request.Request(url, headers={"Accept": accept or "text/turtle, application/rdf+xml"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def _extract_terms(graph, prefixes: tuple[str, ...]) -> dict[str, list[str]]:
    """Categorize declared terms by RDF role within the target namespaces."""

    from rdflib import OWL, RDF, RDFS, URIRef

    classes: set[str] = set()
    properties: set[str] = set()
    individuals: set[str] = set()
    datatypes: set[str] = set()

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

    def in_scope(term) -> bool:
        return isinstance(term, URIRef) and str(term).startswith(prefixes)

    for subject, rdf_type in graph.subject_objects(RDF.type):
        if not in_scope(subject):
            continue
        iri = str(subject)
        if rdf_type in class_types:
            classes.add(iri)
        elif rdf_type in property_types:
            properties.add(iri)
        elif rdf_type == RDFS.Datatype:
            datatypes.add(iri)
        elif rdf_type == OWL.NamedIndividual:
            individuals.add(iri)

    # Role inference for terms declared only structurally.
    for subject in graph.subjects(RDFS.subClassOf):
        if in_scope(subject):
            classes.add(str(subject))
    for pred in (RDFS.subPropertyOf, RDFS.domain, RDFS.range):
        for subject in graph.subjects(pred):
            if in_scope(subject) and str(subject) not in classes:
                properties.add(str(subject))
    for obj in graph.objects(None, RDFS.subClassOf):
        if in_scope(obj):
            classes.add(str(obj))
    for pred in (RDFS.domain, RDFS.range):
        for obj in graph.objects(None, pred):
            if in_scope(obj) and str(obj) not in properties:
                classes.add(str(obj))

    # Vocabulary members typed by an in-scope class (e.g. time:Friday a
    # time:DayOfWeek) count as individuals.
    for subject, rdf_type in graph.subject_objects(RDF.type):
        if in_scope(subject) and in_scope(rdf_type):
            iri = str(subject)
            if iri not in classes and iri not in properties:
                individuals.add(iri)

    properties -= classes  # punned terms count as classes for rdf:type use
    return {
        "classes": sorted(classes),
        "properties": sorted(properties),
        "individuals": sorted(individuals - classes - properties),
        "datatypes": sorted(datatypes),
    }


def _version_metadata(graph) -> dict[str, str]:
    from rdflib import OWL, RDF

    meta: dict[str, str] = {}
    for ontology in graph.subjects(RDF.type, OWL.Ontology):
        version_iri = graph.value(ontology, OWL.versionIRI)
        version_info = graph.value(ontology, OWL.versionInfo)
        if version_iri:
            meta["version_iri"] = str(version_iri)
        if version_info:
            meta["version_info"] = str(version_info)
        if meta:
            break
    return meta


def build_registry(source_dir: Path | None) -> dict:
    import rdflib

    ontologies: dict[str, dict] = {}
    for key, spec in ONTOLOGY_SOURCES.items():
        prefixes = tuple(spec["namespace_prefixes"])
        graph = rdflib.Graph()
        if source_dir is not None:
            data = (source_dir / spec["local_file"]).read_bytes()
        else:
            data = _fetch(spec["source_url"], spec.get("accept"))
        graph.parse(data=data, format=spec["format"])
        terms = _extract_terms(graph, prefixes)
        entry = {
            "title": spec["title"],
            "profile": spec["profile"],
            "namespace_prefixes": spec["namespace_prefixes"],
            "source_url": spec["source_url"],
            **_version_metadata(graph),
            "term_counts": {k: len(v) for k, v in terms.items()},
            **terms,
        }
        ontologies[key] = entry
        print(
            f"{key}: {entry['term_counts']['classes']} classes, "
            f"{entry['term_counts']['properties']} properties, "
            f"{entry['term_counts']['individuals']} individuals, "
            f"{entry['term_counts']['datatypes']} datatypes"
        )

    return {
        "registry_version": "1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "generator": "mcp_server/tools/build_upper_ontology_registry.py",
        "description": (
            "Exact declared terms of upper/external ontologies that UCO "
            "maintains CDO-Shapes profiles for. Strict concept coverage "
            "accepts only these terms inside the profiled namespaces."
        ),
        "ontologies": ontologies,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=None,
        help="Read ontology files from this directory instead of fetching over HTTP.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REGISTRY_PATH,
        help=f"Registry output path (default: {REGISTRY_PATH})",
    )
    args = parser.parse_args()

    registry = build_registry(args.source_dir)
    args.output.write_text(json.dumps(registry, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    total = sum(
        sum(entry["term_counts"].values()) for entry in registry["ontologies"].values()
    )
    print(f"Wrote {args.output} ({total} terms across {len(registry['ontologies'])} ontologies).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
