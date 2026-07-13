"""Shared schema loading and bound model-response schema generation."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
SUPPORTED_SCHEMA_VERSION = "1.2.0"
HEX64 = "^[a-fA-F0-9]{64}$"


def load_json_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def model_response_schema() -> dict[str, Any]:
    return load_json_schema("critic-model-response.schema.json")


def model_response_schema_sha256() -> str:
    raw = (SCHEMA_DIR / "critic-model-response.schema.json").read_bytes()
    return hashlib.sha256(raw).hexdigest()


def bound_model_response_schema(
    *,
    graph_sha256: str,
    prompt_package_hash: str,
    serializer_sha256: str | None = None,
    session_id: str | None = None,
    pass_number: int | None = None,
    schema_version: str = SUPPORTED_SCHEMA_VERSION,
    review_request_sha256: str | None = None,
) -> dict[str, Any]:
    """Return the authoritative schema with per-pass const bindings."""

    schema = copy.deepcopy(model_response_schema())
    props = schema.setdefault("properties", {})
    required = set(schema.get("required") or [])

    def bind(name: str, value: Any, *, require: bool) -> None:
        entry = props.setdefault(name, {})
        if isinstance(entry, dict):
            entry["const"] = value
        if require:
            required.add(name)

    bind("schema_version", schema_version, require=True)
    bind("graph_sha256", graph_sha256, require=True)
    bind("prompt_package_hash", prompt_package_hash, require=True)

    if serializer_sha256 is None:
        # Forbid unexpected serializer hashes: only null allowed.
        props["serializer_sha256"] = {"type": "null"}
    else:
        bind("serializer_sha256", serializer_sha256, require=True)

    if session_id is None:
        props["session_id"] = {"type": "null"}
    else:
        bind("session_id", session_id, require=True)

    if pass_number is None:
        props["pass_number"] = {"type": "null"}
    else:
        bind("pass_number", pass_number, require=True)

    if review_request_sha256 is not None:
        bind("review_request_sha256", review_request_sha256, require=True)

    schema["required"] = sorted(required)
    return schema


def compute_review_request_sha256(
    *,
    schema_version: str,
    session_id: str | None,
    pass_number: int | None,
    graph_sha256: str,
    serializer_sha256: str | None,
    source_sha256: dict[str, str],
    coverage_contract_sha256: str | None,
    prompt_package_hash: str,
) -> str:
    payload = {
        "schema_version": schema_version,
        "session_id": session_id,
        "pass_number": pass_number,
        "graph_sha256": graph_sha256,
        "serializer_sha256": serializer_sha256,
        "source_sha256": dict(sorted(source_sha256.items())),
        "coverage_contract_sha256": coverage_contract_sha256,
        "prompt_package_hash": prompt_package_hash,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
