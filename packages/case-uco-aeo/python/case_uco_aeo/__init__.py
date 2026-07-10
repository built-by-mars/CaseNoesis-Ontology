"""Adversary Engagement Ontology — CASE/UCO SDK extension bindings."""

__version__ = "0.2.1"

NAMESPACES: dict[str, str] = {
    "attack": "https://ontology.adversaryengagement.org/ae/attack/",
    "engagement": "https://ontology.adversaryengagement.org/ae/engagement/",
    "identity": "https://ontology.adversaryengagement.org/ae/identity/",
    "objective": "https://ontology.adversaryengagement.org/ae/objective/",
    "role": "https://ontology.adversaryengagement.org/ae/role/",
    "vocabulary": "https://ontology.adversaryengagement.org/ae/vocabulary/",
}

_REGISTRY_PATH = __file__.replace("__init__.py", "_registry.json")
