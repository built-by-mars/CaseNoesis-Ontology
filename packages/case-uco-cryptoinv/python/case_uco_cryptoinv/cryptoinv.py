"""Cryptocurrency and Financial Crime Investigation Extension — cryptoinv module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AssetSeizureAction:
    """An investigative action in which law enforcement takes custody of assets — including virtual assets seized by using recovered private keys to transfer wallet contents to government-controlled addresse"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/AssetSeizureAction"
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
class CriminalCharge:
    """A criminal charge is a formal accusation, stated as a count within a charging instrument (indictment or information), that a person committed a specific statutory offense — e.g. Count One, Money Laund"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/CriminalCharge"
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
    charge_description: Optional[str] = field(default=None)
    count_number: Optional[int] = field(default=None)
    statute_citation: list[str] = field(default_factory=list)


@dataclass
class CryptocurrencyAddressFacet:
    """A cryptocurrency address facet is a grouping of characteristics unique to a blockchain address used to send and receive virtual assets on a distributed ledger network. A virtual currency address is ro"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/CryptocurrencyAddressFacet"
    address_format: Optional[str] = field(default=None)
    address_value: Optional[str] = field(default=None)
    blockchain_network: Optional[str] = field(default=None)
    cryptocurrency_type: Optional[str] = field(default=None)


@dataclass
class CryptocurrencyMixingService:
    """A cryptocurrency mixing service (mixer or tumbler) obscures the link between transaction inputs and outputs by combining or shuffling the virtual assets of multiple users — for example via coinjoin, a"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/CryptocurrencyMixingService"
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
class CryptocurrencyTransactionFacet:
    """A cryptocurrency transaction facet is a grouping of characteristics unique to a transfer of value recorded on a blockchain distributed ledger. Attach to a uco-observable:ObservableObject representing """

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/CryptocurrencyTransactionFacet"
    block_hash: Optional[str] = field(default=None)
    block_number: Optional[int] = field(default=None)
    confirmation_count: Optional[int] = field(default=None)
    transaction_fee: Optional[float] = field(default=None)
    transaction_hash: Optional[str] = field(default=None)
    transaction_status: Optional[str] = field(default=None)
    transaction_type: Optional[str] = field(default=None)


@dataclass
class CryptocurrencyWalletFacet:
    """A cryptocurrency wallet facet is a grouping of characteristics unique to a wallet: software, a device, or a hosted service that keeps track of the private keys used to sign virtual-asset transactions,"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/CryptocurrencyWalletFacet"
    address_count: Optional[int] = field(default=None)
    wallet_identifier: Optional[str] = field(default=None)
    wallet_type: Optional[str] = field(default=None)


@dataclass
class DarknetMarket:
    """A darknet market is an e-commerce platform, typically reachable only via anonymizing networks such as Tor, through which vendors can sell illegal goods and services such as narcotics, stolen financial"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/DarknetMarket"
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
class ForfeitureOrder:
    """A forfeiture order (or forfeiture allegation, prior to conviction) requires a defendant to forfeit to the government property involved in or traceable to the offense, under statutes such as 18 U.S.C. """

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/ForfeitureOrder"
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
    money_judgment_amount: Optional[float] = field(default=None)
    money_judgment_currency_code: Optional[str] = field(default=None)


@dataclass
class PleaAgreement:
    """A plea agreement is a negotiated agreement under Federal Rule of Criminal Procedure 11(c) (https://www.law.cornell.edu/rules/frcrmp/rule_11) in which a defendant agrees to plead guilty to one or more """

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/PleaAgreement"
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
    plea_date: Optional[datetime] = field(default=None)
    pleads_guilty_to: list[CriminalCharge] = field(default_factory=list)


@dataclass
class RestitutionOrder:
    """A restitution order (or restitution request) compensates victims for losses caused by the offense. For most federal property crimes restitution is mandatory under the Mandatory Victims Restitution Act"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/RestitutionOrder"
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
    restitution_description: Optional[str] = field(default=None)
    restitution_in_kind: Optional[bool] = field(default=None)


@dataclass
class SentencingOutcome:
    """A sentencing outcome records a sentence recommended by a party or imposed by the court under 18 U.S.C. § 3553(a) (https://www.law.cornell.edu/uscode/text/18/3553) and the United States Sentencing Guid"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/SentencingOutcome"
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
    guideline_range_high_months: Optional[int] = field(default=None)
    guideline_range_low_months: Optional[int] = field(default=None)
    offense_level: Optional[int] = field(default=None)
    sentence_duration_months: Optional[int] = field(default=None)
    sentence_status: Optional[str] = field(default=None)
    sentencing_date: Optional[datetime] = field(default=None)
    supervised_release_months: Optional[int] = field(default=None)


@dataclass
class VirtualAssetHoldingFacet:
    """A virtual asset holding facet is a grouping of characteristics describing a point-in-time quantity of a specific virtual asset held at, contained in, or seized from a wallet, address, or account — for"""

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/VirtualAssetHoldingFacet"
    asset_quantity: Optional[float] = field(default=None)
    asset_symbol: Optional[str] = field(default=None)
    fiat_currency_code: Optional[str] = field(default=None)
    fiat_value: Optional[float] = field(default=None)
    valuation_date: Optional[datetime] = field(default=None)


@dataclass
class VirtualAssetServiceProvider:
    """A virtual asset service provider (VASP) is any natural or legal person who as a business conducts one or more of the following activities for or on behalf of another natural or legal person: exchange """

    CLASS_IRI: str = "http://example.org/ontology/cryptoinv/VirtualAssetServiceProvider"
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

