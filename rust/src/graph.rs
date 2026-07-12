//! CaseGraph — main entry point for building and serializing CASE/UCO graphs in Rust.

use serde::Serialize;
use serde_json::{json, Map, Value};
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use uuid::Uuid;

/// Raised when a node with the same `@id` conflicts with an existing node.
#[derive(Debug, Clone)]
pub struct DuplicateNodeError {
    pub node_id: String,
    pub detail: String,
}

impl std::fmt::Display for DuplicateNodeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Duplicate @id '{}'", self.node_id)?;
        if !self.detail.is_empty() {
            write!(f, ": {}", self.detail)?;
        }
        Ok(())
    }
}

impl std::error::Error for DuplicateNodeError {}

/// Graph composition and lookup errors.
#[derive(Debug)]
pub enum GraphError {
    Duplicate(DuplicateNodeError),
    NotFound(String),
    InvalidArgument(String),
}

impl std::fmt::Display for GraphError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            GraphError::Duplicate(e) => write!(f, "{e}"),
            GraphError::NotFound(id) => write!(f, "No node with @id '{id}'"),
            GraphError::InvalidArgument(msg) => write!(f, "{msg}"),
        }
    }
}

impl std::error::Error for GraphError {}

/// Errors from loading JSON-LD into a graph.
#[derive(Debug)]
pub enum LoadError {
    Json(serde_json::Error),
    Duplicate(DuplicateNodeError),
}

impl std::fmt::Display for LoadError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LoadError::Json(e) => write!(f, "{e}"),
            LoadError::Duplicate(e) => write!(f, "{e}"),
        }
    }
}

impl std::error::Error for LoadError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            LoadError::Json(e) => Some(e),
            LoadError::Duplicate(e) => Some(e),
        }
    }
}

/// Trait implemented by generated CASE/UCO types so that `CaseGraph::create`
/// can read the class IRI and type name without manual arguments.
pub trait CaseObject {
    fn class_iri() -> &'static str;
    fn type_name() -> &'static str;
    /// Validate ontology-required fields. Returns `Ok(())` if all required
    /// fields are present, or `Err` with a message identifying the first
    /// missing field.
    fn validate(&self) -> Result<(), String> {
        Ok(())
    }
}

/// Build a CASE/UCO JSON-LD graph with typed objects.
pub struct CaseGraph {
    context: HashMap<String, String>,
    objects: Vec<Value>,
    iri_index: HashMap<String, usize>,
    /// When true, [`CaseGraph::load`] rejects duplicate `@id` instead of merging.
    reject_duplicates: bool,
}

impl CaseGraph {
    pub fn new(kb_prefix: &str) -> Self {
        let mut context = default_context();
        context.insert("kb".to_string(), kb_prefix.to_string());

        CaseGraph {
            context,
            objects: Vec::new(),
            iri_index: HashMap::new(),
            reject_duplicates: false,
        }
    }

    /// When true, [`load`](Self::load) raises on duplicate `@id` instead of merging.
    /// Default is false (merge-compatible) for backward compatibility with merge workflows.
    pub fn reject_duplicates(&self) -> bool {
        self.reject_duplicates
    }

    pub fn set_reject_duplicates(&mut self, reject: bool) {
        self.reject_duplicates = reject;
    }

    pub fn add_context(&mut self, prefix: &str, iri: &str) {
        self.context.insert(prefix.to_string(), iri.to_string());
    }

    /// Add a generated CASE/UCO object to the graph, auto-generating a UUID-based @id.
    ///
    /// This is the preferred API — the type name and class IRI are read from
    /// the [`CaseObject`] trait that the code generator implements on every
    /// generated struct. Returns the assigned @id.
    ///
    /// Panics if any ontology-required field is missing.
    pub fn create<T: CaseObject + Serialize>(&mut self, instance: &T) -> String {
        if let Err(msg) = instance.validate() {
            panic!("{}", msg);
        }
        let id = format!("kb:{}-{}", T::type_name(), Uuid::new_v4());
        self.add_with_id(&id, T::class_iri(), instance)
    }

