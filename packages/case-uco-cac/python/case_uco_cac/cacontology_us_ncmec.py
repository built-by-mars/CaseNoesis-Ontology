"""CAC Ontology - Crimes Against Children — cacontology-us-ncmec module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AccountLinking:
    """Process of linking digital accounts to suspects through NCMEC tip analysis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#AccountLinking"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    analysis_confidence: Optional[str] = field(default=None)
    analysis_of: Optional[NCMECCybertipReport] = field(default=None)
    performer: Optional[Person] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    account_confidence: Optional[str] = field(default=None)
    linked_to_account: list[DigitalAccount] = field(default_factory=list)


@dataclass
class CSAMSolicitationAnnotation:
    """Annotation indicating the report is associated with solicitation of CSAM. Source: NCMEC Cybertip API Section B.1.1, reportAnnotations/csamSolicitation element."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#CSAMSolicitationAnnotation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: Optional[str] = field(default=None)
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
class ChildSexTourismIncident:
    """Incidents involving child sex tourism. Source: NCMEC Cybertip API Section B.1.1, incidentType 'Child Sex Tourism'."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#ChildSexTourismIncident"
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
    incident_code: Optional[str] = field(default=None)


@dataclass
class ChildSexTraffickingIncident:
    """Incidents involving child sex trafficking. Source: NCMEC Cybertip API Section B.1.1, incidentType 'Child Sex Trafficking'."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#ChildSexTraffickingIncident"
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
    incident_code: Optional[str] = field(default=None)


@dataclass
class ContentIdentification:
    """Identification and classification of illegal content in NCMEC tips."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#ContentIdentification"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    analysis_confidence: Optional[str] = field(default=None)
    analysis_of: Optional[NCMECCybertipReport] = field(default=None)
    performer: Optional[Person] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    identified_content: list[DigitalArtifact] = field(default_factory=list)


@dataclass
class CyberTipAnalysis:
    """Analytical processing and assessment of NCMEC CyberTip reports by law enforcement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#CyberTipAnalysis"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    analysis_confidence: Optional[str] = field(default=None)
    analysis_of: Optional[NCMECCybertipReport] = field(default=None)
    performer: Optional[Person] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class FederalReferral:
    """Referral of NCMEC tip to federal law enforcement agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#FederalReferral"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    referral_jurisdiction: Optional[str] = field(default=None)
    trigger_criteria: list[str] = field(default_factory=list)
    triggered_by: Optional[NCMECCybertipReport] = field(default=None)
    urgency_level: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class InvestigationTrigger:
    """Event or information that triggers law enforcement investigation based on NCMEC tip."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#InvestigationTrigger"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    referral_jurisdiction: Optional[str] = field(default=None)
    trigger_criteria: list[str] = field(default_factory=list)
    triggered_by: Optional[NCMECCybertipReport] = field(default=None)
    urgency_level: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class LocalLawEnforcementReferral:
    """Referral of NCMEC tip to local law enforcement agency."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#LocalLawEnforcementReferral"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    referral_jurisdiction: Optional[str] = field(default=None)
    trigger_criteria: list[str] = field(default_factory=list)
    triggered_by: Optional[NCMECCybertipReport] = field(default=None)
    urgency_level: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MinorToMinorInteractionAnnotation:
    """Annotation indicating the report is associated with an interaction between minors. Source: NCMEC Cybertip API Section B.1.1, reportAnnotations/minorToMinorInteraction element."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#MinorToMinorInteractionAnnotation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: Optional[str] = field(default=None)
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
class NCMECCybertipReport:
    """A report submitted to NCMEC's CyberTipline. This class represents the root structure of a NCMEC report as defined in the NCMEC Cybertip API documentation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#NCMECCybertipReport"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: Optional[str] = field(default=None)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    has_ncmec_incident_type: Optional[NCMECIncidentType] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class NCMECIncidentType:
    """Types of incidents as defined by NCMEC Cybertip API (Section B.1.1). This class represents the standardized incident categories used in NCMEC reporting."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#NCMECIncidentType"
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
    incident_code: Optional[str] = field(default=None)


@dataclass
class NCMECReportAnnotation:
    """Tags to describe the NCMEC report. Source: NCMEC Cybertip API Section B.1.1, reportAnnotations element."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#NCMECReportAnnotation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: Optional[str] = field(default=None)
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
class OnlineEnticementIncident:
    """Incidents involving online enticement of children for sexual acts. Source: NCMEC Cybertip API Section B.1.1, incidentType 'Online Enticement of Children for Sexual Acts'."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#OnlineEnticementIncident"
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
    incident_code: Optional[str] = field(default=None)


@dataclass
class PhoneNumberTrace:
    """Tracing of phone numbers linked to accounts in NCMEC tips."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#PhoneNumberTrace"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    analysis_confidence: Optional[str] = field(default=None)
    analysis_of: Optional[NCMECCybertipReport] = field(default=None)
    performer: Optional[Person] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    phone_verification_status: Optional[str] = field(default=None)
    traced_to_phone: Optional[PhoneNumber] = field(default=None)


