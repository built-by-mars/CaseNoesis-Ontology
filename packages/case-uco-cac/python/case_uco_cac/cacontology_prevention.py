"""CAC Ontology - Crimes Against Children — cacontology-prevention module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AffiliateCoordination:
    """Coordination activities between CAC affiliate organizations for unified prevention efforts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#AffiliateCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class AffiliateResourceSharing:
    """Coordinated sharing of educational resources and prevention materials among CAC affiliates."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#AffiliateResourceSharing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class AgeTargetedEducation:
    """Education programs targeted to specific age groups."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#AgeTargetedEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ArchivePublicationSystem:
    """Knowledge repository system providing access to archived educational publications and historical safety information."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ArchivePublicationSystem"
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
class BehavioralPrevention:
    """Prevention strategies focused on behavioral changes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#BehavioralPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class BullyingPrevention:
    """Prevention programs focused on reducing bullying and shaming."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#BullyingPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ChildAbusePreventionMonth:
    """National Child Abuse Prevention Month coordinated awareness activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ChildAbusePreventionMonth"


@dataclass
class ChildSafetyEducation:
    """Education programs teaching children about safety."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ChildSafetyEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class CommunityEducation:
    """Education programs for community members."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class CommunityEducator:
    """Educator working in community prevention programs."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityEducator"
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
class CommunityEmailList:
    """Organized email communication system for ongoing safety updates to parents and community members."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityEmailList"
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
class CommunityEngagement:
    """Measurement of community engagement in prevention."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityEngagement"
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
    created_time: Optional[datetime] = field(default=None)
    community_participation: Optional[float] = field(default=None)


@dataclass
class CommunityEngagementMetrics:
    """Comprehensive metrics for measuring community engagement across multiple communication channels."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityEngagementMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class CommunityNewsletterSystem:
    """Regular newsletter communication system for ongoing community engagement and safety updates."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityNewsletterSystem"
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
class CommunityOutreach:
    """Outreach programs to engage communities in child protection. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityOutreach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class CommunityOutreachEffectiveness:
    """Measurement of community outreach program effectiveness in generating victim disclosures and arrests."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityOutreachEffectiveness"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class CommunityPartnershipInitiative:
    """Initiative building partnerships with community organizations for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CommunityPartnershipInitiative"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class CourseCompletionTracking:
    """System for tracking participant progress and completion rates in interactive safety courses."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#CourseCompletionTracking"
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
class DigitalLiteracy:
    """Education on digital literacy and safe technology use."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#DigitalLiteracy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class DigitalSafety:
    """Prevention programs focused on digital safety."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#DigitalSafety"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class DisclosureBarrierReduction:
    """Strategies to reduce barriers preventing victim disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#DisclosureBarrierReduction"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class DisclosureEncouragementStrategy:
    """Strategy for encouraging victims to disclose abuse through education and support."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#DisclosureEncouragementStrategy"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class DiscreetAccessSystem:
    """System allowing discreet access to safety information to reduce bullying and shaming."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#DiscreetAccessSystem"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class EducationPlatformIntegration:
    """Integration capabilities between different educational delivery platforms and content management systems."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EducationPlatformIntegration"
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
class EducationPortal:
    """Online portal providing educational resources for child protection. Modeled as gUFO Object."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EducationPortal"
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
    education_portal_reach: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class EducationalPosterCampaign:
    """School-based poster distribution campaign for prevention education."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EducationalPosterCampaign"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class EducationalResource:
    """Resource designed for educational purposes in child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EducationalResource"
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
    language_availability: list[str] = field(default_factory=list)
    target_audience: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class EducatorTraining:
    """Training programs specifically designed for educators."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EducatorTraining"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class EmailListEngagementMetrics:
    """Metrics tracking email list subscription rates, open rates, and engagement patterns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EmailListEngagementMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class EnvironmentalPrevention:
    """Prevention strategies focused on environmental factors."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#EnvironmentalPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class FAQKnowledgeBase:
    """Structured question and answer system for Internet Crimes Against Children frequently asked questions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#FAQKnowledgeBase"
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
class FAQUsageMetrics:
    """Metrics tracking FAQ access patterns, most searched questions, and help-seeking behaviors."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#FAQUsageMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class HealthcareProviderTraining:
    """Training for healthcare providers on child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#HealthcareProviderTraining"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ICACAffiliateNetwork:
    """Network of formally affiliated CAC organizations for coordinated child protection efforts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ICACAffiliateNetwork"
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
class InformationPoster:
    """Physical poster containing educational information and QR codes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#InformationPoster"
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
    language_availability: list[str] = field(default_factory=list)
    target_audience: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InteractiveCourseMetrics:
    """Metrics tracking course enrollment, completion rates, and learning effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#InteractiveCourseMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InteractiveCourseSystem:
    """Interactive online safety course platform with progression tracking and engagement features."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#InteractiveCourseSystem"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MultimediaEducationContent:
    """Educational content incorporating multiple media types including audio, video, and interactive elements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#MultimediaEducationContent"
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
    language_availability: list[str] = field(default_factory=list)
    target_audience: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class NationwideAwarenessInitiative:
    """Nationwide coordinated awareness campaign involving multiple agencies and communities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#NationwideAwarenessInitiative"


