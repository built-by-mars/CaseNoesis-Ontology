"""Controlled epistemic-tag vocabulary is published and self-consistent."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VOCAB = ROOT / "docs/vocabularies/epistemic-tags.json"
DOC = ROOT / "docs/vocabularies/epistemic-tags.md"


def test_epistemic_tag_vocab_file_exists():
    assert VOCAB.is_file()
    assert DOC.is_file()


def test_epistemic_tag_vocab_structure():
    payload = json.loads(VOCAB.read_text(encoding="utf-8"))
    assert payload["id"] == "case-uco-epistemic-tags"
    assert payload["name"] == "EpistemicTagVocab"
    families = payload["families"]
    assert "epistemic_stance" in families
    assert "hash_and_bytes" in families
    values = {
        m["value"]
        for fam in families.values()
        for m in fam["members"]
    }
    for required in (
        "epistemic:observed",
        "epistemic:reported",
        "epistemic:capability",
        "epistemic:hypothesis",
        "hash-status:not-published",
        "source-bytes:not-acquired",
        "content:not-reproduced",
        "confidence:moderate-verbal",
    ):
        assert required in values


def test_darkwatchman_uses_controlled_epistemic_tags():
    graph = (
        ROOT
        / "examples/cti/darkwatchman_2021/darkwatchman-prevailion.jsonld"
    ).read_text(encoding="utf-8")
    payload = json.loads(VOCAB.read_text(encoding="utf-8"))
    values = {
        m["value"]
        for fam in payload["families"].values()
        for m in fam["members"]
    }
    # At least the core stance + hash tags appear in the exemplar.
    for tag in (
        "epistemic:reported",
        "epistemic:unattributed",
        "hash-status:not-published",
        "content:not-reproduced",
    ):
        assert tag in values
        assert tag in graph
