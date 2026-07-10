"""CAC Ontology - Crimes Against Children — cacontology-law-enforcement-corruption module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AccessPrivilegeAbuse:
    """Abuse of special access privileges granted to law enforcement personnel."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#AccessPrivilegeAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class AuthoritySymbolExploitation:
    """Use of badges, weapons, or other authority symbols to enhance exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#AuthoritySymbolExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)
    has_symbol_visibility: Optional[str] = field(default=None)


@dataclass
class BadgeDisplayedProduction:
    """CSAM production where law enforcement badge is prominently displayed."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#BadgeDisplayedProduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)
    has_symbol_visibility: Optional[str] = field(default=None)


@dataclass
class CorruptArmyReservist:
    """Army reservist engaged in child exploitation activities while in military uniform."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#CorruptArmyReservist"
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
    authority_level: Optional[str] = field(default=None)
    corruption_duration: list[int] = field(default_factory=list)
    department_affiliation: Optional[str] = field(default=None)
    employment_status: Optional[str] = field(default=None)
    has_corruption_dependency: Optional[str] = field(default=None)
    has_position_exploitation_level: Optional[float] = field(default=None)
    has_trust_betrayal_level: Optional[str] = field(default=None)
    participates_in: list[LawEnforcementCorruption] = field(default_factory=list)
    years_of_service: list[int] = field(default_factory=list)


@dataclass
class CorruptLawEnforcementOfficer:
    """Law enforcement officer engaged in child exploitation activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#CorruptLawEnforcementOfficer"
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
    authority_level: Optional[str] = field(default=None)
    corruption_duration: list[int] = field(default_factory=list)
    department_affiliation: Optional[str] = field(default=None)
    employment_status: Optional[str] = field(default=None)
    has_corruption_dependency: Optional[str] = field(default=None)
    has_position_exploitation_level: Optional[float] = field(default=None)
    has_trust_betrayal_level: Optional[str] = field(default=None)
    participates_in: list[LawEnforcementCorruption] = field(default_factory=list)
    years_of_service: list[int] = field(default_factory=list)


@dataclass
class CorruptMetropolitanPoliceDepartmentOfficer:
    """Former or current metropolitan police department officer engaged in child trafficking."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#CorruptMetropolitanPoliceDepartmentOfficer"
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
    authority_level: Optional[str] = field(default=None)
    corruption_duration: list[int] = field(default_factory=list)
    department_affiliation: Optional[str] = field(default=None)
    employment_status: Optional[str] = field(default=None)
    has_corruption_dependency: Optional[str] = field(default=None)
    has_position_exploitation_level: Optional[float] = field(default=None)
    has_trust_betrayal_level: Optional[str] = field(default=None)
    participates_in: list[LawEnforcementCorruption] = field(default_factory=list)
    years_of_service: list[int] = field(default_factory=list)


@dataclass
class CorruptStateTrooper:
    """State trooper engaged in child exploitation activities while in uniform."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#CorruptStateTrooper"
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
    authority_level: Optional[str] = field(default=None)
    corruption_duration: list[int] = field(default_factory=list)
    department_affiliation: Optional[str] = field(default=None)
    employment_status: Optional[str] = field(default=None)
    has_corruption_dependency: Optional[str] = field(default=None)
    has_position_exploitation_level: Optional[float] = field(default=None)
    has_trust_betrayal_level: Optional[str] = field(default=None)
    participates_in: list[LawEnforcementCorruption] = field(default_factory=list)
    years_of_service: list[int] = field(default_factory=list)


