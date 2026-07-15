"""Unit tests for the pinned ATT&CK STIX catalog synchronizer."""

from __future__ import annotations

import json
from pathlib import Path

from tools.sync_attack_catalog import (
    catalog_technique_ids,
    parse_techniques,
    render_catalog,
)

FIXTURE = (
    Path(__file__).resolve().parent / "fixtures" / "enterprise-attack-mini.json"
)


def test_parse_techniques_from_mini_stix():
    bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))
    techniques = parse_techniques(bundle)
    assert "T1566.001" in techniques
    assert techniques["T1566.001"]["name"] == "Spearphishing Attachment"
    assert "Initial Access" in techniques["T1566.001"]["tactics"]


def test_render_catalog_contains_punning_pattern(tmp_path):
    bundle = json.loads(FIXTURE.read_text(encoding="utf-8"))
    techniques = parse_techniques(bundle)
    ttl = render_catalog(
        ["T1566.001", "T1059.007"],
        techniques,
        attack_version="19.1",
        source=str(FIXTURE),
    )
    assert "attack:T1566.001" in ttl
    assert "action:Technique" in ttl
    assert 'action:techniqueID "T1566.001"' in ttl
    assert "GENERATED FILE" in ttl


def test_live_catalog_has_current_membership():
    ids = catalog_technique_ids()
    assert "T1566.001" in ids
    assert "T1059.007" in ids
    assert len(ids) >= 20
