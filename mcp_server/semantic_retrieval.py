"""Offline lexical-semantic retrieval for investigation routing.

The deterministic keyword router (``investigation_router``) is transparent
and auditable, but it misses submissions that describe known concepts in
unfamiliar language ("my kid was blackmailed into sending photos" contains
no catalog keyword). This module adds a second, still fully offline and
deterministic, retrieval stage:

1. **Token normalization** — lowercase, punctuation-stripped, stopword-free
   tokens with light suffix folding (plural/participle endings).
2. **Synonym-group expansion** — curated groups map investigator phrasing
   (blackmail, hacked, dope, kid) onto catalog vocabulary (sextortion,
   intrusion, narcotics, minor). Groups are symmetric: both the query and
   the catalog document expand into the same group identifiers.
3. **Overlap scoring** — the semantic score is a bounded monotonic function
   of the number of distinct shared tokens/groups, with the matched evidence
   returned so every result is explainable.

No embeddings, network access, or model downloads are required, which keeps
closed/offline deployments (Link-Look) fully supported. LLM re-ranking can
be layered on by the calling agent; it is deliberately not built in so that
routing controls (extension loading, concept validation, promotion gates)
cannot be bypassed by a generative step.

Confidence calibration: ``combined_score`` and ``confidence`` are calibrated
against the labeled routing benchmark in
``mcp_server/tests/test_routing_benchmark.py`` — paraphrases route, true
negatives abstain. Tune thresholds there, not in production code reviews.
"""

from __future__ import annotations

import re
from functools import lru_cache

# Bounded monotonic confidence: combined/(combined + _CONFIDENCE_PIVOT).
_CONFIDENCE_PIVOT = 2.5
# Weight of the (0..1) semantic score relative to one keyword hit.
_SEMANTIC_WEIGHT = 3.0
# Semantic-only families need at least this semantic score to be routed
# (0.4 == two distinct evidence hits).
SEMANTIC_MATCH_THRESHOLD = 0.4
# Below this confidence the router abstains and returns extension-gap
# guidance instead of a weak guess.
ABSTAIN_CONFIDENCE = 0.30
# At or above this confidence routing is reported as "high".
HIGH_CONFIDENCE = 0.55

_STOPWORDS = frozenset(
    """a an and are as at be been but by for from had has have he her his i in
    is it its me my of on or our she that the their them they this to was we
    were which who will with you your""".split()
)

_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9.\-]{1,}")

# Curated synonym groups. Each group id joins colloquial investigator
# phrasing with the catalog vocabulary used by family/recipe keyword lists.
# Multi-word entries are matched as substrings of the normalized text.
SYNONYM_GROUPS: dict[str, tuple[str, ...]] = {
    "grp:homicide": (
        "murder", "homicide", "manslaughter", "kill", "killed", "killing",
        "stabbed", "stabbing", "shot", "shooting", "gunned", "slain",
        "strangled", "dead body",
    ),
    "grp:assault": ("assault", "assaulted", "attacked", "beaten", "battery"),
    "grp:kidnap": ("kidnapping", "kidnapped", "abduction", "abducted", "hostage"),
    "grp:weapon": (
        "firearm", "firearms", "gun", "guns", "pistol", "rifle", "handgun",
        "ammunition", "armed", "weapon", "weapons",
    ),
    "grp:drugs": (
        "narcotics", "methamphetamine", "meth", "fentanyl", "cocaine",
        "heroin", "opioid", "opioids", "dope", "controlled substance",
        "drug trafficking", "drug dealer", "drug dealing", "selling drugs",
        "distribute drugs", "pills",
    ),
    "grp:crypto": (
        "cryptocurrency", "bitcoin", "btc", "ethereum", "crypto",
        "blockchain", "wallet", "stablecoin", "tether", "usdt",
        "virtual asset", "digital currency",
    ),
    "grp:launder": (
        "laundering", "launder", "laundered", "mixer", "tumbler",
        "structuring", "smurfing", "money mule", "shell company",
    ),
    "grp:fraud": (
        "fraud", "defrauded", "scam", "scammed", "scammer", "swindle",
        "swindled", "ponzi", "pig butchering", "romance scheme",
        "investment scheme", "fake exchange",
    ),
    "grp:intrusion": (
        "intrusion", "hack", "hacked", "hacker", "hackers", "breach",
        "breached", "compromise", "compromised", "ransomware", "malware",
        "backdoor", "exploit", "exploited", "unauthorized access",
        "broke into our network", "encrypted our files",
    ),
    "grp:phishing": ("phishing", "spearphishing", "phish", "phished", "spear phishing"),
    "grp:c2": ("c2", "command and control", "beacon", "beaconing", "botnet"),
    "grp:exfil": ("exfiltration", "exfiltrated", "data theft", "stole data", "stolen data"),
    "grp:apt": (
        "apt", "nation-state", "nation state", "threat actor", "threat group",
        "implant", "cyber espionage",
    ),
    "grp:mobile": (
        "mobile", "smartphone", "iphone", "android", "cellphone",
        "cell phone", "cellebrite", "graykey", "imei", "sim card",
        "phone extraction", "phone dump",
    ),
    "grp:chat": (
        "chat", "chats", "chat log", "message", "messages", "messaging",
        "texting", "text messages", "whatsapp", "telegram", "signal",
        "imessage", "direct message", "dms", "snapchat", "discord",
    ),
    "grp:email": ("email", "emails", "mailbox", "pst", "mbox", "eml", "inbox"),
    "grp:disk": (
        "disk image", "forensic image", "e01", "dd image", "ntfs",
        "filesystem", "carving", "unallocated", "deleted files",
        "hard drive", "hash list",
    ),
    "grp:child": (
        "child", "children", "minor", "minors", "juvenile", "underage",
        "kid", "kids", "teen", "teenager", "young girl", "young boy",
        "my son", "my daughter", "13-year-old", "14-year-old", "15-year-old",
    ),
    "grp:extortion": (
        "sextortion", "blackmail", "blackmailed", "blackmailing", "extorted",
        "extorting", "threatened to share", "threatened to post",
        "demanded photos", "demanded more images",
    ),
    "grp:csam": ("csam", "child pornography", "child sexual abuse", "explicit images"),
    "grp:grooming": (
        "grooming", "groomed", "enticement", "enticing", "luring", "lured",
        "online predator", "met online",
    ),
    "grp:trafficking-person": (
        "human trafficking", "sex trafficking", "trafficked", "prostitution",
        "commercial sex",
    ),
    "grp:gang": (
        "gang", "cartel", "mafia", "syndicate", "racketeering", "rico",
        "criminal enterprise", "organized crime", "crime family", "mob",
        "street crew",
    ),
    "grp:court": (
        "indictment", "indicted", "docket", "plea", "sentencing",
        "arraignment", "pacer", "judgment", "verdict", "grand jury",
        "prosecutor", "court filing", "charged with", "criminal complaint",
    ),
    "grp:espionage": (
        "espionage", "spy", "spying", "classified", "clearance",
        "top secret", "leaked documents", "unauthorized disclosure",
        "foreign intelligence",
    ),
    "grp:sanctions": (
        "sanctions", "embargo", "ofac", "export control", "itar",
        "export license", "entity list", "dual-use",
    ),
    "grp:insider": (
        "insider threat", "internal investigation", "policy violation",
        "whistleblower", "trade secret", "trade secrets", "departing employee",
        "hr investigation", "workplace investigation",
    ),
    "grp:ediscovery": (
        "e-discovery", "ediscovery", "legal hold", "litigation hold",
        "deposition", "custodian", "interrogatories", "civil action",
        "class action", "discovery request",
    ),
    "grp:wiretransfer": ("wire fraud", "wire transfer", "bank fraud", "bank account"),
    "grp:darknet": ("darknet", "dark web", "tor", "hidden service", "onion"),
}


