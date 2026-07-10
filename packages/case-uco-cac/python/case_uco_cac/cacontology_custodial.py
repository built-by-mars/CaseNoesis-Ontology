"""CAC Ontology - Crimes Against Children — cacontology-custodial module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ActiveCustodyPhase:
    """Phase when custodial relationship is actively maintained and operational. Modeled as anti-rigid gUFO Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#ActiveCustodyPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class AuthorityAbuse:
    """Abuse of authority position to exploit or harm children. Modeled as gUFO SubKind with authority relationship violations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#AuthorityAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_violation_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_violation_end_point: Optional[dateTimeStamp] = field(default=None)
    perpetrated_by: list[AuthorityFigure] = field(default_factory=list)
    trust_level_after: Optional[str] = field(default=None)
    trust_level_before: Optional[str] = field(default=None)
    violation_severity: Optional[str] = field(default=None)
    violation_type: Optional[str] = field(default=None)


@dataclass
class AuthorityFigure:
    """Individual in position of authority, trust, or power over children. Modeled as anti-rigid gUFO Role with relational foundation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#AuthorityFigure"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class Babysitter:
    """Individual temporarily caring for children in parents' absence. Modeled as anti-rigid gUFO Role with temporary scope."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#Babysitter"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class BackgroundCheck:
    """Background verification conducted for custodial or care position. Modeled as gUFO Object with verification results."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#BackgroundCheck"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)
    check_date: Optional[datetime] = field(default=None)
    check_result: Optional[str] = field(default=None)
    check_type: Optional[str] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)


@dataclass
class BreachOfCare:
    """Failure to provide appropriate care while in custodial role. Modeled as gUFO SubKind with care obligation failures."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#BreachOfCare"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_violation_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_violation_end_point: Optional[dateTimeStamp] = field(default=None)
    perpetrated_by: list[AuthorityFigure] = field(default_factory=list)
    trust_level_after: Optional[str] = field(default=None)
    trust_level_before: Optional[str] = field(default=None)
    violation_severity: Optional[str] = field(default=None)
    violation_type: Optional[str] = field(default=None)


@dataclass
class CaregiverRelationship:
    """Relationship involving responsibility for child's care, welfare, or supervision. Modeled as gUFO SubKind of CustodialRelationship."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#CaregiverRelationship"
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)
    caregiving_responsibilities: Optional[str] = field(default=None)
    supervision_level: Optional[str] = field(default=None)


@dataclass
class ChildcareProvider:
    """Professional childcare or daycare provider. Modeled as anti-rigid gUFO Role with professional care obligations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#ChildcareProvider"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class Coach:
    """Sports or activity coach with authority over young participants. Modeled as anti-rigid gUFO Role with activity-based authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#Coach"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class CustodialAbuse:
    """Abuse committed by someone in custodial or caregiving role. Modeled as gUFO SubKind of TrustViolation with role-based context."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#CustodialAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_violation_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_violation_end_point: Optional[dateTimeStamp] = field(default=None)
    perpetrated_by: list[AuthorityFigure] = field(default_factory=list)
    trust_level_after: Optional[str] = field(default=None)
    trust_level_before: Optional[str] = field(default=None)
    violation_severity: Optional[str] = field(default=None)
    violation_type: Optional[str] = field(default=None)


@dataclass
class CustodialAuthorization:
    """Official authorization granting custodial rights or responsibilities. Modeled as gUFO Object with legal authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#CustodialAuthorization"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CustodialCrisisSituation:
    """Emergency situation requiring immediate custodial intervention. Modeled as gUFO Situation with crisis characteristics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#CustodialCrisisSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class CustodialRelationship:
    """Legal or informal relationship involving custody, care, or supervision of a child. Modeled as gUFO Object with Kind typing for rigid identity criteria."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#CustodialRelationship"
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class CustodyArrangement:
    """Formal or informal arrangement for child custody or care. Modeled as gUFO Object with temporal arrangement characteristics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#CustodyArrangement"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class EmergencyCustody:
    """Temporary custody arrangement due to emergency circumstances. Modeled as anti-rigid gUFO Phase with crisis response characteristics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#EmergencyCustody"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)


