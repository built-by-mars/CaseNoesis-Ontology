"""Ensure CTI exemplars only cite ATT&CK techniques present in the catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "extensions/attack-technique/mitre-attack-catalog.ttl"
ATTACK_IRI_RE = re.compile(
    r"https://attack\.mitre\.org/techniques/(T[0-9]{4}(?:\.[0-9]{3})?)"
)

EXEMPLARS = [
    ROOT / "examples/cti/darkwatchman_2021/darkwatchman-prevailion.jsonld",
    ROOT / "examples/cti/lotus_blossom_2025",
]


def _catalog_technique_ids() -> set[str]:
    text = CATALOG.read_text(encoding="utf-8")
    return set(re.findall(r"attack:(T[0-9]{4}(?:\.[0-9]{3})?)", text))


def _graph_paths() -> list[Path]:
    paths: list[Path] = []
    for item in EXEMPLARS:
        if item.is_file() and item.suffix == ".jsonld":
            paths.append(item)
        elif item.is_dir():
            paths.extend(sorted(item.glob("*.jsonld")))
    return paths


def _techniques_in_graph(path: Path) -> set[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    blob = json.dumps(data, ensure_ascii=False)
    return set(ATTACK_IRI_RE.findall(blob))


@pytest.mark.parametrize("graph_path", _graph_paths(), ids=lambda p: p.name)
def test_exemplar_attack_iris_are_in_catalog(graph_path: Path):
    catalog = _catalog_technique_ids()
    used = _techniques_in_graph(graph_path)
    missing = sorted(used - catalog)
    assert not missing, (
        f"{graph_path.name} cites ATT&CK technique(s) absent from "
        f"{CATALOG.relative_to(ROOT)}: {', '.join(missing)}"
    )
