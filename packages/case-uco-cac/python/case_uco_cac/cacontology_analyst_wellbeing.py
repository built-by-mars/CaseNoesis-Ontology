"""CAC Ontology - Crimes Against Children — cacontology-analyst-wellbeing module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExposureMitigationMeasure:
    """A measure, control, or workflow technique used to reduce human exposure to traumatic content while enabling effective review and classification (e.g., blur/previews, hash-only review, progressive reve"""

    CLASS_IRI: str = "https://cacontology.projectvic.org/analyst-wellbeing#ExposureMitigationMeasure"
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
    mitigation_type: Optional[str] = field(default=None)


@dataclass
class OccupationalHarm:
    """Occupational harm experienced by investigators or content analysts arising from exposure to traumatic materials or sustained operational stressors."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/analyst-wellbeing#OccupationalHarm"
    label: list[str] = field(default_factory=list)
    harm_severity: Optional[str] = field(default=None)


@dataclass
class SecondaryTraumaticStress:
    """Occupational stress reactions arising from indirect exposure to others' trauma, including exposure through content review and investigative materials."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/analyst-wellbeing#SecondaryTraumaticStress"
    label: list[str] = field(default_factory=list)
    harm_severity: Optional[str] = field(default=None)


@dataclass
class VicariousTrauma:
    """A form of occupational harm in which repeated exposure to traumatic material produces trauma-like impacts in the reviewer."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/analyst-wellbeing#VicariousTrauma"
    label: list[str] = field(default_factory=list)
    harm_severity: Optional[str] = field(default=None)

