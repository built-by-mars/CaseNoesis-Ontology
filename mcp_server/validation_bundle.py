"""Profile-aware validation bundle planner (#68).

Resolves a deterministic, offline ontology/profile bundle from stable
extension names and upper-ontology profile IDs. SHACL validation and
strict concept coverage must consume the same resolved paths.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from extension_paths import extension_dir as _extension_dir
from graph_validator import (
    PROJECT_ROOT,
    load_extension_ontology_paths,
    resolve_extension_dependencies,
)

# Stable profile IDs → vendored source + CDO-Shapes paths.
PROFILE_REGISTRY: dict[str, dict[str, Any]] = {
    "bfo": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/bfo",
        "sources": ["ontology/upper/bfo.owl"],
        "shapes": ["ontology/upper/shapes/sh-bfo.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {"cac": "not_recommended"},
        "inference": "rdfs",
    },
    "gufo": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/gufo",
        "sources": ["ontology/upper/gufo.ttl"],
        "shapes": ["ontology/upper/shapes/sh-gufo.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {"cac": "included"},
        "inference": "rdfs",
    },
    "prov-o": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/prov-o",
        "sources": ["ontology/upper/prov-o.ttl"],
        "shapes": ["ontology/upper/shapes/sh-prov-o.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "time": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/owl-time",
        "sources": ["ontology/upper/time.ttl"],
        "shapes": ["ontology/upper/shapes/sh-time.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "owl-time": {  # alias
        "alias_of": "time",
    },
    "geosparql": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/geosparql",
        "sources": ["ontology/upper/geo.ttl", "ontology/upper/sf.ttl"],
        "shapes": ["ontology/upper/shapes/sh-geo.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "foaf": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/foaf",
        "sources": ["ontology/upper/foaf.rdf"],
        "shapes": ["ontology/upper/shapes/sh-foaf.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "org": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/org",
        "sources": ["ontology/upper/org.ttl"],
        "shapes": ["ontology/upper/shapes/sh-org.ttl"],
        # Offline import closure from sh-org.ttl (FOAF + PROV-O shapes;
        # SKOS is covered by standard RDF namespaces).
        "depends_on": ["foaf", "prov-o"],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
    "prof": {
        "canonical_id": "https://ontology.unifiedcyberontology.org/profiles/prof",
        "sources": ["ontology/upper/prof.ttl"],
        "shapes": ["ontology/upper/shapes/sh-prof.ttl"],
        "depends_on": [],
        "incompatible_with": [],
        "extension_policy": {},
        "inference": "rdfs",
    },
}

# Foundational profiles that must not be selected together without an
# explicit allow_foundational_pair=True override.
FOUNDATIONAL_EXCLUSIVE = frozenset({"bfo", "gufo"})

_BUNDLE_CACHE: dict[str, "ResolvedValidationBundle"] = {}
_CACHE_MAX = 32


class ValidationBundleError(ValueError):
    """Typed fail-closed error for profile/extension bundle resolution."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class BundleResource:
    role: str  # ontology | shapes | bridge | auxiliary
    path: str  # repository-relative
    absolute_path: str
    sha256: str
    profile_id: str | None = None
    extension: str | None = None


