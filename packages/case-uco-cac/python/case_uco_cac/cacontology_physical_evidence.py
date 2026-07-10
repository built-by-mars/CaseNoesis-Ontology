"""CAC Ontology - Crimes Against Children — cacontology-physical-evidence module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AbuseFacilitationItem:
    """Physical items intended for use in facilitating child abuse or exploitation (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#AbuseFacilitationItem"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class BodycamFootage:
    """Body camera footage from law enforcement officers. Used for suspect identification and evidence. IS a digital observable as it is a digital recording."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#BodycamFootage"
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
    label: Optional[langString] = field(default=None)
    matches_selfie: Optional[bool] = field(default=None)
    recording_date: Optional[datetime] = field(default=None)
    used_for_identification: Optional[bool] = field(default=None)


@dataclass
class CellphoneSearch:
    """Search of cellphone or mobile device for evidence. Typically requires consent or warrant (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#CellphoneSearch"
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
    has_search_completeness: Optional[float] = field(default=None)
    has_search_efficiency: Optional[float] = field(default=None)
    has_search_thoroughness: Optional[str] = field(default=None)
    search_duration: Optional[float] = field(default=None)
    search_scope: Optional[str] = field(default=None)


@dataclass
class ChainOfCustodyBreachSituation:
    """Situation where the chain of custody for evidence has been breached (gUFO Situation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ChainOfCustodyBreachSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class ChildTargetedItem:
    """Items specifically designed to appeal to or attract children (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ChildTargetedItem"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class CommunicationDevice:
    """Devices used to communicate with victims or distribute illegal content (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#CommunicationDevice"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)
    device_brand: Optional[str] = field(default=None)
    device_model: Optional[str] = field(default=None)
    encryption_status: Optional[str] = field(default=None)
    functional_status: Optional[str] = field(default=None)


@dataclass
class ComputerEquipment:
    """Digital devices including computers, laptops, tablets, and mobile phones seized as evidence (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ComputerEquipment"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)
    device_brand: Optional[str] = field(default=None)
    device_model: Optional[str] = field(default=None)
    encryption_status: Optional[str] = field(default=None)
    functional_status: Optional[str] = field(default=None)


@dataclass
class Condoms:
    """Contraceptive devices found as evidence corroborating intent to engage in sexual activity. Extends AbuseFacilitationItem as physical evidence (NOT a digital observable)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#Condoms"
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
    label: Optional[langString] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)
    agreed_to_bring: Optional[bool] = field(default=None)
    condom_brand: Optional[str] = field(default=None)
    condom_quantity: Optional[int] = field(default=None)
    found_in_location: Optional[str] = field(default=None)


@dataclass
class ConsentToSearchAuthorization:
    """Authorization obtained through suspect's consent to search property or devices. Extends investigation:Authorization for CASE ontology integration."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ConsentToSearchAuthorization"
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
    label: Optional[langString] = field(default=None)
    authorization_identifier: list[str] = field(default_factory=list)
    authorization_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    consent_given: Optional[bool] = field(default=None)
    consent_scope: Optional[str] = field(default=None)
    consent_type: Optional[str] = field(default=None)


@dataclass
class CriminalProcurement:
    """Action of acquiring items specifically for criminal purposes (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#CriminalProcurement"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_acquisition_risk: Optional[str] = field(default=None)
    has_procurement_suspicion: Optional[str] = field(default=None)
    has_traceability: Optional[float] = field(default=None)
    payment_method: Optional[str] = field(default=None)
    procurement_cost: Optional[float] = field(default=None)
    procurement_method: Optional[str] = field(default=None)


@dataclass
class DashcamFootage:
    """Dashboard camera footage from police vehicles. Digital observable."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#DashcamFootage"
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
    label: Optional[langString] = field(default=None)
    matches_selfie: Optional[bool] = field(default=None)
    recording_date: Optional[datetime] = field(default=None)
    used_for_identification: Optional[bool] = field(default=None)


@dataclass
class DeviceConsentSearch:
    """Consent authorization specific to electronic device search (cellphone, computer, etc.)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#DeviceConsentSearch"
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
    label: Optional[langString] = field(default=None)
    authorization_identifier: list[str] = field(default_factory=list)
    authorization_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    consent_given: Optional[bool] = field(default=None)
    consent_scope: Optional[str] = field(default=None)
    consent_type: Optional[str] = field(default=None)


@dataclass
class DisguiseItem:
    """Items used to conceal identity or change appearance (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#DisguiseItem"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class DocumentaryEvidence:
    """Physical documents, printed materials, or written items relevant to the investigation (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#DocumentaryEvidence"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class EvidenceAnalysisPhase:
    """Phase during which physical evidence is undergoing forensic analysis (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceAnalysisPhase"
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
class EvidenceCollectionAction:
    """Action of collecting and documenting physical evidence during search. Extends investigation:InvestigativeAction (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceCollectionAction"
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


@dataclass
class EvidenceCollectionPhase:
    """Phase during which physical evidence is being collected (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceCollectionPhase"
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
class EvidenceContaminationSituation:
    """Situation where physical evidence has been contaminated or compromised (gUFO Situation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceContaminationSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class EvidenceCustodianRole:
    """Role of person responsible for evidence custody and chain of custody (gUFO Role - anti-rigid). Roles are non-rigid capacities; persons play roles via holdsRole."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceCustodianRole"
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
    has_custody_integrity: Optional[str] = field(default=None)
    has_documentation_completeness: Optional[float] = field(default=None)


@dataclass
class EvidenceDispositionPhase:
    """Phase during which evidence disposition is determined and executed (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceDispositionPhase"
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
class EvidenceRecoverySituation:
    """Situation involving the recovery of previously lost or missing evidence (gUFO Situation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceRecoverySituation"
    label: list[str] = field(default_factory=list)


@dataclass
class EvidenceSeizure:
    """Legal seizure of physical items as evidence. Extends investigation:InvestigativeAction (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceSeizure"
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


@dataclass
class EvidenceStoragePhase:
    """Phase during which physical evidence is in secure storage (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#EvidenceStoragePhase"
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
class ForensicAnalystRole:
    """Role of person conducting forensic analysis of physical evidence (gUFO Role - anti-rigid). Roles are non-rigid capacities; persons play roles via holdsRole."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ForensicAnalystRole"
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
    has_analysis_accuracy: Optional[float] = field(default=None)
    has_analysis_reliability: Optional[str] = field(default=None)
    has_method_validation: Optional[str] = field(default=None)


@dataclass
class GloveCompartmentSearch:
    """Search of vehicle glove compartment as specific evidence location (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#GloveCompartmentSearch"
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
    has_search_completeness: Optional[float] = field(default=None)
    has_search_efficiency: Optional[float] = field(default=None)
    has_search_thoroughness: Optional[str] = field(default=None)
    search_duration: Optional[float] = field(default=None)
    search_scope: Optional[str] = field(default=None)


@dataclass
class IntoxicatingSubstance:
    """Alcohol, drugs, or other intoxicating substances intended to impair victim judgment. Extends AbuseFacilitationItem."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#IntoxicatingSubstance"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class ItemModification:
    """Alteration or customization of items to facilitate criminal activity (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ItemModification"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class OnlinePurchase:
    """Purchase of items through online platforms for criminal purposes (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#OnlinePurchase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_acquisition_risk: Optional[str] = field(default=None)
    has_procurement_suspicion: Optional[str] = field(default=None)
    has_traceability: Optional[float] = field(default=None)
    payment_method: Optional[str] = field(default=None)
    procurement_cost: Optional[float] = field(default=None)
    procurement_method: Optional[str] = field(default=None)


@dataclass
class PersonalItem:
    """Personal belongings that may contain evidence or indicate criminal behavior (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#PersonalItem"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class PhysicalEvidence:
    """Tangible items collected as evidence in CAC investigations (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#PhysicalEvidence"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class PhysicalEvidenceProvenanceRecord:
    """Provenance record tracking chain of custody and handling of physical evidence. Extends investigation:ProvenanceRecord for CASE ontology integration."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#PhysicalEvidenceProvenanceRecord"
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
    object: list[UcoObject] = field(default_factory=list)
    exhibit_number: Optional[str] = field(default=None)
    root_exhibit_number: list[str] = field(default_factory=list)


@dataclass
class PhysicalPurchase:
    """In-person purchase of items for criminal purposes (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#PhysicalPurchase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_acquisition_risk: Optional[str] = field(default=None)
    has_procurement_suspicion: Optional[str] = field(default=None)
    has_traceability: Optional[float] = field(default=None)
    payment_method: Optional[str] = field(default=None)
    procurement_cost: Optional[float] = field(default=None)
    procurement_method: Optional[str] = field(default=None)


@dataclass
class PhysicalSearch:
    """Law enforcement search of physical premises for evidence. Extends investigation:InvestigativeAction for CASE ontology integration (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#PhysicalSearch"
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
    has_search_completeness: Optional[float] = field(default=None)
    has_search_efficiency: Optional[float] = field(default=None)
    has_search_thoroughness: Optional[str] = field(default=None)
    search_duration: Optional[float] = field(default=None)
    search_scope: Optional[str] = field(default=None)


@dataclass
class RecordingEquipment:
    """Devices used to create audio or video recordings of criminal activity (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#RecordingEquipment"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class ResidenceSearch:
    """Search of residential premises including homes and apartments (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#ResidenceSearch"
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
    has_search_completeness: Optional[float] = field(default=None)
    has_search_efficiency: Optional[float] = field(default=None)
    has_search_thoroughness: Optional[str] = field(default=None)
    search_duration: Optional[float] = field(default=None)
    search_scope: Optional[str] = field(default=None)


@dataclass
class RestraintItem:
    """Items intended for restraining or controlling victims (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#RestraintItem"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class SearchOfficerRole:
    """Role of law enforcement officer conducting physical searches (gUFO Role - anti-rigid). Roles are non-rigid capacities; persons play roles via holdsRole."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#SearchOfficerRole"
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
class StorageMedia:
    """External storage devices including hard drives, USB drives, memory cards, and optical media (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#StorageMedia"
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
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)


@dataclass
class SurveillanceRecording:
    """Recording from surveillance or security cameras. Digital observable."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#SurveillanceRecording"
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
class SuspectVehicle:
    """Vehicle registered to or used by suspect in CAC offense. Used for evidence tracking when suspect travels to meet alleged minor. Physical evidence item."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#SuspectVehicle"
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
    label: Optional[langString] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)
    registered_to_suspect: Optional[bool] = field(default=None)
    used_in_offense: Optional[bool] = field(default=None)
    vehicle_color: Optional[str] = field(default=None)
    vehicle_license_plate: Optional[str] = field(default=None)
    vehicle_make: Optional[str] = field(default=None)
    vehicle_model: Optional[str] = field(default=None)
    vehicle_vin: Optional[str] = field(default=None)
    vehicle_year: Optional[int] = field(default=None)


@dataclass
class VapeDevice:
    """Electronic vaporizer or e-cigarette found as evidence. Often brought to lure or facilitate abuse of minors. Extends AbuseFacilitationItem as physical evidence (NOT a digital observable)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#VapeDevice"
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
    label: Optional[langString] = field(default=None)
    comment: Optional[str] = field(default=None)
    collection_date: Optional[datetime] = field(default=None)
    collection_location: Optional[str] = field(default=None)
    evidence_category: Optional[str] = field(default=None)
    evidence_condition: Optional[str] = field(default=None)
    evidence_number: Optional[str] = field(default=None)
    evidence_status: Optional[str] = field(default=None)
    evidence_type: Optional[str] = field(default=None)
    has_contamination_level: Optional[float] = field(default=None)
    has_evidence_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_end_point: Optional[dateTimeStamp] = field(default=None)
    has_evidence_integrity: Optional[str] = field(default=None)
    has_evidence_reliability: Optional[float] = field(default=None)
    has_forensic_value: Optional[str] = field(default=None)
    has_preservation_quality: Optional[str] = field(default=None)
    agreed_to_bring: Optional[bool] = field(default=None)
    found_in_location: Optional[str] = field(default=None)
    vape_brand: Optional[str] = field(default=None)
    vape_flavor: Optional[str] = field(default=None)


@dataclass
class VehicleConsentSearch:
    """Consent authorization specific to vehicle search."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#VehicleConsentSearch"
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
    label: Optional[langString] = field(default=None)
    authorization_identifier: list[str] = field(default_factory=list)
    authorization_type: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    consent_given: Optional[bool] = field(default=None)
    consent_scope: Optional[str] = field(default=None)
    consent_type: Optional[str] = field(default=None)


@dataclass
class VehicleSearch:
    """Search of motor vehicles for evidence or contraband. May be conducted with consent or warrant (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#VehicleSearch"
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
    has_search_completeness: Optional[float] = field(default=None)
    has_search_efficiency: Optional[float] = field(default=None)
    has_search_thoroughness: Optional[str] = field(default=None)
    search_duration: Optional[float] = field(default=None)
    search_scope: Optional[str] = field(default=None)


@dataclass
class WorkplaceSearch:
    """Search of workplace or commercial premises (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/physical#WorkplaceSearch"
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
    has_search_completeness: Optional[float] = field(default=None)
    has_search_efficiency: Optional[float] = field(default=None)
    has_search_thoroughness: Optional[str] = field(default=None)
    search_duration: Optional[float] = field(default=None)
    search_scope: Optional[str] = field(default=None)

