"""CAC Ontology - Crimes Against Children — cacontology-multi-jurisdiction module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AllFBIFieldOfficesOperation:
    """Operation involving all 55 FBI field offices in coordinated enforcement effort."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#AllFBIFieldOfficesOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class AutomatedEvidenceDistribution:
    """Automated system for distributing evidence packages to appropriate jurisdictions based on user location and evidence strength."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#AutomatedEvidenceDistribution"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class CEOSCoordinatedOperation:
    """Operation coordinated by Child Exploitation and Obscenity Section (CEOS)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CEOSCoordinatedOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ChildRescueCoordination:
    """Coordination of child rescue operations across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ChildRescueCoordination"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class CommunityOutreachTriggeredInvestigation:
    """Investigation triggered by victim disclosure following community outreach presentation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CommunityOutreachTriggeredInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class ComplianceMonitoringOperation:
    """Large-scale operation monitoring sex offender compliance and registration requirements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ComplianceMonitoringOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class ComplianceVisitCoordination:
    """Coordination of multiple compliance visits across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ComplianceVisitCoordination"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class CoordinatedArrestWave:
    """Coordinated arrests conducted as part of larger operation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CoordinatedArrestWave"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class CoordinatedCharging:
    """Coordinated charging decisions across multiple jurisdictions to ensure consistent prosecution approach."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CoordinatedCharging"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class CoordinatingAgent:
    """Personnel responsible for coordinating multi-jurisdictional activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CoordinatingAgent"
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
class CrossBorderOperation:
    """Law enforcement operation that crosses state or national borders."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CrossBorderOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    border_type: Optional[str] = field(default=None)
    legal_framework: Optional[str] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)


@dataclass
class CrossStateEvidence:
    """Evidence collected across multiple states in trafficking investigation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#CrossStateEvidence"
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
class DistributedProsecutionTeam:
    """Prosecution team distributed across multiple jurisdictions for handling massive caseloads."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#DistributedProsecutionTeam"
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
class ExtraditionRequest:
    """Legal request to transfer suspect between jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ExtraditionRequest"
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
class FederalAgency:
    """Law enforcement agency with federal jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#FederalAgency"
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
    has_capability_level: Optional[str] = field(default=None)
    has_cooperation_willingness: Optional[float] = field(default=None)
    has_resource_capacity: Optional[str] = field(default=None)


@dataclass
class FederalJurisdiction:
    """Legal authority under federal law and courts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#FederalJurisdiction"
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
    has_compliance_score: Optional[float] = field(default=None)
    has_harmonization_level: Optional[str] = field(default=None)
    jurisdiction_type: Optional[str] = field(default=None)


@dataclass
class FederalJurisdictionTrigger:
    """Interstate activity that triggers federal jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#FederalJurisdictionTrigger"
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
class HandsOnOffenseInvestigation:
    """Investigation specifically targeting hands-on sexual offenses against children."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#HandsOnOffenseInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class InformationSharing:
    """Formal sharing of intelligence or evidence between jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InformationSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    classification_level: Optional[str] = field(default=None)
    has_actionability: Optional[float] = field(default=None)
    has_intelligence_value: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[float] = field(default=None)
    has_timeliness: Optional[str] = field(default=None)
    reciprocity_required: Optional[bool] = field(default=None)
    sharing_date: Optional[datetime] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)


@dataclass
class InformationSharingAgreement:
    """Agreement governing sharing of sensitive information between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InformationSharingAgreement"
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
class InformationSynthesisPhase:
    """Phase involving compilation and analysis of multi-jurisdictional evidence."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InformationSynthesisPhase"
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


@dataclass
class InitialCoordinationPhase:
    """Phase involving initial contact and coordination between jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InitialCoordinationPhase"
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


@dataclass
class InteragencyAgreement:
    """Formal agreement between agencies for cooperation and resource sharing."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InteragencyAgreement"
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
class InteragencyCooperationSituation:
    """Situation involving successful coordination between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InteragencyCooperationSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class InternationalAgency:
    """Law enforcement agency from foreign jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InternationalAgency"
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
    has_capability_level: Optional[str] = field(default=None)
    has_cooperation_willingness: Optional[float] = field(default=None)
    has_resource_capacity: Optional[str] = field(default=None)


@dataclass
class InternationalJurisdiction:
    """Legal authority in foreign countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InternationalJurisdiction"
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
    has_compliance_score: Optional[float] = field(default=None)
    has_harmonization_level: Optional[str] = field(default=None)
    jurisdiction_type: Optional[str] = field(default=None)


@dataclass
class InternationalLegalHarmonization:
    """Harmonization of legal approaches across countries for consistent prosecution of global platform users."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InternationalLegalHarmonization"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    border_type: Optional[str] = field(default=None)
    legal_framework: Optional[str] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)


