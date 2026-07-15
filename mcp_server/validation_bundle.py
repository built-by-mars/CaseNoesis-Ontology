"""Compatibility shim — implementation lives in ``case_uco.validation.bundle``."""

from case_uco.validation.bundle import *  # noqa: F403
from case_uco.validation.bundle import (  # noqa: F401
    PROFILE_REGISTRY,
    RESOLVER_SCHEMA_VERSION,
    ValidationBundleError,
    clear_bundle_cache,
    hash_validation_bundle_identity,
    list_profile_ids,
    resolve_validation_bundle,
    _normalize_profile_id,
)
