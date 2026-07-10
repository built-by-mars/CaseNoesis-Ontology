"""Legal Process and Procedure Extension — legalproc module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChargingInstrument:
    """A charging instrument is a formal document that initiates or amends criminal charges against one or more defendants, such as a criminal complaint, indictment, superseding indictment, or information. S"""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/ChargingInstrument"
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
    instrument_type: Optional[str] = field(default=None)


@dataclass
class CriminalCharge:
    """A criminal charge is a formal accusation, stated as one or more counts within a charging instrument, that a person committed a specific statutory offense. Inchoate and derivative offenses (conspiracy,"""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/CriminalCharge"
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
    asserted_in: list[ChargingInstrument] = field(default_factory=list)
    charge_classification: Optional[str] = field(default=None)
    charge_disposition: list[str] = field(default_factory=list)
    count_label: Optional[str] = field(default=None)
    count_number: list[int] = field(default_factory=list)
    object_offense: list[CriminalCharge] = field(default_factory=list)
    offense_form: Optional[str] = field(default=None)
    statute_citation: list[str] = field(default_factory=list)


@dataclass
class CriminalProceeding:
    """A criminal proceeding is a formal event in a criminal case conducted before a tribunal, such as an arraignment, detention hearing, trial, plea hearing, sentencing hearing, or appeal."""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/CriminalProceeding"
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
    proceeding_type: Optional[str] = field(default=None)


@dataclass
class ForfeitureOrder:
    """A forfeiture order is an order, or pre-conviction allegation, requiring surrender to the state of property involved in or traceable to an offense. See 18 U.S.C. §§ 981-982 (https://www.law.cornell.edu"""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/ForfeitureOrder"
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
    currency_code: Optional[str] = field(default=None)
    monetary_amount: Optional[float] = field(default=None)


@dataclass
class Plea:
    """A plea is a defendant's formal answer to a criminal charge. See Federal Rule of Criminal Procedure 11 (https://www.law.cornell.edu/rules/frcrmp/rule_11)."""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/Plea"
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
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    plea_type: Optional[str] = field(default=None)


@dataclass
class RestitutionOrder:
    """A restitution order is an order or request that an offender compensate victims for losses caused by the offense, monetarily or in kind. See 18 U.S.C. § 3663A (https://www.law.cornell.edu/uscode/text/1"""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/RestitutionOrder"
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
    currency_code: Optional[str] = field(default=None)
    monetary_amount: Optional[float] = field(default=None)


@dataclass
class Sentence:
    """A sentence is a penalty recommended by a party or imposed by a tribunal upon conviction of a criminal charge, including custodial terms, supervised release, and special assessments. See 18 U.S.C. § 35"""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/Sentence"
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
    sentence_status: Optional[str] = field(default=None)
    sentence_term: Optional[str] = field(default=None)


@dataclass
class Verdict:
    """A verdict is a finder of fact's formal determination on a criminal charge, such as a jury's finding of guilty or not guilty on a count. See Federal Rule of Criminal Procedure 31 (https://www.law.corne"""

    CLASS_IRI: str = "http://example.org/ontology/legalproc/Verdict"
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
    concerns_charge: list[CriminalCharge] = field(default_factory=list)
    verdict_type: Optional[str] = field(default=None)