    /// Add a generated CASE/UCO object with a user-supplied @id.
    ///
    /// Use this when you need deterministic or externally-controlled IRIs
    /// instead of auto-generated UUIDs.
    ///
    /// Panics if any ontology-required field is missing.
    pub fn create_with_id<T: CaseObject + Serialize>(&mut self, id: &str, instance: &T) -> String {
        if let Err(msg) = instance.validate() {
            panic!("{}", msg);
        }
        self.add_with_id(id, T::class_iri(), instance)
    }

    /// Add a serializable object to the graph with explicit type info.
    /// Returns the assigned @id.
    pub fn add<T: Serialize>(&mut self, type_name: &str, class_iri: &str, instance: &T) -> String {
        let id = format!("kb:{}-{}", type_name, Uuid::new_v4());
        self.add_with_id(&id, class_iri, instance)
    }

    /// Add a serializable object with a specific @id and class IRI.
    pub fn add_with_id<T: Serialize>(&mut self, id: &str, class_iri: &str, instance: &T) -> String {
        let compact_type = self.compact_iri(class_iri);

        let mut obj_value = match serde_json::to_value(instance) {
            Ok(v) => v,
            Err(e) => panic!("failed to serialize object into JSON-LD value: {e}"),
        };
        obj_value = self.convert_value(obj_value);
        if let Value::Object(ref mut map) = obj_value {
            map.insert("@id".to_string(), Value::String(id.to_string()));
            map.insert("@type".to_string(), Value::String(compact_type));
            map.remove("class_iri");
        }

        self.append_object(obj_value)
            .unwrap_or_else(|e| panic!("failed to add object: {e}"));
        id.to_string()
    }

    /// Expand a compact IRI using this graph's context.
    pub fn expand_iri(&self, node_id: &str) -> String {
        expand_compact_iri(node_id, &self.context)
    }

    /// Return true if a node with this `@id` (compact or expanded) exists.
    pub fn contains(&self, node_id: &str) -> bool {
        self.find_object_index(node_id).is_some()
    }

    /// Return the JSON-LD object for a node by compact or expanded `@id`.
    pub fn get(&self, node_id: &str) -> Option<&Map<String, Value>> {
        self.find_object_index(node_id)
            .and_then(|idx| self.objects[idx].as_object())
    }

    /// Create or update a JSON-LD node by `@id`.
    pub fn upsert_node(
        &mut self,
        node_id: &str,
        types: Option<Value>,
        properties: Option<Map<String, Value>>,
    ) -> Result<&mut Map<String, Value>, GraphError> {
        if let Some(idx) = self.find_object_index(node_id) {
            let obj = self.objects[idx].as_object_mut().expect("indexed node must be object");
            if let Some(types_val) = types {
                let merged = merge_types(obj.get("@type"), Some(types_val));
                obj.insert("@type".to_string(), normalize_type_value(merged));
            }
            if let Some(props) = properties {
                for (key, value) in props {
                    set_property(obj, &key, value);
                }
            }
            return Ok(self.objects[idx].as_object_mut().unwrap());
        }

        let mut obj = Map::new();
        obj.insert("@id".to_string(), Value::String(node_id.to_string()));
        if let Some(types_val) = types {
            obj.insert("@type".to_string(), normalize_type_value(types_val));
        }
        if let Some(props) = properties {
            for (key, value) in props {
                set_property(&mut obj, &key, value);
            }
        }
        self.append_object(Value::Object(obj)).map_err(GraphError::Duplicate)?;
        Ok(self
            .objects
            .last_mut()
            .unwrap()
            .as_object_mut()
            .unwrap())
    }