@dataclass
class FamilialRelationship:
    """Family-based relationship with natural or assumed custodial responsibilities. Modeled as gUFO SubKind with inherent care obligations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#FamilialRelationship"
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class FamilyFriend:
    """Friend of family with trusted access to children. Modeled as anti-rigid gUFO Role with social trust basis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#FamilyFriend"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class FormalCustody:
    """Legally established custody arrangement with court orders or official documentation. Modeled as gUFO SubKind with legal foundation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#FormalCustody"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class Guardian:
    """Legal or appointed guardian responsible for child's welfare. Modeled as anti-rigid gUFO Role with legal authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#Guardian"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class InformalCustody:
    """Informal custody arrangement without legal documentation. Modeled as gUFO SubKind with social agreement basis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#InformalCustody"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class Mentor:
    """Adult mentor or role model with trusted relationship with child. Modeled as anti-rigid gUFO Role with developmental basis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#Mentor"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class ParentalConsent:
    """Consent given by parent or guardian for custodial arrangement. Modeled as gUFO Object with authorization characteristics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#ParentalConsent"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class PositionOfTrust:
    """Role or position that grants special access to or authority over children. Modeled as anti-rigid gUFO Role with temporal participation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#PositionOfTrust"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    trust_basis: Optional[str] = field(default=None)
    trust_scope: Optional[str] = field(default=None)


@dataclass
class ProbationaryCustodyPhase:
    """Phase when custodial relationship is under evaluation or supervision. Modeled as anti-rigid gUFO Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#ProbationaryCustodyPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class ProfessionalCareRelationship:
    """Professional relationship involving child care or supervision duties. Modeled as gUFO SubKind with professional obligations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#ProfessionalCareRelationship"
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class Relative:
    """Family member in position of trust or authority over child. Modeled as anti-rigid gUFO Role with familial basis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#Relative"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class RestrictedContactArrangement:
    """A visitation or contact arrangement that restricts or suspends offender or high-risk contact after disclosure, investigation, or safeguarding concerns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#RestrictedContactArrangement"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)
    contact_restriction_type: Optional[str] = field(default=None)
    custody_schedule: Optional[str] = field(default=None)


@dataclass
class SupervisionBreakdownSituation:
    """Situation where supervision systems have failed or become inadequate. Modeled as gUFO Situation with system failure characteristics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#SupervisionBreakdownSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class SupervisionFailure:
    """Failure to properly supervise or protect child while in position of authority. Modeled as gUFO SubKind with supervision duty violations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#SupervisionFailure"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_violation_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_violation_end_point: Optional[dateTimeStamp] = field(default=None)
    perpetrated_by: list[AuthorityFigure] = field(default_factory=list)
    trust_level_after: Optional[str] = field(default=None)
    trust_level_before: Optional[str] = field(default=None)
    violation_severity: Optional[str] = field(default=None)
    violation_type: Optional[str] = field(default=None)
    contributing_factors: Optional[str] = field(default=None)
    failure_severity: Optional[str] = field(default=None)
    failure_type: Optional[str] = field(default=None)


@dataclass
class SuspendedCustodyPhase:
    """Phase when custodial relationship is temporarily suspended but not terminated. Modeled as anti-rigid gUFO Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#SuspendedCustodyPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class Teacher:
    """Educational professional with authority over students. Modeled as anti-rigid gUFO Role with institutional authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#Teacher"
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
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class TemporaryCustody:
    """Short-term custody arrangement or supervision of a child. Modeled as anti-rigid gUFO Phase with temporal boundaries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#TemporaryCustody"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class TerminatedCustodyPhase:
    """Phase when custodial relationship has been formally ended. Modeled as anti-rigid gUFO Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#TerminatedCustodyPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
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
    end_time: Optional[datetime] = field(default=None)
    is_directional: Optional[bool] = field(default=None)
    kind_of_relationship: Optional[str] = field(default=None)
    source: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    target: Optional[UcoObject] = field(default=None)
    comment: Optional[str] = field(default=None)
    access_level: Optional[str] = field(default=None)
    has_custody_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_custody_end_point: Optional[dateTimeStamp] = field(default=None)
    in_custody_phase: Optional[Phase] = field(default=None)
    relationship_duration: Optional[float] = field(default=None)
    relationship_type: Optional[str] = field(default=None)
    trust_level: Optional[str] = field(default=None)


@dataclass
class TrustBreachSituation:
    """Situation arising from violation of trust or authority position. Modeled as gUFO Situation with trust violation context."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#TrustBreachSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class TrustViolation:
    """Action that violates a position of trust or custodial responsibility. Modeled as gUFO Event with temporal boundaries and participation patterns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#TrustViolation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_violation_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_violation_end_point: Optional[dateTimeStamp] = field(default=None)
    perpetrated_by: list[AuthorityFigure] = field(default_factory=list)
    trust_level_after: Optional[str] = field(default=None)
    trust_level_before: Optional[str] = field(default=None)
    violation_severity: Optional[str] = field(default=None)
    violation_type: Optional[str] = field(default=None)


@dataclass
class VisitationArrangement:
    """Scheduled visitation or contact arrangement with child. Modeled as gUFO SubKind with temporal scheduling patterns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#VisitationArrangement"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class VulnerabilityExposureSituation:
    """Situation where child vulnerability factors create elevated risk. Modeled as gUFO Situation with protection need characteristics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/custodial#VulnerabilityExposureSituation"
    label: list[str] = field(default_factory=list)

