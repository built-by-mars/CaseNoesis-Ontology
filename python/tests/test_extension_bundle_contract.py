"""Installed-wheel / external-bundle contract for named extensions."""

from __future__ import annotations

from pathlib import Path

import pytest

from case_uco.validation.extension_paths import find_extension_dir

ROOT = Path(__file__).resolve().parents[2]


def test_named_extension_resolves_from_monorepo_project_root():
    found = find_extension_dir("attack-technique", project_root=ROOT)
    assert found is not None
    assert (found / "manifest.json").is_file()


def test_named_extension_absent_without_ontology_checkout(tmp_path):
    """A bare install has no extensions/ tree — named lookup must fail closed."""

    empty = tmp_path / "empty-root"
    empty.mkdir()
    assert find_extension_dir("attack-technique", project_root=empty) is None


@pytest.mark.skipif(
    __import__("case_uco.validation", fromlist=["validator_available"]).validator_available()
    is False,
    reason="case_validate not installed",
)
def test_validate_named_extension_requires_project_root_or_checkout():
    from case_uco.validation import validate_graph_file

    graph = ROOT / "examples/cti/darkwatchman_2021/darkwatchman-prevailion.jsonld"
    # Explicit project_root is the supported wheel+bundle contract.
    report = validate_graph_file(
        graph,
        extensions=["attack-technique:full"],
        project_root=ROOT,
    )
    assert report.conforms is True
    assert report.verification_status == "complete"
