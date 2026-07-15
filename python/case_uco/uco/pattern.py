"""Auto-generated uco-pattern classes for the CASE/UCO ontology."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union

from case_uco.typed_literal import TypedLiteral
from case_uco.uco.core import UcoInherentCharacterizationThing
from case_uco.uco.core import UcoObject

_PATTERN_EXPRESSION_IRI = (
    "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression"
)


@dataclass
class Pattern(UcoObject):
    """A pattern is a combination of properties, acts, tendencies, etc., forming a consistent or characteristic arrangement."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/pattern/Pattern"
    NAMESPACE_PREFIX: str = "uco-pattern"



@dataclass
class LogicalPattern(Pattern):
    """A logical pattern is a grouping of characteristics unique to an informational pattern expressed via a structured pattern expression following the rules of logic."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/pattern/LogicalPattern"
    NAMESPACE_PREFIX: str = "uco-pattern"

    # UCO 1.4 declares sh:datatype pattern:PatternExpression (custom RDF datatype).
    pattern_expression: Optional[Union[str, TypedLiteral]] = field(
        default=None,
        metadata={
            "jsonld_key": "uco-pattern:patternExpression",
            "required": False,
            "cardinality": "zero_or_one",
            "range_iri": _PATTERN_EXPRESSION_IRI,
            "alternate_range_iris": [],
            "literal_datatype": True,
        },
    )


@dataclass
class PatternExpression(UcoInherentCharacterizationThing):
    """A pattern expression is a grouping of characteristics unique to an explicit logical expression defining a pattern (e.g., regular expression, SQL Select expression, etc.)."""

    CLASS_IRI: str = "https://ontology.unifiedcyberontology.org/uco/pattern/PatternExpression"
    NAMESPACE_PREFIX: str = "uco-pattern"


