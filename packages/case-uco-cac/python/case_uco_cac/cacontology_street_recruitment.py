"""CAC Ontology - Crimes Against Children — cacontology-street-recruitment module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgeVulnerabilityIndicator:
    """Apparent youth or minor status making individual vulnerable to exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#AgeVulnerabilityIndicator"
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
    apparent_age: Optional[int] = field(default=None)


@dataclass
class AlcoholFacilitation:
    """Use of alcohol to impair victim judgment and facilitate exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#AlcoholFacilitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    substance_type: Optional[str] = field(default=None)
    administration_method: Optional[str] = field(default=None)


@dataclass
class BehavioralVulnerabilityIndicator:
    """Behavioral patterns indicating vulnerability (isolation, confusion, seeking help)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#BehavioralVulnerabilityIndicator"
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
    distress_indicators: Optional[str] = field(default=None)


@dataclass
class BodySellingProposition:
    """Explicit suggestion that victim can make money by 'selling their body'."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#BodySellingProposition"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)
    money_amount_mentioned: Optional[float] = field(default=None)


@dataclass
class CasualConversationApproach:
    """Approach through seemingly innocent casual conversation to assess vulnerability."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#CasualConversationApproach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)
    conversation_topic: Optional[str] = field(default=None)


@dataclass
class CommercialDistrict:
    """Commercial areas with restaurants, shops, and businesses used for recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#CommercialDistrict"
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
class DelayedReporting:
    """Victim reporting that occurs days or weeks after initial incident."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DelayedReporting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_method: Optional[str] = field(default=None)


@dataclass
class DemographicTargeting:
    """Targeting individuals based on specific demographic characteristics indicating vulnerability."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DemographicTargeting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)


@dataclass
class DigitalFollowUp:
    """Follow-up through digital communication channels (text, social media, calls)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DigitalFollowUp"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)


@dataclass
class DigitalToPhysicalBridge:
    """Use of digital communication to maintain connection after physical encounter."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DigitalToPhysicalBridge"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)


@dataclass
class DirectSolicitationApproach:
    """Direct approach with immediate commercial sexual proposition."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DirectSolicitationApproach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)


@dataclass
class DirectTraffickingProposition:
    """Explicit, immediate proposition for victim to engage in commercial sexual activity."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DirectTraffickingProposition"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)


@dataclass
class DisclosureToAuthorities:
    """Victim's disclosure of trafficking recruitment or exploitation to law enforcement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DisclosureToAuthorities"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_method: Optional[str] = field(default=None)


@dataclass
class DrugFacilitatedVulnerability:
    """Creation or exploitation of vulnerability through substance administration."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#DrugFacilitatedVulnerability"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    substance_type: Optional[str] = field(default=None)
    administration_method: Optional[str] = field(default=None)


@dataclass
class EconomicIncentivePresentation:
    """Presentation of financial benefits and earning potential from commercial sexual activity."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#EconomicIncentivePresentation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)
    economic_incentive: Optional[str] = field(default=None)


@dataclass
class EscapeAttempt:
    """Victim's attempt to escape from trafficking situation or recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#EscapeAttempt"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)
    resistance_level: Optional[str] = field(default=None)


@dataclass
class ExplicitCommercialOffer:
    """Direct offer of money in exchange for sexual services or performances."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ExplicitCommercialOffer"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)
    money_amount_mentioned: Optional[float] = field(default=None)


@dataclass
class FoodOfferApproach:
    """Approach offering food or meals to establish trust and create obligation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#FoodOfferApproach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)
    pretext_used: Optional[str] = field(default=None)
    help_offer_type: Optional[str] = field(default=None)


@dataclass
class HelpOfferApproach:
    """Approach offering assistance such as phone charging, food, transportation, or shelter."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#HelpOfferApproach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)
    pretext_used: Optional[str] = field(default=None)
    help_offer_type: Optional[str] = field(default=None)


@dataclass
class HelpSeekingBehavior:
    """Victim's attempts to seek help or report trafficking recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#HelpSeekingBehavior"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)


@dataclass
class HighTrafficArea:
    """Public area with high pedestrian traffic used for victim identification."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#HighTrafficArea"
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
class HighwayLocation:
    """Location near or alongside highways used for isolated exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#HighwayLocation"
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
class ImmediateExploitationAttempt:
    """Attempt to immediately engage victim in commercial sexual activity without extended grooming."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ImmediateExploitationAttempt"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)


