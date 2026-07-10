"""CAC Ontology - Crimes Against Children — cacontology-legal-harmonization module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AdvocacyProcess:
    """Process used in legislative advocacy."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#AdvocacyProcess"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class AgeVerificationLaw:
    """Laws requiring age verification for online services."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#AgeVerificationLaw"
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
class AmendmentProcess:
    """Process of amending legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#AmendmentProcess"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    process_date: Optional[date] = field(default=None)
    process_status: Optional[str] = field(default=None)


@dataclass
class AnnualReview:
    """Annual compliance review process."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#AnnualReview"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class AuditProcess:
    """Audit for compliance verification."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#AuditProcess"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class BestPractice:
    """Best practice in child protection legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#BestPractice"
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
class BillDrafting:
    """Process of drafting legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#BillDrafting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    process_date: Optional[date] = field(default=None)
    process_status: Optional[str] = field(default=None)


@dataclass
class BillSponsor:
    """Legislator who introduces or sponsors legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#BillSponsor"
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
class CSAMCriminalization:
    """Legislation criminalizing child sexual abuse material."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CSAMCriminalization"
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
class CSAMModelLaw:
    """Model legislation for Child Sexual Abuse Material regulations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CSAMModelLaw"
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
    has_data_quality: Optional[str] = field(default=None)
    has_legal_effectiveness: Optional[str] = field(default=None)
    legal_system_type: Optional[str] = field(default=None)


@dataclass
class CapacityBuilding:
    """Building legal capacity for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CapacityBuilding"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CertificationProcess:
    """Process for obtaining compliance certification."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CertificationProcess"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ChildExploitationLaw:
    """Laws addressing child exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ChildExploitationLaw"
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
class ChildTraffickingLaw:
    """Legislation addressing child trafficking crimes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ChildTraffickingLaw"
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
class CoalitionBuilding:
    """Building coalitions to support advocacy goals."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CoalitionBuilding"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CommitteeMember:
    """Member of a legislative committee."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CommitteeMember"
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
class CommitteeReview:
    """Review of legislation by a committee."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#CommitteeReview"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    process_date: Optional[date] = field(default=None)
    process_status: Optional[str] = field(default=None)


@dataclass
class ComplianceBenchmark:
    """Benchmark for measuring legal compliance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ComplianceBenchmark"
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
class ComplianceDocumentationArtifact:
    """Documentation artifact (record/report/audit trail element) used to prove appropriate action to regulators and support claims of good-faith compliance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ComplianceDocumentationArtifact"
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
    verification_status: Optional[str] = field(default=None)


@dataclass
class ComplianceIntelligenceFramework:
    """A verified compliance intelligence framework used to document good-faith content moderation and reporting efforts (beyond simple detection) and support risk-stratified operational decisions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ComplianceIntelligenceFramework"
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
class ComplianceMetrics:
    """Metrics for measuring legal compliance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ComplianceMetrics"
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
    has_data_quality: Optional[str] = field(default=None)


@dataclass
class ComplianceProcess:
    """Process for ensuring legal compliance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ComplianceProcess"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class Correspondence:
    """Communication between actors regarding legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#Correspondence"
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
    corresponds_about: list[LegislativeInstrument] = field(default_factory=list)


@dataclass
class DataProtectionForMinorsLaw:
    """Laws protecting children's personal data."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#DataProtectionForMinorsLaw"
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
class ExtraditionAgreement:
    """Agreement enabling extradition for child protection crimes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ExtraditionAgreement"
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
    label: list[str] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class FloorVote:
    """Vote on legislation by the full legislative body."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#FloorVote"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    process_date: Optional[date] = field(default=None)
    process_status: Optional[str] = field(default=None)


@dataclass
class GlobalLegalReview:
    """Comprehensive review of child protection legislation across countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#GlobalLegalReview"
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
    countries_analyzed: Optional[int] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class GrantCompliance:
    """Compliance with grant requirements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#GrantCompliance"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class GrassrootsAdvocacy:
    """Mobilizing public support for advocacy goals."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#GrassrootsAdvocacy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class HarmonizationInitiative:
    """Organized effort to harmonize laws across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#HarmonizationInitiative"
    label: list[str] = field(default_factory=list)


@dataclass
class HarmonizationProgress:
    """Progress measurement for policy harmonization."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#HarmonizationProgress"
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
class ImpactAssessment:
    """Assessing the impact of proposed legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ImpactAssessment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class InternationalLawEnforcement:
    """Law enforcement cooperation across international boundaries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#InternationalLawEnforcement"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_cooperation_intensity: Optional[str] = field(default=None)


@dataclass
class InternationalStandard:
    """International standard for child protection legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#InternationalStandard"
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
class JurisdictionalCoordination:
    """Framework for coordinating across legal jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#JurisdictionalCoordination"
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
class JurisdictionalVariation:
    """Variation in legal approaches across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#JurisdictionalVariation"
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
class KnowingParadox:
    """A policy incentive conflict where platforms face liability both for detecting content (creating knowledge) and for failing to detect content, discouraging proactive detection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#KnowingParadox"
    label: list[str] = field(default_factory=list)


@dataclass
class LawEnforcementOfficer:
    """Officer involved in child safety investigations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LawEnforcementOfficer"
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
class LegalCompliance:
    """Situation of compliance with international standards."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegalCompliance"
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
    has_compliance_level: Optional[float] = field(default=None)
    legal_alignment_level: Optional[str] = field(default=None)
    measured_by: list[ComplianceMetrics] = field(default_factory=list)


