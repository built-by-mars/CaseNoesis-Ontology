"""CAC Ontology - Crimes Against Children — cacontology-temporal module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Age:
    """Age of a person modeled as a gUFO Quality whose concrete value is attributed in time-bounded situations. Intended for age-of-consent, Romeo-and-Juliet, and other age-dependent legal reasoning."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#Age"


@dataclass
class AgeAtTimeSituation:
    """gUFO QualityValueAttributionSituation specializing in attribution of an Age quality value to a specific person over a time-bounded interval (e.g., the victim was 13 years old during a 2025 grooming ev"""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#AgeAtTimeSituation"
    label: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    age_subject: Optional[Person] = field(default=None)
    has_age_in_years: Optional[float] = field(default=None)


@dataclass
class AnalysisTransitionEvent:
    """Event transitioning investigation from Initial to Analysis Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#AnalysisTransitionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class ClosureEvent:
    """Event transitioning investigation from Resolution to Completed Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ClosureEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class CompletedPhase:
    """Terminal phase indicating investigation has been fully concluded with all actions finalized."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#CompletedPhase"
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
class ConcurrentInvestigationSituation:
    """Situation where multiple investigations run simultaneously, potentially sharing resources or evidence. Modeled as gUFO Situation with temporal overlap constraints."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ConcurrentInvestigationSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class EventSequence:
    """Ordered sequence of investigation events with temporal dependencies. Modeled as gUFO structured event pattern."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#EventSequence"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class EvidenceTransitionEvent:
    """Event transitioning investigation from Legal Process to Evidence Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#EvidenceTransitionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class InitiationEvent:
    """Event transitioning investigation from non-existence to Initial Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#InitiationEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class InvestigationLifecycle:
    """Complete temporal structure of CAC investigation from initiation to closure. Modeled as gUFO Kind with definite phase sequence and temporal constraints."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#InvestigationLifecycle"


@dataclass
class LegalProcessTransitionEvent:
    """Event transitioning investigation from Analysis to Legal Process Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#LegalProcessTransitionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class MultiJurisdictionCoordinationSituation:
    """Situation where investigation requires coordination across multiple jurisdictions with timing synchronization. Modeled as gUFO Situation with coordination constraints."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#MultiJurisdictionCoordinationSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class ParallelEventCluster:
    """Set of investigation events occurring simultaneously or with temporal overlap. Modeled as gUFO composite event pattern."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ParallelEventCluster"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ParallelEvidenceCollectionSituation:
    """Situation where multiple evidence collection activities occur simultaneously across different phases. Modeled as gUFO Situation allowing phase overlap."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ParallelEvidenceCollectionSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class PhaseTransitionEvent:
    """Event marking transition between investigation phases. Modeled as gUFO Event with temporal boundaries and phase change effects."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#PhaseTransitionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class ResolutionPhase:
    """Phase focused on resolution of investigation outcomes such as plea agreements, sentencing, and restitution orders."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ResolutionPhase"
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
class ResolutionTransitionEvent:
    """Event transitioning investigation from Evidence to Resolution Phase."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ResolutionTransitionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transitions_from: Optional[Phase] = field(default=None)
    transitions_to: Optional[Phase] = field(default=None)


@dataclass
class ResumptionEvent:
    """Event causing investigation to exit suspended state and resume active phase. Modeled as gUFO Event terminating suspension situation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#ResumptionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    resumes: Optional[CACInvestigation] = field(default=None)
    terminates_suspension: Optional[SuspendedSituation] = field(default=None)


@dataclass
class RoleConflictSituation:
    """Situation where person's multiple roles create potential conflict of interest. Modeled as gUFO Situation requiring resolution."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#RoleConflictSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class RoleEscalation:
    """Role transition involving increased responsibility or authority (e.g., analyst to lead investigator)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#RoleEscalation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class RoleReassignment:
    """Role transition involving change in assignment without authority change (e.g., different investigator)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#RoleReassignment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class RoleTransition:
    """Event representing change in person's role within investigation. Modeled as gUFO Event with role change effects."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#RoleTransition"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class SimultaneousRoleSituation:
    """Situation where person plays multiple roles simultaneously in investigation context. Modeled as gUFO Situation with role overlap."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#SimultaneousRoleSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class SuspendedSituation:
    """Situation where investigation is temporarily suspended pending resources, legal decisions, or external factors. Modeled as gUFO Situation with temporal duration."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#SuspendedSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class SuspensionEvent:
    """Event causing investigation to enter suspended state. Modeled as gUFO Event creating suspension situation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#SuspensionEvent"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    creates_suspension: Optional[SuspendedSituation] = field(default=None)
    suspends: Optional[CACInvestigation] = field(default=None)


@dataclass
class UrgentRescueLifecycle:
    """Accelerated investigation lifecycle for urgent child rescue situations. Compressed phase durations with parallel processing."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/temporal#UrgentRescueLifecycle"

