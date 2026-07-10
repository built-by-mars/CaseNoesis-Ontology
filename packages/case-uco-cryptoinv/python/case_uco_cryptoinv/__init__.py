"""Cryptocurrency and Financial Crime Investigation Extension — CASE/UCO SDK extension bindings."""

__version__ = "0.1.0"

NAMESPACES: dict[str, str] = {
    "cryptoinv": "http://example.org/ontology/cryptoinv/",
}

_REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")
