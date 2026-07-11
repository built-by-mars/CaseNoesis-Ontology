"""Queryable index over the vendored SOLVE-IT knowledge base.

SOLVE-IT (Systematic Objective-based Listing of Various Established digital
Investigation Techniques, https://solveit-df.org) organizes digital forensic
practice as objectives -> techniques -> weaknesses -> mitigations, with
weaknesses classified by ASTM E3016-18 error category. The SDK vendors the
upstream-compiled RDF knowledge base at
``extensions/solveit/solve-it-kb.ttl`` (pinned by
``mcp_server/tools/sync_solveit.py``); this module parses it once and serves
the MCP tools ``search_solveit``, ``get_solveit_details``, and
``plan_solveit_workflow``.

Everything returned is bounded, plain-text metadata from the pinned
knowledge base — no caller-supplied content is echoed back beyond the query
terms used for matching.
"""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_PATH = PROJECT_ROOT / "extensions" / "solveit" / "solve-it-kb.ttl"

SOLVEIT_CORE = "https://ontology.solveit-df.org/solveit/core/"

KINDS = ("objective", "technique", "weakness", "mitigation")

# Bounds on tool output (privacy/context-size posture matches the routers).
MAX_SEARCH_RESULTS = 25
MAX_LINKED_ITEMS = 40
MAX_PLAN_OBJECTIVES = 5
MAX_PLAN_TECHNIQUES = 8
MAX_TEXT = 600


@dataclass
class SolveItRecord:
    """One knowledge-base entry (objective, technique, weakness, or mitigation)."""

    item_id: str
    kind: str
    name: str
    iri: str
    description: str = ""
    details: str = ""
    synonyms: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    astm_categories: tuple[str, ...] = ()
    case_input_classes: tuple[str, ...] = ()
    case_output_classes: tuple[str, ...] = ()
    # Cross-references, all by SOLVE-IT identifier (DFT-*/DFW-*/DFM-*/DFO-*).
    technique_ids: tuple[str, ...] = ()      # objective -> techniques; mitigation -> techniques
    subtechnique_ids: tuple[str, ...] = ()   # technique -> subtechniques
    weakness_ids: tuple[str, ...] = ()       # technique -> weaknesses
    mitigation_ids: tuple[str, ...] = ()     # weakness -> mitigations
    objective_ids: tuple[str, ...] = ()      # technique -> objectives (reverse)
    name_tokens: frozenset[str] = field(default=frozenset(), repr=False)
    body_tokens: frozenset[str] = field(default=frozenset(), repr=False)


@dataclass
class SolveItIndex:
    records: dict[str, SolveItRecord]
    kb_path: Path

    def by_kind(self, kind: str) -> list[SolveItRecord]:
        return [r for r in self.records.values() if r.kind == kind]


_INDEX: SolveItIndex | None = None
_INDEX_LOCK = threading.Lock()
_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9._-]+")

# Common words that would otherwise dominate overlap scoring.
_STOPWORDS = frozenset({
    "and", "are", "com", "can", "could", "data", "for", "from", "has", "have",
    "how", "into", "its", "may", "need", "not", "one", "our", "that", "the",
    "them", "then", "there", "these", "this", "was", "were", "what", "when",
    "which", "will", "with", "would", "you", "your",
})


def _truncate(text: str, limit: int = MAX_TEXT) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "\u2026"


def _tokens(text: str) -> set[str]:
    return {t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS}