def _fold(token: str) -> str:
    """Light suffix folding so plural/participle variants align."""

    for suffix in ("ing", "ers", "ies", "es", "ed", "er", "s"):
        if token.endswith(suffix) and len(token) - len(suffix) >= 4:
            return token[: -len(suffix)]
    return token


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def tokenize(text: str) -> set[str]:
    tokens: set[str] = set()
    for raw in _TOKEN_RE.findall(normalize(text)):
        raw = raw.strip(".-")
        if len(raw) < 3 or raw in _STOPWORDS:
            continue
        tokens.add(_fold(raw))
    return tokens


@lru_cache(maxsize=1)
def _group_index() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """(single-token entry -> groups, phrase entry -> groups) lookup tables."""

    token_map: dict[str, set[str]] = {}
    phrase_map: dict[str, set[str]] = {}
    for group_id, entries in SYNONYM_GROUPS.items():
        for entry in entries:
            entry_norm = normalize(entry)
            if " " in entry_norm or "-" in entry_norm:
                phrase_map.setdefault(entry_norm, set()).add(group_id)
            else:
                token_map.setdefault(_fold(entry_norm), set()).add(group_id)
    return token_map, phrase_map


def expand(text: str) -> set[str]:
    """Tokens plus every synonym-group id the text triggers."""

    token_map, phrase_map = _group_index()
    normalized = normalize(text)
    expanded = tokenize(text)
    for token in list(expanded):
        for group in token_map.get(token, ()):
            expanded.add(group)
    for phrase, groups in phrase_map.items():
        if phrase in normalized:
            expanded.update(groups)
    return expanded


def semantic_score(query_text: str, document_text: str) -> tuple[float, list[str]]:
    """Bounded (0..1) overlap score plus matched-evidence terms.

    Only synonym-group hits and distinctive shared tokens (length >= 5)
    count as evidence, which keeps generic words from inflating scores.
    """

    query = expand(query_text)
    document = expand(document_text)
    shared = query & document
    evidence = sorted(
        term for term in shared if term.startswith("grp:") or len(term) >= 5
    )
    score = len(evidence) / (len(evidence) + 3.0)
    return score, evidence[:10]


def combined_confidence(keyword_score: int, semantic: float) -> float:
    """Calibrated 0..1 confidence from both retrieval stages."""

    combined = keyword_score + _SEMANTIC_WEIGHT * semantic
    return round(combined / (combined + _CONFIDENCE_PIVOT), 3)


def confidence_level(confidence: float) -> str:
    if confidence < ABSTAIN_CONFIDENCE:
        return "abstain"
    if confidence < HIGH_CONFIDENCE:
        return "low"
    return "high"