@dataclass
class LegalCoverageAssessment:
    """Assessment of legal coverage for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegalCoverageAssessment"
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
class LegalEffectiveness:
    """Assessment of legal framework effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegalEffectiveness"
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
class LegalFrameworkGap:
    """Identified gap in legal framework coverage."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegalFrameworkGap"
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
    has_gap_severity: Optional[str] = field(default=None)
    policy_gap_severity: Optional[str] = field(default=None)
    requires_reform: list[LegalReform] = field(default_factory=list)


@dataclass
class LegalReform:
    """Process of reforming child protection legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegalReform"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_reform_urgency: Optional[str] = field(default=None)
    reform_priority: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)


@dataclass
class LegalSystemCompatibility:
    """Compatibility situation between different legal systems."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegalSystemCompatibility"
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


@dataclass
class LegislativeAdvocate:
    """Person who advocates for legislative change."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeAdvocate"
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
class LegislativeAssessment:
    """Assessment of existing child protection legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeAssessment"
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
    has_assessment_reliability: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    legislative_compliance: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class LegislativeDrafting:
    """Process of drafting child protection legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeDrafting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class LegislativeEducation:
    """Educating legislators on issues."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeEducation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class LegislativeInstrument:
    """A bill, resolution, or other legislative document."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeInstrument"
    involves_process: list[LegislativeProcess] = field(default_factory=list)
    name: list[str] = field(default_factory=list)


@dataclass
class LegislativeProcess:
    """A step in the legislative lifecycle - applicable across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeProcess"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    process_date: Optional[date] = field(default=None)
    process_status: Optional[str] = field(default=None)


@dataclass
class LegislativeRole:
    """Role an actor plays in the legislative ecosystem."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#LegislativeRole"
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
class Legislator:
    """Elected member of a legislative body."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#Legislator"
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
class MandatoryReporting:
    """Required reporting to authorities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#MandatoryReporting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class MandatoryReportingLaw:
    """Legislation requiring mandatory reporting of child abuse."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#MandatoryReportingLaw"
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
class MediaOutreach:
    """Engaging media to support advocacy goals."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#MediaOutreach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class MinimumStandard:
    """Minimum standard for child protection laws."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#MinimumStandard"
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
class MutualLegalAssistance:
    """Framework for mutual legal assistance between countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#MutualLegalAssistance"
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
class NationalLegislation:
    """National child protection legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#NationalLegislation"
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
    label: list[str] = field(default_factory=list)
    applies_to_country: Optional[Location] = field(default=None)
    has_implementation_quality: Optional[str] = field(default=None)
    has_legal_effectiveness: Optional[str] = field(default=None)
    has_legal_robustness: Optional[str] = field(default=None)
    implementation_status: Optional[str] = field(default=None)
    legal_system_type: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class OnlineGroomingLaw:
    """Legislation addressing online grooming behaviors."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#OnlineGroomingLaw"
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
class OnlineSafetyLaw:
    """General laws addressing online child safety."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#OnlineSafetyLaw"
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
class PlatformAccountabilityLaw:
    """Laws holding online platforms accountable for child safety."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#PlatformAccountabilityLaw"
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
class PolicyAnalyst:
    """Person who analyzes and develops policy recommendations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#PolicyAnalyst"
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
class PolicyDevelopment:
    """Development of child protection policies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#PolicyDevelopment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class PolicyHarmonization:
    """Process of harmonizing policies across jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#PolicyHarmonization"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_harmonization_degree: Optional[str] = field(default=None)


@dataclass
class ProsecutorAdvocate:
    """Prosecutor who advocates for stronger laws."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#ProsecutorAdvocate"
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
class PublicHearing:
    """Public hearing on proposed legislation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#PublicHearing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    process_date: Optional[date] = field(default=None)
    process_status: Optional[str] = field(default=None)


@dataclass
class RegionalFramework:
    """Regional legal framework for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#RegionalFramework"
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
class SafeHarbor:
    """A statutory or regulatory safe harbor provision intended to distinguish good-faith compliance efforts from negligence (e.g., incentives for verified compliance intelligence frameworks)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#SafeHarbor"
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
    good_faith_criteria: Optional[str] = field(default=None)
    supported_by_framework: list[ComplianceIntelligenceFramework] = field(default_factory=list)


@dataclass
class SextortionLaw:
    """Laws addressing sextortion of children."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#SextortionLaw"
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
class StakeholderEngagement:
    """Engaging stakeholders in advocacy efforts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#StakeholderEngagement"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class Statute:
    """Enacted law within a jurisdiction."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#Statute"
    name: list[str] = field(default_factory=list)


@dataclass
class StatutoryReporting:
    """Reporting required by statute."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#StatutoryReporting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class TaskForceLiaison:
    """Person who coordinates between task forces and other entities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#TaskForceLiaison"
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
class TechnicalAssistance:
    """Technical assistance for legal framework development."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#TechnicalAssistance"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class TestimonySubmission:
    """Submitting testimony to legislative bodies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#TestimonySubmission"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class TreatyFramework:
    """International treaty framework for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#TreatyFramework"
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
    label: list[str] = field(default_factory=list)
    applies_to_country: list[Location] = field(default_factory=list)
    facilitates_cooperation: list[InternationalLawEnforcement] = field(default_factory=list)
    has_treaty_strength: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class VictimAdvocate:
    """Person who advocates on behalf of crime victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#VictimAdvocate"
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
class VictimProtectionLaw:
    """Legislation protecting child victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/legal-harmonization#VictimProtectionLaw"
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

