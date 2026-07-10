"""CAC Ontology - Crimes Against Children — cacontology-platform-infrastructure module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AccountFreezing:
    """Freezing financial accounts and cryptocurrency wallets associated with platform operations (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#AccountFreezing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    has_takedown_completeness: Optional[float] = field(default=None)
    has_takedown_effectiveness: Optional[float] = field(default=None)
    has_takedown_speed: Optional[str] = field(default=None)
    takedown_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    accounts_frozen: Optional[int] = field(default=None)


@dataclass
class AnalystRole:
    """Role of person conducting infrastructure analysis (gUFO Role - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#AnalystRole"
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
class AnonymityInfrastructure:
    """Systems providing anonymity to users and operators, including Tor integration and VPN services (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#AnonymityInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    has_anonymity_effectiveness: Optional[float] = field(default=None)
    has_obfuscation_complexity: Optional[str] = field(default=None)
    has_security_strength: Optional[str] = field(default=None)
    obfuscation_methods: list[str] = field(default_factory=list)
    anonymity_level: Optional[str] = field(default=None)


@dataclass
class ContentDeliveryNetwork:
    """CDN infrastructure used for distributing illegal content globally with high availability and performance (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#ContentDeliveryNetwork"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    bandwidth_capacity: Optional[float] = field(default=None)


@dataclass
class CryptocurrencyInfrastructure:
    """Cryptocurrency wallets, exchanges, and payment processing systems used for anonymous financial transactions (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#CryptocurrencyInfrastructure"
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
    has_financial_complexity: Optional[str] = field(default=None)
    has_financial_traceability: Optional[float] = field(default=None)
    monthly_revenue: Optional[float] = field(default=None)
    payment_methods: list[str] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)
    crypto_currency_types: list[str] = field(default_factory=list)


@dataclass
class DataMirrorCreation:
    """Creating forensic mirrors of seized infrastructure for analysis and evidence preservation (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#DataMirrorCreation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    has_takedown_completeness: Optional[float] = field(default=None)
    has_takedown_effectiveness: Optional[float] = field(default=None)
    has_takedown_speed: Optional[str] = field(default=None)
    takedown_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    data_volume_mirrored: Optional[float] = field(default=None)


@dataclass
class DatabaseInfrastructure:
    """Database systems storing user accounts, content metadata, and platform operational data (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#DatabaseInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    storage_capacity: Optional[float] = field(default=None)


@dataclass
class DomainInfrastructure:
    """Domain name system infrastructure including domain registration, DNS services, and subdomain management (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#DomainInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    domain_count: Optional[int] = field(default=None)


@dataclass
class DomainSinkholing:
    """Redirecting domain traffic to law enforcement controlled servers to gather intelligence (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#DomainSinkholing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    has_takedown_completeness: Optional[float] = field(default=None)
    has_takedown_effectiveness: Optional[float] = field(default=None)
    has_takedown_speed: Optional[str] = field(default=None)
    takedown_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    domains_sinkholed: Optional[int] = field(default=None)


@dataclass
class EncryptionInfrastructure:
    """Encryption systems protecting data transmission, storage, and user communications (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#EncryptionInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    has_anonymity_effectiveness: Optional[float] = field(default=None)
    has_obfuscation_complexity: Optional[str] = field(default=None)
    has_security_strength: Optional[str] = field(default=None)
    obfuscation_methods: list[str] = field(default_factory=list)
    encryption_strength: Optional[str] = field(default=None)


@dataclass
class FinancialFlowAnalysis:
    """Analysis of financial transactions and payment flows through platform monetization systems (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#FinancialFlowAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)
    has_analysis_accuracy: Optional[float] = field(default=None)
    has_analysis_depth: Optional[str] = field(default=None)
    has_analysis_timeliness: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    financial_complexity: Optional[str] = field(default=None)


@dataclass
class FinancialObfuscation:
    """Methods used to obscure financial transactions and payment flows to avoid detection (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#FinancialObfuscation"
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
    has_financial_complexity: Optional[str] = field(default=None)
    has_financial_traceability: Optional[float] = field(default=None)
    monthly_revenue: Optional[float] = field(default=None)
    payment_methods: list[str] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class GeographicDistribution:
    """Geographic distribution of infrastructure across multiple countries to complicate law enforcement efforts (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#GeographicDistribution"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    geographic_locations: Optional[int] = field(default=None)


@dataclass
class HostingProvider:
    """Organizations providing server hosting, cloud services, or infrastructure-as-a-service for platforms (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#HostingProvider"
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
    hosting_provider: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InfrastructureAnalysis:
    """Analysis of seized infrastructure to understand platform operations and identify additional targets (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)
    has_analysis_accuracy: Optional[float] = field(default=None)
    has_analysis_depth: Optional[str] = field(default=None)
    has_analysis_timeliness: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class InfrastructureCompromiseSituation:
    """Situation where platform infrastructure has been compromised or breached (gUFO Situation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureCompromiseSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class InfrastructureDecommissionPhase:
    """Phase during which infrastructure is being decommissioned or shut down (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureDecommissionPhase"
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
class InfrastructureDeploymentPhase:
    """Phase during which platform infrastructure is being deployed and configured (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureDeploymentPhase"
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
class InfrastructureDiscoverySituation:
    """Situation involving the discovery of previously unknown infrastructure components (gUFO Situation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureDiscoverySituation"
    label: list[str] = field(default_factory=list)


@dataclass
class InfrastructureFailureSituation:
    """Situation involving infrastructure failure or outage (gUFO Situation)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureFailureSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class InfrastructureMaintenancePhase:
    """Phase during which infrastructure undergoes maintenance and updates (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureMaintenancePhase"
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
class InfrastructureOperationalPhase:
    """Phase during which platform infrastructure is actively supporting operations (gUFO Phase - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureOperationalPhase"
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
class InfrastructureTakedown:
    """Coordinated operation to dismantle platform infrastructure including servers, domains, and supporting systems (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#InfrastructureTakedown"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    has_takedown_completeness: Optional[float] = field(default=None)
    has_takedown_effectiveness: Optional[float] = field(default=None)
    has_takedown_speed: Optional[str] = field(default=None)
    takedown_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class LoadBalancer:
    """Load balancing infrastructure distributing traffic across multiple servers for high availability (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#LoadBalancer"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class NetworkInfrastructure:
    """Network topology and routing infrastructure supporting platform connectivity and distribution (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#NetworkInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class NetworkTopologyAnalysis:
    """Analysis of network architecture and connectivity patterns within platform infrastructure (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#NetworkTopologyAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)
    has_analysis_accuracy: Optional[float] = field(default=None)
    has_analysis_depth: Optional[str] = field(default=None)
    has_analysis_timeliness: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    network_complexity: Optional[str] = field(default=None)


@dataclass
class PaymentProcessing:
    """Financial processing systems enabling platform monetization through subscription fees, content purchases, or cryptocurrency transactions (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#PaymentProcessing"
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
    has_financial_complexity: Optional[str] = field(default=None)
    has_financial_traceability: Optional[float] = field(default=None)
    monthly_revenue: Optional[float] = field(default=None)
    payment_methods: list[str] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class PlatformInfrastructure:
    """Technical infrastructure supporting child exploitation platforms, including servers, networks, and supporting systems (gUFO Object)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#PlatformInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class ProxyInfrastructure:
    """Proxy servers and reverse proxy systems used to hide platform origins and provide redundancy (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#ProxyInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class SecurityInfrastructure:
    """Security systems protecting platform infrastructure from detection and takedown efforts (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#SecurityInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    has_anonymity_effectiveness: Optional[float] = field(default=None)
    has_obfuscation_complexity: Optional[str] = field(default=None)
    has_security_strength: Optional[str] = field(default=None)
    obfuscation_methods: list[str] = field(default_factory=list)


@dataclass
class SecurityOperatorRole:
    """Role of person managing security infrastructure and operations (gUFO Role - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#SecurityOperatorRole"
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
class ServerInfrastructure:
    """Server and hosting infrastructure supporting platform operations, including web servers, database servers, and application servers (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#ServerInfrastructure"
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
    comment: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None)
    has_infrastructure_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_end_point: Optional[dateTimeStamp] = field(default=None)
    has_infrastructure_performance: Optional[str] = field(default=None)
    has_infrastructure_reliability: Optional[float] = field(default=None)
    has_infrastructure_scalability: Optional[str] = field(default=None)
    has_infrastructure_vulnerability: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    cloud_platform: Optional[str] = field(default=None)
    server_count: Optional[int] = field(default=None)


@dataclass
class ServerSeizure:
    """Physical or virtual seizure of servers hosting platform infrastructure (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#ServerSeizure"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    has_takedown_completeness: Optional[float] = field(default=None)
    has_takedown_effectiveness: Optional[float] = field(default=None)
    has_takedown_speed: Optional[str] = field(default=None)
    takedown_duration: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    servers_seized: Optional[int] = field(default=None)


@dataclass
class SubscriptionManagement:
    """Systems managing user subscriptions, access levels, and recurring payment processing (gUFO FunctionalComplex)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#SubscriptionManagement"
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
    has_financial_complexity: Optional[str] = field(default=None)
    has_financial_traceability: Optional[float] = field(default=None)
    monthly_revenue: Optional[float] = field(default=None)
    payment_methods: list[str] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)
    subscription_tiers: Optional[int] = field(default=None)


@dataclass
class SystemAdministratorRole:
    """Role of person responsible for infrastructure system administration (gUFO Role - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#SystemAdministratorRole"
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
class TakedownOperatorRole:
    """Role of law enforcement personnel conducting takedown operations (gUFO Role - anti-rigid)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#TakedownOperatorRole"
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
class UserAccessPatternAnalysis:
    """Analysis of user access patterns and geographic distribution based on infrastructure logs (gUFO Event)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/infrastructure#UserAccessPatternAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
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
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)
    has_analysis_accuracy: Optional[float] = field(default=None)
    has_analysis_depth: Optional[str] = field(default=None)
    has_analysis_timeliness: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    user_geographic_spread: Optional[int] = field(default=None)