def load_index(kb_path: Path = KB_PATH, *, force: bool = False) -> SolveItIndex:
    """Parse the vendored KB once and cache the resulting index."""

    global _INDEX
    with _INDEX_LOCK:
        if _INDEX is not None and not force and _INDEX.kb_path == kb_path:
            return _INDEX

        import rdflib
        from rdflib import RDF, RDFS, URIRef

        if not kb_path.is_file():
            raise FileNotFoundError("solveit_kb_missing")
        graph = rdflib.Graph()
        graph.parse(str(kb_path), format="turtle")

        core = SOLVEIT_CORE

        def values(node, prop) -> tuple[str, ...]:
            return tuple(sorted(str(v) for v in graph.objects(node, URIRef(core + prop))))

        def one(node, prop) -> str:
            value = graph.value(node, URIRef(core + prop))
            return str(value) if value is not None else ""

        records: dict[str, SolveItRecord] = {}
        iri_to_id: dict[str, str] = {}

        kind_specs = [
            ("objective", "Objective", "objectiveID", "objectiveName", "objectiveDescription"),
            ("technique", "Technique", "techniqueID", "techniqueName", "techniqueDescription"),
            ("weakness", "Weakness", "weaknessID", "weaknessName", "weaknessDescription"),
            ("mitigation", "Mitigation", "mitigationID", "mitigationName", "mitigationDescription"),
        ]
        nodes_by_kind: dict[str, list] = {}
        for kind, class_name, id_prop, name_prop, desc_prop in kind_specs:
            for node in graph.subjects(RDF.type, URIRef(core + class_name)):
                item_id = one(node, id_prop)
                if not item_id:
                    continue
                record = SolveItRecord(
                    item_id=item_id,
                    kind=kind,
                    name=one(node, name_prop) or item_id,
                    iri=str(node),
                    description=one(node, desc_prop),
                )
                records[item_id] = record
                iri_to_id[str(node)] = item_id
                nodes_by_kind.setdefault(kind, []).append(node)

        def linked_ids(node, prop) -> tuple[str, ...]:
            ids = []
            for target in graph.objects(node, URIRef(core + prop)):
                target_id = iri_to_id.get(str(target))
                if target_id:
                    ids.append(target_id)
            return tuple(sorted(ids))

        for node in nodes_by_kind.get("objective", []):
            record = records[iri_to_id[str(node)]]
            record.technique_ids = linked_ids(node, "includesTechnique")

        for node in nodes_by_kind.get("technique", []):
            record = records[iri_to_id[str(node)]]
            record.details = one(node, "techniqueDetails")
            record.synonyms = values(node, "hasSynonym")
            record.examples = values(node, "hasExample")
            record.case_input_classes = values(node, "hasCASEInputClass")
            record.case_output_classes = values(node, "hasCASEOutputClass")
            record.weakness_ids = linked_ids(node, "hasPotentialWeakness")
            record.subtechnique_ids = linked_ids(node, "hasSubtechnique")

        for node in nodes_by_kind.get("weakness", []):
            record = records[iri_to_id[str(node)]]
            record.mitigation_ids = linked_ids(node, "hasPotentialMitigation")
            categories = []
            for cat in graph.objects(node, URIRef(core + "hasWeaknessClass")):
                label = graph.value(cat, RDFS.label)
                categories.append(str(label) if label else str(cat).rsplit("/", 1)[-1])
            record.astm_categories = tuple(sorted(categories))

        for node in nodes_by_kind.get("mitigation", []):
            record = records[iri_to_id[str(node)]]
            record.technique_ids = linked_ids(node, "linksToTechnique")

        # Reverse link: technique -> objectives that include it.
        for objective in (r for r in records.values() if r.kind == "objective"):
            for tech_id in objective.technique_ids:
                tech = records.get(tech_id)
                if tech is not None:
                    tech.objective_ids = tuple(sorted(set(tech.objective_ids) | {objective.item_id}))

        for record in records.values():
            record.name_tokens = frozenset(
                _tokens(" ".join([record.item_id, record.name] + list(record.synonyms)))
            )
            record.body_tokens = frozenset(
                _tokens(" ".join([record.description, record.details] + list(record.examples)))
            )

        _INDEX = SolveItIndex(records=records, kb_path=kb_path)
        return _INDEX


def clear_index_cache() -> None:
    global _INDEX
    with _INDEX_LOCK:
        _INDEX = None


def _token_matches(token: str, vocabulary: frozenset[str]) -> bool:
    """Exact token match with a light singular/plural fallback."""

    if token in vocabulary:
        return True
    if token.endswith("s") and token[:-1] in vocabulary:
        return True
    return (token + "s") in vocabulary


def _score(record: SolveItRecord, query_tokens: set[str], query: str) -> float:
    if not query_tokens:
        return 0.0
    weighted = 0.0
    for token in query_tokens:
        if _token_matches(token, record.name_tokens):
            weighted += 2.0
        elif _token_matches(token, record.body_tokens):
            weighted += 1.0
    score = weighted / (2.0 * len(query_tokens))
    if query.strip().lower() == record.item_id.lower():
        score += 10.0  # exact identifier lookup always wins
    elif query.strip().lower() in record.name.lower():
        score += 0.5
    return score


