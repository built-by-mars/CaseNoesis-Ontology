"""Tests for profile-aware validation bundle planner (#68)."""

from __future__ import annotations

import pytest

from validation_bundle import (
    ValidationBundleError,
    clear_bundle_cache,
    list_profile_ids,
    resolve_validation_bundle,
)


@pytest.fixture(autouse=True)
def _clear_cache():
    clear_bundle_cache()
    yield
    clear_bundle_cache()


def test_list_profiles_includes_org_prof():
    ids = list_profile_ids()
    for required in ("bfo", "gufo", "prov-o", "time", "geosparql", "foaf", "org", "prof"):
        assert required in ids


def test_unknown_profile_fails_closed():
    with pytest.raises(ValidationBundleError) as exc:
        resolve_validation_bundle(profiles=["not-a-real-profile"])
    assert exc.value.code == "unknown_profile"


def test_bfo_gufo_exclusive():
    with pytest.raises(ValidationBundleError) as exc:
        resolve_validation_bundle(profiles=["bfo", "gufo"])
    assert exc.value.code == "incompatible_profiles"


def test_bfo_with_cac_rejected():
    with pytest.raises(ValidationBundleError) as exc:
        resolve_validation_bundle(extensions=["cac"], profiles=["bfo"])
    assert exc.value.code == "incompatible_extension_profile"


def test_geosparql_includes_simple_features():
    bundle = resolve_validation_bundle(profiles=["geosparql"])
    paths = [r.path for r in bundle.resources]
    assert any(p.endswith("geo.ttl") for p in paths)
    assert any(p.endswith("sf.ttl") for p in paths)
    assert any("sh-geo.ttl" in p for p in paths)


def test_unrelated_profile_not_loaded():
    bundle = resolve_validation_bundle(profiles=["time"])
    paths = " ".join(r.path for r in bundle.resources)
    assert "time.ttl" in paths
    assert "bfo.owl" not in paths
    assert "gufo.ttl" not in paths
    assert "geo.ttl" not in paths


def test_bundle_fingerprint_stable():
    a = resolve_validation_bundle(profiles=["prov-o"])
    b = resolve_validation_bundle(profiles=["prov-o"])
    assert a.fingerprint == b.fingerprint
    assert a.to_manifest()["profiles"] == ["prov-o"]


def test_owl_time_alias():
    bundle = resolve_validation_bundle(profiles=["owl-time"])
    assert bundle.profiles == ("time",)


def test_uco_profiles_ids_match_profile_registry():
    """Discovery catalog and validation registry must stay in sync (#68)."""
    from domain_index import UCO_PROFILES
    from validation_bundle import list_profile_ids, PROFILE_REGISTRY

    catalog_ids = {p["id"] for p in UCO_PROFILES}
    assert catalog_ids == set(list_profile_ids())
    for profile in UCO_PROFILES:
        reg = PROFILE_REGISTRY[profile["id"]]
        sources = reg.get("sources") or []
        if sources and isinstance(profile.get("local_source"), str):
            assert profile["local_source"] in sources


def test_org_resolves_foaf_and_prov_dependencies():
    bundle = resolve_validation_bundle(profiles=["org"])
    assert "org" in bundle.profiles
    assert "foaf" in bundle.profiles
    assert "prov-o" in bundle.profiles
    paths = " ".join(r.path for r in bundle.resources)
    assert "org.ttl" in paths
    assert "foaf" in paths.lower() or "foaf.rdf" in paths
    assert "prov-o.ttl" in paths
    assert any("depends_on" in n for n in bundle.compatibility_notes)


def test_portable_manifest_omits_absolute_paths():
    bundle = resolve_validation_bundle(profiles=["time"])
    portable = bundle.to_manifest(portable=True)
    for resource in portable["resources"]:
        assert "absolute_path" not in resource
        assert "sha256" in resource
        assert not str(resource["path"]).startswith("/")


def test_cache_invalidates_when_resource_file_changes(tmp_path, monkeypatch):
    from pathlib import Path
    import validation_bundle as vb

    # Build a tiny fake profile registry rooted at tmp_path.
    ont = tmp_path / "ontology" / "upper"
    shapes = ont / "shapes"
    shapes.mkdir(parents=True)
    ont_file = ont / "toy.ttl"
    shape_file = shapes / "sh-toy.ttl"
    ont_file.write_text("@prefix : <http://example.org/> .\n:A a owl:Class .\n", encoding="utf-8")
    shape_file.write_text("@prefix sh: <http://www.w3.org/ns/shacl#> .\n", encoding="utf-8")

    monkeypatch.setitem(
        vb.PROFILE_REGISTRY,
        "toy",
        {
            "canonical_id": "https://example.org/profiles/toy",
            "sources": ["ontology/upper/toy.ttl"],
            "shapes": ["ontology/upper/shapes/sh-toy.ttl"],
            "depends_on": [],
            "incompatible_with": [],
            "extension_policy": {},
            "inference": "rdfs",
        },
    )
    first = vb.resolve_validation_bundle(profiles=["toy"], project_root=tmp_path)
    cached = vb.resolve_validation_bundle(profiles=["toy"], project_root=tmp_path)
    assert cached.fingerprint == first.fingerprint
    ont_file.write_text(
        "@prefix : <http://example.org/> .\n:A a owl:Class .\n:B a owl:Class .\n",
        encoding="utf-8",
    )
    second = vb.resolve_validation_bundle(profiles=["toy"], project_root=tmp_path)
    assert second.fingerprint != first.fingerprint


def test_cache_invalidates_when_resource_file_missing(tmp_path, monkeypatch):
    import validation_bundle as vb

    ont = tmp_path / "ontology" / "upper"
    shapes = ont / "shapes"
    shapes.mkdir(parents=True)
    ont_file = ont / "toy.ttl"
    shape_file = shapes / "sh-toy.ttl"
    ont_file.write_text(":A a owl:Class .\n", encoding="utf-8")
    shape_file.write_text("\n", encoding="utf-8")
    monkeypatch.setitem(
        vb.PROFILE_REGISTRY,
        "toy",
        {
            "canonical_id": "https://example.org/profiles/toy",
            "sources": ["ontology/upper/toy.ttl"],
            "shapes": ["ontology/upper/shapes/sh-toy.ttl"],
            "depends_on": [],
            "incompatible_with": [],
            "extension_policy": {},
            "inference": "rdfs",
        },
    )
    vb.resolve_validation_bundle(profiles=["toy"], project_root=tmp_path)
    ont_file.unlink()
    with pytest.raises(vb.ValidationBundleError) as exc:
        vb.resolve_validation_bundle(profiles=["toy"], project_root=tmp_path)
    assert exc.value.code == "missing_resource"
