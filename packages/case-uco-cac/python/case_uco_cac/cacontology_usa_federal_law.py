"""CAC Ontology - Crimes Against Children — cacontology-usa-federal-law module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AbusiveContactWithMinor:
    """Federal crime involving abusive sexual contact with minor victims. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#AbusiveContactWithMinor"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class AggravatedSexualAbuse:
    """Federal crime of aggravated sexual abuse involving children in federal jurisdiction. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#AggravatedSexualAbuse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class CEOSAttorneyRole:
    """Role of DOJ CEOS attorney specializing in child exploitation prosecution. Modeled as anti-rigid gUFO Role."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#CEOSAttorneyRole"
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
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    role_experience: Optional[int] = field(default=None)
    role_specialization: list[str] = field(default_factory=list)
    collaborates_with: list[FederalInvestigatorRole] = field(default_factory=list)


@dataclass
class CEOSdivision:
    """DOJ Child Exploitation and Obscenity Section serving unique and critical function in enforcement of federal laws protecting children from exploitation and prohibiting distribution of obscenity. Modele"""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#CEOSdivision"
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
class ChildPornographyDistribution:
    """Federal crime of distributing child pornography across state or international boundaries. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildPornographyDistribution"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_interstate_nexus: list[str] = field(default_factory=list)


@dataclass
class ChildPornographyPossession:
    """Federal crime of possessing child pornography that has traveled in interstate or foreign commerce. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildPornographyPossession"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ChildPornographyProduction:
    """Federal crime of producing child pornography, carrying severe mandatory minimum sentences. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildPornographyProduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    crime_jurisdiction: list[str] = field(default_factory=list)
    crime_severity_level: Optional[int] = field(default=None)
    mandatory_minimum_sentence: Optional[int] = field(default=None)


@dataclass
class ChildPornographyReceipt:
    """Federal crime of knowingly receiving child pornography through interstate or foreign commerce. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildPornographyReceipt"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ChildSupportEnforcementLaw:
    """Federal laws related to child support enforcement that intersect with child exploitation cases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildSupportEnforcementLaw"
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
class ChildSupportEvasion:
    """Federal crime of willfully failing to pay child support across state lines. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildSupportEvasion"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ChildSupportExploitationLink:
    """Connection between child support violations and child exploitation crimes. Modeled as gUFO Situation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ChildSupportExploitationLink"
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
class CommercialSexualExploitation:
    """Federal crime involving commercial sexual exploitation of children through force, fraud, or coercion. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#CommercialSexualExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ExtraterritorialProduction:
    """Federal crime of producing child pornography outside U.S. by U.S. citizens or residents. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ExtraterritorialProduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    foreign_countries_involved: list[str] = field(default_factory=list)
    involves_international_elements: list[bool] = field(default_factory=list)


@dataclass
class ExtraterritorialSexualExploitationLaw:
    """Federal laws criminalizing sexual exploitation of children committed by U.S. citizens or residents abroad."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ExtraterritorialSexualExploitationLaw"
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
class FederalChildExploitationLaw:
    """U.S. federal law related to child exploitation as enforced by CEOS. Modeled as gUFO Object providing legal framework."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalChildExploitationLaw"
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
class FederalChildPornographyLaw:
    """Federal statutes criminalizing child pornography production, distribution, receipt, and possession."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalChildPornographyLaw"
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
class FederalChildSexTraffickingLaw:
    """Federal statutes criminalizing child sex trafficking, commercial sexual exploitation, and related crimes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalChildSexTraffickingLaw"
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
class FederalChildSexualAbuseLaw:
    """Federal statutes criminalizing child sexual abuse in federal jurisdiction or involving interstate elements."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalChildSexualAbuseLaw"
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
class FederalDefendantRole:
    """Role of individual charged in federal child exploitation case. Modeled as anti-rigid gUFO Role."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalDefendantRole"
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
    defended_by: list[ExploitationEvent] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class FederalInvestigation:
    """Federal investigation of child exploitation crimes. Modeled as gUFO Event with temporal boundaries and evidence gathering."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalInvestigation"
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
    collects_evidence: list[ObservableObject] = field(default_factory=list)
    investigated_by: list[FederalInvestigatorRole] = field(default_factory=list)
    involves_digital_evidence: Optional[bool] = field(default=None)
    requires_forensic_analysis: Optional[bool] = field(default=None)


@dataclass
class FederalInvestigatorRole:
    """Role of federal investigator (FBI, ICE, etc.) investigating child exploitation. Modeled as anti-rigid gUFO Role."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalInvestigatorRole"
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
class FederalObscenityLaw:
    """U.S. federal law related to obscenity distribution and enforcement as managed by CEOS. Modeled as gUFO Object providing legal framework."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalObscenityLaw"
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
class FederalProsecution:
    """Federal legal prosecution process for child exploitation crimes. Modeled as gUFO Event with temporal progression through phases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalProsecution"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_legal_phase: list[Phase] = field(default_factory=list)
    has_prosecution_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_prosecution_end_point: Optional[dateTimeStamp] = field(default=None)
    prosecuted_by: list[FederalProsecutorRole] = field(default_factory=list)
    prosecution_complexity: Optional[str] = field(default=None)
    prosecution_severity: Optional[str] = field(default=None)
    prosecution_status: Optional[str] = field(default=None)


@dataclass
class FederalProsecutorRole:
    """Role of federal prosecutor handling child exploitation cases. Modeled as anti-rigid gUFO Role."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalProsecutorRole"
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
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    role_experience: Optional[int] = field(default=None)
    role_specialization: Optional[str] = field(default=None)


