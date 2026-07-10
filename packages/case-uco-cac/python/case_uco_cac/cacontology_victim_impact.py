"""CAC Ontology - Crimes Against Children — cacontology-victim-impact module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AcuteImpactPhase:
    """Immediate phase following victimization with acute psychological impact."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#AcuteImpactPhase"
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
class AcuteTrauma:
    """Immediate psychological trauma following victimization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#AcuteTrauma"
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
    duration: Optional[float] = field(default=None)
    harm_type: Optional[str] = field(default=None)
    onset_timing: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)


@dataclass
class BehavioralIndicator:
    """Changes in behavior that indicate trauma or distress."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#BehavioralIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    frequency: Optional[str] = field(default=None)
    indicator_severity: Optional[str] = field(default=None)
    indicator_type: Optional[str] = field(default=None)


@dataclass
class ChildExploitationTaskForce:
    """Joint task force between FBI and local law enforcement for child exploitation cases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#ChildExploitationTaskForce"
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
class ChronicTrauma:
    """Long-term psychological trauma from prolonged or repeated victimization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#ChronicTrauma"
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
    duration: Optional[float] = field(default=None)
    harm_type: Optional[str] = field(default=None)
    onset_timing: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)


@dataclass
class CognitiveBehavioralTherapy:
    """CBT-based therapeutic intervention for trauma and behavioral issues."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#CognitiveBehavioralTherapy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    intervention_type: Optional[str] = field(default=None)
    session_count: Optional[int] = field(default=None)
    treatment_duration: Optional[float] = field(default=None)
    treatment_modality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class CognitiveIndicator:
    """Changes in thinking, memory, or learning ability due to trauma."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#CognitiveIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    frequency: Optional[str] = field(default=None)
    indicator_severity: Optional[str] = field(default=None)
    indicator_type: Optional[str] = field(default=None)


@dataclass
class CommunitySupport:
    """Community-based support services for trafficking victims during reintegration."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#CommunitySupport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class ComplexTrauma:
    """Complex trauma resulting from multiple types of victimization or prolonged abuse."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#ComplexTrauma"
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
    duration: Optional[float] = field(default=None)
    harm_type: Optional[str] = field(default=None)
    onset_timing: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)
    attachment_disruption: Optional[bool] = field(default=None)
    developmental_impact: Optional[bool] = field(default=None)
    trauma_type: Optional[str] = field(default=None)


@dataclass
class ComprehensiveImpactAssessment:
    """Detailed evaluation of victim impact for legal proceedings and treatment planning."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#ComprehensiveImpactAssessment"
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
    label: Optional[str] = field(default=None)
    has_confidence: Optional[float] = field(default=None)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    assessment_date: Optional[datetime] = field(default=None)
    assessment_duration: Optional[float] = field(default=None)
    assessment_type: Optional[str] = field(default=None)
    assessor_credentials: Optional[str] = field(default=None)
    severity_level: Optional[str] = field(default=None)
    assessment_domains: Optional[int] = field(default=None)
    standardized_instruments: Optional[bool] = field(default=None)


@dataclass
class CrisisIntervention:
    """Immediate therapeutic intervention for acute crisis situations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#CrisisIntervention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    intervention_type: Optional[str] = field(default=None)
    session_count: Optional[int] = field(default=None)
    treatment_duration: Optional[float] = field(default=None)
    treatment_modality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class DevelopmentalImpact:
    """Impact on normal child development due to victimization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#DevelopmentalImpact"
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
    duration: Optional[float] = field(default=None)
    harm_type: Optional[str] = field(default=None)
    onset_timing: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)
    age_at_impact: Optional[int] = field(default=None)
    developmental_delay: Optional[bool] = field(default=None)
    developmental_domain: Optional[str] = field(default=None)


@dataclass
class EducationalSupport:
    """Educational accommodations and support for victim's schooling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#EducationalSupport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class EmergencyHelpSeeking:
    """Victim's attempt to seek emergency help during trafficking or exploitation, such as calling 911 (e.g., Wilmington, NC call)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#EmergencyHelpSeeking"


@dataclass
class EmergencyResponse:
    """Immediate response to victim emergency help requests, including law enforcement and victim services coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#EmergencyResponse"
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
class EmotionalIndicator:
    """Emotional symptoms or reactions indicating trauma."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#EmotionalIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    frequency: Optional[str] = field(default=None)
    indicator_severity: Optional[str] = field(default=None)
    indicator_type: Optional[str] = field(default=None)


@dataclass
class FamilyReunification:
    """Process of reuniting trafficking victims with their families."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#FamilyReunification"
    label: list[str] = field(default_factory=list)
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
    recovery_milestones: Optional[int] = field(default=None)
    recovery_progress: Optional[str] = field(default=None)
    recovery_stage: Optional[str] = field(default=None)
    time_in_recovery: Optional[float] = field(default=None)


