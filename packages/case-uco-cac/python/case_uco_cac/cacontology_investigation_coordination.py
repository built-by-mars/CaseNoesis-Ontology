"""CAC Ontology - Crimes Against Children — cacontology-investigation-coordination module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaseInformationSharing:
    """Sharing of case-specific information including case files, reports, witness statements, and investigative findings."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CaseInformationSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class CaseResolutionTimeMetrics:
    """Metrics measuring impact of coordination on case resolution times and outcomes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CaseResolutionTimeMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class CommunicationProtocol:
    """Formal protocols governing communication between agencies including channels, frequencies, and procedures."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CommunicationProtocol"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class CoordinationAgreement:
    """Formal agreements governing coordination between agencies including MOUs, MOAs, and operational agreements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CoordinationAgreement"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class CoordinationEffectivenessMetrics:
    """Metrics measuring overall effectiveness of coordination efforts and outcomes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CoordinationEffectivenessMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class CoordinationMetrics:
    """Performance metrics for measuring effectiveness and efficiency of inter-agency coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CoordinationMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class CostEfficiencyMetrics:
    """Metrics measuring cost efficiency and financial benefits of coordination activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#CostEfficiencyMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class EmergencyCommunicationChannel:
    """Emergency communication channels for urgent coordination and crisis response."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#EmergencyCommunicationChannel"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class EncryptedCommunicationChannel:
    """Encrypted communication channels providing enhanced security for sensitive operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#EncryptedCommunicationChannel"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class EquipmentSharing:
    """Sharing of specialized equipment including forensic tools, surveillance equipment, and technical devices."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#EquipmentSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class EvidenceSharing:
    """Formal sharing of evidence between agencies including digital evidence, physical evidence, and forensic analysis results."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#EvidenceSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class ExpertiseSharing:
    """Sharing of specialized expertise including subject matter experts, consultants, and technical specialists."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#ExpertiseSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class FacilitySharing:
    """Sharing of facilities including laboratories, command centers, training facilities, and secure meeting spaces."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#FacilitySharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class FederalCoordination:
    """Coordination involving federal agencies and national-level law enforcement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#FederalCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class FormalAgreement:
    """Comprehensive formal agreement with legal binding terms for inter-agency coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#FormalAgreement"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class FormalCommunicationChannel:
    """Official communication channels following established protocols and hierarchies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#FormalCommunicationChannel"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class FundingSharing:
    """Coordinated funding arrangements including cost sharing, joint funding, and resource pooling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#FundingSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class InformalAgreement:
    """Informal agreement or understanding for coordination without formal legal binding."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#InformalAgreement"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InformalCommunicationChannel:
    """Informal communication channels for rapid information exchange and coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#InformalCommunicationChannel"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class InformationSharing:
    """Systematic sharing of information between agencies including intelligence, evidence, case data, and technical information."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#InformationSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class InformationSharingRateMetrics:
    """Metrics measuring the rate and volume of information sharing between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#InformationSharingRateMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class IntelligenceLiaison:
    """Intelligence liaison officer managing intelligence sharing and coordination activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#IntelligenceLiaison"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class IntelligenceSharing:
    """Specialized sharing of intelligence information including tactical, strategic, operational, and threat assessment data."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#IntelligenceSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    has_actionability: Optional[float] = field(default=None)
    has_intelligence_value: Optional[str] = field(default=None)
    information_accuracy: Optional[str] = field(default=None)
    intelligence_type: Optional[str] = field(default=None)
    source_reliability: Optional[str] = field(default=None)


@dataclass
class InternationalCoordination:
    """Coordination activities involving international agencies and cross-border cooperation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#InternationalCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class InvestigationCoordination:
    """Comprehensive framework for coordinating investigations across multiple agencies, jurisdictions, and organizational boundaries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#InvestigationCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class JointInvestigation:
    """Formal joint investigation involving multiple agencies working together with shared resources, command structure, and unified reporting."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#JointInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    has_coordination_intensity: Optional[str] = field(default=None)
    has_unification_level: Optional[float] = field(default=None)
    investigation_scope: Optional[str] = field(default=None)
    resource_pooling: Optional[bool] = field(default=None)
    shared_command: Optional[bool] = field(default=None)
    unified_reporting: Optional[bool] = field(default=None)


@dataclass
class JointOperationsPlan:
    """Detailed operational plan for joint investigations and coordinated activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#JointOperationsPlan"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class LegalLiaison:
    """Legal liaison officer handling legal aspects of inter-agency coordination and agreements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#LegalLiaison"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class LiaisonCommunicationChannel:
    """Communication channels managed through designated liaison officers for inter-agency coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#LiaisonCommunicationChannel"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class LiaisonOfficer:
    """Designated officer responsible for maintaining communication and coordination between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#LiaisonOfficer"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class LocalCoordination:
    """Coordination activities within local jurisdictions and municipal boundaries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#LocalCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MemorandumOfAgreement:
    """Formal MOA defining specific terms and conditions for inter-agency cooperation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#MemorandumOfAgreement"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class MemorandumOfUnderstanding:
    """Formal MOU establishing framework for ongoing cooperation and coordination between agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#MemorandumOfUnderstanding"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class MissingChildRescueOperation:
    """Time-boxed, multi-party operation focused on locating missing children/teens at risk of endangerment, exploitation, or harm, and connecting them with appropriate services and supports. Modeled as an i"""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#MissingChildRescueOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
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
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)
    cases_in_progress_count: Optional[int] = field(default=None)
    children_located_count: Optional[int] = field(default=None)


