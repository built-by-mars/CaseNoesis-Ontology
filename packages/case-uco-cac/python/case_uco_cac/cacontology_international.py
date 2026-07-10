"""CAC Ontology - Crimes Against Children — cacontology-international module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AutomatedCrossMatching:
    """Automated system for continuous cross-matching of new data against international databases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#AutomatedCrossMatching"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CountryPartnership:
    """A bilateral or multilateral partnership between specific countries for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CountryPartnership"
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
    coordination_method: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_trust_level: Optional[str] = field(default=None)
    partner_country_count: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class CrossBorderDeviceSeizure:
    """Seizure of electronic devices across international borders with subsequent evidence sharing through MLAT processes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossBorderDeviceSeizure"
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
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class CrossBorderEffectiveness:
    """Effectiveness measurement for cross-border operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossBorderEffectiveness"
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
class CrossBorderForensics:
    """Forensic analysis requiring coordination across multiple countries for large-scale evidence processing."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossBorderForensics"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CrossBorderInvestigation:
    """Investigation requiring coordination across national boundaries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossBorderInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)


@dataclass
class CrossBorderOperation:
    """Investigation or operation spanning multiple countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossBorderOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class CrossBorderThreatAlert:
    """Alert about threats that require immediate action across multiple countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossBorderThreatAlert"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class CrossJurisdictionalInvestigation:
    """Investigation spanning multiple jurisdictions and countries targeting international criminal networks."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossJurisdictionalInvestigation"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)


@dataclass
class CrossReferenceAnalysis:
    """Analysis correlating data across multiple international databases to identify connections and patterns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossReferenceAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CrossReferralProtocol:
    """Protocol for referring reports between national hotlines."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#CrossReferralProtocol"
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
class DataExchangeProtocol:
    """Technical protocol for secure data exchange between international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#DataExchangeProtocol"
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
class DistributedIntelligenceProcessing:
    """Distributed processing of intelligence across multiple international systems for scalable analysis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#DistributedIntelligenceProcessing"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class EmergencyCoordinationProtocol:
    """Protocol for emergency coordination when immediate international response is required."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#EmergencyCoordinationProtocol"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class EuropeanCooperationFramework:
    """Framework for cooperation among European Union member states in child protection operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#EuropeanCooperationFramework"
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
    coordination_method: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_trust_level: Optional[str] = field(default=None)
    partner_country_count: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class EuropolCoordination:
    """Coordination framework provided by Europol for international law enforcement operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#EuropolCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class EuropolOperation:
    """Large-scale international operation coordinated by Europol involving multiple EU member states and international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#EuropolOperation"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)


