"""Unit tests for IRI-indexed graph composition API (#67)."""

from __future__ import annotations

import json
import warnings

import pytest

from case_uco import CASEGraph, DuplicateNodeError
from case_uco.uco.identity import Organization
from case_uco.uco.tool import Tool


def test_get_contains_expand_iri():
    g = CASEGraph(kb_prefix="https://example.org/kb/")
    g.create(Tool, id="kb:tool-1", name="FTK")
    assert g.contains("kb:tool-1")
    expanded = g.expand_iri("kb:tool-1")
    assert expanded.startswith("https://example.org/kb/")
    assert g.get(expanded) is not None
    assert g.get("kb:tool-1")["uco-core:name"] == "FTK"


def test_get_returns_copy_index_immutable():
    g = CASEGraph()
    g.upsert_node("kb:n1", types="uco-core:UcoObject", properties={"uco-core:name": "N"})
    view = g.get("kb:n1")
    assert view is not None
    view["@id"] = "kb:mutated"
    view["uco-core:name"] = "mutated"
    assert g.contains("kb:n1")
    assert not g.contains("kb:mutated")
    assert g.get("kb:n1")["uco-core:name"] == "N"


def test_get_deep_copy_nested_mutation():
    g = CASEGraph()
    g.upsert_node(
        "kb:n1",
        types="uco-core:UcoObject",
        properties={
            "uco-core:hasFacet": [{"@id": "kb:f1"}],
            "uco-core:tag": ["a", "b"],
        },
    )
    view = g.get("kb:n1")
    view["uco-core:hasFacet"][0]["@id"] = "kb:mutated"
    view["uco-core:tag"].append("c")
    stored = g.get("kb:n1")
    assert stored["uco-core:hasFacet"][0]["@id"] == "kb:f1"
    assert stored["uco-core:tag"] == ["a", "b"]


def test_upsert_returns_copy_not_live():
    g = CASEGraph()
    returned = g.upsert_node(
        "kb:n1",
        types="uco-core:UcoObject",
        properties={"uco-core:name": "N"},
    )
    returned["uco-core:name"] = "mutated"
    returned["nested"] = {"x": 1}
    assert g.get("kb:n1")["uco-core:name"] == "N"
    assert "nested" not in g.get("kb:n1")


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


def test_load_default_reject_duplicate():
    g = CASEGraph()
    g.upsert_node("kb:x", types="uco-core:UcoObject")
    payload = json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{"@id": "kb:x", "@type": "uco-core:UcoObject"}],
    })
    with pytest.raises(DuplicateNodeError):
        g.load(payload)


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


def test_merge_identical_conflict():
    g = CASEGraph()
    g.upsert_node("kb:x", types="uco-core:UcoObject", properties={"uco-core:name": "A"})
    payload = json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{
            "@id": "kb:x",
            "@type": "uco-core:UcoObject",
            "uco-core:name": "B",
        }],
    })
    with pytest.raises(DuplicateNodeError, match="merge_identical conflict"):
        g.load(payload, on_duplicate="merge_identical")


def test_merge_identical_allows_equal_and_new():
    g = CASEGraph()
    g.upsert_node("kb:x", types="uco-core:UcoObject", properties={"uco-core:name": "A"})
    payload = json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{
            "@id": "kb:x",
            "@type": "uco-core:UcoObject",
            "uco-core:name": "A",
            "uco-core:description": "added",
        }],
    })
    g.load(payload, on_duplicate="merge_identical")
    node = g.get("kb:x")
    assert node["uco-core:name"] == "A"
    assert node["uco-core:description"] == "added"


def test_merge_compatible_scalar_conflict_raises():
    g = CASEGraph()
    g.upsert_node("kb:x", types="uco-core:UcoObject", properties={"uco-core:name": "A"})
    payload = json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{
            "@id": "kb:x",
            "@type": "uco-core:UcoObject",
            "uco-core:name": "B",
        }],
    })
    with pytest.raises(DuplicateNodeError, match="merge_compatible scalar conflict"):
        g.load(payload, on_duplicate="merge_compatible")


def test_replace_overwrites_properties():
    g = CASEGraph()
    g.upsert_node(
        "kb:x",
        types="uco-core:UcoObject",
        properties={"uco-core:name": "A", "uco-core:description": "keep?"},
    )
    payload = json.dumps({
        "@context": {"kb": "http://example.org/kb/"},
        "@graph": [{
            "@id": "kb:x",
            "@type": "uco-core:UcoObject",
            "uco-core:name": "B",
        }],
    })
    g.load(payload, on_duplicate="replace")
    node = g.get("kb:x")
    assert node["uco-core:name"] == "B"
    assert "uco-core:description" not in node


def test_context_collision_rejected():
    g = CASEGraph()
    payload = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-core": "https://evil.example.org/uco/core/",
        },
        "@graph": [],
    })
    with pytest.raises(ValueError, match="Context prefix collision"):
        g.load(payload)


def test_from_jsonld_multi_type_most_specific():
    json_str = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [{
            "@id": "kb:org-1",
            "@type": [
                "uco-identity:Organization",
                "uco-identity:Identity",
            ],
            "uco-core:name": "Acme",
        }],
    })
    graph, objects = CASEGraph.from_jsonld(json_str)
    assert len(objects) == 1
    assert isinstance(objects[0], Organization)
    types = CASEGraph._as_type_list(graph.get("kb:org-1")["@type"])
    assert "uco-identity:Organization" in types
    assert "uco-identity:Identity" in types
    assert graph.contains("kb:org-1")


