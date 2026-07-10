"""Racketeering and Criminal Enterprise Extension — CASE/UCO SDK extension bindings."""

__version__ = "0.1.0"

NAMESPACES: dict[str, str] = {
    "rico": "http://example.org/ontology/rico/",
}

_REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")