@dataclass
class ExtraditionAgreement:
    """Agreement for extraditing suspects between countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#ExtraditionAgreement"
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
class FederatedDatabaseQuery:
    """Query system enabling simultaneous searches across multiple international databases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#FederatedDatabaseQuery"
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
class GlobalCaseTracking:
    """System for tracking cases across multiple jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalCaseTracking"
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
class GlobalDatabaseNetwork:
    """Network of interconnected international databases enabling comprehensive cross-referencing and correlation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalDatabaseNetwork"
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
class GlobalHotlineNetwork:
    """Network of interconnected national hotlines for child protection reporting."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalHotlineNetwork"
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
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class GlobalInvestigativeTeam:
    """Multi-national investigative team for large-scale operations like platform takedowns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalInvestigativeTeam"
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
class GlobalMissingChildrenCenter:
    """International coordination center for missing children cases across borders."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalMissingChildrenCenter"
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
class GlobalPlatformTakedown:
    """Takedown of global platforms with international user bases requiring coordinated action across multiple countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalPlatformTakedown"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class GlobalReach:
    """Measurement of international coverage and impact."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalReach"
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
class GlobalTakedownCoordination:
    """Real-time coordination for simultaneous takedown operations across multiple countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#GlobalTakedownCoordination"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InformationSharingAgreement:
    """Formal agreement governing information sharing between countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InformationSharingAgreement"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InstantAlertSystem:
    """System for instant notification of threats, discoveries, and urgent coordination needs across international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InstantAlertSystem"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class IntelligenceDataLake:
    """Centralized repository aggregating intelligence from multiple international sources for comprehensive analysis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#IntelligenceDataLake"
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
class IntelligenceFusion:
    """Real-time fusion of intelligence from multiple international sources to create comprehensive threat pictures."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#IntelligenceFusion"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalAlert:
    """Alert system for sharing critical information across borders."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalAlert"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalAnalyst:
    """Analyst specializing in cross-border case analysis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalAnalyst"
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
class InternationalCoordination:
    """Coordination activities between international law enforcement and child protection organizations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class InternationalCoordinator:
    """Role responsible for international coordination activities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalCoordinator"
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
class InternationalDatabase:
    """Shared database accessible by multiple countries for child protection."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalDatabase"
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
class InternationalEvidence:
    """Evidence collected from international operations requiring coordination across multiple jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalEvidence"
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
class InternationalEvidenceSharing:
    """Sharing of evidence between countries through formal legal assistance mechanisms and treaties."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalEvidenceSharing"
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
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalHotlineCoordination:
    """Coordination mechanism between different national hotlines."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalHotlineCoordination"
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
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalImpact:
    """Assessment of international program effectiveness."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalImpact"
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
class InternationalIntelligenceSharing:
    """Intelligence sharing framework for large-scale operations requiring coordination across multiple intelligence agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalIntelligenceSharing"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalNetworkDisruption:
    """Coordinated international effort to disrupt criminal networks operating across borders."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalNetworkDisruption"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)


@dataclass
class InternationalPartnership:
    """A formal partnership between countries or organizations for child protection cooperation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalPartnership"
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
    coordination_method: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_trust_level: Optional[str] = field(default=None)
    partner_country_count: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalProsecution:
    """Prosecution strategy coordinated across multiple countries for users identified in large-scale operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalProsecution"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class InternationalReferral:
    """Referral of cases or information to international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalReferral"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_time_international: Optional[float] = field(default=None)
    undercover_coordination: Optional[bool] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class InternationalResourceCoordination:
    """Coordination of technical and human resources across countries for large-scale operations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalResourceCoordination"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class InternationalTaskForce:
    """Multi-national task force for coordinating child protection investigations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalTaskForce"
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
class InternationalWarrant:
    """Warrant recognized across multiple jurisdictions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#InternationalWarrant"
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
class JurisdictionalCoordination:
    """Coordination mechanism for resolving jurisdictional conflicts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#JurisdictionalCoordination"
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
class LiaisonOfficer:
    """Officer serving as liaison between international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#LiaisonOfficer"
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
class LiveIntelligenceFeed:
    """Continuous feed of intelligence updates shared in real-time between international law enforcement agencies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#LiveIntelligenceFeed"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class MassUserAnalysis:
    """Analysis of massive user databases requiring international coordination for processing users across multiple countries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#MassUserAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class MultiCountryTakedown:
    """Coordinated takedown operation involving law enforcement from multiple countries (like Kidflix operation involving multiple nations)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#MultiCountryTakedown"
    has_begin_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[datetime] = field(default=None)
    label: list[str] = field(default_factory=list)
    coordination_complexity: Optional[str] = field(default=None)
    cross_border_capability: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_operational_urgency: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_success_likelihood: Optional[float] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    modified_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    jurisdiction_count: Optional[int] = field(default=None)


@dataclass
class MultilingualSupport:
    """Support for multiple languages in international coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#MultilingualSupport"
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
    language_support: list[str] = field(default_factory=list)


@dataclass
class MutualLegalAssistance:
    """Formal legal assistance between countries for investigations and prosecutions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#MutualLegalAssistance"
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
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class MutualLegalAssistanceTreatyOperation:
    """Operational process using Mutual Legal Assistance Treaty (MLAT) for international evidence sharing and cooperation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#MutualLegalAssistanceTreatyOperation"
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
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    treaty_basis: Optional[str] = field(default=None)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class OperationalSyncronization:
    """Real-time synchronization of operational activities across multiple countries for coordinated response."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#OperationalSyncronization"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class RealTimeIntelligenceSharing:
    """Real-time sharing of intelligence and alerts between international partners for immediate threat response and coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#RealTimeIntelligenceSharing"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class RegionalCoordination:
    """Coordination mechanisms within specific geographic regions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#RegionalCoordination"
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
    coordination_method: Optional[str] = field(default=None)
    has_coordination_effectiveness: Optional[str] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    has_trust_level: Optional[str] = field(default=None)
    partner_country_count: Optional[int] = field(default=None)
    created_time: Optional[datetime] = field(default=None)
    global_coverage: Optional[str] = field(default=None)


@dataclass
class SecureChannel:
    """Secure communication mechanism for international coordination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#SecureChannel"
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
class SecureCommunicationChannel:
    """Encrypted communication channel for secure real-time coordination between international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#SecureCommunicationChannel"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)


@dataclass
class ThreatAssessmentSharing:
    """Real-time sharing of threat assessments and risk evaluations between international partners."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/international#ThreatAssessmentSharing"
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
    has_agreement_stability: Optional[str] = field(default=None)
    has_compliance: Optional[float] = field(default=None)
    has_data_quality: Optional[str] = field(default=None)
    has_reliability_score: Optional[float] = field(default=None)
    information_sharing_level: Optional[str] = field(default=None)
    multilateral_agreement: Optional[bool] = field(default=None)
    shares_data_with: list[Organization] = field(default_factory=list)
    created_time: Optional[datetime] = field(default=None)