def test_from_jsonld_uses_iri_index():
    json_str = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        },
        "@graph": [{
            "@id": "kb:tool-idx",
            "@type": "uco-tool:Tool",
            "uco-core:name": "Indexed",
        }],
    })
    graph, objects = CASEGraph.from_jsonld(json_str)
    assert isinstance(objects[0], Tool)
    assert graph.get("kb:tool-idx")["uco-core:name"] == "Indexed"
    expanded = graph.expand_iri("kb:tool-idx")
    assert graph.get(expanded) is not None


def test_create_relationship_deterministic():
    g = CASEGraph()
    g.upsert_node("kb:src", types="uco-core:UcoObject")
    g.upsert_node("kb:tgt", types="uco-core:UcoObject")
    r1 = g.create_relationship("kb:src", "kb:tgt", "Derived_From")
    r2 = g.create_relationship("kb:src", "kb:tgt", "Derived_From")
    assert r1["@id"] == r2["@id"]
    assert len(g) == 3  # src, tgt, one relationship


def test_create_relationship_assertion_id_coexists():
    g = CASEGraph()
    g.upsert_node("kb:src", types="uco-core:UcoObject")
    g.upsert_node("kb:tgt", types="uco-core:UcoObject")
    r1 = g.create_relationship(
        "kb:src", "kb:tgt", "Derived_From", relationship_id="kb:rel-a"
    )
    r2 = g.create_relationship(
        "kb:src", "kb:tgt", "Derived_From", assertion_id="kb:rel-b"
    )
    assert r1["@id"] != r2["@id"]
    assert len(g) == 4


def test_relationship_kind_slug_safe():
    g = CASEGraph()
    g.upsert_node("kb:src", types="uco-core:UcoObject")
    g.upsert_node("kb:tgt", types="uco-core:UcoObject")
    rel = g.create_relationship("kb:src", "kb:tgt", "Derived From/../evil\n")
    assert "/" not in rel["@id"].split("kb:rel-", 1)[-1].rsplit("-", 1)[0]
    assert "\n" not in rel["@id"]


def test_set_property_replaces_scalar():
    g = CASEGraph()
    g.upsert_node("kb:x", types="uco-core:UcoObject", properties={"uco-core:name": "A"})
    g.set_property("kb:x", "uco-core:name", "B")
    assert g.get("kb:x")["uco-core:name"] == "B"


def test_add_property_scalar_conflict_raises():
    g = CASEGraph()
    g.upsert_node("kb:x", types="uco-core:UcoObject", properties={"uco-core:name": "A"})
    with pytest.raises(DuplicateNodeError, match="merge_compatible scalar conflict"):
        g.add_property("kb:x", "uco-core:name", "B")


def test_semantic_equality_typed_literal_and_id_ref():
    g = CASEGraph()
    g.upsert_node(
        "kb:x",
        types="uco-core:UcoObject",
        properties={
            "uco-core:isDirectional": {"@type": "xsd:boolean", "@value": "true"},
            "uco-core:object": {"@id": "kb:y"},
        },
    )
    g.add_property(
        "kb:x",
        "uco-core:isDirectional",
        {"@type": "http://www.w3.org/2001/XMLSchema#boolean", "@value": "true"},
    )
    g.add_property("kb:x", "uco-core:object", {"@id": "kb:y"})
    node = g.get("kb:x")
    assert node["uco-core:isDirectional"]["@value"] == "true"
    assert node["uco-core:object"]["@id"] == "kb:y"


def test_load_transactional_rollback():
    g = CASEGraph()
    g.upsert_node("kb:keep", types="uco-core:UcoObject", properties={"uco-core:name": "K"})
    payload = json.dumps({
        "@context": {
            "kb": "http://example.org/kb/",
            "uco-core": "https://evil.example.org/uco/core/",
        },
        "@graph": [{"@id": "kb:new", "@type": "uco-core:UcoObject"}],
    })
    with pytest.raises(ValueError, match="Context prefix collision"):
        g.load(payload)
    assert g.contains("kb:keep")
    assert not g.contains("kb:new")
    assert g._context["uco-core"].startswith("https://ontology.unifiedcyberontology.org/")


def test_constructor_extra_context_collision():
    with pytest.raises(ValueError, match="Context prefix collision"):
        CASEGraph(extra_context={"uco-core": "https://evil.example.org/uco/core/"})


def test_split_rejects_non_positive():
    from case_uco import InvalidSplitSizeError

    g = CASEGraph()
    g.upsert_node("kb:n", types="uco-core:UcoObject")
    with pytest.raises(InvalidSplitSizeError):
        g.split(0)
    with pytest.raises(InvalidSplitSizeError):
        g.split(-1)


def test_estimate_triples_counts_multi_type():
    g = CASEGraph()
    g.upsert_node(
        "kb:x",
        types=["uco-core:UcoObject", "prov:Entity"],
        properties={"uco-core:name": "X"},
    )
    # 2 types + 1 name property
    assert g.estimate_triples() == 3


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
    assert set(g.partition_by_label(boundary).keys()) == set(parts.keys())


def test_write_streaming_roundtrip(tmp_path):
    g = CASEGraph()
    g.create(Tool, id="kb:t", name="X")
    out = tmp_path / "stream.jsonld"
    g.write_streaming(str(out))
    loaded = CASEGraph()
    loaded.load_file(str(out), on_duplicate="merge_compatible")
    assert loaded.get("kb:t")["uco-core:name"] == "X"
