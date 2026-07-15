"""Compatibility shim — implementation lives in ``case_uco.validation.bundle``."""

from __future__ import annotations

from case_uco.validation.bundle import (
    FOUNDATIONAL_EXCLUSIVE,
    PROFILE_REGISTRY,
    RESOLVER_SCHEMA_VERSION,
    BundleResource,
    ResolvedValidationBundle,
    ValidationBundleError,
    _normalize_profile_id,
    clear_bundle_cache,
    hash_validation_bundle_identity,
    list_profile_ids,
    resolve_validation_bundle,
)

__all__ = [
    "FOUNDATIONAL_EXCLUSIVE",
    "PROFILE_REGISTRY",
    "RESOLVER_SCHEMA_VERSION",
    "BundleResource",
    "ResolvedValidationBundle",
    "ValidationBundleError",
    "_normalize_profile_id",
    "clear_bundle_cache",
    "hash_validation_bundle_identity",
    "list_profile_ids",
    "resolve_validation_bundle",
]
