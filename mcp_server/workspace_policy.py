"""Filesystem trust boundary for MCP tools that accept local paths.

``process_document_file`` and ``validate_graph`` accept caller-controlled
paths. In an agent-connected deployment the MCP server should not be an
arbitrary file read/write primitive, so deployments can configure a
workspace policy through environment variables:

- ``CASE_UCO_MCP_READ_ROOTS`` — path-separator-delimited directories that
  source/graph files must live under (evidence roots, read-only).
- ``CASE_UCO_MCP_WRITE_ROOTS`` — path-separator-delimited directories that
  output and progress files must live under (the case workspace).
- ``CASE_UCO_MCP_ALLOW_OVERWRITE`` — set to ``1``/``true`` to allow output
  paths to overwrite existing files. Under an active policy the default is
  non-overwrite.

Both variables accept ``os.pathsep`` (``:`` on POSIX, ``;`` on Windows) or
comma-separated lists. When neither variable is set, no policy is active and
behavior is unchanged (backward compatible); ``mcp_server/README.md``
documents the recommended secure deployment configuration.

Containment is decided on fully resolved paths (``Path.resolve()`` follows
symlinks), so ``..`` traversal and symlink escapes out of a configured root
are rejected with typed errors: ``source_outside_read_roots``,
``output_outside_write_roots``, ``progress_outside_write_roots``,
``output_exists``, ``source_output_conflict``. Error messages never echo the
offending path back to the caller.
"""

from __future__ import annotations

import os
from pathlib import Path

READ_ROOTS_ENV = "CASE_UCO_MCP_READ_ROOTS"
WRITE_ROOTS_ENV = "CASE_UCO_MCP_WRITE_ROOTS"
ALLOW_OVERWRITE_ENV = "CASE_UCO_MCP_ALLOW_OVERWRITE"


def _parse_roots(raw: str | None) -> tuple[Path, ...]:
    if not raw:
        return ()
    parts: list[str] = []
    for chunk in raw.split(os.pathsep):
        parts.extend(chunk.split(","))
    roots: list[Path] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        roots.append(Path(part).expanduser().resolve())
    return tuple(roots)


def read_roots() -> tuple[Path, ...]:
    return _parse_roots(os.environ.get(READ_ROOTS_ENV))


def write_roots() -> tuple[Path, ...]:
    return _parse_roots(os.environ.get(WRITE_ROOTS_ENV))


def overwrite_allowed() -> bool:
    return os.environ.get(ALLOW_OVERWRITE_ENV, "").strip().lower() in {"1", "true", "yes"}


def policy_active() -> bool:
    """True when a deployment has configured any filesystem restriction."""

    return bool(read_roots() or write_roots())


def _is_contained(path: Path, roots: tuple[Path, ...]) -> bool:
    for root in roots:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def check_read_path(path: str | Path, *, include_write_roots: bool = False) -> Path:
    """Resolve a caller-supplied read path and enforce the read policy.

    Returns the fully resolved path. Raises ``ValueError`` with a typed,
    non-sensitive message when the resolved path (after following symlinks)
    escapes every configured read root. With ``include_write_roots`` the
    write workspace also counts as readable — used by ``validate_graph``,
    which typically reads graphs the server itself just produced.
    """

    resolved = Path(path).expanduser().resolve()
    roots = read_roots()
    if not roots:
        # Read containment is enforced only when read roots are configured;
        # a write-roots-only policy constrains writes without locking reads.
        return resolved
    if include_write_roots:
        roots = roots + write_roots()
    if not _is_contained(resolved, roots):
        raise ValueError("source_outside_read_roots")
    return resolved


def check_write_path(
    path: str | Path,
    *,
    error_code: str = "output_outside_write_roots",
    enforce_no_overwrite: bool = True,
) -> Path:
    """Resolve a caller-supplied write path and enforce the write policy.

    Under an active policy, the resolved path must be contained in a write
    root and (unless ``CASE_UCO_MCP_ALLOW_OVERWRITE`` is set) must not
    already exist. ``Path.resolve()`` on a not-yet-existing file resolves
    symlinks in every existing ancestor, so symlinked directories that point
    outside the workspace are rejected.
    """

    resolved = Path(path).expanduser().resolve()
    roots = write_roots()
    if roots:
        if not _is_contained(resolved, roots):
            raise ValueError(error_code)
        if enforce_no_overwrite and resolved.exists() and not overwrite_allowed():
            raise ValueError("output_exists")
    return resolved


def check_distinct(source: Path, output: Path) -> None:
    """Reject source and destination resolving to the same file."""

    if source == output:
        raise ValueError("source_output_conflict")
