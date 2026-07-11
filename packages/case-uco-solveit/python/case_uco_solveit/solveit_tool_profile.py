"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit-tool-profile module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConditionTargetType:
    """Enumeration of action components that conditions can evaluate against."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/ConditionTargetType"


@dataclass
class MitigationCapability:
    """A declared capability that a specific mitigation is provided by a tool, optionally subject to conditions expressed as SHACL shapes."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/MitigationCapability"
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


@dataclass
class SolveitAwareInstrument:
    """A specialised tool that has been evaluated against SOLVE-IT tool capability profiles. Adds the consultedProfile property to link an instrument to the profiles used during mitigation assessment."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/SolveitAwareInstrument"
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
    creator: Optional[Identity] = field(default=None)
    references: list[str] = field(default_factory=list)
    service_pack: Optional[str] = field(default=None)
    tool_type: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)


@dataclass
class ToolCapabilityProfile:
    """A declaration of what techniques a specific version of a tool can perform and what mitigations it implements, published by a named party. Distributed as a TTL file per tool version per publisher."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/tool-profile/ToolCapabilityProfile"
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

