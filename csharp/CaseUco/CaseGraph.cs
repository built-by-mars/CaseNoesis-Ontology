// CaseGraph — main entry point for building and serializing CASE/UCO graphs in C#.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;

namespace CaseUco
{
    /// <summary>
    /// Build a CASE/UCO JSON-LD graph with typed objects.
    /// </summary>
    public class CaseGraph
    {
        private readonly Dictionary<string, string> _context;
        private readonly List<Dictionary<string, object>> _objects;
        private readonly Dictionary<object, string> _idMap;
        private readonly Dictionary<string, int> _iriIndex = new Dictionary<string, int>();

        /// <summary>
        /// When true, <see cref="Load"/> raises on duplicate <c>@id</c> instead of merging.
        /// Default is false (merge-compatible) for backward compatibility with merge workflows.
        /// </summary>
        public bool RejectDuplicates { get; set; }

        public CaseGraph(string kbPrefix = "http://example.org/kb/")
        {
            _context = new Dictionary<string, string>(DefaultContext);
            _context["kb"] = kbPrefix;
            _objects = new List<Dictionary<string, object>>();
            _idMap = new Dictionary<object, string>(new ReferenceEqualityComparer());
        }

        public void AddContext(string prefix, string iri)
        {
            _context[prefix] = iri;
        }

        /// <summary>Add an object to the graph with an auto-generated UUID @id.</summary>
        public string Add(object instance)
        {
            var id = MintId(instance);
            return AddWithId(instance, id);
        }

        /// <summary>Add an object to the graph with a user-supplied @id for deterministic IRIs.</summary>
        public string AddWithId(object instance, string id)
        {
            Validate(instance);
            _idMap[instance] = id;
            var jsonObj = ToJsonLd(instance, id);
            AppendObject(jsonObj);
            return id;
        }

        /// <summary>Validate required fields on a CASE/UCO object before adding it.</summary>
        private void Validate(object instance)
        {
            if (instance == null) return;
            foreach (var prop in instance.GetType()
                .GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Where(p => p.GetCustomAttribute<CaseRequiredAttribute>(inherit: true) != null))
            {
                var value = prop.GetValue(instance);
                if (value == null)
                    throw new System.ArgumentException(
                        $"{instance.GetType().Name}.{prop.Name} is required but was not provided.");
                if (value is IList list && list.Count == 0)
                    throw new System.ArgumentException(
                        $"{instance.GetType().Name}.{prop.Name} requires at least one value.");
            }
        }

        /// <summary>Get the @id assigned to a previously-added instance.</summary>
        public string GetId(object instance)
        {
            return _idMap.TryGetValue(instance, out var id) ? id : null;
        }

        /// <summary>Return the JSON-LD dict for a node by compact or expanded @id.</summary>
        public Dictionary<string, object> Get(string id)
        {
            return FindObject(id);
        }

        /// <summary>Return true if a node with this @id (compact or expanded) exists.</summary>
        public bool Contains(string id)
        {
            return FindObject(id) != null;
        }

        /// <summary>Expand a compact IRI using this graph's context.</summary>
        public string ExpandIri(string id)
        {
            return ExpandCompactIri(id, _context);
        }

        /// <summary>Create or update a JSON-LD node by @id.</summary>
        public Dictionary<string, object> UpsertNode(
            string id,
            object types = null,
            Dictionary<string, object> properties = null)
        {
            var obj = FindObject(id);
            if (obj == null)
            {
                obj = new Dictionary<string, object> { ["@id"] = id };
                if (types != null)
                    obj["@type"] = NormalizeTypeValue(types);
                if (properties != null)
                {
                    foreach (var kv in properties)
                        SetProperty(obj, kv.Key, kv.Value);
                }
                AppendObject(obj);
                return obj;
            }

            if (types != null)
                obj["@type"] = NormalizeTypeValue(MergeTypes(obj.ContainsKey("@type") ? obj["@type"] : null, types));
            if (properties != null)
            {
                foreach (var kv in properties)
                    SetProperty(obj, kv.Key, kv.Value);
            }
            return obj;
        }

