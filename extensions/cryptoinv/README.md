# Cryptocurrency and Financial Crime Investigation Extension (cryptoinv)

An extension ontology that extends CASE/UCO into the cryptocurrency / fraud
investigation and criminal legal process domain. Authored per the
[CDO Community Playground Guide](https://docs.google.com/document/d/1EiXQiAeUGk-629xdKx7HZHVn927k891LGkPcQzNLLr8/edit?usp=sharing)
(separate OWL / SHACL / exemplar files, `owl:Class` only, every class
subclassed from UCO/CASE, cited descriptions).

## Provenance

Grounded in three sources:

1. **United States v. Lichtenstein & Morgan**, No. 1:23-cr-00239-CKK (D.D.C.) —
   the 2016 Bitfinex hack money-laundering prosecution (Information, Plea
   Agreement, Statement of Facts, Statement of the Offense, Sentencing
   Memorandum). The SDK exemplar built from these documents is at
   `examples/pacer/doj_crypto_2023_239/`.
2. **[UCO issue #675](https://github.com/ucoProject/UCO/issues/675)** — the
   pending cryptocurrency address/transaction change proposal (revised to
   exclude sanctions coverage per ontology committee feedback). The
   `CryptocurrencyAddressFacet` / `CryptocurrencyTransactionFacet` /
   `transferAmount` terms here mirror that proposal and MUST be retired if
   UCO adopts them.
3. **[CASE issue #87](https://github.com/casework/CASE/issues/87)** and the
   **[INTERPOL DW-VA Taxonomy](https://interpol-innovation-centre.github.io/DW-VA-Taxonomy/)** —
   wallet/VASP/mixing definitions.

## Scope

| Module | Classes |
|---|---|
| Cryptocurrency observables (facets) | `CryptocurrencyAddressFacet`, `CryptocurrencyTransactionFacet`, `CryptocurrencyWalletFacet`, `VirtualAssetHoldingFacet` |
| Financial-crime infrastructure | `VirtualAssetServiceProvider`, `DarknetMarket`, `CryptocurrencyMixingService` (all subclasses of `uco-identity:Organization`) |
| Legal process | `CriminalCharge`, `PleaAgreement`, `SentencingOutcome`, `ForfeitureOrder`, `RestitutionOrder`, `AssetSeizureAction` |
| Annotations | `launderingTechnique` (open vocabulary on actions), `transferAmount` (on Transaction_Input/Output relationships) |

Deliberately **out of scope**:

- **Sanctions designations** — excluded per the UCO ontology committee comment
  on [issue #675](https://github.com/ucoProject/UCO/issues/675); to be
  proposed separately (likely against CASE, aligned with
  `uco-analysis:ArtifactClassification`).
- **Time-varying wallet balances** — blocked upstream by
  [UCO issue #535](https://github.com/ucoProject/UCO/issues/535) (Qualities).
  `VirtualAssetHoldingFacet` records point-in-time snapshots with a
  `valuationDate` instead.

## Transaction input/output pattern

Transactions are `ObservableObject`s with a `CryptocurrencyTransactionFacet`.
Addresses connect to transactions through `uco-observable:ObservableRelationship`
instances with `kindOfRelationship` `"Transaction_Input"` / `"Transaction_Output"`
and a `cryptoinv:transferAmount`. This natively supports UTXO chains
(multi-input/multi-output) and account-based chains.

## Validation

```bash
case_validate --built-version case-1.4.0 \
  --ontology-graph extensions/cryptoinv/cryptoinv.ttl \
  --ontology-graph extensions/cryptoinv/cryptoinv-shapes.ttl \
  --inference rdfs --allow-info \
  extensions/cryptoinv/cryptoinv-exemplar.ttl
```

The MCP `validate_graph` tool accepts `extensions=["cryptoinv"]`, which loads
this extension for SHACL validation and strict concept coverage.
