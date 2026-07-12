"""CASEGraph — the main entry point for building and serializing CASE/UCO graphs."""

from __future__ import annotations

import hashlib
import json
import uuid
import warnings
from dataclasses import Field, fields, is_dataclass
from datetime import date, datetime
from typing import Any, Callable, Iterator, TypeVar, Type

T = TypeVar("T")

_builtin_id = id


class DuplicateNodeError(ValueError):
    """Raised when a node with the same @id conflicts with an existing node.

    Default policy is reject-on-conflict. Compatible multi-typing should use
    :meth:`CASEGraph.add_type` / :meth:`CASEGraph.upsert_node` instead of
    appending a second top-level object with the same IRI.
    """

    def __init__(self, node_id: str, detail: str = ""):
        self.node_id = node_id
        msg = f"Duplicate @id {node_id!r}"
        if detail:
            msg = f"{msg}: {detail}"
        super().__init__(msg)

# Standard CASE/UCO JSON-LD context prefixes
DEFAULT_CONTEXT: dict[str, str] = {
    "case-investigation": "https://ontology.caseontology.org/case/investigation/",
    "kb": "http://example.org/kb/",
    "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
    "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
    "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
    "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
    "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
    "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
    "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
    "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
    "uco-victim": "https://ontology.unifiedcyberontology.org/uco/victim/",
    "uco-analysis": "https://ontology.unifiedcyberontology.org/uco/analysis/",
    "uco-configuration": "https://ontology.unifiedcyberontology.org/uco/configuration/",
    "uco-marking": "https://ontology.unifiedcyberontology.org/uco/marking/",
    "uco-pattern": "https://ontology.unifiedcyberontology.org/uco/pattern/",
    "uco-time": "https://ontology.unifiedcyberontology.org/uco/time/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

_RANGE_IRI_TO_TYPED_LITERAL = {
    "http://www.w3.org/2001/XMLSchema#boolean": "xsd:boolean",
    "http://www.w3.org/2001/XMLSchema#integer": "xsd:integer",
    "http://www.w3.org/2001/XMLSchema#nonNegativeInteger": "xsd:nonNegativeInteger",
    "http://www.w3.org/2001/XMLSchema#positiveInteger": "xsd:positiveInteger",
    "http://www.w3.org/2001/XMLSchema#decimal": "xsd:decimal",
    "http://www.w3.org/2001/XMLSchema#float": "xsd:float",
    "http://www.w3.org/2001/XMLSchema#double": "xsd:double",
    "http://www.w3.org/2001/XMLSchema#dateTime": "xsd:dateTime",
    "http://www.w3.org/2001/XMLSchema#hexBinary": "xsd:hexBinary",
}


class CASEGraph:
    """Build a CASE/UCO JSON-LD graph with typed objects.

    Usage:
        graph = CASEGraph(kb_prefix="http://example.org/kb/")
        tool = graph.create(Tool, name="Tool A")
        print(graph.serialize())
    """

    def __init__(
        self,
        kb_prefix: str = "http://example.org/kb/",
        extra_context: dict[str, str] | None = None,
    ):
        self.kb_prefix = kb_prefix
        self._context = dict(DEFAULT_CONTEXT)
        self._context["kb"] = kb_prefix
        if extra_context:
            self._context.update(extra_context)
        self._objects: list[dict[str, Any]] = []
        self._id_map: dict[int, str] = {}
        self._instances: list[Any] = []
        # Expanded IRI → index into _objects (O(1) lookup).
        self._iri_index: dict[str, int] = {}
        # Compact form and expanded form both index to the same slot.
        self._iri_aliases: dict[str, str] = {}
        self._used_prefix_set: set[str] = set()
        self.on_duplicate: str = "reject"  # reject | merge_compatible

    def create(self, cls: Type[T], *, id: str | None = None, **kwargs: Any) -> T:
        """Create an instance of a CASE/UCO class and add it to the graph.

        Args:
            cls: The CASE/UCO class to instantiate.
            id: Optional user-supplied @id for deterministic IRIs.
                If not provided, a UUID-based @id is auto-generated.
            **kwargs: Arguments passed to the class constructor.

        Returns the created instance so it can be referenced by other objects.
        """
        instance = cls(**kwargs)
        self._validate_instance(instance)
        obj_id = id if id is not None else self._mint_id(instance)
        self._id_map[_builtin_id(instance)] = obj_id
        self._instances.append(instance)
        json_obj = self._to_jsonld(instance, obj_id)
        self._append_object(json_obj)
        return instance

    def add(self, instance: Any, *, id: str | None = None) -> str:
        """Add a pre-created instance to the graph.

        Args:
            instance: A dataclass instance of a CASE/UCO type.
            id: Optional user-supplied @id for deterministic IRIs.

        Returns the assigned @id.
        """
        self._validate_instance(instance)
        obj_id = id if id is not None else self._mint_id(instance)
        self._id_map[_builtin_id(instance)] = obj_id
        self._instances.append(instance)
        json_obj = self._to_jsonld(instance, obj_id)
        self._append_object(json_obj)
        return obj_id

    def get_id(self, instance: Any) -> str | None:
        """Get the @id for a previously added instance."""
        return self._id_map.get(_builtin_id(instance))

    def expand_iri(self, node_id: str) -> str:
        """Expand a compact IRI using this graph's context."""
        return _expand_iri(node_id, self._context)

    def contains(self, node_id: str) -> bool:
        """Return True if a node with this @id (compact or expanded) exists."""
        return self._find_object(node_id) is not None

    def get(self, node_id: str) -> dict[str, Any] | None:
        """Return the JSON-LD dict for a node by compact or expanded ``@id``."""
        return self._find_object(node_id)

    def upsert_node(
        self,
        node_id: str,
        *,
        types: list[str] | str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create or update a JSON-LD node by ``@id``.

        Use for external ontology terms and multi-typed enrichment on the
        same IRI as a ``create()`` object. Does not replace SDK dataclass
        instances — call ``add_type`` / ``add_property`` after ``create()``
        when enriching typed CASE/UCO objects.
        """
        obj = self._find_object(node_id)
        if obj is None:
            obj = {"@id": node_id}
            if types is not None:
                obj["@type"] = self._normalize_type_value(types)
            if properties:
                for key, value in properties.items():
                    self._set_property(obj, key, value)
            self._append_object(obj)
            return obj

        if types is not None:
            merged = self._merge_types(obj.get("@type"), types)
            obj["@type"] = self._normalize_type_value(merged)
        if properties:
            for key, value in properties.items():
                self._set_property(obj, key, value)
        self._track_prefixes_for(obj)
        return obj

    def add_type(self, node_id: str, type_iri: str) -> None:
        """Add an ``rdf:type`` to an existing node (same ``@id``)."""
        obj = self._require_object(node_id)
        merged = self._merge_types(obj.get("@type"), type_iri)
        obj["@type"] = self._normalize_type_value(merged)
        self._track_prefixes_for({"@type": type_iri})

    def add_property(self, node_id: str, key: str, value: Any) -> None:
        """Add or merge a property on an existing node."""
        obj = self._require_object(node_id)
        self._set_property(obj, key, value)
        self._track_prefixes_for({key: value})

    def link(
        self,
        source_id: str,
        predicate: str,
        target_id: str | dict[str, Any],
    ) -> None:
        """Add a direct property edge ``source --predicate--> target``.

        Prefer :meth:`create_relationship` for ``uco-core:Relationship`` nodes.
        Use ``link`` for ontology properties such as ``prov:wasDerivedFrom``.
        """
        target_ref: dict[str, Any]
        if isinstance(target_id, str):
            target_ref = {"@id": target_id}
        else:
            target_ref = target_id
        self.add_property(source_id, predicate, target_ref)

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        kind: str,
        *,
        directional: bool = True,
        description: str | None = None,
        relationship_id: str | None = None,
        extra_types: list[str] | str | None = None,
        properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a ``uco-core:Relationship`` node with deterministic ``@id``.

        Validates that source and target nodes exist. Relationship IDs are
        derived from source, target, and kind unless ``relationship_id`` is set.
        """
        if not self.contains(source_id):
            raise KeyError(f"Relationship source not in graph: {source_id!r}")
        if not self.contains(target_id):
            raise KeyError(f"Relationship target not in graph: {target_id!r}")
        if not kind:
            raise ValueError("kindOfRelationship is required")

        rel_id = relationship_id or self._deterministic_relationship_id(
            source_id, target_id, kind
        )
        types: list[str] = ["uco-core:Relationship"]
        if extra_types:
            types = self._merge_types(types, extra_types)
        props: dict[str, Any] = {
            "uco-core:source": [{"@id": source_id}],
            "uco-core:target": [{"@id": target_id}],
            "uco-core:kindOfRelationship": kind,
            "uco-core:isDirectional": {
                "@type": "xsd:boolean",
                "@value": "true" if directional else "false",
            },
        }
        if description:
            props["uco-core:description"] = description
        if properties:
            props.update(properties)
        return self.upsert_node(rel_id, types=types, properties=props)

    def __len__(self) -> int:
        """Return the number of objects in the graph."""
        return len(self._objects)

    def serialize(self, format: str = "json-ld", indent: int = 4) -> str:
        """Serialize the graph to JSON-LD string."""
        if format != "json-ld":
            raise ValueError(f"Unsupported format: {format}. Only 'json-ld' is supported.")
        doc = {
            "@context": self._pruned_context(),
            "@graph": self._objects,
        }
        return json.dumps(doc, indent=indent, default=str)

    def write(self, path: str, format: str = "json-ld", indent: int = 4) -> None:
        """Write the graph to a file (materializes full string then writes)."""
        content = self.serialize(format=format, indent=indent)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def write_streaming(
        self,
        path: str,
        *,
        format: str = "json-ld",
        indent: int = 2,
    ) -> None:
        """Stream JSON-LD to disk without building a second full document string.

        Emits ``@context`` then each ``@graph`` element incrementally. Peak
        memory is dominated by the in-memory graph itself rather than a
        duplicate serialized buffer. Retains :meth:`serialize` for callers
        that need a complete string.
        """
        if format != "json-ld":
            raise ValueError(f"Unsupported format: {format}. Only 'json-ld' is supported.")
        ctx = self._pruned_context()
        pad = " " * indent
        with open(path, "w", encoding="utf-8") as f:
            f.write("{\n")
            f.write(f'{pad}"@context": ')
            f.write(json.dumps(ctx, indent=indent, default=str))
            f.write(",\n")
            f.write(f'{pad}"@graph": [\n')
            for i, obj in enumerate(self._objects):
                chunk = json.dumps(obj, indent=indent, default=str)
                indented = "\n".join(pad + pad + line for line in chunk.splitlines())
                f.write(indented)
                if i + 1 < len(self._objects):
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write(f"{pad}]\n")
            f.write("}\n")

    def load(self, json_str: str, *, on_duplicate: str | None = None) -> None:
        """Load a JSON-LD string, merging context and upserting objects.

        Duplicate ``@id`` handling follows ``on_duplicate`` or
        ``self.on_duplicate`` (default ``reject``). Compatible merges use
        ``merge_compatible``.
        """
        policy = on_duplicate or self.on_duplicate
        doc = json.loads(json_str)
        if "@context" in doc and isinstance(doc["@context"], dict):
            self._merge_context(doc["@context"])
        if "@graph" in doc and isinstance(doc["@graph"], list):
            for raw in doc["@graph"]:
                self._ingest_raw_node(raw, policy=policy)

    def load_file(self, path: str, *, on_duplicate: str | None = None) -> None:
        """Read and load a JSON-LD file into this graph."""
        with open(path, "r", encoding="utf-8") as f:
            self.load(f.read(), on_duplicate=on_duplicate)

    def validate(self, *, case_version: str = "case-1.4.0") -> str:
        """Validate this graph against CASE/UCO SHACL constraints.

        Requires ``case-utils`` to be installed::

            pip install case-uco[validation]

        Returns the validation output on success.
        Raises ``RuntimeError`` if validation fails or ``case_validate``
        is not available on PATH.
        """
        import os
        import shutil
        import subprocess
        import tempfile

        if not shutil.which("case_validate"):
            raise RuntimeError(
                "case_validate not found on PATH. "
                "Install with: pip install case-uco[validation]"
            )
        fd, tmp = tempfile.mkstemp(suffix=".jsonld")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(self.serialize())
            result = subprocess.run(
                ["case_validate", "--built-version", case_version, tmp],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                msg = result.stderr.strip() or result.stdout.strip()
                raise RuntimeError(f"Validation failed:\n{msg}")
            return result.stdout
        finally:
            os.unlink(tmp)

    def estimate_triples(self) -> int:
        """Estimate the number of RDF triples this graph will produce.

        Counts @type (1 triple), @id (implicit, not counted), and each
        property value as individual triples. Nested objects contribute
        their own triples recursively.
        """
        return sum(self._count_triples(obj) for obj in self._objects)

    @staticmethod
    def _count_triples(obj: dict[str, Any]) -> int:
        count = 0
        for key, value in obj.items():
            if key == "@id":
                continue
            if key == "@type":
                count += 1
                continue
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        count += 1 + CASEGraph._count_triples(item)
                    else:
                        count += 1
            elif isinstance(value, dict):
                if "@value" in value:
                    count += 1
                else:
                    count += 1 + CASEGraph._count_triples(value)
            else:
                count += 1
        return count

    def split(self, max_objects: int = 10000) -> list[CASEGraph]:
        """Split this graph into smaller chunks of at most max_objects each.

        .. warning::
            Object-count splitting is only safe for independent catalog-style
            graphs. For investigation graphs use :meth:`partition_by` instead.
        """
        warnings.warn(
            "CASEGraph.split() partitions by object count and can break "
            "investigative relationships; prefer partition_by() for CASE graphs.",
            UserWarning,
            stacklevel=2,
        )
        chunks: list[CASEGraph] = []
        for i in range(0, len(self._objects), max_objects):
            chunk = CASEGraph(kb_prefix=self.kb_prefix)
            chunk._context = dict(self._context)
            for obj in self._objects[i:i + max_objects]:
                chunk._append_object(dict(obj))
            chunks.append(chunk)
        return chunks

    def partition_by(
        self,
        boundary_key: Callable[[dict[str, Any]], str | None],
        *,
        shared_ids: set[str] | None = None,
        include_dangling_relationships: bool = True,
    ) -> dict[str, CASEGraph]:
        """Partition by a natural forensic/security boundary.

        ``boundary_key`` maps each top-level node to a partition name (or
        ``None`` to leave it unassigned until referenced). Shared nodes listed
        in ``shared_ids`` are copied into every partition that needs them.
        Relationships whose source and target fall in different partitions are
        either duplicated into both (default) or dropped.
        """
        shared_ids = shared_ids or set()
        partitions: dict[str, CASEGraph] = {}
        membership: dict[str, str] = {}

        for obj in self._objects:
            oid = obj.get("@id")
            if not oid:
                continue
            key = boundary_key(obj)
            if key is None:
                continue
            membership[oid] = key
            if key not in partitions:
                partitions[key] = CASEGraph(
                    kb_prefix=self.kb_prefix,
                    extra_context=dict(self._context),
                )
                partitions[key].on_duplicate = "merge_compatible"
            partitions[key]._append_object(dict(obj))

        # Copy shared + cross-partition relationship endpoints.
        by_id = {o.get("@id"): o for o in self._objects if o.get("@id")}
        for obj in self._objects:
            types = obj.get("@type", [])
            if isinstance(types, str):
                types = [types]
            if "uco-core:Relationship" not in types:
                continue
            sources = obj.get("uco-core:source") or []
            targets = obj.get("uco-core:target") or []
            if not sources or not targets:
                continue
            sid = sources[0]["@id"] if isinstance(sources[0], dict) else sources[0]
            tid = targets[0]["@id"] if isinstance(targets[0], dict) else targets[0]
            s_part = membership.get(sid)
            t_part = membership.get(tid)
            if s_part and t_part and s_part == t_part:
                continue
            if not include_dangling_relationships and s_part != t_part:
                continue
            for part_name in {s_part, t_part} - {None}:
                pg = partitions.setdefault(
                    part_name,  # type: ignore[arg-type]
                    CASEGraph(kb_prefix=self.kb_prefix, extra_context=dict(self._context)),
                )
                pg.on_duplicate = "merge_compatible"
                for nid in (sid, tid, obj.get("@id")):
                    if nid and nid in by_id:
                        try:
                            pg._ingest_raw_node(dict(by_id[nid]), policy="merge_compatible")
                        except DuplicateNodeError:
                            pass

        for sid in shared_ids:
            node = by_id.get(sid)
            if not node:
                continue
            for pg in partitions.values():
                try:
                    pg._ingest_raw_node(dict(node), policy="merge_compatible")
                except DuplicateNodeError:
                    pass

        return partitions

    @classmethod
    def merge_files(cls, paths: list[str], kb_prefix: str = "http://example.org/kb/") -> CASEGraph:
        """Load and merge multiple JSON-LD graph files into a single graph.

        Contexts are merged (later files override earlier ones for
        conflicting prefixes). All objects are concatenated.
        """
        merged = cls(kb_prefix=kb_prefix)
        for path in paths:
            merged.load_file(path)
        return merged

    def _mint_id(self, instance: Any) -> str:
        """Generate a UUID-based @id for an instance."""
        cls_name = type(instance).__name__
        # Convert PascalCase to kebab-case for the IRI local name
        prefix = self._get_prefix(instance)
        return f"{prefix}:{cls_name}-{uuid.uuid4()}"

    def _mint_relationship_id(self, source_id: str, predicate: str) -> str:
        local = predicate.split(":", 1)[-1] if ":" in predicate else predicate
        return f"{source_id}/{local}-{uuid.uuid4()}"

    def _deterministic_relationship_id(
        self, source_id: str, target_id: str, kind: str
    ) -> str:
        digest = hashlib.sha256(
            f"{self.expand_iri(source_id)}|{self.expand_iri(target_id)}|{kind}".encode()
        ).hexdigest()[:12]
        safe_kind = kind.replace(" ", "_")
        return f"kb:rel-{safe_kind}-{digest}"

    def _append_object(self, obj: dict[str, Any]) -> None:
        node_id = obj.get("@id")
        if node_id and self._find_object(node_id) is not None:
            raise DuplicateNodeError(
                node_id,
                "use add_type/upsert_node/merge_compatible instead of appending a second node",
            )
        self._objects.append(obj)
        if node_id:
            self._index_node(node_id, len(self._objects) - 1)
        self._track_prefixes_for(obj)

    def _index_node(self, node_id: str, index: int) -> None:
        expanded = self.expand_iri(node_id)
        self._iri_index[expanded] = index
        self._iri_aliases[node_id] = expanded
        if expanded != node_id:
            self._iri_aliases[expanded] = expanded

    def _find_object(self, node_id: str) -> dict[str, Any] | None:
        expanded = self.expand_iri(node_id)
        idx = self._iri_index.get(expanded)
        if idx is None:
            # Fallback linear scan then rebuild index (legacy graphs / tests).
            for i, obj in enumerate(self._objects):
                oid = obj.get("@id")
                if oid is None:
                    continue
                if oid == node_id or self.expand_iri(oid) == expanded:
                    self._index_node(oid, i)
                    return obj
            return None
        if idx >= len(self._objects):
            return None
        return self._objects[idx]

    def _require_object(self, node_id: str) -> dict[str, Any]:
        obj = self._find_object(node_id)
        if obj is None:
            raise KeyError(f"No node with @id {node_id!r}")
        return obj

    def _merge_context(self, incoming: dict[str, Any]) -> None:
        for prefix, ns in incoming.items():
            if not isinstance(ns, str):
                continue
            existing = self._context.get(prefix)
            if existing is not None and existing != ns:
                raise ValueError(
                    f"Context prefix collision for {prefix!r}: "
                    f"existing {existing!r} vs incoming {ns!r}"
                )
            self._context[prefix] = ns

    def _ingest_raw_node(self, raw: dict[str, Any], *, policy: str) -> None:
        node_id = raw.get("@id")
        if not node_id:
            self._objects.append(raw)
            self._track_prefixes_for(raw)
            return
        existing = self._find_object(node_id)
        if existing is None:
            self._append_object(raw)
            return
        if policy == "reject":
            raise DuplicateNodeError(node_id, "conflicting duplicate during load")
        if policy == "merge_compatible":
            if "@type" in raw:
                existing["@type"] = self._normalize_type_value(
                    self._merge_types(existing.get("@type"), raw["@type"])
                )
            for key, value in raw.items():
                if key in ("@id", "@type"):
                    continue
                self._set_property(existing, key, value)
            self._track_prefixes_for(raw)
            return
        raise ValueError(f"Unknown duplicate policy: {policy!r}")

    def _track_prefixes_for(self, node: Any) -> None:
        self._collect_prefixes(node, set(self._context.keys()), self._used_prefix_set)

    @staticmethod
    def _as_type_list(types: list[str] | str | None) -> list[str]:
        if types is None:
            return []
        if isinstance(types, str):
            return [types]
        return list(types)

    @staticmethod
    def _normalize_type_value(types: list[str] | str) -> list[str] | str:
        type_list = CASEGraph._as_type_list(types)
        if len(type_list) == 1:
            return type_list[0]
        return type_list

    def _merge_types(
        self,
        existing: list[str] | str | None,
        new_types: list[str] | str,
    ) -> list[str]:
        merged = self._as_type_list(existing)
        for type_iri in self._as_type_list(new_types):
            if type_iri not in merged:
                merged.append(type_iri)
        return merged

    def _set_property(self, obj: dict[str, Any], key: str, value: Any) -> None:
        if key not in obj:
            obj[key] = value
            return
        existing = obj[key]
        if existing == value:
            return
        if isinstance(existing, list):
            if value not in existing and (
                not isinstance(value, dict) or value not in existing
            ):
                # Avoid duplicate @id refs
                if isinstance(value, dict) and "@id" in value:
                    if any(
                        isinstance(item, dict) and item.get("@id") == value["@id"]
                        for item in existing
                    ):
                        return
                existing.append(value)
            return
        if isinstance(existing, dict) and isinstance(value, dict):
            if existing.get("@id") and existing.get("@id") == value.get("@id"):
                return
        obj[key] = [existing, value]

    def _get_prefix(self, instance: Any) -> str:
        """Get the namespace prefix for an instance (defaults to kb)."""
        return "kb"

    def _to_jsonld(self, instance: Any, obj_id: str) -> dict[str, Any]:
        """Convert a dataclass instance to a JSON-LD dictionary."""
        result: dict[str, Any] = {"@id": obj_id}

        cls = type(instance)
        if hasattr(cls, "CLASS_IRI"):
            # Convert full IRI to prefixed form
            class_iri = cls.CLASS_IRI
            result["@type"] = self._compact_iri(class_iri)

        if not is_dataclass(instance):
            return result

        for f in fields(instance):
            if f.name in ("CLASS_IRI", "NAMESPACE_PREFIX"):
                continue

            value = getattr(instance, f.name)
            if value is None:
                continue
            if isinstance(value, list) and len(value) == 0:
                continue

            prop_key = self._property_key(instance, f)
            range_iri = f.metadata.get("range_iri")

            if isinstance(value, list):
                result[prop_key] = [self._convert_value(v, range_iri=range_iri) for v in value]
            else:
                result[prop_key] = self._convert_value(value, range_iri=range_iri)

        return result

    def _property_key(self, instance: Any, field_info: Field[Any]) -> str:
        """Resolve the JSON-LD property key from generated field metadata when available."""
        metadata_key: str | None = field_info.metadata.get("jsonld_key")
        if metadata_key:
            return metadata_key

        parts = field_info.name.split("_")
        camel = parts[0] + "".join(p.capitalize() for p in parts[1:])
        ns_prefix = getattr(type(instance), "NAMESPACE_PREFIX", "uco-core")
        return f"{ns_prefix}:{camel}"

    def _convert_value(self, value: Any, range_iri: str | None = None) -> Any:
        """Convert a Python value to JSON-LD representation."""
        if is_dataclass(value) and not isinstance(value, type):
            # Nested object — create inline or reference
            self._validate_instance(value)
            if _builtin_id(value) in self._id_map:
                return {"@id": self._id_map[_builtin_id(value)]}
            # Inline as a facet-like sub-object
            inline_id = self._mint_id(value)
            return self._to_jsonld(value, inline_id)

        if range_iri in _RANGE_IRI_TO_TYPED_LITERAL:
            return self._typed_literal(_RANGE_IRI_TO_TYPED_LITERAL[range_iri], value)

        if isinstance(value, datetime):
            return self._typed_literal("xsd:dateTime", value)
        if isinstance(value, date):
            return self._typed_literal("xsd:dateTime", datetime.combine(value, datetime.min.time()))
        if isinstance(value, bool):
            return self._typed_literal("xsd:boolean", value)
        if isinstance(value, int):
            return self._typed_literal("xsd:integer", value)
        if isinstance(value, float):
            return self._typed_literal("xsd:decimal", value)

        return value

    def _typed_literal(self, xsd_type: str, value: Any) -> dict[str, str]:
        if isinstance(value, bool):
            rendered = str(value).lower()
        elif isinstance(value, datetime):
            rendered = value.isoformat()
        else:
            rendered = str(value)
        return {"@type": xsd_type, "@value": rendered}

    def _validate_instance(self, instance: Any) -> None:
        """Validate required generated fields before adding/serializing an instance."""
        if not is_dataclass(instance):
            return

        for field_info in fields(instance):
            if field_info.name in ("CLASS_IRI", "NAMESPACE_PREFIX"):
                continue

            metadata: dict[str, Any] = dict(field_info.metadata) if field_info.metadata else {}
            if not metadata:
                continue

            value = getattr(instance, field_info.name)
            required = bool(metadata.get("required", False))
            cardinality = metadata.get("cardinality")

            if required:
                if value is None:
                    raise ValueError(
                        f"{type(instance).__name__}.{field_info.name} is required but was not provided."
                    )
                if isinstance(value, list) and len(value) == 0:
                    raise ValueError(
                        f"{type(instance).__name__}.{field_info.name} requires at least one value."
                    )

            if cardinality in {"exactly_one", "zero_or_one"} and isinstance(value, list):
                raise ValueError(
                    f"{type(instance).__name__}.{field_info.name} does not accept multiple values."
                )

            if isinstance(value, list):
                for item in value:
                    if is_dataclass(item):
                        self._validate_instance(item)
            elif is_dataclass(value):
                self._validate_instance(value)

    @classmethod
    def from_jsonld(
        cls,
        json_str: str,
        *,
        extra_classes: list[type] | None = None,
        kb_prefix: str = "http://example.org/kb/",
    ) -> tuple[CASEGraph, list[Any]]:
        """Deserialize a JSON-LD string into typed Python objects.

        Returns a tuple of (CASEGraph, list_of_typed_objects). Each object in
        the ``@graph`` array is matched to a generated Python class by its
        ``@type`` IRI.  Objects whose type cannot be resolved are returned as
        plain dicts and still added to the graph.

        Args:
            json_str: A JSON-LD string containing ``@context`` and ``@graph``.
            extra_classes: Additional classes (e.g. extension dataclasses)
                to include in the type registry alongside the built-in ones.
            kb_prefix: Knowledge-base prefix for the returned graph.
        """
        iri_to_class = _build_class_registry(extra_classes)

        doc = json.loads(json_str)
        context = doc.get("@context", {})
        graph_items = doc.get("@graph", [])

        graph = cls(kb_prefix=kb_prefix, extra_context=context if isinstance(context, dict) else None)

        typed_objects: list[Any] = []
        for raw in graph_items:
            obj = _rehydrate(raw, iri_to_class, context if isinstance(context, dict) else {})
            typed_objects.append(obj)

            if is_dataclass(obj) and not isinstance(obj, type):
                obj_id = raw.get("@id", graph._mint_id(obj))
                graph._id_map[_builtin_id(obj)] = obj_id
                graph._objects.append(raw)
            else:
                graph._objects.append(raw)

        return graph, typed_objects

    def _pruned_context(self) -> dict[str, str]:
        """Return a copy of the context containing only prefixes used in the graph."""
        used = self._used_prefix_set or self._used_prefixes()
        if not used:
            used = self._used_prefixes()
        return {k: v for k, v in self._context.items() if k in used}

    def _used_prefixes(self) -> set[str]:
        """Collect all namespace prefixes referenced in the graph objects."""
        prefixes: set[str] = set()
        context_keys = set(self._context.keys())
        for obj in self._objects:
            self._collect_prefixes(obj, context_keys, prefixes)
        return prefixes

    @staticmethod
    def _extract_prefix(value: str, context_keys: set[str]) -> str | None:
        if "://" in value:
            return None
        colon = value.find(":")
        if colon > 0:
            prefix = value[:colon]
            if prefix in context_keys:
                return prefix
        return None

    @staticmethod
    def _collect_prefixes(
        node: Any, context_keys: set[str], out: set[str]
    ) -> None:
        if isinstance(node, dict):
            for key, val in node.items():
                p = CASEGraph._extract_prefix(key, context_keys)
                if p:
                    out.add(p)
                if isinstance(val, str):
                    p = CASEGraph._extract_prefix(val, context_keys)
                    if p:
                        out.add(p)
                else:
                    CASEGraph._collect_prefixes(val, context_keys, out)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, str):
                    p = CASEGraph._extract_prefix(item, context_keys)
                    if p:
                        out.add(p)
                else:
                    CASEGraph._collect_prefixes(item, context_keys, out)

    def _compact_iri(self, iri: str) -> str:
        """Compact a full IRI to prefixed form using the context."""
        for prefix, ns in self._context.items():
            if iri.startswith(ns):
                local = iri[len(ns):]
                return f"{prefix}:{local}"
        return iri


def _build_class_registry(extra_classes: list[type] | None = None) -> dict[str, type]:
    """Build a mapping from CLASS_IRI -> Python dataclass for all generated classes.

    The core registry is cached process-wide (#70). Extension classes from
    ``extra_classes`` are layered on a shallow copy so callers cannot mutate
    the shared cache.
    """
    global _CLASS_REGISTRY_CACHE
    if _CLASS_REGISTRY_CACHE is None:
        registry: dict[str, type] = {}
        import importlib
        module_names = [
            "case_uco.case.investigation",
            "case_uco.uco.action",
            "case_uco.uco.analysis",
            "case_uco.uco.configuration",
            "case_uco.uco.core",
            "case_uco.uco.identity",
            "case_uco.uco.location",
            "case_uco.uco.marking",
            "case_uco.uco.observable",
            "case_uco.uco.pattern",
            "case_uco.uco.role",
            "case_uco.uco.time",
            "case_uco.uco.tool",
            "case_uco.uco.types",
            "case_uco.uco.victim",
        ]

        for mod_name in module_names:
            try:
                mod = importlib.import_module(mod_name)
            except ImportError:
                continue
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if isinstance(attr, type) and is_dataclass(attr) and hasattr(attr, "CLASS_IRI"):
                    registry[attr.CLASS_IRI] = attr
        _CLASS_REGISTRY_CACHE = registry

    result = dict(_CLASS_REGISTRY_CACHE)
    if extra_classes:
        for cls in extra_classes:
            if hasattr(cls, "CLASS_IRI"):
                result[cls.CLASS_IRI] = cls
    return result


_CLASS_REGISTRY_CACHE: dict[str, type] | None = None


def clear_class_registry_cache() -> None:
    """Invalidate the process-wide deserialization class registry (#70)."""
    global _CLASS_REGISTRY_CACHE
    _CLASS_REGISTRY_CACHE = None


def _expand_iri(compact: str, context: dict[str, str]) -> str:
    """Expand a prefixed IRI (e.g. 'uco-tool:Tool') to a full IRI."""
    if "://" in compact:
        return compact
    if ":" in compact:
        prefix, local = compact.split(":", 1)
        ns = context.get(prefix)
        if ns:
            return ns + local
    return compact


def _rehydrate(
    raw: dict[str, Any],
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> Any:
    """Convert a JSON-LD dict back to a typed Python dataclass instance."""
    type_value = raw.get("@type")
    if not type_value:
        return raw

    type_iri = _expand_iri(type_value, context)
    cls = iri_to_class.get(type_iri)
    if cls is None:
        return raw

    if not is_dataclass(cls):
        return raw

    jsonld_key_to_field: dict[str, tuple[str, Field[Any]]] = {}
    for f in fields(cls):
        key = f.metadata.get("jsonld_key")
        if key:
            jsonld_key_to_field[key] = (f.name, f)

    kwargs: dict[str, Any] = {}
    for key, value in raw.items():
        if key in ("@id", "@type"):
            continue
        field_info = jsonld_key_to_field.get(key)
        if field_info is None:
            continue
        field_name, f = field_info
        kwargs[field_name] = _coerce_value(value, f, iri_to_class, context)

    try:
        return cls(**kwargs)
    except (TypeError, ValueError):
        return raw


def _coerce_value(
    value: Any,
    field_info: Field[Any],
    iri_to_class: dict[str, type],
    context: dict[str, str],
) -> Any:
    """Coerce a JSON-LD value back to the Python type expected by the field."""
    if isinstance(value, dict):
        if "@value" in value:
            raw_val = value["@value"]
            xsd_type = value.get("@type", "")
            if "boolean" in xsd_type:
                return raw_val == "true" or raw_val is True
            if "integer" in xsd_type:
                return int(raw_val)
            if "decimal" in xsd_type or "float" in xsd_type or "double" in xsd_type:
                return float(raw_val)
            if "dateTime" in xsd_type:
                return datetime.fromisoformat(str(raw_val))
            return raw_val
        if "@type" in value:
            return _rehydrate(value, iri_to_class, context)
        if "@id" in value:
            return value["@id"]
        return value

    if isinstance(value, list):
        return [_coerce_value(item, field_info, iri_to_class, context) for item in value]

    return value
