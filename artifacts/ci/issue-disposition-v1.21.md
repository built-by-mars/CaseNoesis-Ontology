# v1.21.0 issue disposition (#59–#73)

**Verified executable-code SHA:** `d5b6987bce18a2797fd0f53ebedfd438e03e2a9d`  
(CI: https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29215329562 · CodeQL: https://github.com/vulnmaster/CASE-UCO-SDK/actions/runs/29215329710 · open code-scanning alerts: 0)

Prior green feature SHA: `1b22f43818772684b3443165f7bdfc5df7da57bc` (recipe-gate import fix). `d5b6987` adds only a CodeQL hygiene deletion of a repeated test import.

**Release tag target:** `v1.21.0`  
The final tag commit may contain documentation/evidence-only changes after this verified code SHA.

**Scope policy:** v1.21 ships a deliberately scoped cross-ontology stack; remaining original acceptance breadth moves to v1.22 unless listed completed below.

## #59 BFO/gUFO — scoped complete for v1.21
| Acceptance | Disposition | Evidence |
|---|---|---|
| Selection matrix + six mappings + anti-patterns | Completed | `docs/recipes/foundational-typing-bfo-gufo.md`, builders |
| BFO process (BFO_0000015) not spatiotemporal region | Completed | BFO exemplar |
| Category-error negative fixture | Completed | `invalid_category_mistake.jsonld` + recipe gate |
| Explicit MCP routing distinction tests | Deferred v1.22 | Follow-up on routing eval corpus |

## #60 PROV-O — partial; breadth deferred
| Acceptance | Disposition | Evidence |
|---|---|---|
| Minimal examiner/activity/source/image/tool chain | Completed | `examples/upper-ontology/prov-o-lineage/` |
| Full two-agent / three-activity / delegation / invalidation / replacement / queries / negative fixture | Deferred v1.22 | Expand exemplar |

## #61 OWL-Time — partial; breadth deferred
| Acceptance | Disposition | Evidence |
|---|---|---|
| Closed + open intervals, native action times | Completed | `examples/upper-ontology/owl-time/` |
| Source vs normalized time, auth-overlap queries, invalid fixture | Deferred v1.22 | Expand exemplar |

## #62 GeoSPARQL — substantial; queries deferred
| Acceptance | Disposition | Evidence |
|---|---|---|
| Point, warrant, sector, route, analyst polygon + PROV derivation | Completed | geosparql builder + gate |
| Outside observation, invalid geom fixture, within/nearest/distance queries | Deferred v1.22 | Expand exemplar |

## #63 FOAF/ORG — strong partial
| Acceptance | Disposition | Evidence |
|---|---|---|
| Org/unit/role/membership/post/shared account + person-as-account fixture | Completed | foaf-org exemplar + expect_invalid |
| Structured attribution confidence + SPARQL competency queries | Deferred v1.22 | Expand exemplar |

## #64 PROF — scoped complete with warning disposition
| Acceptance | Disposition | Evidence |
|---|---|---|
| Profile + ResourceDescriptor + versioned reports + PROV validation activity | Completed | prof-metadata exemplar |
| Expected NonExistentCDOConceptWarning for UCO namespace root | Accepted (documented) | `artifacts/ci/prof-warnings-disposition.md` |
| Fail-closed malformed profile fixture | Deferred v1.22 | Add expect_invalid |

## #65 SOLVE-IT — strong partial
| Acceptance | Disposition | Evidence |
|---|---|---|
| Plan ≠ execution; qualified Association; invalidation; weakness evals | Completed | solveit-plan-execution exemplar |
| Omitted mitigation, residual-risk, plan-vs-execution queries, negative fixture | Deferred v1.22 | Expand exemplar |

## #66 Composition — core complete; breadth deferred
| Acceptance | Disposition | Evidence |
|---|---|---|
| Ordered routing + primary composition recipe | Completed | `investigation_router.py` |
| Multi-profile composite (gUFO/PROV/Time/Geo/FOAF/ORG) | Completed | composition exemplar |
| Relationship-kind registry + lint in recipe gate | Completed (scoped) | `relationship_kinds.py` + tests + runner |
| Full CAC/SOLVE-IT/AI progressive set, other-language RDF round-trip, performance | Deferred v1.22 | Epic remainder |

## #67 Graph API — core complete; perf → #73
| Acceptance | Disposition | Evidence |
|---|---|---|
| Deep-copy get, named policies, multi-type, context collision, UTF-8 Java | Completed | four language CaseGraph + tests |
| 1K/10K/100K performance acceptance | Deferred / moved to #73 | Python bench only |

## #68 Validation bundle — core complete
| Acceptance | Disposition | Evidence |
|---|---|---|
| Literal same-bundle SHACL+coverage, structured profile_not_selected, portable manifests | Completed | validation_bundle + concept_coverage |
| Cold/warm resolution + peak-memory benchmarks | Deferred v1.22 | Under #73 |

## #69 Recipe quality gate — narrowed for v1.21
| Acceptance | Disposition | Evidence |
|---|---|---|
| Upper-ontology exemplar gate (9 recipes), fail-closed promote without metadata | Completed | recipe-execution.json + promote_recipe |
| Repository-wide operational catalog migration + competency queries on all recipes | Deferred v1.22 | Explicit rename/narrow |

## #70–#73 — experimental; retargeted to v1.22
| Issue | Disposition |
|---|---|
| #70 class registry cache | Experimental Python foundation → v1.22 cross-language |
| #71 streaming serialization | Experimental Python → v1.22 four languages |
| #72 partitioning | Experimental label/boundary → v1.22 dependency-aware |
| #73 benchmarks | Python harness → v1.22 cross-language CI matrix |
