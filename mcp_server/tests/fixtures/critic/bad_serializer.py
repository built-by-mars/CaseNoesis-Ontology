"""Intentionally defective serializer for critic AST fixtures."""

from __future__ import annotations

import json
import uuid


def make_id() -> str:
    return f"kb:{uuid.uuid4()}"


def build():
    graph = {"@graph": []}
    try:
        graph["_objects"]  # noqa: B018 — private access pattern for fixture
    except Exception:
        pass

    if not validator_available():  # noqa: F821 — intentional for fail-open fixture shape
        return True

    # Pretend public API while dumping raw JSON
    return json.dumps(graph)


# Direct private mutation pattern
class FakeGraph:
    def __init__(self):
        self._objects = {}

    def bad(self):
        self._objects["x"] = 1