    /// Add an `rdf:type` to an existing node (same `@id`).
    pub fn add_type(&mut self, node_id: &str, type_iri: &str) -> Result<(), GraphError> {
        let idx = self
            .find_object_index(node_id)
            .ok_or_else(|| GraphError::NotFound(node_id.to_string()))?;
        let obj = self.objects[idx].as_object_mut().unwrap();
        let merged = merge_types(obj.get("@type"), Some(Value::String(type_iri.to_string())));
        obj.insert("@type".to_string(), normalize_type_value(merged));
        Ok(())
    }

    /// Add or merge a property on an existing node.
    pub fn add_property(
        &mut self,
        node_id: &str,
        key: &str,
        value: Value,
    ) -> Result<(), GraphError> {
        let idx = self
            .find_object_index(node_id)
            .ok_or_else(|| GraphError::NotFound(node_id.to_string()))?;
        let obj = self.objects[idx].as_object_mut().unwrap();
        set_property(obj, key, value);
        Ok(())
    }

    /// Add a direct property edge source --predicate--> target.
    pub fn link(
        &mut self,
        source_id: &str,
        predicate: &str,
        target_id: &str,
    ) -> Result<(), GraphError> {
        self.add_property(
            source_id,
            predicate,
            json!({ "@id": target_id }),
        )
    }

    /// Create a `uco-core:Relationship` node with deterministic `@id`.
    pub fn create_relationship(
        &mut self,
        source_id: &str,
        target_id: &str,
        kind: &str,
        directional: bool,
        description: Option<&str>,
    ) -> Result<Map<String, Value>, GraphError> {
        if !self.contains(source_id) {
            return Err(GraphError::InvalidArgument(format!(
                "Relationship source not in graph: {source_id}"
            )));
        }
        if !self.contains(target_id) {
            return Err(GraphError::InvalidArgument(format!(
                "Relationship target not in graph: {target_id}"
            )));
        }
        if kind.is_empty() {
            return Err(GraphError::InvalidArgument(
                "kindOfRelationship is required".into(),
            ));
        }

        let rel_id = self.deterministic_relationship_id(source_id, target_id, kind);
        let mut props = Map::new();
        props.insert(
            "uco-core:source".to_string(),
            json!([{ "@id": source_id }]),
        );
        props.insert(
            "uco-core:target".to_string(),
            json!([{ "@id": target_id }]),
        );
        props.insert(
            "uco-core:kindOfRelationship".to_string(),
            Value::String(kind.to_string()),
        );
        props.insert(
            "uco-core:isDirectional".to_string(),
            json!({
                "@type": "xsd:boolean",
                "@value": if directional { "true" } else { "false" },
            }),
        );
        if let Some(desc) = description {
            props.insert(
                "uco-core:description".to_string(),
                Value::String(desc.to_string()),
            );
        }

        let rel = self.upsert_node(
            &rel_id,
            Some(Value::String("uco-core:Relationship".to_string())),
            Some(props),
        )?;
        Ok(rel.clone())
    }

    /// Return the number of objects in the graph.
    pub fn len(&self) -> usize {
        self.objects.len()
    }

    /// Return true if the graph contains no objects.
    pub fn is_empty(&self) -> bool {
        self.objects.is_empty()
    }

    /// Load a JSON-LD string into this graph, merging context and upserting objects.
    pub fn load(&mut self, json: &str) -> Result<(), LoadError> {
        let doc: Value = serde_json::from_str(json).map_err(LoadError::Json)?;
        if let Some(ctx) = doc.get("@context") {
            if let Some(ctx_map) = ctx.as_object() {
                for (k, v) in ctx_map {
                    if let Some(s) = v.as_str() {
                        self.context.insert(k.clone(), s.to_string());
                    }
                }
            }
        }
        if let Some(graph) = doc.get("@graph") {
            if let Some(arr) = graph.as_array() {
                for obj in arr {
                    self.ingest_raw_node(obj.clone())
                        .map_err(LoadError::Duplicate)?;
                }
            }
        }
        Ok(())
    }