        /// <summary>Add an rdf:type to an existing node (same @id).</summary>
        public void AddType(string id, string typeIri)
        {
            var obj = RequireObject(id);
            obj["@type"] = NormalizeTypeValue(MergeTypes(obj.ContainsKey("@type") ? obj["@type"] : null, typeIri));
        }

        /// <summary>Add or merge a property on an existing node.</summary>
        public void AddProperty(string id, string key, object value)
        {
            var obj = RequireObject(id);
            SetProperty(obj, key, value);
        }

        /// <summary>Add a direct property edge source --predicate--> target.</summary>
        public void Link(string sourceId, string predicate, string targetId)
        {
            AddProperty(sourceId, predicate, new Dictionary<string, object> { ["@id"] = targetId });
        }

        /// <summary>Create a uco-core:Relationship node with deterministic @id.</summary>
        public Dictionary<string, object> CreateRelationship(
            string sourceId,
            string targetId,
            string kind,
            bool directional = true,
            string description = null)
        {
            if (!Contains(sourceId))
                throw new KeyNotFoundException($"Relationship source not in graph: {sourceId}");
            if (!Contains(targetId))
                throw new KeyNotFoundException($"Relationship target not in graph: {targetId}");
            if (string.IsNullOrEmpty(kind))
                throw new ArgumentException("kindOfRelationship is required", nameof(kind));

            var relId = DeterministicRelationshipId(sourceId, targetId, kind);
            var props = new Dictionary<string, object>
            {
                ["uco-core:source"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = sourceId },
                },
                ["uco-core:target"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = targetId },
                },
                ["uco-core:kindOfRelationship"] = kind,
                ["uco-core:isDirectional"] = TypedLiteral("xsd:boolean", directional ? "true" : "false"),
            };
            if (description != null)
                props["uco-core:description"] = description;

