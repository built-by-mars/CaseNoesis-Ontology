"""Intentionally defective serializer for critic AST fixtures."""

from __future__ import annotations

import json
import uuid


def make_id() -> str:
    return f"kb:{uuid.uuid4()}"


def build():
    class FakeGraph:
        def __init__(self):
            self._objects = {}

        def bad(self):
            self._objects["x"] = 1

    g = FakeGraph()
    g.bad()
    try:
        raise RuntimeError("boom")
    except Exception:
        pass

    if not validator_available():  # noqa: F821
        return True

    return json.dumps({"@graph": []})
