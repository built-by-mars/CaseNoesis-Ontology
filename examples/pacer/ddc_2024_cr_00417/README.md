# U.S. v. Lam et al. — RICO Conspiracy, the "SE Enterprise" (D.D.C.)

Validated CASE/UCO exemplar for **1:24-cr-00417-CKK** (D.D.C., Judge
Colleen Kollar-Kotelly): the RICO prosecution of seventeen members and
associates of the **Social Engineering Enterprise** under
**18 U.S.C. § 1962(d)**, with wire-fraud conspiracy (§ 1349),
money-laundering conspiracy (§ 1956(h)), and obstruction (§ 1512(c))
counts. First exemplar of the **`rico` extension**
(`extensions/rico/`).

## Case summary

The SE Enterprise grew out of friendships formed on online gaming
platforms and operated from no later than October 2023 through at least
May 2025. Its members divided labor into charged roles — database
hackers, organizers, target identifiers, callers, money launderers, and
a residential burglar — to cold-call cryptocurrency holders while posing
as exchange security staff, steal their virtual currency, launder it
through peel chains, pass-through wallets, and chain-hopping into Monero
on no-KYC exchanges (Thorswap, eXch), and convert it to bulk cash,
exotic cars, jewelry, and rental mansions.

On 2024-08-19 the crew stole approximately **$245,093,239** from
Victim-7 at his Washington, D.C. home after convincing him to install a
remote desktop program. Other charged conduct includes a 2024-07-08
break-in at Victim-4's New Mexico home hunting hardware wallets (with a
telephone-camera livestream posted across the street), a $3,000,000
crypto-to-cash conversion for a Los Angeles rental mansion, the "Hesby
House" lease under the fake identity "Sean McGarry", and — after the
first arrests — Lam tossing his phone into Biscayne Bay, Tangeman
watching the FBI search Lam's Miami homes through remote
security-camera access, and Tangeman directing Desmond to destroy
co-conspirators' devices.

Charged in three instruments: a sealed two-defendant indictment (Doc 1,
2024-09-14), a fourteen-defendant superseding indictment (Doc 50,
2025-04-30), and a second superseding indictment adding three defendants
(Doc 229, 2025-10-29; redacted Doc 245, 2025-11-17). As of the docket
printout: nine guilty pleas and three sentencings — Ferro 78 months,
Tangeman 70 months, Desmond 36 months' probation.

## Sources

| File | PACER Doc | SHA-256 (prefix) |
|---|---|---|
| `pacer -- racketeering -- docket.pdf` | docket sheet | `b85de5b8...` |
| `pacer -- racketeering -- superseding indictment.pdf` | 50 | `6524fab7...` |
| `pacer -- racketeering -- second superseding indictment.pdf` | 245 (redacted) | `f602adbb...` |
| `pacer -- racketeering -- statement of offense.pdf` | 257 (Tangeman) | `0d7d3471...` |
| `pacer -- racketeering -- sentencing memorandum.pdf` | 318 (gov't, Tangeman) | `82b88df8...` |

Extracted text and Layer-1 `process_document_file` graphs in
`mcp_outputs/`. The statement of offense and superseding indictment are
scanned PDFs and required OCR.

## Modeling notes

- **The enterprise is a node.** `rico:RacketeeringEnterprise`
  (subclass of `uco-identity:Organization`) with
  `enterpriseType: association-in-fact`; charged purposes verbatim in
  the description; membership as `Member_Of` relationships.
- **Roles are nodes.** Six `rico:EnterpriseRole` nodes with
  `roleFunction` (`database-hacker` ... `residential-burglar`),
  `Has_Role` from persons and `Role_Within` to the enterprise, following
  the indictment's "Defendants' Roles in the Enterprise" section
  (¶¶ 28-32).
- **Predicates are queryable.** All fifteen RICO charge nodes carry the
  eight § 1961(1) predicate categories as `rico:predicateStatute`
  values.
- **Per-defendant per-count charges, docket labels verbatim.** 41
  `legalproc:CriminalCharge` nodes on each defendant's operative
  instrument, with PACER's `1`/`1s`/`1ss` suffixes in `countLabel` and
  dispositions from the docket (`pending`, `convicted-by-plea`,
  `dismissed`). Tangeman's count-label discrepancy (minute entry
  "1ss" vs. docket-header terminated counts "1, 3, 3s") is recorded, not
  resolved.
- **Crypto evidence via `cryptoinv`.** Forfeiture items C1/C2 as
  observables with `CryptocurrencyAddressFacet` +
  `VirtualAssetHoldingFacet` (addresses flagged as OCR-transcribed);
  Thorswap and eXch as `VirtualAssetServiceProvider`;
  `launderingTechnique` values on the laundering actions.
- **Source fidelity.** Victims stay "Victim-1"–"Victim-9"; unindicted
  associates keep their designations (COCONSPIRATOR M.F., MONEY
  EXCHANGER-1) without speculating about identity; court dates render at
  local midnight Eastern with seasonal offsets.

## Build and validate

```bash
python3 examples/pacer/ddc_2024_cr_00417/build_lam_ddc_2024_racketeering.py
```

The builder writes `lam-ddc-2024-racketeering.jsonld` (276 nodes),
recomputes source hashes from the PDFs beside the script, and validates
against CASE 1.4.0 plus the `legalproc`, `rico`, and `cryptoinv`
extension ontologies (Conforms: True).
