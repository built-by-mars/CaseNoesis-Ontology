# U.S. v. Grayson et al. — Murder-for-Hire (W.D. Tenn.)

Validated CASE/UCO exemplar for **2:23-cr-20121-TLP** (W.D. Tenn.,
Memphis): the murder-for-hire prosecution of Ashley Grayson and her
husband Joshua Grayson under **18 U.S.C. § 1958** (Use of Interstate
Facility in Commission of Murder-for-Hire).

## Case summary

Ashley Grayson, 35, of Dallas, Texas, ran an internet-based business and
gained notoriety online. After a 2021 falling out with a Southaven,
Mississippi woman who ran a similar online business — Grayson suspected
her of creating fake online profiles criticizing her — Grayson offered a
Memphis couple at least $20,000 per killing to murder three people: the
Southaven woman, Grayson's former boyfriend, and a Texas woman who had
posted negatively about her. On 2022-09-10 the Memphis woman
video-recorded a call in which Grayson confirmed she wanted the Southaven
woman killed as soon as possible and offered an extra $5,000 to do it
within a week. The couple staged a failed "attempt" using a photo of
police lights from an unrelated Memphis incident and collected $10,000
from the Graysons in Dallas.

A July 2023 grand jury returned a one-count § 1958 indictment against
both spouses. After a five-day jury trial in March 2024, the jury
convicted Ashley and acquitted Joshua. On 2024-10-31 Judge Thomas L.
Parker sentenced Ashley Grayson to 120 months — the statutory maximum —
plus three years of supervised release. The Sixth Circuit affirmed
(No. 24-5988, 2025-08-14) and the Supreme Court granted certiorari
(No. 25-851, writ issued 2026-06-24).

## Sources

| File | SHA-256 |
|---|---|
| `pacer -- murder for hire -- docket.pdf` | `30a244c6...84f8fa` |
| `pacer -- murder for hire -- press release.pdf` | `d1f9b0d3...1907a4` |

Extracted text in `mcp_outputs/`.

## Modeling notes

- **Per-defendant charges on a shared count.** The single § 1958 count
  was charged against both defendants but resolved oppositely, so each
  defendant gets their own `legalproc:CriminalCharge` node
  (`convicted-at-trial` vs. `acquitted-at-trial`) — mirroring how PACER
  tracks counts per defendant.
- **Verdicts per outcome.** Separate guilty and not-guilty
  `legalproc:Verdict` nodes, each linked to its charge via
  `concernsCharge` and to the trial via `Occurred_During`.
- **Full appellate ladder.** `legalproc:CriminalProceeding` nodes for the
  jury trial, sentencing, the Sixth Circuit appeal (`proceedingType:
  appeal`), and Supreme Court review (`proceedingType: certiorari`),
  chained with `Reviews` relationships (certiorari → appeal → sentence).
- **Interstate-facility evidence as observables.** The video-recorded
  2022-09-10 call is a `uco-observable:Call`; the fake profiles, the
  Texas woman's negative posts, the staged police-lights photo, and the
  government's Trial Exhibit 5 (Apple iPhone extraction report, D.E. 231)
  are `ObservableObject`s.
- **Source fidelity.** Intended victims are identified by role only (no
  names appear in the sources); the judgment's no-contact initials D.H.,
  S.H., and P.T. are kept verbatim without mapping them to victims. The
  fake-profile attribution is recorded as Grayson's suspicion, not fact.

## Build and validate

```bash
.venv/bin/python examples/pacer/wdtn_2023_cr_20121/build_grayson_wdtn_2023_murder_for_hire.py
```

The builder writes `grayson-wdtn-2023-murder-for-hire.jsonld` (93 nodes)
and validates it with `case_validate` against CASE 1.4.0 plus the
`legalproc` extension ontology (Conforms: True).