            return UpsertNode(relId, "uco-core:Relationship", props);
        }

        /// <summary>Return the number of objects in the graph.</summary>
        public int Count => _objects.Count;

        /// <summary>Load a JSON-LD string into this graph, merging context and appending objects.</summary>
        public void Load(string json)
        {
            var doc = ParseJson(json);
            if (doc.TryGetValue("@context", out var ctxObj) && ctxObj is Dictionary<string, object> ctx)
            {
                foreach (var kv in ctx.Where(kv => kv.Value is string))
                {
                    _context[kv.Key] = (string)kv.Value;
                }
            }
            if (doc.TryGetValue("@graph", out var graphObj) && graphObj is List<object> graphList)
            {
                foreach (var item in graphList.OfType<Dictionary<string, object>>())
                {
                    IngestRawNode(item, RejectDuplicates);
                }
            }
        }

        /// <summary>Parse a JSON-LD string into typed objects where possible.
        /// Types are matched by scanning loaded assemblies for classes with a static ClassIri field.</summary>
        public static FromJsonLdResult FromJsonLd(string json)
        {
            var doc = ParseJson(json);
            var graph = new CaseGraph();

            if (doc.TryGetValue("@context", out var ctxObj) && ctxObj is Dictionary<string, object> ctx)
            {
                foreach (var kv in ctx.Where(kv => kv.Value is string))
                    graph._context[kv.Key] = (string)kv.Value;
            }

            var objects = new List<object>();

            if (doc.TryGetValue("@graph", out var graphObj) && graphObj is List<object> graphList)
            {
                foreach (var item in graphList.OfType<Dictionary<string, object>>())
                {
                    graph.AppendObject(item);
                    var typed = TryInstantiate(item, graph._context);
                    objects.Add(typed ?? (object)item);
                }
            }

            return new FromJsonLdResult { Graph = graph, Objects = objects };
        }

        private static string ExpandCompactIri(string value, Dictionary<string, string> context)
        {
            if (value == null) return null;
            var colonIdx = value.IndexOf(':');
            if (colonIdx > 0)
            {
                var prefix = value.Substring(0, colonIdx);
                if (context.TryGetValue(prefix, out var ns))
                    return ns + value.Substring(colonIdx + 1);
            }
            return value;
        }

        private static object TryInstantiate(Dictionary<string, object> obj, Dictionary<string, string> context)
        {
            if (!obj.TryGetValue("@type", out var typeObj) || !(typeObj is string typeStr))
                return null;

            var expandedIri = ExpandCompactIri(typeStr, context);

            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                Type[] types;
                try { types = asm.GetTypes(); }
                catch (ReflectionTypeLoadException ex) { types = ex.Types.Where(t => t != null).ToArray(); }

                foreach (var type in types.Where(t =>
                    t.IsClass && !t.IsAbstract && t.Namespace != null &&
                    t.Namespace.StartsWith("CaseUco")))
                {
                    var field = type.GetField("ClassIri", BindingFlags.Public | BindingFlags.Static);
                    if (field == null || (string)field.GetValue(null) != expandedIri)
                        continue;

                    try
                    {
                        var instance = Activator.CreateInstance(type);
                        SetPropertiesFromJsonLd(instance, obj, context);
                        return instance;
                    }
                    catch (MemberAccessException) { return null; }
                    catch (TargetInvocationException) { return null; }
                }
            }

            return null;
        }

        private static void SetPropertiesFromJsonLd(object instance, Dictionary<string, object> obj, Dictionary<string, string> context)
        {
            var type = instance.GetType();
            foreach (var prop in type.GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Where(p => p.CanWrite))
            {
                string matchKey = null;

                var attr = prop.GetCustomAttribute<JsonLdPropertyAttribute>(inherit: true);
                if (attr != null && obj.ContainsKey(attr.Key))
                    matchKey = attr.Key;

                if (matchKey == null)
                {
                    var nsField = (prop.DeclaringType ?? type).GetField("NamespacePrefix");
                    var ns = nsField != null ? (string)nsField.GetValue(null) : "uco-core";
                    var camelName = char.ToLower(prop.Name[0]) + prop.Name.Substring(1);
                    var candidate = ns + ":" + camelName;
                    if (obj.ContainsKey(candidate))
                        matchKey = candidate;
                }

                if (matchKey == null) continue;

                try { prop.SetValue(instance, ConvertToClrType(obj[matchKey], prop.PropertyType)); }
                catch (ArgumentException) { /* skip: property type mismatch during deserialization */ }
                catch (TargetException) { /* skip: target object mismatch */ }
                catch (TargetInvocationException) { /* skip: setter threw */ }
            }
        }

        private static object ConvertToClrType(object value, Type target)
        {
            if (value == null) return null;

            if (value is Dictionary<string, object> dict && dict.TryGetValue("@value", out var raw))
            {
                if (raw is string rawStr)
                {
                    if (target == typeof(string)) return rawStr;
                    if (target == typeof(int)) return int.Parse(rawStr, CultureInfo.InvariantCulture);
                    if (target == typeof(long)) return long.Parse(rawStr, CultureInfo.InvariantCulture);
                    if (target == typeof(double)) return double.Parse(rawStr, CultureInfo.InvariantCulture);
                    if (target == typeof(bool)) return rawStr == "true";
                    if (target == typeof(DateTime)) return DateTime.Parse(rawStr, CultureInfo.InvariantCulture);
                }
                return raw;
            }

            if (target == typeof(string) && value is string s) return s;
            if (target == typeof(long) && value is long l) return l;
            if (target == typeof(int) && value is long li) return (int)li;
            if (target == typeof(double) && value is double d) return d;
            if (target == typeof(bool) && value is bool b) return b;

            return value;
        }

        /// <summary>Serialize the graph to a JSON-LD string.</summary>
        public string Serialize(bool indented = true)
        {
            var doc = new Dictionary<string, object>
            {
                ["@context"] = PrunedContext(),
                ["@graph"] = _objects,
            };
            return ToJsonString(doc, indented ? 0 : -1);
        }

        private Dictionary<string, string> PrunedContext()
        {
            var used = UsedPrefixes();
            return _context
                .Where(kv => used.Contains(kv.Key))
                .ToDictionary(kv => kv.Key, kv => kv.Value);
        }

        private HashSet<string> UsedPrefixes()
        {
            var prefixes = new HashSet<string>();
            var contextKeys = new HashSet<string>(_context.Keys);
            foreach (var obj in _objects)
                CollectPrefixes(obj, contextKeys, prefixes);
            return prefixes;
        }

        private static string ExtractPrefix(string value, HashSet<string> contextKeys)
        {
            if (value.Contains("://")) return null;
            var colon = value.IndexOf(':');
            if (colon > 0)
            {
                var prefix = value.Substring(0, colon);
                if (contextKeys.Contains(prefix)) return prefix;
            }
            return null;
        }

        private static void CollectPrefixes(object node, HashSet<string> contextKeys, HashSet<string> output)
        {
            if (node is Dictionary<string, object> dict)
            {
                foreach (var kv in dict)
                {
                    var p = ExtractPrefix(kv.Key, contextKeys);
                    if (p != null) output.Add(p);
                    if (kv.Value is string strVal)
                    {
                        p = ExtractPrefix(strVal, contextKeys);
                        if (p != null) output.Add(p);
                    }
                    else
                    {
                        CollectPrefixes(kv.Value, contextKeys, output);
                    }
                }
            }
            else if (node is List<object> list)
            {
                foreach (var item in list)
                {
                    if (item is string strItem)
                    {
                        var p = ExtractPrefix(strItem, contextKeys);
                        if (p != null) output.Add(p);
                    }
                    else
                    {
                        CollectPrefixes(item, contextKeys, output);
                    }
                }
            }
        }

        /// <summary>Write the graph to a file.</summary>
        public void Write(string path)
        {
            System.IO.File.WriteAllText(path, Serialize());
        }

        /// <summary>Validate this graph against CASE/UCO SHACL constraints using case_validate.
        /// Requires case-utils (pip install case-utils) to be installed and case_validate on PATH.</summary>
        /// <param name="caseVersion">The CASE built-version to validate against (default "case-1.4.0").</param>
        /// <returns>The validation output on success.</returns>
        /// <exception cref="InvalidOperationException">Thrown if validation fails or case_validate is not found.</exception>
        public string ValidateGraph(string caseVersion = "case-1.4.0")
        {
            var tmpPath = System.IO.Path.GetTempFileName() + ".jsonld";
            try
            {
                System.IO.File.WriteAllText(tmpPath, Serialize());
                var psi = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = "case_validate",
                    Arguments = $"--built-version {caseVersion} \"{tmpPath}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                };
                System.Diagnostics.Process process;
                try
                {
                    process = System.Diagnostics.Process.Start(psi);
                }
                catch (System.ComponentModel.Win32Exception)
                {
                    throw new InvalidOperationException(
                        "case_validate not found on PATH. Install with: pip install case-utils");
                }
                var stdout = process.StandardOutput.ReadToEnd();
                var stderr = process.StandardError.ReadToEnd();
                process.WaitForExit();
                if (process.ExitCode != 0)
                {
                    var msg = string.IsNullOrWhiteSpace(stderr) ? stdout : stderr;
                    throw new InvalidOperationException($"Validation failed:\n{msg.Trim()}");
                }
                return stdout;
            }
            finally
            {
                if (System.IO.File.Exists(tmpPath))
                    System.IO.File.Delete(tmpPath);
            }
        }

        /// <summary>Estimate the number of RDF triples this graph will produce.</summary>
        public int EstimateTriples()
        {
            int total = 0;
            foreach (var obj in _objects)
                total += CountTriples(obj);
            return total;
        }

        private static int CountTriples(Dictionary<string, object> obj)
        {
            int count = 0;
            foreach (var kv in obj.Where(kv => kv.Key != "@id"))
            {
                if (kv.Key == "@type") { count++; continue; }
                if (kv.Value is List<object> list)
                {
                    foreach (var item in list)
                    {
                        if (item is Dictionary<string, object> nested)
                            count += 1 + CountTriples(nested);
                        else
                            count++;
                    }
                }
                else if (kv.Value is Dictionary<string, object> dict)
                {
                    if (dict.ContainsKey("@value"))
                        count++;
                    else
                        count += 1 + CountTriples(dict);
                }
                else
                {
                    count++;
                }
            }
            return count;
        }

        /// <summary>Split the graph into smaller chunks of at most maxObjects each.</summary>
        public List<CaseGraph> Split(int maxObjects = 10000)
        {
            var chunks = new List<CaseGraph>();
            for (int i = 0; i < _objects.Count; i += maxObjects)
            {
                var chunk = new CaseGraph(_context["kb"]);
                foreach (var kv in _context)
                    chunk._context[kv.Key] = kv.Value;
                int end = Math.Min(i + maxObjects, _objects.Count);
                for (int j = i; j < end; j++)
                    chunk.AppendObject(new Dictionary<string, object>(_objects[j]));
                chunks.Add(chunk);
            }
            return chunks;
        }

        /// <summary>Load and merge multiple JSON-LD files into a single graph.</summary>
        public static CaseGraph MergeFiles(IEnumerable<string> paths, string kbPrefix = "http://example.org/kb/")
        {
            var merged = new CaseGraph(kbPrefix);
            foreach (var path in paths)
            {
                merged.Load(System.IO.File.ReadAllText(path));
            }
            return merged;
        }

        private void AppendObject(Dictionary<string, object> obj)
        {
            var nodeId = obj.TryGetValue("@id", out var idObj) ? idObj as string : null;
            if (nodeId != null && FindObject(nodeId) != null)
            {
                throw new InvalidOperationException(
                    $"Duplicate @id '{nodeId}': use AddType/UpsertNode or merge-compatible Load instead of appending a second node");
            }
            _objects.Add(obj);
            if (nodeId != null)
                IndexNode(nodeId, _objects.Count - 1);
        }

        private void IndexNode(string nodeId, int index)
        {
            var expanded = ExpandIri(nodeId);
            _iriIndex[expanded] = index;
        }

        private Dictionary<string, object> FindObject(string nodeId)
        {
            var expanded = ExpandIri(nodeId);
            if (_iriIndex.TryGetValue(expanded, out var idx))
            {
                if (idx < _objects.Count)
                    return _objects[idx];
            }
            for (var i = 0; i < _objects.Count; i++)
            {
                var obj = _objects[i];
                if (!obj.TryGetValue("@id", out var oidObj) || !(oidObj is string oid))
                    continue;
                if (oid == nodeId || ExpandIri(oid) == expanded)
                {
                    IndexNode(oid, i);
                    return obj;
                }
            }
            return null;
        }

        private Dictionary<string, object> RequireObject(string nodeId)
        {
            var obj = FindObject(nodeId);
            if (obj == null)
                throw new KeyNotFoundException($"No node with @id '{nodeId}'");
            return obj;
        }

        private void IngestRawNode(Dictionary<string, object> raw, bool rejectDuplicates)
        {
            if (!raw.TryGetValue("@id", out var idObj) || !(idObj is string nodeId))
            {
                _objects.Add(raw);
                return;
            }

            var existing = FindObject(nodeId);
            if (existing == null)
            {
                AppendObject(raw);
                return;
            }

            if (rejectDuplicates)
            {
                throw new InvalidOperationException(
                    $"Duplicate @id '{nodeId}': conflicting duplicate during load");
            }

            if (raw.ContainsKey("@type"))
            {
                existing["@type"] = NormalizeTypeValue(
                    MergeTypes(existing.ContainsKey("@type") ? existing["@type"] : null, raw["@type"]));
            }
            foreach (var kv in raw)
            {
                if (kv.Key == "@id" || kv.Key == "@type")
                    continue;
                SetProperty(existing, kv.Key, kv.Value);
            }
        }

        private static List<string> AsTypeList(object types)
        {
            if (types == null)
                return new List<string>();
            if (types is string s)
                return new List<string> { s };
            if (types is IEnumerable<string> seq)
                return seq.ToList();
            if (types is IEnumerable<object> objSeq)
                return objSeq.Select(o => o?.ToString()).Where(o => o != null).ToList();
            return new List<string> { types.ToString() };
        }

        private static object NormalizeTypeValue(object types)
        {
            var list = AsTypeList(types);
            if (list.Count == 1)
                return list[0];
            return list;
        }

        private static object MergeTypes(object existing, object newTypes)
        {
            var merged = AsTypeList(existing);
            foreach (var typeIri in AsTypeList(newTypes))
            {
                if (!merged.Contains(typeIri))
                    merged.Add(typeIri);
            }
            return merged;
        }

        private static void SetProperty(Dictionary<string, object> obj, string key, object value)
        {
            if (!obj.ContainsKey(key))
            {
                obj[key] = value;
                return;
            }

            var existing = obj[key];
            if (Equals(existing, value))
                return;

            if (existing is List<object> list)
            {
                if (value is Dictionary<string, object> dictVal && dictVal.TryGetValue("@id", out var refId))
                {
                    if (list.OfType<Dictionary<string, object>>()
                        .Any(item => item.TryGetValue("@id", out var itemId) && Equals(itemId, refId)))
                        return;
                }
                if (!list.Contains(value))
                    list.Add(value);
                return;
            }

            if (existing is Dictionary<string, object> existingDict &&
                value is Dictionary<string, object> valueDict &&
                existingDict.TryGetValue("@id", out var existingRef) &&
                valueDict.TryGetValue("@id", out var valueRef) &&
                Equals(existingRef, valueRef))
            {
                return;
            }

            obj[key] = new List<object> { existing, value };
        }

        private string DeterministicRelationshipId(string sourceId, string targetId, string kind)
        {
            var payload = $"{ExpandIri(sourceId)}|{ExpandIri(targetId)}|{kind}";
            using var sha = SHA256.Create();
            var digest = BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(payload)))
                .Replace("-", "")
                .Substring(0, 12)
                .ToLowerInvariant();
            var safeKind = kind.Replace(" ", "_");
            return $"kb:rel-{safeKind}-{digest}";
        }

        private string MintId(object instance)
        {
            var typeName = instance.GetType().Name;
            return $"kb:{typeName}-{Guid.NewGuid()}";
        }

        private Dictionary<string, object> ToJsonLd(object instance, string id)
        {
            var result = new Dictionary<string, object> { ["@id"] = id };
            var type = instance.GetType();

            var classIriField = type.GetField("ClassIri");
            if (classIriField != null)
            {
                var iri = (string)classIriField.GetValue(null);
                result["@type"] = CompactIri(iri);
            }

            foreach (var prop in type
                .GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Where(prop => prop.GetIndexParameters().Length == 0))
            {
                var value = prop.GetValue(instance);
                if (value == null)
                    continue;

                if (value is IList listValue && listValue.Count == 0)
                    continue;

                var attribute = prop.GetCustomAttribute<JsonLdPropertyAttribute>(inherit: true);
                var propKey = attribute != null ? attribute.Key : InferPropertyKey(prop, type);
                result[propKey] = ConvertValue(value);
            }

            return result;
        }

        private object ConvertValue(object value)
        {
            if (value == null)
                return null;

            if (value is string)
                return value;

            if (value is bool boolValue)
                return TypedLiteral("xsd:boolean", boolValue ? "true" : "false");

            if (value is sbyte || value is byte || value is short || value is ushort ||
                value is int || value is uint || value is long || value is ulong)
                return TypedLiteral("xsd:integer", Convert.ToString(value, CultureInfo.InvariantCulture));

            if (value is float || value is double || value is decimal)
                return TypedLiteral("xsd:decimal", Convert.ToString(value, CultureInfo.InvariantCulture));

            if (value is DateTime dateTime)
                return TypedLiteral("xsd:dateTime", dateTime.ToString("o", CultureInfo.InvariantCulture));

            if (!(value is string) && value is IEnumerable enumerable)
            {
                var items = new List<object>();
                foreach (var item in enumerable)
                    items.Add(ConvertValue(item));
                return items;
            }

            if (_idMap.TryGetValue(value, out var id))
                return new Dictionary<string, object> { ["@id"] = id };

            var nestedClassIri = value.GetType().GetField("ClassIri");
            if (nestedClassIri != null)
                return ToJsonLd(value, MintId(value));

            return value;
        }

        private Dictionary<string, string> TypedLiteral(string xsdType, string value)
        {
            return new Dictionary<string, string>
            {
                ["@type"] = xsdType,
                ["@value"] = value,
            };
        }

        private string CompactIri(string iri)
        {
            foreach (var kv in _context.Where(kv => iri.StartsWith(kv.Value)))
            {
                return $"{kv.Key}:{iri.Substring(kv.Value.Length)}";
            }
            return iri;
        }

        private string InferPropertyKey(PropertyInfo prop, Type fallbackType)
        {
            var declaringType = prop.DeclaringType ?? fallbackType;
            var nsField = declaringType.GetField("NamespacePrefix");
            var ns = nsField != null ? (string)nsField.GetValue(null) : "uco-core";
            return $"{ns}:{char.ToLower(prop.Name[0])}{prop.Name.Substring(1)}";
        }

        private static readonly Dictionary<string, string> DefaultContext = new Dictionary<string, string>
        {
            ["case-investigation"] = "https://ontology.caseontology.org/case/investigation/",
            ["kb"] = "http://example.org/kb/",
            ["uco-action"] = "https://ontology.unifiedcyberontology.org/uco/action/",
            ["uco-analysis"] = "https://ontology.unifiedcyberontology.org/uco/analysis/",
            ["uco-configuration"] = "https://ontology.unifiedcyberontology.org/uco/configuration/",
            ["uco-core"] = "https://ontology.unifiedcyberontology.org/uco/core/",
            ["uco-identity"] = "https://ontology.unifiedcyberontology.org/uco/identity/",
            ["uco-location"] = "https://ontology.unifiedcyberontology.org/uco/location/",
            ["uco-marking"] = "https://ontology.unifiedcyberontology.org/uco/marking/",
            ["uco-observable"] = "https://ontology.unifiedcyberontology.org/uco/observable/",
            ["uco-pattern"] = "https://ontology.unifiedcyberontology.org/uco/pattern/",
            ["uco-role"] = "https://ontology.unifiedcyberontology.org/uco/role/",
            ["uco-time"] = "https://ontology.unifiedcyberontology.org/uco/time/",
            ["uco-tool"] = "https://ontology.unifiedcyberontology.org/uco/tool/",
            ["uco-types"] = "https://ontology.unifiedcyberontology.org/uco/types/",
            ["uco-victim"] = "https://ontology.unifiedcyberontology.org/uco/victim/",
            ["uco-vocabulary"] = "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
            ["xsd"] = "http://www.w3.org/2001/XMLSchema#",
        };

        private string ToJsonString(object value, int indent)
        {
            if (value == null)
                return "null";

            if (value is string stringValue)
                return "\"" + Escape(stringValue) + "\"";

            if (value is bool || value is sbyte || value is byte || value is short || value is ushort ||
                value is int || value is uint || value is long || value is ulong ||
                value is float || value is double || value is decimal)
                return Convert.ToString(value, CultureInfo.InvariantCulture);

            if (value is IDictionary dictionary)
                return SerializeDictionary(dictionary, indent);

            if (!(value is string) && value is IEnumerable enumerable)
                return SerializeEnumerable(enumerable, indent);

            return "\"" + Escape(Convert.ToString(value, CultureInfo.InvariantCulture)) + "\"";
        }

        private string SerializeDictionary(IDictionary dictionary, int indent)
        {
            var items = new List<string>();
            foreach (DictionaryEntry entry in dictionary)
            {
                items.Add($"\"{Escape(Convert.ToString(entry.Key, CultureInfo.InvariantCulture))}\": {ToJsonString(entry.Value, NextIndent(indent))}");
            }

            if (indent < 0)
                return "{" + string.Join(",", items) + "}";

            if (items.Count == 0)
                return "{}";

            var pad = new string(' ', indent * 4);
            var childPad = new string(' ', (indent + 1) * 4);
            return "{\n" + childPad + string.Join(",\n" + childPad, items) + "\n" + pad + "}";
        }

        private string SerializeEnumerable(IEnumerable enumerable, int indent)
        {
            var items = new List<string>();
            foreach (var item in enumerable)
                items.Add(ToJsonString(item, NextIndent(indent)));

            if (indent < 0)
                return "[" + string.Join(",", items) + "]";

            if (items.Count == 0)
                return "[]";

            var pad = new string(' ', indent * 4);
            var childPad = new string(' ', (indent + 1) * 4);
            return "[\n" + childPad + string.Join(",\n" + childPad, items) + "\n" + pad + "]";
        }

        private int NextIndent(int indent)
        {
            return indent < 0 ? -1 : indent + 1;
        }

        private string Escape(string value)
        {
            return value
                .Replace("\\", "\\\\")
                .Replace("\"", "\\\"")
                .Replace("\n", "\\n")
                .Replace("\r", "\\r")
                .Replace("\t", "\\t");
        }

        private static Dictionary<string, object> ParseJson(string json)
        {
            return (Dictionary<string, object>)ParseJsonValue(json.Trim(), 0, out _);
        }

        private static object ParseJsonValue(string json, int pos, out int end)
        {
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;

            if (json[pos] == '{')
                return ParseJsonObject(json, pos, out end);
            if (json[pos] == '[')
                return ParseJsonArray(json, pos, out end);
            if (json[pos] == '"')
                return ParseJsonString(json, pos, out end);

            int start = pos;
            while (pos < json.Length && json[pos] != ',' && json[pos] != '}' && json[pos] != ']' && !char.IsWhiteSpace(json[pos]))
                pos++;
            end = pos;
            var token = json.Substring(start, pos - start);
            if (token == "true") return true;
            if (token == "false") return false;
            if (token == "null") return null;
            if (token.Contains("."))
                return double.Parse(token, CultureInfo.InvariantCulture);
            return long.Parse(token, CultureInfo.InvariantCulture);
        }

        private static Dictionary<string, object> ParseJsonObject(string json, int pos, out int end)
        {
            var result = new Dictionary<string, object>();
            pos++; // skip '{'
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;

            if (json[pos] == '}') { end = pos + 1; return result; }

            while (true)
            {
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                var key = ParseJsonString(json, pos, out pos);
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                pos++; // skip ':'
                var value = ParseJsonValue(json, pos, out pos);
                result[key] = value;
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                if (json[pos] == '}') { end = pos + 1; return result; }
                pos++; // skip ','
            }
        }

        private static List<object> ParseJsonArray(string json, int pos, out int end)
        {
            var result = new List<object>();
            pos++; // skip '['
            while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;

            if (json[pos] == ']') { end = pos + 1; return result; }

            while (true)
            {
                var value = ParseJsonValue(json, pos, out pos);
                result.Add(value);
                while (pos < json.Length && char.IsWhiteSpace(json[pos])) pos++;
                if (json[pos] == ']') { end = pos + 1; return result; }
                pos++; // skip ','
            }
        }

        private static string ParseJsonString(string json, int pos, out int end)
        {
            pos++; // skip opening '"'
            var sb = new System.Text.StringBuilder();
            while (json[pos] != '"')
            {
                if (json[pos] == '\\')
                {
                    pos++;
                    switch (json[pos])
                    {
                        case '"': sb.Append('"'); break;
                        case '\\': sb.Append('\\'); break;
                        case 'n': sb.Append('\n'); break;
                        case 'r': sb.Append('\r'); break;
                        case 't': sb.Append('\t'); break;
                        default: sb.Append(json[pos]); break;
                    }
                }
                else
                {
                    sb.Append(json[pos]);
                }
                pos++;
            }
            end = pos + 1; // skip closing '"'
            return sb.ToString();
        }
    }

    /// <summary>Result type returned by <see cref="CaseGraph.FromJsonLd"/>.</summary>
    public class FromJsonLdResult
    {
        public CaseGraph Graph { get; set; }
        public List<object> Objects { get; set; }
    }
}