def _summary(record: SolveItRecord) -> dict:
    payload = {
        "id": record.item_id,
        "kind": record.kind,
        "name": _truncate(record.name, 200),
        "iri": record.iri,
    }
    if record.description:
        payload["description"] = _truncate(record.description, 300)
    if record.astm_categories:
        payload["astm_categories"] = list(record.astm_categories)
    return payload


def search(query: str, kind: str | None = None, limit: int = 10) -> dict:
    """Keyword search across the knowledge base; bounded, ranked results."""

    index = load_index()
    limit = max(1, min(int(limit), MAX_SEARCH_RESULTS))
    if kind is not None and kind not in KINDS:
        return {
            "error": "unknown_kind",
            "detail": f"kind must be one of {', '.join(KINDS)}",
        }
    query_tokens = _tokens(query)
    scored: list[tuple[float, SolveItRecord]] = []
    for record in index.records.values():
        if kind and record.kind != kind:
            continue
        score = _score(record, query_tokens, query)
        if score > 0:
            scored.append((score, record))
    scored.sort(key=lambda pair: (-pair[0], pair[1].item_id))
    return {
        "query": _truncate(query, 200),
        "kind": kind or "all",
        "total_matches": len(scored),
        "results": [_summary(record) for _, record in scored[:limit]],
        "knowledge_base": _kb_provenance(),
    }


def _expand(index: SolveItIndex, ids: tuple[str, ...], limit: int = MAX_LINKED_ITEMS) -> list[dict]:
    expanded = []
    for item_id in ids[:limit]:
        record = index.records.get(item_id)
        if record:
            expanded.append(_summary(record))
    return expanded


def details(item_id: str) -> dict:
    """Full record for one SOLVE-IT identifier, with linked entities."""

    index = load_index()
    record = index.records.get(item_id.strip().upper())
    if record is None:
        return {
            "error": "unknown_id",
            "detail": "no objective/technique/weakness/mitigation with that "
                      "identifier in the pinned knowledge base (expected forms: "
                      "DFO-1006, DFT-1002, DFW-1004, DFM-1004)",
        }
    payload = _summary(record)
    payload["description"] = _truncate(record.description)
    if record.details:
        payload["details"] = _truncate(record.details)
    if record.synonyms:
        payload["synonyms"] = list(record.synonyms)
    if record.examples:
        payload["example_tools"] = list(record.examples)
    if record.case_input_classes:
        payload["case_input_classes"] = list(record.case_input_classes)
    if record.case_output_classes:
        payload["case_output_classes"] = list(record.case_output_classes)

    if record.kind == "objective":
        payload["techniques"] = _expand(index, record.technique_ids)
    elif record.kind == "technique":
        payload["objectives"] = _expand(index, record.objective_ids)
        if record.subtechnique_ids:
            payload["subtechniques"] = _expand(index, record.subtechnique_ids)
        weaknesses = []
        for weakness_id in record.weakness_ids[:MAX_LINKED_ITEMS]:
            weakness = index.records.get(weakness_id)
            if weakness is None:
                continue
            entry = _summary(weakness)
            entry["mitigations"] = _expand(index, weakness.mitigation_ids)
            weaknesses.append(entry)
        payload["weaknesses"] = weaknesses
        payload["modeling_guidance"] = (
            "Record execution as a solveit-core:SolveitInvestigativeAction with "
            f"solveit-core:usedTechnique <{record.iri}> and "
            "solveit-core:appliedMitigation for each mitigation actively applied; "
            "or type the action directly with the punned technique class "
            "(UCO 1.5.0 metaclass style). Validate with "
            "validate_graph(extensions=['solveit'])."
        )
    elif record.kind == "weakness":
        payload["mitigations"] = _expand(index, record.mitigation_ids)
        techniques = [
            _summary(tech) for tech in index.by_kind("technique")
            if record.item_id in tech.weakness_ids
        ][:MAX_LINKED_ITEMS]
        payload["affects_techniques"] = techniques
    elif record.kind == "mitigation":
        payload["implemented_by_techniques"] = _expand(index, record.technique_ids)
        weaknesses = [
            _summary(weak) for weak in index.by_kind("weakness")
            if record.item_id in weak.mitigation_ids
        ][:MAX_LINKED_ITEMS]
        payload["mitigates_weaknesses"] = weaknesses

    payload["knowledge_base"] = _kb_provenance()
    return payload


