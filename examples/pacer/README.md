# PACER / ICAC Federal Court Examples

Validated CASE/UCO/CAC knowledge graphs built from public PACER PDFs using the CASE/UCO MCP document pipeline.

## Agent workflow

1. **`process_document_file`** — extract text + Layer 1 CASE/UCO graph per PDF
2. **`route_investigation_content`** — detect the investigation type and get recipes/extensions (then **`route_cac_content`** for the deep CAC checklists when CAC is detected)
3. **Build script** — agent-authored Layer 2–3 graph (see `build_*.py`)
4. **`validate_graph(..., extensions=[...])`** — required before returning to caller (`cac` for CAC cases, `legalproc` for general prosecutions, `cryptoinv` for crypto cases)

Full recipe: [`docs/recipes/cac-pacer-document-ingestion.md`](../docs/recipes/cac-pacer-document-ingestion.md)

## Cases

| Folder | Docket | Documents | Status |
|---|---|---|---|
| [`anchorage_pd_2022_004/`](anchorage_pd_2022_004/) | `3:20-cr-00029-SLG-MMS` (D. Alaska) | Indictment, trial brief, judgment | Merged validated graph (193 nodes; granular trial-brief evidence + supervision conditions; source-fidelity reviewed — no fabricated timestamps) |
| [`doj_ceos_2025_014/`](doj_ceos_2025_014/) | `1:20-cr-00252-JLT-BAM` (E.D. Cal.) | Trial brief, plea agreement | Validated |
| [`doj_ceos_2026_012/`](doj_ceos_2026_012/) | `1:25-cr-00069-WCG` (E.D. Wis.) | Judgment (AO 245B) | Validated |
| [`usss_2017_006/`](usss_2017_006/) | USSS complaint pattern | Criminal complaint | Validated |
| [`doj_crypto_2023_239/`](doj_crypto_2023_239/) | `1:23-cr-00239-CKK` (D.D.C.) | Information, statement of facts, statement of offense, plea agreement, sentencing memorandum | Validated (Bitfinex hack laundering; uses the `cryptoinv` extension — crypto facets + legal process; two scanned PDFs required OCR) |
| [`wdmo_2022_cr_04065/`](wdmo_2022_cr_04065/) | `2:22-cr-04065-BCW` (W.D. Mo.) | Docket, third superseding indictment, sentencing memorandum | Validated (militia conspiracy / attempted murder of FBI agents; **non-CAC case** — uses the `legalproc` extension for 45 counts with conspiracy/attempt/derivative offense forms, § 924(c) `objectOffense` links, verdicts, mid-trial plea, life sentences, forfeiture, restitution) |
| [`edla_2022_cr_00115/`](edla_2022_cr_00115/) | `2:22-cr-00115-ILRL-KWR` (E.D. La.) | Docket, superseding indictment, factual basis, judgment | Validated (elder fraud / Treasury-impersonation money couriers; **non-CAC case** — `legalproc` extension with per-defendant dispositions (plea vs. dismissal), deferred/amended restitution, hybrid cyber evidence (spoofed calls, dispatch texts, payment cards, cell-site records) + gUFO-typed physical handoff items; two scanned PDFs required OCR; drove the `elder-fraud-impersonation.md` recipe) |
| [`ndca_2024_cr_00141/`](ndca_2024_cr_00141/) | `3:24-cr-00141-VC` (N.D. Cal.) | Indictment, superseding indictment, second superseding indictment, WeChat thread translation, jury verdict | Validated (insider threat / Google AI trade secrets, U.S. v. Linwei Ding; **non-CAC case** — `legalproc` extension with a three-instrument charging chain, per-category § 1832 theft + § 1831 economic-espionage counts, 14 guilty jury verdicts, forfeiture allegation; exfiltration action wired with instruments (MacBook + Apple Notes), 7 trade-secret-category observables, corporate detection chain vs. FBI warrant chain, gUFO-typed access badge; verdict form and WeChat exhibit required OCR; drove the `insider-threat-trade-secrets.md` recipe) |
| [`dma_2023_cr_10159/`](dma_2023_cr_10159/) | `1:23-cr-10159-IT` (D. Mass.) | Indictment, plea agreement, sentencing memorandum | Validated (Espionage Act / classified NDI leaks to Discord, U.S. v. Jack Douglas Teixeira; **non-CAC case** — `legalproc` extension with complaint → indictment chain, six § 793(e) counts, Rule 11(c)(1)(C) plea, forfeiture, 200-month recommended sentence; **first exemplar using UCO's `uco-marking` namespace** — per-count TS//SCI and SECRET classification banners as `MarkingDefinition` + `StatementMarking` via `uco-core:objectMarking`, with the defendant's contradictory 'TS//NOFORN//FVEY' quote preserved as message content, not a marking; gUFO-typed SCIF and paper printouts; indictment and plea agreement required OCR; drove the `espionage-classified-disclosure.md` recipe) |
| [`ndca_2020_cr_00446/`](ndca_2020_cr_00446/) | `3:20-cr-00446-WHA` (N.D. Cal.) | Docket, indictment, government sentencing memorandum | Validated (export control / IEEPA, U.S. v. Han Li and Lin Chen; **non-CAC case** — `legalproc` extension with per-defendant charges on four shared counts (Chen: plea to Count 4 + three dismissals; Li: all pending), sealed indictment unsealed at a 2024 border arrest with warrant `Authorization`, 27-month/$255,000 recommended vs. 4-month/$5,000 imposed sentence pair, forfeiture allegation; dated Entity List designation Actions (GaStone 2014, CETC 55 2018) gating lawfulness, gUFO-typed DTX-150 wafer scriber + consumables with EAR99 in descriptions, false EEI/AES filing as the cyber observable, papered-consignee (JHI/Nanjing) vs. true-end-user (GaStone/Chengdu) concealment chain; indictment PDF had CID-mapped text that stripped digits and required re-OCR; drove the `export-control-sanctions.md` recipe) |
| [`wdtn_2023_cr_20121/`](wdtn_2023_cr_20121/) | `2:23-cr-20121-TLP` (W.D. Tenn.) | Docket, press release | Validated (murder-for-hire, U.S. v. Grayson et al.; **non-CAC case** — `legalproc` extension with per-defendant charge nodes on a single shared § 1958 count (jury conviction vs. jury acquittal), trial/sentencing/appellate/certiorari proceedings, 120-month imposed sentence) |
| [`ndnd_2025_cr_00005/`](ndnd_2025_cr_00005/) | `3:25-cr-00005-PDW` (D.N.D.) | Second superseding indictment, plea agreement, judgment | Validated (kidnapping-for-ransom over a drug debt, U.S. v. Lindell et al.; **non-CAC case** — `legalproc` extension plus **first exemplars of the `weapons` and `drugs` extensions**: SIG Sauer P365 as `weap:Handgun` with make/model/caliber/serial, charged 500-gram methamphetamine mixture as `drug:ControlledSubstance` with ChEBI identity; § 924(c) `objectOffense` links, 360-month sentence; drove the `weapons-drug-evidence.md` recipe) |
| [`ddc_2024_cr_00417/`](ddc_2024_cr_00417/) | `1:24-cr-00417-CKK` (D.D.C.) | Docket, superseding indictment, second superseding indictment, statement of offense, sentencing memorandum | Validated (RICO conspiracy / $245M crypto theft by the "SE Enterprise", U.S. v. Lam et al.; **non-CAC case** — **first exemplar of the `rico` extension**: the association-in-fact enterprise as `rico:RacketeeringEnterprise`, six `rico:EnterpriseRole` nodes (database hacker → residential burglar), eight § 1961(1) predicate categories as `rico:predicateStatute` on every RICO count; `legalproc` for 3 charging instruments, 41 per-defendant charges with docket dispositions (PACER `1`/`1s`/`1ss` suffixes verbatim), 9 guilty pleas, 3 imposed sentences; `cryptoinv` for forfeiture USDT addresses, no-KYC exchanges (Thorswap, eXch), and `launderingTechnique` values (peel-chain, chain-hopping-to-monero, crypto-to-cash); obstruction chain (phone into Biscayne Bay, remote camera surveillance of the FBI search, directed device destruction); two scanned PDFs required OCR; drove the `racketeering-enterprise.md` recipe and the `rico` extension) |

## Running the Anchorage PD 2022-004 exemplar

```bash
# Layer 1 — MCP document normalize (already run into output/icac_pacer/)
# Re-run from repo root if needed:
# process_document_file via MCP or:
python3 -m document_processor_cli \
  "/mnt/c/.../pacer -- anchorage_pd_2022_004 -- indictment.pdf" \
  output/icac_pacer/anchorage_pd_2022_004/indictment.jsonld

# Layer 2–3 — merged CAC graph + validation
python3 examples/pacer/anchorage_pd_2022_004/build_moore_dalaska_2020_case.py
```

Output: `examples/pacer/anchorage_pd_2022_004/moore-dalaska-2020-icac.jsonld`

MCP extraction artifacts for this case live under `output/icac_pacer/anchorage_pd_2022_004/` (`indictment.jsonld`, `trial_brief.jsonld`, `judgment.jsonld`, `extracted-content.json`, `annotations.jsonld`).

## Filename convention

```text
pacer -- <local_case_ref> -- <document_type>.pdf
```

Use `<local_case_ref>` as the output directory slug; use the ECF case number from the PDF body as `cacontology:caseNumber` in the graph.