@dataclass
class InternationalProsecutionFramework:
    """Framework for coordinating prosecutions across multiple countries for global platform takedowns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InternationalProsecutionFramework"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    border_type: Optional[str] = field(default=None)
    legal_framework: Optional[str] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)


@dataclass
class InterstateCoordination:
    """Coordination between law enforcement agencies across state lines."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InterstateCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    classification_level: Optional[str] = field(default=None)
    has_actionability: Optional[float] = field(default=None)
    has_intelligence_value: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[float] = field(default=None)
    has_timeliness: Optional[str] = field(default=None)
    reciprocity_required: Optional[bool] = field(default=None)
    sharing_date: Optional[datetime] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)


@dataclass
class InterstateFlightFromProsecution:
    """Crossing state lines to avoid prosecution or arrest."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InterstateFlightFromProsecution"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class InterstateTraffickingNetwork:
    """Criminal network operating across state boundaries for trafficking."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InterstateTraffickingNetwork"
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


@dataclass
class InterstateTransportationOffense:
    """Criminal offense involving transportation of victim across state lines."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InterstateTransportationOffense"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class InterstateVictimTransport:
    """Transportation of minor victim across state lines."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#InterstateVictimTransport"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class JointExecutionPhase:
    """Phase involving coordinated execution of multi-jurisdictional operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#JointExecutionPhase"
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


@dataclass
class JointInvestigation:
    """Investigation conducted jointly by multiple law enforcement agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#JointInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class Jurisdiction:
    """Legal authority and geographic area where an agency has enforcement power."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#Jurisdiction"
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
    has_compliance_score: Optional[float] = field(default=None)
    has_harmonization_level: Optional[str] = field(default=None)
    jurisdiction_type: Optional[str] = field(default=None)


@dataclass
class JurisdictionalConflictSituation:
    """Situation involving disputes over jurisdictional authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#JurisdictionalConflictSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class JurisdictionalHandoff:
    """Transfer of investigative authority between state and federal agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#JurisdictionalHandoff"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class JurisdictionalNegotiationPhase:
    """Phase involving determination of lead agency and jurisdictional authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#JurisdictionalNegotiationPhase"
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


@dataclass
class JurisdictionalWarrant:
    """Legal authorization that specifies jurisdictional authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#JurisdictionalWarrant"
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
class LargeScaleOperation:
    """Operation involving 100+ law enforcement actions or extensive coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#LargeScaleOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class LawEnforcementAgency:
    """Government organization responsible for law enforcement within a jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#LawEnforcementAgency"
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
    has_capability_level: Optional[str] = field(default=None)
    has_cooperation_willingness: Optional[float] = field(default=None)
    has_resource_capacity: Optional[str] = field(default=None)


@dataclass
class LeadAgency:
    """Primary agency responsible for coordinating multi-jurisdictional investigation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#LeadAgency"
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
class LiaisonOfficer:
    """Officer responsible for communication between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#LiaisonOfficer"
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
class LocalAgency:
    """Law enforcement agency with local jurisdiction (city, county, municipal)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#LocalAgency"
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
    has_capability_level: Optional[str] = field(default=None)
    has_cooperation_willingness: Optional[float] = field(default=None)
    has_resource_capacity: Optional[str] = field(default=None)