    /// Read and load a JSON-LD file into this graph.
    pub fn load_file(&mut self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let json = std::fs::read_to_string(path)?;
        self.load(&json)?;
        Ok(())
    }

    /// Parse a JSON-LD string and return the graph with its objects.
    ///
    /// Since Rust lacks runtime reflection, objects are returned as raw
    /// `serde_json::Value` items rather than typed structs. Consumers can
    /// match on `@type` fields manually to downcast.
    pub fn from_jsonld(json: &str) -> Result<(CaseGraph, Vec<Value>), String> {
        let doc: Value =
            serde_json::from_str(json).map_err(|e| format!("Failed to parse JSON: {e}"))?;

        let mut graph = CaseGraph::new("http://example.org/kb/");

        if let Some(ctx) = doc.get("@context").and_then(|c| c.as_object()) {
            for (k, v) in ctx {
                if let Some(s) = v.as_str() {
                    graph.context.insert(k.clone(), s.to_string());
                }
            }
        }

        let mut objects = Vec::new();
        if let Some(arr) = doc.get("@graph").and_then(|g| g.as_array()) {
            for obj in arr {
                graph
                    .append_object(obj.clone())
                    .unwrap_or_else(|e| panic!("failed to index parsed object: {e}"));
                objects.push(obj.clone());
            }
        }

        Ok((graph, objects))
    }

    /// Serialize the graph to a JSON-LD string.
    ///
    /// Returns `Err` if the internal structure cannot be serialized
    /// (should not happen under normal use).
    pub fn serialize(&self) -> Result<String, serde_json::Error> {
        let used = self.used_prefixes();
        let context_value: Map<String, Value> = self
            .context
            .iter()
            .filter(|(k, _)| used.contains(k.as_str()))
            .map(|(k, v)| (k.clone(), Value::String(v.clone())))
            .collect();

        let doc = json!({
            "@context": context_value,
            "@graph": self.objects,
        });

        serde_json::to_string_pretty(&doc)
    }

    fn used_prefixes(&self) -> std::collections::HashSet<String> {
        let mut prefixes = std::collections::HashSet::new();
        let context_keys: std::collections::HashSet<&str> =
            self.context.keys().map(|k| k.as_str()).collect();
        for obj in &self.objects {
            collect_prefixes(obj, &context_keys, &mut prefixes);
        }
        prefixes
    }

    /// Write the graph to a file.
    pub fn write(&self, path: &str) -> std::io::Result<()> {
        let json = self.serialize().map_err(std::io::Error::other)?;
        std::fs::write(path, json)
    }

