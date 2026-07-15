"""Compatibility shim — implementation lives in ``case_uco.validation.extension_paths``."""

from __future__ import annotations

from case_uco.validation.extension_paths import (
    PROJECT_ROOT,
    extension_dir,
    extension_manifest_path,
    extension_roots,
    find_extension_dir,
    iter_extension_dirs,
    native_extension_root,
)

__all__ = [
    "PROJECT_ROOT",
    "extension_dir",
    "extension_manifest_path",
    "extension_roots",
    "find_extension_dir",
    "iter_extension_dirs",
    "native_extension_root",
]