@dataclass(frozen=True)
class ResolvedValidationBundle:
    extensions: tuple[str, ...]
    profiles: tuple[str, ...]
    resources: tuple[BundleResource, ...]
    inference: str | None
    compatibility_notes: tuple[str, ...]
    fingerprint: str
    built_version: str = "case-1.4.0"
    requested_profiles: tuple[str, ...] = ()

    def ontology_graph_paths(self) -> list[Path]:
        return [Path(r.absolute_path) for r in self.resources]

    def to_manifest(self, *, portable: bool = True) -> dict[str, Any]:
        resources = []
        for r in self.resources:
            entry = {
                "role": r.role,
                "path": r.path,
                "sha256": r.sha256,
                "profile_id": r.profile_id,
                "extension": r.extension,
            }
            if not portable:
                entry["absolute_path"] = r.absolute_path
            resources.append(entry)
        return {
            "built_version": self.built_version,
            "requested_profiles": list(self.requested_profiles),
            "extensions": list(self.extensions),
            "profiles": list(self.profiles),
            "inference": self.inference,
            "compatibility_notes": list(self.compatibility_notes),
            "fingerprint": self.fingerprint,
            "resources": resources,
        }

    def write_manifest(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_manifest(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalize_profile_id(profile_id: str) -> str:
    entry = PROFILE_REGISTRY.get(profile_id)
    if entry is None:
        raise ValidationBundleError("unknown_profile", f"Unknown profile id {profile_id!r}")
    if "alias_of" in entry:
        return entry["alias_of"]
    return profile_id


def list_profile_ids() -> list[str]:
    return sorted(pid for pid, meta in PROFILE_REGISTRY.items() if "alias_of" not in meta)


def resolve_validation_bundle(
    extensions: list[str] | None = None,
    profiles: list[str] | None = None,
    *,
    project_root: Path = PROJECT_ROOT,
    allow_foundational_pair: bool = False,
    extra_ontology_graphs: list[str | Path] | None = None,
    use_cache: bool = True,
) -> ResolvedValidationBundle:
    """Resolve extension + profile ontology graphs into one fingerprinted bundle."""

    extensions = list(extensions or [])
    profiles = list(profiles or [])
    cache_key = json.dumps(
        {
            "ext": extensions,
            "prof": profiles,
            "pair": allow_foundational_pair,
            "extra": [str(p) for p in (extra_ontology_graphs or [])],
            "root": str(project_root),
        },
        sort_keys=True,
    )
    if use_cache and cache_key in _BUNDLE_CACHE:
        cached = _BUNDLE_CACHE[cache_key]
        # Re-verify fingerprints; never return a stale bundle after a file change.
        try:
            for resource in cached.resources:
                path = Path(resource.absolute_path)
                if not path.exists() or _sha256_file(path) != resource.sha256:
                    del _BUNDLE_CACHE[cache_key]
                    break
            else:
                return cached
        except KeyError:
            pass

    notes: list[str] = []
    requested_profiles = [_normalize_profile_id(pid) for pid in profiles]
    normalized_profiles: list[str] = list(requested_profiles)

    # Resolve profile depends_on transitively (e.g. ORG → FOAF + PROV-O).
    resolved: list[str] = []
    seen_prof: set[str] = set()
    queue = list(normalized_profiles)
    while queue:
        pid = queue.pop(0)
        if pid in seen_prof:
            continue
        seen_prof.add(pid)
        resolved.append(pid)
        meta = PROFILE_REGISTRY[pid]
        for dep in meta.get("depends_on", []):
            dep_norm = _normalize_profile_id(dep)
            if dep_norm not in seen_prof:
                queue.append(dep_norm)
                notes.append(f"Profile {pid!r} depends_on {dep_norm!r}")
    normalized_profiles = resolved

    foundational = [p for p in normalized_profiles if p in FOUNDATIONAL_EXCLUSIVE]
    if len(set(foundational)) > 1 and not allow_foundational_pair:
        raise ValidationBundleError(
            "incompatible_profiles",
            "BFO and gUFO are alternative foundational profiles; select one, "
            "or pass allow_foundational_pair=True with an explicit rationale "
            "and a dedicated compatibility fixture.",
        )
    if len(set(foundational)) > 1 and allow_foundational_pair:
        notes.append(
            "allow_foundational_pair=True: BFO and gUFO co-selected; "
            "caller must supply a compatibility fixture."
        )

    expanded_ext = resolve_extension_dependencies(extensions, project_root) if extensions else []

    for pid in normalized_profiles:
        meta = PROFILE_REGISTRY[pid]
        for ext in expanded_ext:
            clean = ext.removesuffix(":full")
            policy = meta.get("extension_policy", {}).get(clean)
            if policy == "not_recommended":
                notes.append(
                    f"Profile {pid!r} is marked not_recommended with extension {clean!r}"
                )
                raise ValidationBundleError(
                    "incompatible_extension_profile",
                    f"Profile {pid!r} is not_recommended with extension {clean!r}. "
                    f"Choose gUFO for CAC graphs, or omit the foundational profile.",
                )
            if policy == "included":
                notes.append(f"Profile {pid!r} is included/compatible with {clean!r}")

    resources: list[BundleResource] = []
    seen_abs: set[str] = set()

    def _add(path: Path, role: str, *, profile_id: str | None = None, extension: str | None = None) -> None:
        if not path.exists():
            raise ValidationBundleError(
                "missing_resource",
                f"Required ontology/shape file missing: {path}",
            )
        abs_s = str(path.resolve())
        if abs_s in seen_abs:
            return
        seen_abs.add(abs_s)
        try:
            rel = str(path.resolve().relative_to(project_root.resolve()))
        except ValueError:
            rel = abs_s
        resources.append(
            BundleResource(
                role=role,
                path=rel,
                absolute_path=abs_s,
                sha256=_sha256_file(path),
                profile_id=profile_id,
                extension=extension,
            )
        )

    for ext_name in expanded_ext:
        mode = "full" if ext_name.endswith(":full") else "subset"
        clean = ext_name.removesuffix(":full")
        for full in load_extension_ontology_paths(clean, mode=mode, project_root=project_root):
            role = "shapes" if "shape" in full.name.lower() else "ontology"
            _add(full, role, extension=clean)

    for pid in normalized_profiles:
        meta = PROFILE_REGISTRY[pid]
        for rel in meta.get("sources", []):
            _add(project_root / rel, "ontology", profile_id=pid)
        for rel in meta.get("shapes", []):
            _add(project_root / rel, "shapes", profile_id=pid)

    for extra in extra_ontology_graphs or []:
        _add(Path(extra), "auxiliary")

    inference: str | None = None
    if normalized_profiles:
        inference = "rdfs"
    elif any(not e.endswith(":full") for e in expanded_ext):
        # validation-subset extensions historically skip rdfs; profiles force it
        inference = None
    elif expanded_ext:
        inference = "rdfs"

    fingerprint_material = json.dumps(
        [
            {
                "path": r.path,
                "sha256": r.sha256,
                "role": r.role,
                "profile": r.profile_id,
                "ext": r.extension,
            }
            for r in resources
        ],
        sort_keys=True,
    ).encode()
    fingerprint = hashlib.sha256(fingerprint_material).hexdigest()

    bundle = ResolvedValidationBundle(
        extensions=tuple(expanded_ext),
        profiles=tuple(normalized_profiles),
        resources=tuple(resources),
        inference=inference,
        compatibility_notes=tuple(notes),
        fingerprint=fingerprint,
        requested_profiles=tuple(requested_profiles),
    )

    if use_cache:
        if len(_BUNDLE_CACHE) >= _CACHE_MAX:
            _BUNDLE_CACHE.pop(next(iter(_BUNDLE_CACHE)))
        _BUNDLE_CACHE[cache_key] = bundle
    return bundle


def clear_bundle_cache() -> None:
    _BUNDLE_CACHE.clear()