@dataclass
class OnlineSafetyEducation:
    """Education about staying safe online."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#OnlineSafetyEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class OutreachTriggeredInvestigation:
    """Investigation initiated as direct result of community outreach presentation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#OutreachTriggeredInvestigation"
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
class ParentCommunityEmailList:
    """Specialized email list for parent and community safety updates and archived publication access."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ParentCommunityEmailList"
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
class ParentEducation:
    """Education programs for parents and caregivers."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ParentEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ParentalControl:
    """Technology tools for parental oversight."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ParentalControl"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class ParentalVigilanceProgram:
    """Program educating parents on recognizing signs of child exploitation and reporting."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#ParentalVigilanceProgram"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class PlatformSafety:
    """Safety measures implemented by technology platforms."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PlatformSafety"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PodcastEducationSeries:
    """Audio-based educational content delivery system, such as the Protect Kids Online (PKO) Podcast."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PodcastEducationSeries"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class PodcastEngagementMetrics:
    """Metrics tracking podcast download rates, completion rates, and listener engagement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PodcastEngagementMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PostPresentationDisclosure:
    """Victim disclosure that occurs following a safety presentation or educational event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PostPresentationDisclosure"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class PosterDistributionMetrics:
    """Metrics tracking poster distribution and reach."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PosterDistributionMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PreventionAdvocate:
    """Advocate promoting prevention initiatives."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionAdvocate"
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
class PreventionCurriculum:
    """Structured curriculum for prevention education."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionCurriculum"
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
class PreventionEffectiveness:
    """Assessment of prevention program effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionEffectiveness"
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
    created_time: Optional[datetime] = field(default=None)
    prevention_effectiveness: Optional[float] = field(default=None)


@dataclass
class PreventionMaterial:
    """Educational material focused on prevention strategies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionMaterial"
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
    language_availability: list[str] = field(default_factory=list)
    target_audience: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PreventionMetrics:
    """Metrics for measuring prevention program effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PreventionProgram:
    """Structured program designed to prevent child abuse and exploitation. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionProgram"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class PreventionSpecialist:
    """Professional specializing in prevention programs."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PreventionSpecialist"
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
class PrimaryPrevention:
    """Prevention strategies that stop abuse before it occurs."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PrimaryPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class PublicAwareness:
    """Campaigns to raise public awareness about child protection. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#PublicAwareness"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class QRCodeEngagementMetrics:
    """Metrics tracking QR code usage and engagement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#QRCodeEngagementMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class QRCodeIntegration:
    """QR code system for discreet access to prevention information."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#QRCodeIntegration"
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
class RapidResponseDisclosureWorkflow:
    """Workflow enabling rapid response from victim disclosure to arrest (e.g., 8-hour timeline)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#RapidResponseDisclosureWorkflow"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class RiskAssessmentTool:
    """Tool for assessing risks to child safety."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#RiskAssessmentTool"
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
class RiskPrevention:
    """Programs focused on preventing risk factors for child abuse. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#RiskPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class RiskReduction:
    """Measurement of risk reduction achieved."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#RiskReduction"
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
    created_time: Optional[datetime] = field(default=None)
    risk_reduction_level: Optional[float] = field(default=None)


@dataclass
class SafeDisclosureEnvironment:
    """Creation of safe environment where victims feel comfortable disclosing abuse."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SafeDisclosureEnvironment"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class SafetyCoordinator:
    """Coordinator responsible for safety programs."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SafetyCoordinator"
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
class SafetyGuideline:
    """Guidelines for maintaining child safety."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SafetyGuideline"
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
    language_availability: list[str] = field(default_factory=list)
    target_audience: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class SafetyProtocol:
    """Protocol designed to ensure child safety in various settings."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SafetyProtocol"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class SchoolAllegationProtocol:
    """Protocol for managing allegations of abuse in school settings. Modeled as gUFO Object."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SchoolAllegationProtocol"
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
class SchoolCounselorTraining:
    """Training program for school counselors."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SchoolCounselorTraining"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SchoolDistribution:
    """Distribution of educational materials to schools."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SchoolDistribution"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class SchoolPolicy:
    """Policy governing child protection in schools."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SchoolPolicy"
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
class SchoolPresentationProgram:
    """FBI school presentation program for child safety education and disclosure encouragement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SchoolPresentationProgram"


@dataclass
class SchoolSafetyProgram:
    """Safety program implemented in school settings."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SchoolSafetyProgram"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SecondaryPrevention:
    """Early intervention strategies to prevent escalation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SecondaryPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SextortionAwareness:
    """Prevention program focused on sextortion education and awareness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SextortionAwareness"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SextortionEducation:
    """Educational content specifically addressing sextortion risks and prevention."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SextortionEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SextortionResponse:
    """Response protocol for sextortion incidents."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SextortionResponse"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class SextortionWarningSign:
    """Identifiable warning signs of sextortion activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#SextortionWarningSign"
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
class StatewideCampaignMetrics:
    """Metrics for measuring statewide prevention campaign effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#StatewideCampaignMetrics"
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
    created_time: Optional[datetime] = field(default=None)


@dataclass
class StudentEducation:
    """Safety education program for students."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#StudentEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TeacherTraining:
    """Training program specifically for teachers."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#TeacherTraining"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TertiaryPrevention:
    """Prevention of re-victimization and recurrence."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#TertiaryPrevention"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    participant_count: Optional[int] = field(default=None)
    program_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TrustedAdultIdentification:
    """Education helping children identify trusted adults for disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#TrustedAdultIdentification"
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
    implementation_status: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class TwelvePlusEducation:
    """Safety education targeted specifically for students 12 years and older."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#TwelvePlusEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    age_group: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class VictimDisclosureTriggering:
    """Safety education event that triggers victim disclosure of ongoing abuse."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/prevention#VictimDisclosureTriggering"