    /// Validate this graph against CASE/UCO SHACL constraints using `case_validate`.
    ///
    /// Requires `case-utils` (`pip install case-utils`) and `case_validate` on PATH.
    /// Returns the validation output on success, or an error message on failure.
    pub fn validate(&self, case_version: &str) -> Result<String, String> {
        use std::io::Write;
        let json = self.serialize().map_err(|e| format!("Serialization failed: {e}"))?;
        let mut tmp = tempfile::NamedTempFile::new()
            .map_err(|e| format!("Failed to create temp file: {e}"))?;
        tmp.write_all(json.as_bytes())
            .map_err(|e| format!("Failed to write temp file: {e}"))?;
        let output = std::process::Command::new("case_validate")
            .arg("--built-version")
            .arg(case_version)
            .arg(tmp.path())
            .output()
            .map_err(|e| format!("case_validate not found on PATH (pip install case-utils): {e}"))?;
        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            let stdout = String::from_utf8_lossy(&output.stdout);
            let msg = if stderr.is_empty() { stdout } else { stderr };
            return Err(format!("Validation failed:\n{}", msg.trim()));
        }
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }

    /// Estimate the number of RDF triples this graph will produce.
    pub fn estimate_triples(&self) -> usize {
        self.objects.iter().map(count_triples).sum()
    }

    /// Split the graph into smaller chunks of at most `max_objects` each.
    ///
    /// Each chunk gets a clone of the context. The original graph is not modified.
    pub fn split(&self, max_objects: usize) -> Vec<CaseGraph> {
        self.objects
            .chunks(max_objects)
            .map(|chunk| {
                let mut part = CaseGraph {
                    context: self.context.clone(),
                    objects: Vec::new(),
                    iri_index: HashMap::new(),
                    reject_duplicates: self.reject_duplicates,
                };
                for obj in chunk {
                    part.append_object(obj.clone())
                        .unwrap_or_else(|e| panic!("failed to split graph: {e}"));
                }
                part
            })
            .collect()
    }

    /// Load and merge multiple JSON-LD files into a single graph.
    pub fn merge_files(paths: &[&str], kb_prefix: &str) -> Result<CaseGraph, Box<dyn std::error::Error>> {
        let mut merged = CaseGraph::new(kb_prefix);
        for path in paths {
            merged.load_file(path)?;
        }
        Ok(merged)
    }

    fn compact_iri(&self, iri: &str) -> String {
        for (prefix, ns) in &self.context {
            if iri.starts_with(ns.as_str()) {
                return format!("{}:{}", prefix, &iri[ns.len()..]);
            }
        }
        iri.to_string()
    }

    fn append_object(&mut self, obj: Value) -> Result<(), DuplicateNodeError> {
        let node_id = obj
            .as_object()
            .and_then(|map| map.get("@id"))
            .and_then(|id| id.as_str())
            .map(str::to_string);

        if let Some(ref id) = node_id {
            if self.find_object_index(id).is_some() {
                return Err(DuplicateNodeError {
                    node_id: id.clone(),
                    detail: "use add_type/upsert_node or merge-compatible load instead of appending a second node".into(),
                });
            }
        }

        self.objects.push(obj);
        if let Some(id) = node_id {
            self.index_node(&id, self.objects.len() - 1);
        }
        Ok(())
    }

    fn index_node(&mut self, node_id: &str, index: usize) {
        let expanded = self.expand_iri(node_id);
        self.iri_index.insert(expanded, index);
    }

    fn find_object_index(&self, node_id: &str) -> Option<usize> {
        let expanded = self.expand_iri(node_id);
        if let Some(&idx) = self.iri_index.get(&expanded) {
            if idx < self.objects.len() {
                return Some(idx);
            }
        }
        for (i, obj) in self.objects.iter().enumerate() {
            if let Some(oid) = obj.get("@id").and_then(|v| v.as_str()) {
                if oid == node_id || self.expand_iri(oid) == expanded {
                    return Some(i);
                }
            }
        }
        None
    }

    fn ingest_raw_node(&mut self, raw: Value) -> Result<(), DuplicateNodeError> {
        let node_id = raw
            .as_object()
            .and_then(|map| map.get("@id"))
            .and_then(|id| id.as_str())
            .map(str::to_string);

        let Some(node_id) = node_id else {
            self.objects.push(raw);
            return Ok(());
        };

        if let Some(idx) = self.find_object_index(&node_id) {
            if self.reject_duplicates {
                return Err(DuplicateNodeError {
                    node_id,
                    detail: "conflicting duplicate during load".into(),
                });
            }

            let existing = self.objects[idx].as_object_mut().unwrap();
            if let Some(types) = raw.get("@type") {
                let merged = merge_types(existing.get("@type"), Some(types.clone()));
                existing.insert("@type".to_string(), normalize_type_value(merged));
            }
            if let Some(raw_map) = raw.as_object() {
                for (key, value) in raw_map {
                    if key == "@id" || key == "@type" {
                        continue;
                    }
                    set_property(existing, key, value.clone());
                }
            }
            return Ok(());
        }

        self.append_object(raw)
    }

    fn deterministic_relationship_id(&self, source_id: &str, target_id: &str, kind: &str) -> String {
        let payload = format!(
            "{}|{}|{}",
            self.expand_iri(source_id),
            self.expand_iri(target_id),
            kind
        );
        let digest = Sha256::digest(payload.as_bytes());
        let hex: String = digest.iter().take(6).map(|b| format!("{b:02x}")).collect();
        let safe_kind = kind.replace(' ', "_");
        format!("kb:rel-{safe_kind}-{hex}")
    }

    fn convert_value(&self, value: Value) -> Value {
        match value {
            Value::Object(map) => {
                let converted: Map<String, Value> = map
                    .into_iter()
                    .map(|(k, v)| (k, self.convert_value(v)))
                    .collect();
                Value::Object(converted)
            }
            Value::Array(items) => {
                Value::Array(items.into_iter().map(|item| self.convert_value(item)).collect())
            }
            Value::Bool(boolean) => json!({
                "@type": "xsd:boolean",
                "@value": if boolean { "true" } else { "false" },
            }),
            Value::Number(number) => {
                if number.is_i64() || number.is_u64() {
                    json!({
                        "@type": "xsd:integer",
                        "@value": number.to_string(),
                    })
                } else {
                    json!({
                        "@type": "xsd:decimal",
                        "@value": number.to_string(),
                    })
                }
            }
            other => other,
        }
    }
}

