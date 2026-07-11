"""SOLVE-IT Digital Forensics Knowledge Base and Ontology — solveit-wa module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WeaknessEvaluation:
    """A risk assessment of a single SOLVE-IT weakness, capturing likelihood, impact, and optionally detectability ratings with computed scores."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/weakness-assessment/WeaknessEvaluation"
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
    statement: list[str] = field(default_factory=list)
    detect_difficulty_rating: Optional[int] = field(default=None)
    evaluates_weakness: Optional[Weakness] = field(default=None)
    impact_rating: Optional[int] = field(default=None)
    li_impact_score: Optional[int] = field(default=None)
    likelihood_rating: Optional[int] = field(default=None)
    rpn_score: Optional[int] = field(default=None)


@dataclass
class WeaknessEvaluationSet:
    """A collection of weakness evaluations scoped to a technique or context, with authorship and date metadata. Represents one assessment session."""

    CLASS_IRI: str = "https://ontology.solveit-df.org/solveit/weakness-assessment/WeaknessEvaluationSet"
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
    object: list[UcoObject] = field(default_factory=list)
    evaluated_by: list[Identity] = field(default_factory=list)
    has_evaluation: list[WeaknessEvaluation] = field(default_factory=list)

