# Code-scanning disposition — second pass (32 remaining)

Source: open alerts fetched 2026-07-12 from
`repos/vulnmaster/CASE-UCO-SDK/code-scanning/alerts?state=open`.

| # | Rule | Path | Disposition | Fix |
|---|------|------|-------------|-----|
| 418 | cs/linq/missed-where | CaseGraph.cs MergeTypes | fixed | `AddRange(...Where(...))` |
| 426 | cs/linq/missed-select | CaseGraph.cs typed rehydrate | fixed | `Select`/`Where`/`Distinct` |
| 437 | cs/linq/missed-where | merge_identical loop | fixed | `raw.Where(...)` |
| 438 | cs/linq/missed-where | merge_compatible loop | fixed | `raw.Where(...)` |
| 439 | cs/linq/missed-where | AccumulateListValue | fixed | `Where` instead of continue |
| 440–443 | cs/inefficient-containskey | CaseGraph.cs | fixed | `TryGetValue` |
| 444–445 | py/empty-except | knowledge_lifecycle.py | fixed | log + comment |
| 446 | py/empty-except | run_recipe_examples.py | fixed | log + comment |
| 447 | py/unused-import | knowledge_lifecycle.py | fixed | removed `tempfile` |
| 448 | py/multiple-definition | run_recipe_examples.py | fixed | direct `return` exit codes |
| 449 | py/unused-local-variable | solveit builder | fixed | drop unused bind |
| 450 | py/unused-local-variable | foaf-org builder | fixed | drop unused bind |
| 451 | py/unused-local-variable | geosparql builder | fixed | drop unused bind |
| 452–466 | py/unused-local-variable | phantom_gate_longtail.py | fixed | required-key check loop |

**Counts:** 32 fixed, 0 false_positive, 0 accepted_debt.