fn expand_compact_iri(compact: &str, context: &HashMap<String, String>) -> String {
    if compact.contains("://") {
        return compact.to_string();
    }
    if let Some(colon) = compact.find(':') {
        if colon > 0 {
            let prefix = &compact[..colon];
            if let Some(ns) = context.get(prefix) {
                return format!("{}{}", ns, &compact[colon + 1..]);
            }
        }
    }
    compact.to_string()
}

fn as_type_list(types: Option<&Value>) -> Vec<String> {
    match types {
        None => Vec::new(),
        Some(Value::String(s)) => vec![s.clone()],
        Some(Value::Array(arr)) => arr
            .iter()
            .filter_map(|v| v.as_str().map(str::to_string))
            .collect(),
        Some(other) => vec![other.to_string()],
    }
}

fn normalize_type_value(types: Value) -> Value {
    match types {
        Value::Array(arr) if arr.len() == 1 => arr[0].clone(),
        other => other,
    }
}

fn merge_types(existing: Option<&Value>, new_types: Option<Value>) -> Value {
    let mut merged = as_type_list(existing);
    for type_iri in as_type_list(new_types.as_ref()) {
        if !merged.contains(&type_iri) {
            merged.push(type_iri);
        }
    }
    if merged.len() == 1 {
        Value::String(merged[0].clone())
    } else {
        Value::Array(merged.into_iter().map(Value::String).collect())
    }
}

fn set_property(obj: &mut Map<String, Value>, key: &str, value: Value) {
    use serde_json::map::Entry;

    match obj.entry(key.to_string()) {
        Entry::Vacant(entry) => {
            entry.insert(value);
        }
        Entry::Occupied(mut entry) => {
            let existing = entry.get().clone();
            if existing == value {
                return;
            }

            if let Value::Array(mut list) = existing {
                if let Some(ref_id) = value.get("@id").and_then(|v| v.as_str()) {
                    if list.iter().any(|item| {
                        item.get("@id")
                            .and_then(|v| v.as_str())
                            .map(|id| id == ref_id)
                            .unwrap_or(false)
                    }) {
                        return;
                    }
                }
                if !list.iter().any(|item| item == &value) {
                    list.push(value);
                }
                entry.insert(Value::Array(list));
                return;
            }

            if let (Some(existing_id), Some(value_id)) = (
                existing.get("@id").and_then(|v| v.as_str()),
                value.get("@id").and_then(|v| v.as_str()),
            ) {
                if existing_id == value_id {
                    return;
                }
            }

            entry.insert(Value::Array(vec![existing, value]));
        }
    }
}