def plan_workflow(description: str) -> dict:
    """Map free-text investigation goals to objectives, techniques, and an
    Error Mitigation Analysis checklist.

    The description is investigator/agent-supplied planning text; it is
    treated as untrusted content — only match metadata from the pinned
    knowledge base is returned, never the submitted text (beyond a bounded
    echo of the terms that matched).
    """

    index = load_index()
    query_tokens = _tokens(description)

    technique_scores: dict[str, float] = {}
    for record in index.by_kind("technique"):
        score = _score(record, query_tokens, description)
        if score > 0:
            technique_scores[record.item_id] = score

    # Objective relevance = its own text match plus the strength of its
    # best-matching member techniques, so "image the seized drive" surfaces
    # "Acquire data" even though the objective text itself is terse.
    objectives = []
    for record in index.by_kind("objective"):
        own = _score(record, query_tokens, description)
        member = sorted(
            (technique_scores.get(tid, 0.0) for tid in record.technique_ids),
            reverse=True,
        )
        lifted = own + 0.6 * sum(member[:3])
        if lifted > 0:
            objectives.append((lifted, record))
    objectives.sort(key=lambda pair: (-pair[0], pair[1].item_id))
    top_objectives = [record for _, record in objectives[:MAX_PLAN_OBJECTIVES]]

    objective_technique_ids = {
        tech_id for objective in top_objectives for tech_id in objective.technique_ids
    }
    scored_techniques = [
        (score + (0.25 if item_id in objective_technique_ids else 0.0),
         index.records[item_id])
        for item_id, score in technique_scores.items()
    ]
    scored_techniques.sort(key=lambda pair: (-pair[0], pair[1].item_id))
    top_techniques = [record for _, record in scored_techniques[:MAX_PLAN_TECHNIQUES]]

    technique_entries = []
    for tech in top_techniques:
        entry = _summary(tech)
        checklist = []
        for weakness_id in tech.weakness_ids[:MAX_LINKED_ITEMS]:
            weakness = index.records.get(weakness_id)
            if weakness is None:
                continue
            checklist.append({
                "weakness": _summary(weakness),
                "mitigations": _expand(index, weakness.mitigation_ids, limit=10),
            })
        entry["error_mitigation_checklist"] = checklist
        technique_entries.append(entry)

    guidance = [
        "1. Confirm the objective(s) below match the investigative goal; use "
        + "get_solveit_details(objective id) to see every candidate technique.",
        "2. For each selected technique, review its error_mitigation_checklist "
        + "(weaknesses are classified per ASTM E3016-18) and decide which "
        + "mitigations to apply.",
        "3. Record each executed step as a solveit-core:SolveitInvestigativeAction "
        + "with usedTechnique and appliedMitigation, then validate the graph with "
        + "validate_graph(extensions=['solveit']).",
        "4. Optionally rate residual risk with solveit-wa:WeaknessEvaluation "
        + "(likelihood x impact), as shown in the solve-it-investigation-planning "
        + "recipe.",
    ]
    return {
        "content_trust": "untrusted-source-content",
        "matched_objectives": [_summary(record) for record in top_objectives],
        "candidate_techniques": technique_entries,
        "workflow_guidance": guidance,
        "recipe": "docs/recipes/solve-it-investigation-planning.md",
        "knowledge_base": _kb_provenance(),
    }


def _kb_provenance() -> dict:
    """Bounded provenance stamp for every tool response."""

    import json

    manifest_path = PROJECT_ROOT / "extensions" / "solveit" / "manifest.json"
    try:
        provenance = json.loads(manifest_path.read_text(encoding="utf-8")).get("provenance", {})
    except (OSError, ValueError):
        provenance = {}
    return {
        "source": "SOLVE-IT (https://solveit-df.org)",
        "release": provenance.get("knowledge_base_release", "unknown"),
        "ontology_version": provenance.get("ontology_version", "unknown"),
    }
