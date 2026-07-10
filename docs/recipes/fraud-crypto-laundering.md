# Fraud, Cryptocurrency, and Money Laundering Investigations

> See [Recipe Index](INDEX.md) for all recipes.

Model end-to-end financial fraud investigations that combine messaging coercion, fake investment platforms, blockchain tracing, exchange subpoena returns, and location correlation. This recipe targets pig-butchering / fake-platform workflows and general crypto laundering cases using core CASE/UCO types. Pair with [threaded-messaging.md](threaded-messaging.md) for chat evidence and [accounts.md](accounts.md) for cross-platform identity linking.

## Scope

| Layer | What it captures | Primary classes |
|---|---|---|
| **Communication** | Grooming chats, platform handles, coercion | `MessageThread`, `Message`, `InstantMessagingAddress`, `Person` |
| **Financial instruments** | Wallets, exchange accounts, fiat ramps | `ObservableObject`, `AccountFacet`, wallet observables |
| **Blockchain trace** | Wallet hops, cluster attribution | `InvestigativeAction`, `Relationship`, `ObservableObject` |
| **Exchange returns** | KYC, account holder, cash-out | `Person`, `Organization`, `InvestigativeAction`, `ProvenanceRecord` |
| **Location correlation** | Meetups, geofence hits, registered addresses | `Location`, `SimpleAddressFacet`, `Relationship` |

## Key classes

| Class | Role |
|---|---|
| `Investigation` | Case container linking victims, suspects, and financial artifacts |
| `InvestigativeAction` | Subpoena service, blockchain trace, exchange analysis, arrest |
| `Person` / `Identity` | Victims, groomers, mules, exchange account holders |
| `Organization` | Exchanges, OTC desks, fake investment platforms |
| `MessageThread` + `MessageFacet` | Coercion and grooming chat evidence |
| `InstantMessagingAddress` | Telegram/WhatsApp handles tied to speakers |
| `ObservableObject` | Wallet addresses, exchange account IDs, platform URLs |
| `Relationship` | `Sent`, `Transferred_To`, `Resolved_To`, `Associated_With` |
| `ProvenanceRecord` | Chain from raw exchange CSV/PDF to derived wallet clusters |
| `Location` + `SimpleAddressFacet` | Registered addresses, meetup sites, geofence hits |

## Pattern

```
Investigation
    ├── object ──▶ MessageThread (coercion / grooming)
    │                 └── participant ──▶ Person + InstantMessagingAddress
    ├── object ──▶ InvestigativeAction (blockchain trace)
    │                 ├── instrument ──▶ Tool (tracer, e.g. Chainalysis-class)
    │                 ├── object ──▶ seed wallet ObservableObject
    │                 └── result ──▶ wallet-hop subgraph (Relationship chain)
    ├── object ──▶ InvestigativeAction (exchange subpoena return)
    │                 ├── result ──▶ KYC Person + exchange AccountFacet
    │                 └── was_informed_by ──▶ blockchain trace action
    └── object ──▶ Location nodes (registered address, meetup, geofence)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import Investigation, InvestigativeAction, ProvenanceRecord
from case_uco.uco.identity import Person, Organization
from case_uco.uco.core import Relationship
from case_uco.uco.tool import Tool
from case_uco.uco.observable import (
    ObservableObject,
    Message, MessageFacet, MessageThreadFacet,
    InstantMessagingAddressFacet,
    URLFacet,
)
from case_uco.uco.location import Location, SimpleAddressFacet

graph = CASEGraph(kb_prefix="http://example.org/kb/")

victim = graph.create(Person, name="Eleanor Vance")
groomer = graph.create(Person, name="Marcus Hale")
platform = graph.create(Organization, name="Northstar Capital Vault")

groomer_handle = graph.create(
    ObservableObject,
    has_facet=[InstantMessagingAddressFacet(address_value="@northstar_mike_synth")],
)
fake_site = graph.create(
    ObservableObject,
    has_facet=[URLFacet(full_value="https://northstar-vault.example.invalid")],
)

thread = graph.create(
    ObservableObject,
    has_facet=[
        MessageThreadFacet(participant=[groomer_handle]),
    ],
)
graph.create(
    Message,
    has_facet=[
        MessageFacet(
            message_text="Withdrawal blocked until compliance fee paid.",
            from_=groomer_handle,
        )
    ],
)

seed_wallet = graph.create(
    ObservableObject,
    name="0xabc123…",  # from blockchain export
)
tracer = graph.create(Tool, name="Blockchain Tracer", version="2026.1")
trace_action = graph.create(
    InvestigativeAction,
    name="Trace victim deposit cluster",
    instrument=tracer,
    object=[seed_wallet],
)

exchange_return = graph.create(
    InvestigativeAction,
    name="Analyze Coinbase subpoena return",
)
account_holder = graph.create(Person, name="Dylan Reyes")
registered_address = graph.create(
    Location,
    has_facet=[
        SimpleAddressFacet(
            street="1555 Oak Street",
            locality="San Jose",
            region="California",
            postal_code="95110",
        )
    ],
)

investigation = graph.create(
    Investigation,
    name="Synthetic fraud-crypto case 2026-001",
    object=[thread, trace_action, exchange_return, registered_address],
)

graph.create(
    Relationship,
    source=[groomer],
    target=[groomer_handle],
    kind_of_relationship="Associated_With",
    is_directional=True,
)
graph.create(
    Relationship,
    source=[account_holder],
    target=[registered_address],
    kind_of_relationship="Located_At",
    is_directional=True,
)

graph.write("fraud-crypto-case.jsonld")
graph.validate()
```

