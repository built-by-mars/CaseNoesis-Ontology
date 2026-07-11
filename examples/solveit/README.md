# SOLVE-IT worked example — laptop acquisition

Synthetic (Tier T0) worked example behind
`docs/recipes/solve-it-investigation-planning.md`: a seized laptop SSD is
imaged and hash-verified, with every step documented against the
[SOLVE-IT](https://solveit-df.org) knowledge base vendored in
`ontology/solveit/`.

What it demonstrates:

- Stating the investigation objective (DFO-1006 "Acquire data").
- Recording the acquisition as a `solveit-core:SolveitInvestigativeAction`
  with `usedTechnique` (DFT-1002) and `appliedMitigation` (DFM-1003,
  DFM-1004) pointing at canonical knowledge-base IRIs.
- SOLVE-IT observables: `PhysicalImageContainer` containing a `Bitstream`,
  plus a `HashVerificationResult`.
- Error Mitigation Analysis: risk-rating weakness DFW-1004 with
  `solveit-wa:WeaknessEvaluation` (likelihood x impact).
- The UCO 1.5.0 metaclass style: an action typed directly with the punned
  technique class `solveit-data:techniqueDFT-1042`.

Rebuild and validate:

```bash
.venv/bin/python examples/solveit/build_laptop_acquisition_solveit.py
```

The builder writes `laptop-acquisition-solveit.jsonld` and runs
`case_validate` with `extensions=["solveit"]` (must conform).
