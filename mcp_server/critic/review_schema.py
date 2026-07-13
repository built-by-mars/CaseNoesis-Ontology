"""JSON Schema validation for CriticReview payloads (issue #75 Round 4)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"


def _inline_ref(path: str) -> dict[str, Any]:
    key = path.rsplit("/", 1)[-1].replace(".schema.json", "").replace("-", "_")
    return {"$ref": f"#/$defs/{key}"}


def _load_review_schema() -> dict[str, Any]:
    review = json.loads((SCHEMA_DIR / "critic-review.schema.json").read_text(encoding="utf-8"))
    defs = dict(review.get("$defs") or {})

    for sibling in (
        "critic-finding.schema.json",
        "critic-scorecard.schema.json",
        "critic-rule-execution.schema.json",
    ):
        sibling_schema = json.loads((SCHEMA_DIR / sibling).read_text(encoding="utf-8"))
        key = sibling.replace(".schema.json", "").replace("-", "_")
        # Drop nested $id to avoid absolute-URI confusion when inlined.
        sibling_schema = dict(sibling_schema)
        sibling_schema.pop("$id", None)
        sibling_schema.pop("$schema", None)
        defs[key] = sibling_schema
        nested = sibling_schema.get("$defs")
        if isinstance(nested, dict):
            defs.update(nested)

    review["$defs"] = defs
    props = dict(review.get("properties") or {})

    for field in ("deterministic_findings", "critic_findings", "merged_findings"):
        entry = props.get(field)
        if isinstance(entry, dict) and isinstance(entry.get("items"), dict):
            items = entry["items"]
            if "$ref" in items:
                props[field] = {**entry, "items": _inline_ref(items["$ref"])}

    scorecard = props.get("scorecard")
    if isinstance(scorecard, dict) and "$ref" in scorecard:
        props["scorecard"] = _inline_ref(scorecard["$ref"])

    executions = props.get("rule_executions")
    if isinstance(executions, dict) and isinstance(executions.get("items"), dict):
        items = executions["items"]
        if "$ref" in items:
            props["rule_executions"] = {
                **executions,
                "items": _inline_ref(items["$ref"]),
            }

    review["properties"] = props
    Draft202012Validator.check_schema(review)
    return review


_REVIEW_SCHEMA: dict[str, Any] | None = None


def validate_critic_review(data: dict[str, Any]) -> None:
    """Validate a review dict against critic-review.schema.json.

    Raises ValueError on schema mismatch.
    """

    global _REVIEW_SCHEMA
    if _REVIEW_SCHEMA is None:
        _REVIEW_SCHEMA = _load_review_schema()

    validator = Draft202012Validator(_REVIEW_SCHEMA)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        path = "/".join(str(p) for p in first.path)
        location = f" at {path}" if path else ""
        raise ValueError(f"critic_review_schema_mismatch{location}: {first.message}")
