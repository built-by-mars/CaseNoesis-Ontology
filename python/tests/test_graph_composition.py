"""Unit tests for IRI-indexed graph composition API (#67)."""

from __future__ import annotations

import json
import warnings

import pytest

from case_uco import CASEGraph, DuplicateNodeError
from case_uco.uco.tool import Tool


def test_get_contains_expand_iri():
    g = CASEGraph(kb_prefix="https://example.org/kb/")
    g.create(Tool, id="kb:tool-1", name="FTK")
    assert g.contains("kb:tool-1")
    expanded = g.expand_iri("kb:tool-1")
    assert expanded.startswith("https://example.org/kb/")
    assert g.get(expanded) is not None
    assert g.get("kb:tool-1")["uco-core:name"] == "FTK"


def test_add_type_same_iri_no_duplicate():
    g = CASEGraph(extra_context={"prov": "http://www.w3.org/ns/prov#"})
    g.create(Tool, id="kb:imager", name="FTK Imager")
    g.add_type("kb:imager", "prov:Entity")
    types = g.get("kb:imager")["@type"]
    assert isinstance(types, list)
    assert "uco-tool:Tool" in types or any("Tool" in t for t in types)
    assert "prov:Entity" in types
    assert len(g) == 1


def test_duplicate_reject_on_append():
    g = CASEGraph()
    g.upsert_node("kb:a", types="uco-core:UcoObject")
    with pytest.raises(DuplicateNodeError):
        g._append_object({"@id": "kb:a", "@type": "uco-core:UcoObject"})


def test_load_merge_compatible():
    g = CASEGraph(extra_context={"prov": "http://www.w3.org/ns/prov#"})
    g.upsert_node("kb:x", types="uco-core:UcoObject", properties={"uco-core:name": "X"})
    payload = json.dumps({
        "@context": g._context,
        "@graph": [{
            "@id": "kb:x",
            "@type": ["uco-core:UcoObject", "prov:Entity"],
            "uco-core:description": "enriched",
        }],
    })
    g.load(payload, on_duplicate="merge_compatible")
    node = g.get("kb:x")
    assert "prov:Entity" in CASEGraph._as_type_list(node["@type"])
    assert node["uco-core:name"] == "X"
    assert node["uco-core:description"] == "enriched"


def test_create_relationship_deterministic():
    g = CASEGraph()
    g.upsert_node("kb:src", types="uco-core:UcoObject")
    g.upsert_node("kb:tgt", types="uco-core:UcoObject")
    r1 = g.create_relationship("kb:src", "kb:tgt", "Derived_From")
    r2 = g.create_relationship("kb:src", "kb:tgt", "Derived_From")
    assert r1["@id"] == r2["@id"]
    assert len(g) == 3  # src, tgt, one relationship


def test_link_property_edge():
    g = CASEGraph(extra_context={"prov": "http://www.w3.org/ns/prov#"})
    g.upsert_node("kb:a", types="prov:Entity")
    g.upsert_node("kb:b", types="prov:Activity")
    g.link("kb:a", "prov:wasGeneratedBy", "kb:b")
    assert g.get("kb:a")["prov:wasGeneratedBy"]["@id"] == "kb:b"


def test_split_warns():
    g = CASEGraph()
    for i in range(5):
        g.upsert_node(f"kb:n{i}", types="uco-core:UcoObject")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        chunks = g.split(2)
    assert len(chunks) == 3
    assert any("partition_by" in str(w.message) for w in caught)


def test_partition_by_boundary():
    g = CASEGraph()
    g.upsert_node("kb:art-a", types="uco-core:UcoObject", properties={"uco-core:name": "A"})
    g.upsert_node("kb:art-b", types="uco-core:UcoObject", properties={"uco-core:name": "B"})
    g.create_relationship("kb:art-a", "kb:art-b", "Related_To")

    def boundary(node):
        name = node.get("uco-core:name")
        if name == "A":
            return "part-a"
        if name == "B":
            return "part-b"
        return None

    parts = g.partition_by(boundary)
    assert "part-a" in parts and "part-b" in parts


def test_write_streaming_roundtrip(tmp_path):
    g = CASEGraph()
    g.create(Tool, id="kb:t", name="X")
    out = tmp_path / "stream.jsonld"
    g.write_streaming(str(out))
    loaded = CASEGraph()
    loaded.load_file(str(out), on_duplicate="merge_compatible")
    assert loaded.get("kb:t")["uco-core:name"] == "X"