@dataclass
class FamilyTherapy:
    """Therapeutic intervention involving the victim's family."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#FamilyTherapy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    intervention_type: Optional[str] = field(default=None)
    session_count: Optional[int] = field(default=None)
    treatment_duration: Optional[float] = field(default=None)
    treatment_modality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class FearlessHudsonValleySupport:
    """Support services provided by Fearless! Hudson Valley organization for trafficking victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#FearlessHudsonValleySupport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class GroupTherapy:
    """Therapeutic intervention conducted in group settings with other victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#GroupTherapy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    intervention_type: Optional[str] = field(default=None)
    session_count: Optional[int] = field(default=None)
    treatment_duration: Optional[float] = field(default=None)
    treatment_modality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class HelpSeekingBarrier:
    """Factor that prevents or impedes victim from seeking help (fear, control, isolation, trauma bonding)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#HelpSeekingBarrier"
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
class HelpSeekingFacilitator:
    """Factor that enables or encourages victim to seek help (opportunity, trust, desperation, external support)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#HelpSeekingFacilitator"
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
class HometownReturn:
    """Return of trafficking victim to their hometown or place of origin."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#HometownReturn"
    label: list[str] = field(default_factory=list)
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
    recovery_milestones: Optional[int] = field(default=None)
    recovery_progress: Optional[str] = field(default=None)
    recovery_stage: Optional[str] = field(default=None)
    time_in_recovery: Optional[float] = field(default=None)


@dataclass
class HospitalDischarge:
    """Discharge of trafficking victim from hospital with safety planning and transportation arrangements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#HospitalDischarge"
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
class HospitalIntervention:
    """Medical intervention and assessment of trafficking victim at hospital following emergency call."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#HospitalIntervention"
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
class HumanTraffickingSquad:
    """Specialized law enforcement unit focused on human trafficking investigations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#HumanTraffickingSquad"
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
class InitialImpactAssessment:
    """Initial evaluation of victim impact conducted early in investigation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#InitialImpactAssessment"
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
    label: Optional[str] = field(default=None)
    has_confidence: Optional[float] = field(default=None)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    assessment_date: Optional[datetime] = field(default=None)
    assessment_duration: Optional[float] = field(default=None)
    assessment_type: Optional[str] = field(default=None)
    assessor_credentials: Optional[str] = field(default=None)
    severity_level: Optional[str] = field(default=None)


