"""Typed RDF literals for custom (non-XSD) datatypes such as pattern:PatternExpression."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TypedLiteral:
    """Lexical value paired with an RDF datatype IRI.

    Use for UCO custom datatypes declared via ``sh:datatype`` that are not
    XSD types (for example ``pattern:PatternExpression``).
    """

    value: str
    datatype_iri: str

    def __str__(self) -> str:
        return self.value