@dataclass
class ImmediateIsolation:
    """Rapid removal of victim from public space to isolated location for exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ImmediateIsolation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    escalation_timeframe: Optional[float] = field(default=None)


@dataclass
class ImmediateReporting:
    """Victim reporting that occurs immediately or within hours of incident."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ImmediateReporting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_method: Optional[str] = field(default=None)


@dataclass
class ImpairmentExploitation:
    """Exploitation of victim while impaired by substances to reduce resistance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ImpairmentExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    substance_type: Optional[str] = field(default=None)
    impairment_level: Optional[str] = field(default=None)


@dataclass
class InitialStreetContact:
    """First contact between trafficker and victim occurring in public space."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#InitialStreetContact"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)


@dataclass
class IsolatedLocation:
    """Secluded location used for exploitation away from public view."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#IsolatedLocation"
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
class IsolationVulnerabilityIndicator:
    """Indicators that individual is alone or lacks social support (walking alone, no companions)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#IsolationVulnerabilityIndicator"
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
    isolation_level: Optional[str] = field(default=None)


@dataclass
class LocationTransition:
    """Movement of victim from initial contact location to exploitation location."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#LocationTransition"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transportation_method: Optional[str] = field(default=None)


@dataclass
class MarijuanaFacilitation:
    """Use of marijuana to reduce victim inhibitions and facilitate exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#MarijuanaFacilitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    substance_type: Optional[str] = field(default=None)
    administration_method: Optional[str] = field(default=None)


@dataclass
class NeighborhoodTargeting:
    """Targeting specific neighborhoods or geographic areas known for vulnerable populations."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#NeighborhoodTargeting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)


@dataclass
class NextDayFollowUp:
    """Follow-up contact occurring the day after initial encounter."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#NextDayFollowUp"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)


@dataclass
class OpportunisticExploitation:
    """Exploitation of vulnerable individuals encountered in public spaces without prior planning or relationship."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#OpportunisticExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)


@dataclass
class PersistenceAfterRejection:
    """Continued recruitment attempts after initial rejection of trafficking proposition."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#PersistenceAfterRejection"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)
    reinforcement_attempts: Optional[int] = field(default=None)
    persistence_level: Optional[str] = field(default=None)


@dataclass
class PhoneChargingOffer:
    """Specific pretext offering to charge victim's phone in vehicle or location."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#PhoneChargingOffer"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)
    pretext_used: Optional[str] = field(default=None)
    help_offer_type: Optional[str] = field(default=None)


@dataclass
class PhysicalVulnerabilityIndicator:
    """Physical appearance or condition indicating vulnerability (youth, fatigue, distress)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#PhysicalVulnerabilityIndicator"
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
class PostContactReinforcement:
    """Follow-up contact after initial encounter to reinforce trafficking proposition."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#PostContactReinforcement"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)


@dataclass
class PretextBasedApproach:
    """Initial approach using false pretext or offer of assistance to establish contact."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#PretextBasedApproach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)
    pretext_used: Optional[str] = field(default=None)


@dataclass
class ProstitutionProposition:
    """Direct proposition to engage in prostitution or selling sexual services."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ProstitutionProposition"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)
    money_amount_mentioned: Optional[float] = field(default=None)


@dataclass
class PublicSpaceTargeting:
    """Systematic targeting of vulnerable individuals in specific public locations for trafficking recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#PublicSpaceTargeting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)


@dataclass
class RapidEscalationRecruitment:
    """Trafficking recruitment with accelerated timeline from initial contact to exploitation attempt."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#RapidEscalationRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    escalation_timeframe: Optional[float] = field(default=None)


@dataclass
class ResidentialArea:
    """Residential neighborhoods where victims may be walking or living."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#ResidentialArea"
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
class SameDayProgression:
    """Progression from initial contact to sexual assault and trafficking proposition within same day."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#SameDayProgression"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    escalation_timeframe: Optional[float] = field(default=None)
    same_day_progression: Optional[bool] = field(default=None)


@dataclass
class SecondaryLocationExploitation:
    """Exploitation occurring at secondary location away from initial contact point."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#SecondaryLocationExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    transportation_method: Optional[str] = field(default=None)
    distance_from_contact: Optional[float] = field(default=None)
    exploitation_location: Optional[str] = field(default=None)