fn count_triples(value: &Value) -> usize {
    match value {
        Value::Object(map) => {
            let mut count = 0;
            for (key, val) in map {
                if key == "@id" {
                    continue;
                }
                if key == "@type" {
                    count += 1;
                    continue;
                }
                match val {
                    Value::Array(items) => {
                        for item in items {
                            if item.is_object() {
                                count += 1 + count_triples(item);
                            } else {
                                count += 1;
                            }
                        }
                    }
                    Value::Object(inner) => {
                        if inner.contains_key("@value") {
                            count += 1;
                        } else {
                            count += 1 + count_triples(val);
                        }
                    }
                    _ => {
                        count += 1;
                    }
                }
            }
            count
        }
        _ => 0,
    }
}

fn extract_prefix<'a>(
    value: &'a str,
    context_keys: &std::collections::HashSet<&str>,
) -> Option<&'a str> {
    if value.contains("://") {
        return None;
    }
    if let Some(colon) = value.find(':') {
        if colon > 0 {
            let prefix = &value[..colon];
            if context_keys.contains(prefix) {
                return Some(prefix);
            }
        }
    }
    None
}

fn collect_prefixes(
    value: &Value,
    context_keys: &std::collections::HashSet<&str>,
    out: &mut std::collections::HashSet<String>,
) {
    match value {
        Value::Object(map) => {
            for (key, val) in map {
                if let Some(p) = extract_prefix(key, context_keys) {
                    out.insert(p.to_string());
                }
                if let Some(s) = val.as_str() {
                    if let Some(p) = extract_prefix(s, context_keys) {
                        out.insert(p.to_string());
                    }
                } else {
                    collect_prefixes(val, context_keys, out);
                }
            }
        }
        Value::Array(items) => {
            for item in items {
                if let Some(s) = item.as_str() {
                    if let Some(p) = extract_prefix(s, context_keys) {
                        out.insert(p.to_string());
                    }
                } else {
                    collect_prefixes(item, context_keys, out);
                }
            }
        }
        _ => {}
    }
}

fn default_context() -> HashMap<String, String> {
    let mut ctx = HashMap::new();
    ctx.insert("case-investigation".into(), "https://ontology.caseontology.org/case/investigation/".into());
    ctx.insert("kb".into(), "http://example.org/kb/".into());
    ctx.insert("uco-action".into(), "https://ontology.unifiedcyberontology.org/uco/action/".into());
    ctx.insert("uco-analysis".into(), "https://ontology.unifiedcyberontology.org/uco/analysis/".into());
    ctx.insert("uco-configuration".into(), "https://ontology.unifiedcyberontology.org/uco/configuration/".into());
    ctx.insert("uco-core".into(), "https://ontology.unifiedcyberontology.org/uco/core/".into());
    ctx.insert("uco-identity".into(), "https://ontology.unifiedcyberontology.org/uco/identity/".into());
    ctx.insert("uco-location".into(), "https://ontology.unifiedcyberontology.org/uco/location/".into());
    ctx.insert("uco-marking".into(), "https://ontology.unifiedcyberontology.org/uco/marking/".into());
    ctx.insert("uco-observable".into(), "https://ontology.unifiedcyberontology.org/uco/observable/".into());
    ctx.insert("uco-pattern".into(), "https://ontology.unifiedcyberontology.org/uco/pattern/".into());
    ctx.insert("uco-role".into(), "https://ontology.unifiedcyberontology.org/uco/role/".into());
    ctx.insert("uco-time".into(), "https://ontology.unifiedcyberontology.org/uco/time/".into());
    ctx.insert("uco-tool".into(), "https://ontology.unifiedcyberontology.org/uco/tool/".into());
    ctx.insert("uco-types".into(), "https://ontology.unifiedcyberontology.org/uco/types/".into());
    ctx.insert("uco-victim".into(), "https://ontology.unifiedcyberontology.org/uco/victim/".into());
    ctx.insert("uco-vocabulary".into(), "https://ontology.unifiedcyberontology.org/uco/vocabulary/".into());
    ctx.insert("xsd".into(), "http://www.w3.org/2001/XMLSchema#".into());
    ctx
}