@dataclass
class PlatformCooperation:
    """Cooperation from digital platforms in providing information for NCMEC tips."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#PlatformCooperation"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    cooperation_level: Optional[str] = field(default=None)
    data_provided: list[str] = field(default_factory=list)
    involves_platform: Optional[DigitalService] = field(default=None)
    platform_response_time: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PossessionIndicator:
    """Evidence or indicators suggesting possession of child sexual abuse material."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#PossessionIndicator"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    analysis_confidence: Optional[str] = field(default=None)
    analysis_of: Optional[NCMECCybertipReport] = field(default=None)
    performer: Optional[Person] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    indicator_strength: Optional[str] = field(default=None)


@dataclass
class SextortionAnnotation:
    """Annotation indicating the report is associated with sextortion. Source: NCMEC Cybertip API Section B.1.1, reportAnnotations/sextortion element."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#SextortionAnnotation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: Optional[str] = field(default=None)
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
class SpamAnnotation:
    """Annotation indicating the report is associated with spam. Source: NCMEC Cybertip API Section B.1.1, reportAnnotations/spam element."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#SpamAnnotation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: Optional[str] = field(default=None)
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
class TaskForceReferral:
    """Referral of NCMEC tip to appropriate CAC task force for investigation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#TaskForceReferral"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    referral_jurisdiction: Optional[str] = field(default=None)
    trigger_criteria: list[str] = field(default_factory=list)
    triggered_by: Optional[NCMECCybertipReport] = field(default=None)
    urgency_level: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TipEnrichment:
    """Enhancement of NCMEC tips with additional investigative information."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#TipEnrichment"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    processed_tip: Optional[NCMECCybertipReport] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    enrichment_type: list[str] = field(default_factory=list)


@dataclass
class TipPrioritization:
    """Priority assessment and ranking of NCMEC tips for investigation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#TipPrioritization"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    processed_tip: Optional[NCMECCybertipReport] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    priority_level: Optional[str] = field(default=None)


@dataclass
class TipProcessing:
    """Processing workflow for NCMEC tips from receipt to investigation referral."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#TipProcessing"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    processed_tip: Optional[NCMECCybertipReport] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TipValidation:
    """Validation and verification of information in NCMEC tips."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#TipValidation"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    processed_tip: Optional[NCMECCybertipReport] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    validation_status: Optional[str] = field(default=None)


@dataclass
class TransferDetection:
    """Detection of transfer or sharing of child sexual abuse material."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/us/ncmec#TransferDetection"
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
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    analysis_confidence: Optional[str] = field(default=None)
    analysis_of: Optional[NCMECCybertipReport] = field(default=None)
    performer: Optional[Person] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    transfer_frequency: Optional[str] = field(default=None)
    transfer_volume: Optional[float] = field(default=None)