@dataclass
class InterstateVictimServices:
    """Victim services coordination across state lines for trafficking cases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#InterstateVictimServices"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class LegalSupport:
    """Legal assistance and representation for victims in proceedings."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#LegalSupport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class LongTermEffect:
    """Long-term consequences of victimization on the child's life."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#LongTermEffect"
    label: list[str] = field(default_factory=list)
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
    effect_duration: Optional[float] = field(default=None)
    effect_severity: Optional[str] = field(default=None)
    effect_type: Optional[str] = field(default=None)
    functional_impairment: Optional[bool] = field(default=None)


@dataclass
class LongTermMonitoringPhase:
    """Extended phase monitoring long-term effects and continued support needs."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#LongTermMonitoringPhase"
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
class MedicalTraumaAssessment:
    """Medical assessment of physical and psychological trauma in trafficking victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#MedicalTraumaAssessment"
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
    label: Optional[str] = field(default=None)
    has_confidence: Optional[float] = field(default=None)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    assessment_date: Optional[datetime] = field(default=None)
    assessment_duration: Optional[float] = field(default=None)
    assessment_type: Optional[str] = field(default=None)
    assessor_credentials: Optional[str] = field(default=None)
    severity_level: Optional[str] = field(default=None)


@dataclass
class MultiAgencyVictimResponse:
    """Coordinated victim assistance involving multiple agencies across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#MultiAgencyVictimResponse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class NineOneOneCall:
    """Emergency call to 911 by trafficking victim seeking help and reporting forced prostitution."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#NineOneOneCall"


@dataclass
class NonOffendingCaregiverSupport:
    """Support services directed to the non-offending caregiver to stabilize the child-support system after disclosure and reduce pressure toward recantation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#NonOffendingCaregiverSupport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class OngoingDangerAssessment:
    """Assessment of victim's ongoing danger from trafficking network and need for protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#OngoingDangerAssessment"
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
    label: Optional[str] = field(default=None)
    has_confidence: Optional[float] = field(default=None)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    assessment_date: Optional[datetime] = field(default=None)
    assessment_duration: Optional[float] = field(default=None)
    assessment_type: Optional[str] = field(default=None)
    assessor_credentials: Optional[str] = field(default=None)
    severity_level: Optional[str] = field(default=None)


@dataclass
class OngoingImpactMonitoring:
    """Continuous monitoring of victim impact during investigation and recovery."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#OngoingImpactMonitoring"
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
    label: Optional[str] = field(default=None)
    has_confidence: Optional[float] = field(default=None)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    assessment_date: Optional[datetime] = field(default=None)
    assessment_duration: Optional[float] = field(default=None)
    assessment_type: Optional[str] = field(default=None)
    assessor_credentials: Optional[str] = field(default=None)
    severity_level: Optional[str] = field(default=None)


@dataclass
class PeerSupportService:
    """Support rooted in peer connection, mutuality, and survivor- or youth-informed encouragement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#PeerSupportService"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class PhysicalIndicator:
    """Physical symptoms or manifestations of psychological trauma."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#PhysicalIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    frequency: Optional[str] = field(default=None)
    indicator_severity: Optional[str] = field(default=None)
    indicator_type: Optional[str] = field(default=None)


@dataclass
class PortAuthorityYouthServices:
    """Specialized youth services unit within Port Authority Police Department."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#PortAuthorityYouthServices"
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
class PsychologicalHarm:
    """Mental or emotional harm experienced by child victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#PsychologicalHarm"
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
    duration: Optional[float] = field(default=None)
    harm_type: Optional[str] = field(default=None)
    onset_timing: Optional[str] = field(default=None)
    severity: Optional[str] = field(default=None)