@dataclass
class SocioeconomicVulnerabilityIndicator:
    """Indicators of economic hardship or social disadvantage (clothing, possessions, location)."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#SocioeconomicVulnerabilityIndicator"
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
class StreetBasedRecruitment:
    """Trafficking recruitment occurring in public spaces through direct physical approach and opportunistic exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#StreetBasedRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)


@dataclass
class StreetRecruitmentLocation:
    """Specific location where street-based trafficking recruitment occurs."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#StreetRecruitmentLocation"
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
class StreetVulnerabilityAssessment:
    """Rapid assessment of individual vulnerability factors in public space encounters."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#StreetVulnerabilityAssessment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    vulnerability_indicators: Optional[str] = field(default=None)


@dataclass
class StrippingProposition:
    """Specific proposition to engage in stripping or exotic dancing for money."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#StrippingProposition"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    analysis_completeness: Optional[float] = field(default=None)
    behavior_frequency: Optional[str] = field(default=None)
    behavior_intensity: Optional[str] = field(default=None)
    behavior_type: Optional[str] = field(default=None)
    data_confidence: Optional[float] = field(default=None)
    grooming_effectiveness: Optional[float] = field(default=None)
    grooming_stage: Optional[str] = field(default=None)
    manipulation_level: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    explicitness_level: Optional[str] = field(default=None)
    proposition_type: Optional[str] = field(default=None)
    money_amount_mentioned: Optional[float] = field(default=None)


@dataclass
class SubstanceBasedControl:
    """Use of substance dependency or impairment to maintain control over victim."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#SubstanceBasedControl"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    substance_type: Optional[str] = field(default=None)


@dataclass
class SubstanceFacilitatedRecruitment:
    """Use of alcohol or drugs to facilitate trafficking recruitment and reduce victim resistance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#SubstanceFacilitatedRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    substance_type: Optional[str] = field(default=None)


@dataclass
class TextMessageFollowUp:
    """Follow-up through text messaging to reinforce trafficking proposition."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#TextMessageFollowUp"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)


@dataclass
class TraffickingPropositionReinforcement:
    """Repeated presentation of trafficking proposition to overcome initial resistance."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#TraffickingPropositionReinforcement"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    follow_up_delay: Optional[float] = field(default=None)
    follow_up_method: Optional[str] = field(default=None)
    reinforcement_attempts: Optional[int] = field(default=None)


@dataclass
class TraffickingPropositionRejection:
    """Victim's rejection of trafficking proposition or commercial sexual offer."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#TraffickingPropositionRejection"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)


@dataclass
class TransitArea:
    """Transportation hubs or transit areas where vulnerable individuals may be targeted."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#TransitArea"
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
class TransportationOfferApproach:
    """Offer of rides or transportation to isolated locations for exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#TransportationOfferApproach"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    approach_method: Optional[str] = field(default=None)
    contact_duration: Optional[float] = field(default=None)
    initial_contact_location: Optional[str] = field(default=None)
    pretext_used: Optional[str] = field(default=None)
    help_offer_type: Optional[str] = field(default=None)


@dataclass
class VehicleBasedIsolation:
    """Use of vehicle to isolate victim and transport to exploitation location."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VehicleBasedIsolation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: Optional[str] = field(default=None)
    comment: Optional[str] = field(default=None)
    escalation_timeframe: Optional[float] = field(default=None)


@dataclass
class VehicleLocation:
    """Vehicle used as location for exploitation or transportation to exploitation site."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VehicleLocation"
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
class VictimReporting:
    """Victim's decision to report trafficking recruitment or assault to authorities."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VictimReporting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_method: Optional[str] = field(default=None)


@dataclass
class VictimResistance:
    """Active resistance to trafficking recruitment attempts or exploitation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VictimResistance"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)
    resistance_level: Optional[str] = field(default=None)


@dataclass
class VictimStreetResponse:
    """Victim's response to street-based recruitment attempts and trafficking propositions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VictimStreetResponse"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    response_type: Optional[str] = field(default=None)


@dataclass
class VulnerabilityIndicator:
    """Observable characteristic or behavior indicating potential trafficking vulnerability."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VulnerabilityIndicator"
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
class VulnerableNeighborhood:
    """Neighborhood with high poverty, crime, or social vulnerability targeted by traffickers."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/street#VulnerableNeighborhood"
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