@dataclass
class LocalJurisdiction:
    """Legal authority at local level (city, county, municipal)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#LocalJurisdiction"
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
    has_compliance_score: Optional[float] = field(default=None)
    has_harmonization_level: Optional[str] = field(default=None)
    jurisdiction_type: Optional[str] = field(default=None)


@dataclass
class MassChildRescueOperation:
    """Large-scale operation resulting in rescue of 100+ children."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MassChildRescueOperation"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class MassProsecutionCoordination:
    """Coordination of prosecutions for massive user bases from large-scale platform takedowns requiring simultaneous action across multiple jurisdictions (nearly 2 million users for Kidflix operation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MassProsecutionCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MassUserJurisdictionMapping:
    """Mapping of massive user bases to appropriate jurisdictions for prosecution based on location and legal frameworks."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MassUserJurisdictionMapping"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class MultiJurisdictionalInvestigation:
    """Investigation spanning multiple legal jurisdictions requiring coordination between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MultiJurisdictionalInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class MultiJurisdictionalSituation:
    """Complex situation requiring coordination across multiple jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MultiJurisdictionalSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class MultiStateTraffickingInvestigation:
    """Child sex trafficking investigation spanning multiple states."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MultiStateTraffickingInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    border_type: Optional[str] = field(default=None)
    legal_framework: Optional[str] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)


@dataclass
class MutualAidRequest:
    """Formal request for assistance from another jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#MutualAidRequest"
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
class NamedMultiJurisdictionalOperation:
    """Formally named multi-phase operation coordinated across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#NamedMultiJurisdictionalOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class NationalCoordinatedOperation:
    """Operation coordinated across multiple CAC task forces nationally."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#NationalCoordinatedOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class NationwideChildRescueCoordination:
    """Coordination of child rescue operations across entire country."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#NationwideChildRescueCoordination"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class NationwideOperation:
    """Law enforcement operation coordinated across entire country involving all FBI field offices."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#NationwideOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class OperationMetricsTracking:
    """Comprehensive tracking of operation outcomes and effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#OperationMetricsTracking"
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
    has_confidence: Optional[float] = field(default=None)


@dataclass
class OperationSafeOnlineSummerType:
    """Type of national operation coordinated across 61+ CAC Task Forces."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#OperationSafeOnlineSummerType"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ParticipatingAgency:
    """Agency providing support or resources to multi-jurisdictional investigation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ParticipatingAgency"
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
class PriorityProsecutionTrack:
    """High-priority prosecution track for most serious offenders identified in mass user analysis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#PriorityProsecutionTrack"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class ProactiveInvestigationCampaign:
    """Campaign focused on proactive investigation rather than reactive response."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ProactiveInvestigationCampaign"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class ProjectSafeChildhoodOperation:
    """Operation conducted under Project Safe Childhood initiative framework."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ProjectSafeChildhoodOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ProsecutionCapacityAnalysis:
    """Analysis of prosecution capacity across jurisdictions to optimize case distribution for massive operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ProsecutionCapacityAnalysis"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class RapidResponseCoordination:
    """Coordination enabling rapid response from victim disclosure to arrest."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#RapidResponseCoordination"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class RegistrationComplianceViolation:
    """Violation of sex offender registration requirements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#RegistrationComplianceViolation"
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
class ResourceSharing:
    """Sharing of personnel, equipment, or expertise between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#ResourceSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    cost_sharing: Optional[str] = field(default=None)
    has_availability: Optional[float] = field(default=None)
    has_cost_effectiveness: Optional[str] = field(default=None)
    has_resource_utilization: Optional[float] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    resource_value: Optional[float] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)


@dataclass
class SchoolPresentationDisclosureWorkflow:
    """Workflow from school safety presentation to victim disclosure to rapid arrest."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#SchoolPresentationDisclosureWorkflow"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class SexOffenderComplianceCheck:
    """Individual compliance check visit to registered sex offender."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#SexOffenderComplianceCheck"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class SimultaneousChildRescue:
    """Rescue of multiple children across different locations simultaneously."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#SimultaneousChildRescue"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class StateAgency:
    """Law enforcement agency with state-level jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#StateAgency"
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
    has_capability_level: Optional[str] = field(default=None)
    has_cooperation_willingness: Optional[float] = field(default=None)
    has_resource_capacity: Optional[str] = field(default=None)


@dataclass
class StateJurisdiction:
    """Legal authority under state law and courts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#StateJurisdiction"
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
    has_compliance_score: Optional[float] = field(default=None)
    has_harmonization_level: Optional[str] = field(default=None)
    jurisdiction_type: Optional[str] = field(default=None)


@dataclass
class StateLineCrossing:
    """Documented crossing of state boundaries during offense."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#StateLineCrossing"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class StatewideSweep:
    """Statewide operation conducting compliance checks across all jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#StatewideSweep"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class TaskForce:
    """Temporary multi-agency organization formed for specific operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#TaskForce"
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
    has_cohesion_level: Optional[float] = field(default=None)
    has_expertise_level: Optional[str] = field(default=None)
    has_operational_readiness: Optional[str] = field(default=None)


@dataclass
class TaskForceLeader:
    """Officer responsible for leading multi-agency task force operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#TaskForceLeader"
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
class TaskForceOperation:
    """Coordinated operation conducted by multi-agency task force."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#TaskForceOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)


@dataclass
class TraffickingCoordinationCenter:
    """Center coordinating multi-state trafficking investigations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#TraffickingCoordinationCenter"
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
class TraffickingInvestigationTask:
    """Specific investigation task in multi-state trafficking case."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#TraffickingInvestigationTask"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class TransportationForIllegalPurpose:
    """Transportation with intent to engage in criminal sexual activity."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#TransportationForIllegalPurpose"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class USAttorneyOfficeParticipation:
    """Participation of US Attorney's Offices around the country in coordinated operation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#USAttorneyOfficeParticipation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    operation_duration: Optional[float] = field(default=None)
    operation_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class UserTriageProsecution:
    """Prosecution strategy based on automated triage of user risk levels and evidence strength for massive user databases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#UserTriageProsecution"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)


@dataclass
class VictimIdentificationTask:
    """Task focused on identifying new child victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/multi-jurisdiction#VictimIdentificationTask"
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)