@dataclass
class DatabaseAccessAbuse:
    """Misuse of law enforcement database access for personal exploitation activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#DatabaseAccessAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class EvidenceManipulation:
    """Manipulation or destruction of evidence to protect exploitation activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#EvidenceManipulation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class ExternalOversightInvestigation:
    """Investigation by external agency into law enforcement corruption."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#ExternalOversightInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_evidence_integrity: Optional[float] = field(default=None)
    has_investigation_complexity: Optional[str] = field(default=None)


@dataclass
class FormerLawEnforcementOfficer:
    """Former law enforcement officer using previous position and contacts for exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#FormerLawEnforcementOfficer"
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
    authority_level: Optional[str] = field(default=None)
    corruption_duration: list[int] = field(default_factory=list)
    department_affiliation: Optional[str] = field(default=None)
    employment_status: Optional[str] = field(default=None)
    has_corruption_dependency: Optional[str] = field(default=None)
    has_position_exploitation_level: Optional[float] = field(default=None)
    has_trust_betrayal_level: Optional[str] = field(default=None)
    participates_in: list[LawEnforcementCorruption] = field(default_factory=list)
    years_of_service: list[int] = field(default_factory=list)


@dataclass
class InformationLeakage:
    """Leaking of law enforcement information to facilitate exploitation or trafficking."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#InformationLeakage"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class InsiderThreat:
    """Threat posed by individuals within law enforcement or military who exploit their position for criminal activity."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#InsiderThreat"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)


@dataclass
class InsiderThreatDetection:
    """Detection of corruption within law enforcement or military personnel."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#InsiderThreatDetection"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_evidence_integrity: Optional[float] = field(default=None)
    has_investigation_complexity: Optional[str] = field(default=None)


@dataclass
class InternalAffairsInvestigation:
    """Investigation by internal affairs department into officer corruption."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#InternalAffairsInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_evidence_integrity: Optional[float] = field(default=None)
    has_investigation_complexity: Optional[str] = field(default=None)


@dataclass
class InvestigativeAuthorityAbuse:
    """Abuse of investigative powers and access for exploitation purposes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#InvestigativeAuthorityAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class LawEnforcementCorruption:
    """Corruption involving law enforcement personnel in child exploitation activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#LawEnforcementCorruption"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)


@dataclass
class MilitaryUniformProduction:
    """Production of CSAM while wearing military uniform."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#MilitaryUniformProduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)


@dataclass
class OfficerChildTrafficking:
    """Child trafficking conducted by law enforcement officers using their position and authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#OfficerChildTrafficking"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class OfficerProducedCSAM:
    """Child sexual abuse material produced by law enforcement officers, often while in uniform."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#OfficerProducedCSAM"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)


@dataclass
class OfficialVehicleExploitation:
    """Use of official law enforcement vehicles in exploitation activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#OfficialVehicleExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class PoliceUniformProduction:
    """Production of CSAM while wearing police uniform."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#PoliceUniformProduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)


@dataclass
class PositionOfAuthorityAbuse:
    """Abuse of law enforcement or military position of authority for exploitation purposes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#PositionOfAuthorityAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_authority_abuse_degree: Optional[str] = field(default=None)
    has_intimidation_factor: Optional[float] = field(default=None)


@dataclass
class PublicIntegrityInvestigation:
    """Investigation into public integrity violations by law enforcement personnel."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#PublicIntegrityInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_evidence_integrity: Optional[float] = field(default=None)
    has_investigation_complexity: Optional[str] = field(default=None)


@dataclass
class UniformBasedExploitation:
    """Exploitation activity conducted while wearing official law enforcement or military uniform for authority enhancement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#UniformBasedExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)


@dataclass
class UniformEnhancedProduction:
    """Production of CSAM enhanced by wearing official uniform to project authority."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#UniformEnhancedProduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    corruption_duration: list[int] = field(default_factory=list)
    has_corruption_impact: Optional[str] = field(default=None)
    has_corruption_severity: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    has_victim_vulnerability: Optional[float] = field(default=None)
    is_detected_by: Optional[InsiderThreatDetection] = field(default=None)
    victim_count: list[int] = field(default_factory=list)
    has_detection_difficulty: Optional[str] = field(default=None)
    has_authority_enhancement_level: Optional[str] = field(default=None)
    uniform_displayed: Optional[bool] = field(default=None)
    uniform_type: Optional[str] = field(default=None)


@dataclass
class WhistleblowerReport:
    """Report by insider regarding corruption within law enforcement organization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/law-enforcement-corruption#WhistleblowerReport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_evidence_integrity: Optional[float] = field(default=None)
    has_investigation_complexity: Optional[str] = field(default=None)