@dataclass
class RecoveryMilestone:
    """Significant achievement or progress point in victim recovery."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#RecoveryMilestone"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class RecoveryPhase:
    """Phase focused on healing and therapeutic intervention."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#RecoveryPhase"
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
class RecoveryProcess:
    """Process of healing and recovery from victimization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#RecoveryProcess"
    label: list[str] = field(default_factory=list)
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
    recovery_milestones: Optional[int] = field(default=None)
    recovery_progress: Optional[str] = field(default=None)
    recovery_stage: Optional[str] = field(default=None)
    time_in_recovery: Optional[float] = field(default=None)


@dataclass
class ReintegrationPhase:
    """Phase involving return to normal activities and social reintegration."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#ReintegrationPhase"
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
class ResilienceFactors:
    """Protective factors that promote victim resilience and recovery."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#ResilienceFactors"
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
class SafetyPlanning:
    """Development of safety plans to protect victims from further harm."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#SafetyPlanning"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class SocialIndicator:
    """Changes in social behavior or relationships due to trauma."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#SocialIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    frequency: Optional[str] = field(default=None)
    indicator_severity: Optional[str] = field(default=None)
    indicator_type: Optional[str] = field(default=None)


@dataclass
class SuicidalIdeationResponse:
    """Emergency response to trafficking victim reporting suicidal thoughts or intentions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#SuicidalIdeationResponse"
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
class TherapeuticIntervention:
    """Professional therapeutic treatment or intervention for victim recovery."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TherapeuticIntervention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    intervention_type: Optional[str] = field(default=None)
    session_count: Optional[int] = field(default=None)
    treatment_duration: Optional[float] = field(default=None)
    treatment_modality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TherapistRole:
    """Role of mental health professional providing therapeutic services."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TherapistRole"
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
class TherapyParticipant:
    """Role of victim participating in therapeutic interventions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TherapyParticipant"
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
class TraffickerControlBarrier:
    """Control mechanisms used by traffickers that prevent victims from seeking help."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TraffickerControlBarrier"
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
class TraumaIndicator:
    """Observable signs or symptoms indicating psychological trauma."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TraumaIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    frequency: Optional[str] = field(default=None)
    indicator_severity: Optional[str] = field(default=None)
    indicator_type: Optional[str] = field(default=None)


@dataclass
class TraumaTherapy:
    """Specialized therapy for treating trauma and its effects."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TraumaTherapy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    intervention_type: Optional[str] = field(default=None)
    session_count: Optional[int] = field(default=None)
    treatment_duration: Optional[float] = field(default=None)
    treatment_modality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    evidence_based: Optional[bool] = field(default=None)
    trauma_focused: Optional[bool] = field(default=None)


@dataclass
class TraumatizedVictim:
    """Role of a child victim experiencing psychological trauma. Where age at time of victimization or at time of assessment is analytically relevant, that age SHOULD be expressed via cacontology-temporal:Ag"""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#TraumatizedVictim"
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
class VictimAdvocacy:
    """Advocacy services to protect victim rights and interests."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimAdvocacy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class VictimAdvocateRole:
    """Role of professional providing advocacy support to victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimAdvocateRole"
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
class VictimExtraction:
    """Immediate removal of victim from dangerous trafficking situation following emergency call."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimExtraction"
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
class VictimImpactAssessment:
    """Comprehensive assessment of the impact of criminal activity on child victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimImpactAssessment"
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
    label: Optional[str] = field(default=None)
    has_confidence: Optional[float] = field(default=None)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    assessment_date: Optional[datetime] = field(default=None)
    assessment_duration: Optional[float] = field(default=None)
    assessment_type: Optional[str] = field(default=None)
    assessor_credentials: Optional[str] = field(default=None)
    severity_level: Optional[str] = field(default=None)


@dataclass
class VictimInRecovery:
    """Role of a victim actively engaged in recovery process."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimInRecovery"
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
class VictimReintegration:
    """Process of reintegrating trafficking victims back into their communities and families."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimReintegration"
    label: list[str] = field(default_factory=list)
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
    recovery_milestones: Optional[int] = field(default=None)
    recovery_progress: Optional[str] = field(default=None)
    recovery_stage: Optional[str] = field(default=None)
    time_in_recovery: Optional[float] = field(default=None)


@dataclass
class VictimSafetyPlanning:
    """Development of safety plan for trafficking victim to prevent re-victimization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimSafetyPlanning"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class VictimSelfReporting:
    """Victim's direct reporting of their trafficking or exploitation situation to authorities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimSelfReporting"


@dataclass
class VictimServiceCoordination:
    """Coordination of victim services between multiple agencies and organizations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimServiceCoordination"
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
class VictimSupport:
    """Support services provided to child victims and their families."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimSupport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)


@dataclass
class VictimTransportationAssistance:
    """Provision of transportation assistance to trafficking victims (bus tickets, safe transport)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/victim-impact#VictimTransportationAssistance"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    service_provider: Optional[str] = field(default=None)
    service_type: Optional[str] = field(default=None)