@dataclass
class MultiAgencyCoordination:
    """Coordination involving multiple law enforcement agencies at various jurisdictional levels."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#MultiAgencyCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MultiStateCoordination:
    """Coordination activities spanning multiple states requiring interstate cooperation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#MultiStateCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class OperationalLiaison:
    """Operational liaison officer coordinating operational activities and tactical coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#OperationalLiaison"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class ParallelInvestigation:
    """Parallel investigation where multiple agencies investigate related aspects independently while maintaining coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#ParallelInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class PersonnelSharing:
    """Sharing of specialized personnel including investigators, analysts, technical experts, and support staff."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#PersonnelSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    personnel_count: Optional[int] = field(default=None)
    security_clearance: Optional[str] = field(default=None)
    specialization: Optional[str] = field(default=None)


@dataclass
class PrimaryLiaison:
    """Primary liaison officer with full authority for inter-agency communication and coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#PrimaryLiaison"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class RegionalCoordination:
    """Coordination activities spanning regional areas and multiple local jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#RegionalCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ResourceSharing:
    """Systematic sharing of resources between agencies including personnel, equipment, facilities, and expertise."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#ResourceSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class ResourceUtilizationMetrics:
    """Metrics measuring efficiency of shared resource utilization and allocation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#ResourceUtilizationMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class ResponseTimeMetrics:
    """Metrics measuring response times for coordination requests and information sharing."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#ResponseTimeMetrics"
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    benchmark_comparison: Optional[str] = field(default=None)
    has_accuracy: Optional[float] = field(default=None)
    has_reliability: Optional[float] = field(default=None)
    measurement_period: Optional[str] = field(default=None)
    metric_type: Optional[str] = field(default=None)
    metric_value: Optional[float] = field(default=None)


@dataclass
class SecondaryLiaison:
    """Secondary liaison officer providing backup and specialized coordination support."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#SecondaryLiaison"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class SecureCommunicationChannel:
    """Secure communication channels for sensitive information and classified communications."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#SecureCommunicationChannel"
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
    communication_frequency: Optional[str] = field(default=None)
    escalation_procedure: Optional[bool] = field(default=None)
    protocol_type: Optional[str] = field(default=None)
    response_time_requirement: Optional[float] = field(default=None)


@dataclass
class StateCoordination:
    """Coordination activities within state boundaries involving state and local agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#StateCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SuspectInformationSharing:
    """Sharing of suspect-related information including identification, criminal history, and behavioral patterns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#SuspectInformationSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class TaskForceCharter:
    """Charter document establishing task force structure, authority, and operational parameters."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#TaskForceCharter"
    label: Optional[str] = field(default=None)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    agreement_scope: Optional[str] = field(default=None)
    agreement_type: Optional[str] = field(default=None)
    effective_date: Optional[datetime] = field(default=None)
    expiration_date: Optional[datetime] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    renewal_clause: Optional[bool] = field(default=None)
    termination_clause: Optional[bool] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class TaskForceCoordination:
    """Coordination through specialized task forces bringing together personnel from multiple agencies for specific operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#TaskForceCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    coordination_level: Optional[str] = field(default=None)
    coordination_status: Optional[str] = field(default=None)
    coordination_type: Optional[str] = field(default=None)
    has_complexity_level: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_success_rate: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    lead_agency: Optional[str] = field(default=None)
    participating_agencies: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TechnicalDataSharing:
    """Sharing of technical data including forensic tools, methodologies, and technical analysis results."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#TechnicalDataSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class TechnicalLiaison:
    """Technical liaison officer specializing in technical coordination and information sharing."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#TechnicalLiaison"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: Optional[str] = field(default=None)
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
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    comment: Optional[str] = field(default=None)
    assignment_duration: Optional[float] = field(default=None)
    clearance_level: Optional[str] = field(default=None)
    communication_authority: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_liaison_effectiveness: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_trust_level: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    liaison_role: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class TechnologySharing:
    """Sharing of technology resources including software, databases, communication systems, and analytical tools."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#TechnologySharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    availability_level: Optional[str] = field(default=None)
    cost_sharing: Optional[bool] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reimbursement: Optional[bool] = field(default=None)
    resource_type: Optional[str] = field(default=None)
    sharing_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)


@dataclass
class VictimInformationSharing:
    """Coordinated sharing of victim information while maintaining privacy and protection protocols."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/investigation-coordination#VictimInformationSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    classification_level: Optional[str] = field(default=None)
    has_data_completeness: Optional[float] = field(default=None)
    has_data_consistency: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_security_level: Optional[str] = field(default=None)
    has_sharing_efficiency: Optional[str] = field(default=None)
    has_timeliness: Optional[float] = field(default=None)
    has_validation_level: Optional[str] = field(default=None)
    reciprocity: Optional[bool] = field(default=None)
    sharing_agreement: Optional[bool] = field(default=None)
    sharing_mechanism: Optional[str] = field(default=None)
    sharing_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)

