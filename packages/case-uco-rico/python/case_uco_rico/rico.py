"""Racketeering and Criminal Enterprise Extension — rico module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EnterpriseRole:
    """An enterprise role is a functional position or division-of-labor responsibility that a member or associate serves within a racketeering enterprise, as alleged in a charging instrument — for example or"""

    CLASS_IRI: str = "http://example.org/ontology/rico/EnterpriseRole"
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
    role_function: Optional[str] = field(default=None)


@dataclass
class RacketeeringEnterprise:
    """A racketeering enterprise is an 'enterprise' as defined in 18 U.S.C. § 1961(4) (https://www.law.cornell.edu/uscode/text/18/1961): any individual, partnership, corporation, association, or other legal """

    CLASS_IRI: str = "http://example.org/ontology/rico/RacketeeringEnterprise"
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
    enterprise_type: Optional[str] = field(default=None)

