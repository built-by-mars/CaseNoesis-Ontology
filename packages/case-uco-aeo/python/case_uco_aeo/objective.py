"""Adversary Engagement Ontology — objective module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Objective:
    """An objective is some particular condition or state that is desired to be achieved and toward which effort is directed: an aim, goal, or end of action."""

    CLASS_IRI: str = "https://ontology.adversaryengagement.org/ae/objective/Objective"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)