@dataclass
class FederalVictimRole:
    """Role of victim in federal child exploitation prosecution. Modeled as anti-rigid gUFO Role."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FederalVictimRole"
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
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    victimized_by: list[ExploitationEvent] = field(default_factory=list)


@dataclass
class FinancialControlPattern:
    """Pattern where child support evasion is used as mechanism of control in exploitation cases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#FinancialControlPattern"
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
class ForeignCommerceExploitation:
    """Federal crime involving sexual exploitation of children in foreign commerce. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ForeignCommerceExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    foreign_countries_involved: list[str] = field(default_factory=list)
    involves_international_elements: list[bool] = field(default_factory=list)


@dataclass
class ObscenityDistribution:
    """Federal crime of distributing obscene materials through interstate or foreign commerce. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ObscenityDistribution"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ObscenityImportation:
    """Federal crime of importing obscene materials into the United States. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ObscenityImportation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class ObscenityTransportation:
    """Federal crime of transporting obscene materials across state or international boundaries. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#ObscenityTransportation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class OnlineObscenityDistribution:
    """Federal crime of distributing obscene materials through internet and digital platforms. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#OnlineObscenityDistribution"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class PostConvictionPhase:
    """Post-conviction phase including appeals and compliance monitoring."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#PostConvictionPhase"
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
    has_legal_phase: list[Phase] = field(default_factory=list)
    has_prosecution_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_prosecution_end_point: Optional[dateTimeStamp] = field(default=None)
    prosecuted_by: list[FederalProsecutorRole] = field(default_factory=list)
    prosecution_complexity: Optional[str] = field(default=None)
    prosecution_severity: Optional[str] = field(default=None)
    prosecution_status: Optional[str] = field(default=None)


@dataclass
class PreTrialPhase:
    """Pre-trial phase of federal prosecution including investigation and charging."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#PreTrialPhase"
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
    has_legal_phase: list[Phase] = field(default_factory=list)
    has_prosecution_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_prosecution_end_point: Optional[dateTimeStamp] = field(default=None)
    prosecuted_by: list[FederalProsecutorRole] = field(default_factory=list)
    prosecution_complexity: Optional[str] = field(default=None)
    prosecution_severity: Optional[str] = field(default=None)
    prosecution_status: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    is_phase_of: Optional[FederalProsecution] = field(default=None)


@dataclass
class SentencingPhase:
    """Sentencing phase of federal prosecution including penalty determination. Modeled as anti-rigid gUFO Phase that prosecution temporarily exemplifies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#SentencingPhase"
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
    has_legal_phase: list[Phase] = field(default_factory=list)
    has_prosecution_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_prosecution_end_point: Optional[dateTimeStamp] = field(default=None)
    prosecuted_by: list[FederalProsecutorRole] = field(default_factory=list)
    prosecution_complexity: Optional[str] = field(default=None)
    prosecution_severity: Optional[str] = field(default=None)
    prosecution_status: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    is_phase_of: Optional[FederalProsecution] = field(default=None)


@dataclass
class SexTourism:
    """Federal crime of traveling abroad with intent to engage in sexual conduct with minors. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#SexTourism"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    foreign_countries_involved: list[str] = field(default_factory=list)
    involves_international_elements: list[bool] = field(default_factory=list)


@dataclass
class SexTraffickingConspiracy:
    """Federal crime of conspiracy to engage in sex trafficking of minors. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#SexTraffickingConspiracy"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class SexTraffickingOfMinors:
    """Federal crime of sex trafficking involving minors, including recruitment, harboring, transportation, or obtaining. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#SexTraffickingOfMinors"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    crime_severity_level: Optional[int] = field(default=None)
    involves_multiple_states: Optional[bool] = field(default=None)
    mandatory_minimum_sentence: Optional[int] = field(default=None)


@dataclass
class SexualAbuseOfMinor:
    """Federal crime of sexual abuse specifically involving minor victims. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#SexualAbuseOfMinor"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class TransportationForSexualExploitation:
    """Federal crime of transporting minors across international boundaries for sexual exploitation. Modeled as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#TransportationForSexualExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    foreign_countries_involved: list[str] = field(default_factory=list)
    involves_international_elements: list[bool] = field(default_factory=list)


@dataclass
class TrialPhase:
    """Trial phase of federal prosecution including court proceedings."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/usa-federal-law#TrialPhase"
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
    has_legal_phase: list[Phase] = field(default_factory=list)
    has_prosecution_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_prosecution_end_point: Optional[dateTimeStamp] = field(default=None)
    prosecuted_by: list[FederalProsecutorRole] = field(default_factory=list)
    prosecution_complexity: Optional[str] = field(default=None)
    prosecution_severity: Optional[str] = field(default=None)
    prosecution_status: Optional[str] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    is_phase_of: Optional[FederalProsecution] = field(default=None)

