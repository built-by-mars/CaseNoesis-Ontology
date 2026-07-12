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