</details>

## Validation queries

After building the graph, confirm key investigative links are present:

```sparql
PREFIX uco-core: <https://unifiedcyberontology.org/ontology/uco/core#>
PREFIX uco-action: <https://unifiedcyberontology.org/ontology/uco/action#>
PREFIX case-investigation: <https://unifiedcyberontology.org/ontology/case/investigation#>

# Every InvestigativeAction in the case should be reachable from the Investigation
SELECT ?action WHERE {
  ?inv a case-investigation:Investigation ;
       case-investigation:object ?action .
  ?action a case-investigation:InvestigativeAction .
}

# Messaging handles should not float without a Person or Account link
SELECT ?handle WHERE {
  ?handle a uco-observable:InstantMessagingAddress .
  FILTER NOT EXISTS {
    ?rel uco-core:source|uco-core:target ?handle .
  }
}
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Modeling wallet strings as plain `FileFacet` paths | Use `ObservableObject` with descriptive properties or extension wallet facets; keep hashes on `ContentDataFacet` for exported trace files |
| Collapsing groomer chat and exchange KYC into one `Person` without evidence | Keep distinct `Person` nodes until identity resolution is documented with a `Relationship` |
| Skipping `InvestigativeAction` for blockchain tracing | Record the trace as an action with `instrument` (tool) and `result` (hop subgraph) |
| Treating exchange CSV rows as anonymous strings | Map account holder names to `Person` and link to exchange `AccountFacet` observables |
| Omitting provenance on derived wallet clusters | Add `ProvenanceRecord` from raw exchange/blockchain export files to analysis actions |

## Typed crypto observables and legal process: the `cryptoinv` extension

Core CASE/UCO has no cryptocurrency facets yet (pending [UCO #675](https://github.com/ucoProject/UCO/issues/675)). For typed modeling, load the SDK's [`extensions/cryptoinv/`](../../extensions/cryptoinv/) extension and pass `extensions=["cryptoinv"]` to `validate_graph`:

| Need | cryptoinv class |
|---|---|
| Blockchain address | `ObservableObject` + `cryptoinv:CryptocurrencyAddressFacet` (`addressValue`, `cryptocurrencyType`, `blockchainNetwork`, `addressFormat`) |
| Transaction | `ObservableObject` + `cryptoinv:CryptocurrencyTransactionFacet`; inputs/outputs as `ObservableRelationship` (`Transaction_Input` / `Transaction_Output`) with `cryptoinv:transferAmount` |
| Wallet / cluster | `cryptoinv:CryptocurrencyWalletFacet` (`walletType`, `walletIdentifier`, `addressCount`) |
| Point-in-time holdings / seized value | `cryptoinv:VirtualAssetHoldingFacet` (`assetSymbol`, `assetQuantity`, `fiatValue`, `valuationDate`) — snapshots only; time-varying balances are blocked by [UCO #535](https://github.com/ucoProject/UCO/issues/535) |
| Exchanges, darknet markets, mixers | `cryptoinv:VirtualAssetServiceProvider`, `cryptoinv:DarknetMarket`, `cryptoinv:CryptocurrencyMixingService` |
| Laundering conduct | `uco-action:Action` + `cryptoinv:launderingTechnique` (peel-chain, chain-hopping, mixing, …) |
| Charges, pleas, sentencing, forfeiture | `cryptoinv:CriminalCharge`, `PleaAgreement`, `SentencingOutcome`, `ForfeitureOrder`, `RestitutionOrder`, `AssetSeizureAction` |

Worked exemplar: `examples/pacer/doj_crypto_2023_239/build_lichtenstein_ddc_2023_crypto.py` (U.S. v. Lichtenstein & Morgan — Bitfinex hack laundering, validated with strict concept coverage).

## Related recipes

- [elder-fraud-impersonation.md](elder-fraud-impersonation.md) — government-impersonation call centers, money couriers, and cash/prepaid-card schemes without a crypto layer
- [racketeering-enterprise.md](racketeering-enterprise.md) — when the theft-and-laundering operation is charged as a RICO enterprise (enterprise, member roles, predicate categories via the `rico` extension)
- [threaded-messaging.md](threaded-messaging.md) — ordered chat threads and participants
- [accounts.md](accounts.md) — cross-platform identity correlation
- [location.md](location.md) — registered addresses and geospatial correlation
- [network-investigation.md](network-investigation.md) — observed-vs-analyzed separation for tracer output
