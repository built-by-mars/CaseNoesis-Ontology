"""CAC Ontology - Crimes Against Children — cacontology-recantation module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CommunityPressureRisk:
    """A recantation risk created by pressure, shame, or expectation from community, school, faith, or other social networks."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#CommunityPressureRisk"
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
    risk_factor_category: Optional[str] = field(default=None)


@dataclass
class DisclosureStatement:
    """A statement in which a child victim discloses abuse or exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#DisclosureStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)


@dataclass
class OffenderContactRisk:
    """A recantation risk created by continued offender access, visitation, or indirect contact after disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#OffenderContactRisk"
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
    risk_factor_category: Optional[str] = field(default=None)


@dataclass
class PartialRecantationStatement:
    """A recantation that withdraws only part of a prior disclosure or muddies the disclosure without fully retracting it."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#PartialRecantationStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)
    retracts_statement: Optional[DisclosureStatement] = field(default=None)


@dataclass
class PostDisclosureDenialStatement:
    """A denial made after an earlier disclosure has already occurred."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#PostDisclosureDenialStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)


@dataclass
class PostRecantationForensicInterview:
    """A follow-up forensic interview conducted after recantation or denial to explore circumstances, pressure, and statement change dynamics."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#PostRecantationForensicInterview"
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
    assessment_disposition: Optional[str] = field(default=None)


@dataclass
class ReaffirmedDisclosureStatement:
    """A later statement that reaffirms an earlier disclosure after denial, pressure, or recantation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#ReaffirmedDisclosureStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)
    reaffirms_statement: Optional[DisclosureStatement] = field(default=None)


@dataclass
class RecantationAssessment:
    """An investigative or prosecutorial assessment of a recantation, its credibility, surrounding pressures, and implications for case strategy."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#RecantationAssessment"
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
    assessment_disposition: Optional[str] = field(default=None)


@dataclass
class RecantationNotification:
    """An action in which a family member, caregiver, professional, or other person reports that a child has recanted or denied an earlier disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#RecantationNotification"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    notification_channel: Optional[str] = field(default=None)


@dataclass
class RecantationPressure:
    """A coercive or inducement-bearing action intended to influence a victim to deny, minimize, or retract a disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#RecantationPressure"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    pressure_method: Optional[str] = field(default=None)


@dataclass
class RecantationRiskFactor:
    """A factor correlated with increased likelihood of post-disclosure denial or recantation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#RecantationRiskFactor"
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
    risk_factor_category: Optional[str] = field(default=None)


@dataclass
class RecantationStatement:
    """A statement in which a child victim retracts or disavows an earlier disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#RecantationStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)
    retracts_statement: Optional[DisclosureStatement] = field(default=None)


@dataclass
class SiblingSeparationConcern:
    """A concern that sibling removal, foster placement, or sibling separation may drive statement withdrawal."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#SiblingSeparationConcern"
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
    risk_factor_category: Optional[str] = field(default=None)


@dataclass
class StatementChangeContext:
    """A situation capturing the social, familial, investigative, and coercive conditions surrounding a victim's change in statement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#StatementChangeContext"
    label: list[str] = field(default_factory=list)
    assessed_by_action: list[RecantationAssessment] = field(default_factory=list)
    has_recantation_risk_factor: list[RecantationRiskFactor] = field(default_factory=list)
    reported_through_notification: Optional[RecantationNotification] = field(default=None)


@dataclass
class SystemInterventionFear:
    """Fear of court, child-protection action, family breakup, or other multidisciplinary system consequences following disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#SystemInterventionFear"
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
    risk_factor_category: Optional[str] = field(default=None)


@dataclass
class TentativeDisclosureStatement:
    """A partial or testing-the-waters disclosure that precedes fuller disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#TentativeDisclosureStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)


@dataclass
class UnsupportiveFamilyResponse:
    """A family response that sides with the offender, undermines the child, or otherwise erodes support for the disclosure."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#UnsupportiveFamilyResponse"
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
    risk_factor_category: Optional[str] = field(default=None)


@dataclass
class VictimStatement:
    """A statement or account by a child victim concerning abuse, disclosure, denial, or recantation. Modeled as a gUFO Object to support linkage to persons, contexts, and investigative assessments."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recantation#VictimStatement"
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
    statement_about_event: Optional[Crime] = field(default=None)
    statement_date: Optional[datetime] = field(default=None)
    statement_made_by: Optional[Person] = field(default=None)
    statement_received_by: Optional[Person] = field(default=None)

