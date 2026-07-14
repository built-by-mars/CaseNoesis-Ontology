// Tests for CaseGraph builder and JSON-LD serialization.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using CaseUco;
using CaseUco.Uco.Tool;
using CaseUco.Uco.Observable;
using Xunit;

namespace CaseUco.Tests
{
    public class CaseGraphTests
    {
        [Fact]
        public void CreateTool_ProducesValidJsonLd()
        {
            var graph = new CaseGraph();
            var tool = new Tool { Name = "Tool A", Version = "7.0" };
            var id = graph.Add(tool);

            Assert.StartsWith("kb:Tool-", id);
            var json = graph.Serialize();
            Assert.Contains("uco-tool:Tool", json);
            Assert.Contains("uco-core:name", json);
            Assert.DoesNotContain("uco-tool:name", json);
            Assert.Contains("@context", json);
            Assert.Contains("@graph", json);
        }

        [Fact]
        public void GetId_ReturnsAssignedId()
        {
            var graph = new CaseGraph();
            var tool = new Tool();
            var id = graph.Add(tool);
            Assert.Equal(id, graph.GetId(tool));
        }

        [Fact]
        public void AddWithId_UsesDeterministicId()
        {
            var graph = new CaseGraph();
            var tool = new Tool { Name = "Tool A" };
            var id = graph.AddWithId(tool, "kb:Tool-my-stable-id");

            Assert.Equal("kb:Tool-my-stable-id", id);
            Assert.Equal("kb:Tool-my-stable-id", graph.GetId(tool));
            var json = graph.Serialize();
            Assert.Contains("kb:Tool-my-stable-id", json);
        }

        [Fact]
        public void CustomKbPrefix_ReflectedInContext()
        {
            var graph = new CaseGraph("http://mylab.example.org/case/");
            graph.Add(new Tool { Name = "Tool A" });
            var json = graph.Serialize();
            Assert.Contains("http://mylab.example.org/case/", json);
        }

        [Fact]
        public void MultipleObjects_AllSerialized()
        {
            var graph = new CaseGraph();
            graph.Add(new Tool());
            graph.Add(new AnalyticTool());
            var json = graph.Serialize();

            using var doc = JsonDocument.Parse(json);
            var graphArray = doc.RootElement.GetProperty("@graph");
            Assert.Equal(2, graphArray.GetArrayLength());
        }

        [Fact]
        public void BooleanProperties_AreTypedLiterals()
        {
            var graph = new CaseGraph();
            graph.Add(new ObservableObject { HasChanged = true });
            var json = graph.Serialize();
            Assert.Contains("\"@type\":\"xsd:boolean\"", json.Replace(" ", ""));
            Assert.Contains("\"uco-observable:hasChanged\"", json);
        }

        [Fact]
        public void Count_TracksObjects()
        {
            var graph = new CaseGraph();
            Assert.Equal(0, graph.Count);
            graph.Add(new Tool());
            Assert.Equal(1, graph.Count);
            graph.Add(new Tool());
            Assert.Equal(2, graph.Count);
        }

        [Fact]
        public void ContextPrunesUnusedPrefixes()
        {
            var graph = new CaseGraph();
            graph.Add(new Tool { Name = "Tool A" });
            var json = graph.Serialize();

            using var doc = JsonDocument.Parse(json);
            var ctx = doc.RootElement.GetProperty("@context");

            Assert.True(ctx.TryGetProperty("kb", out _), "used prefix kb should be present");
            Assert.True(ctx.TryGetProperty("uco-tool", out _), "used prefix uco-tool should be present");
            Assert.True(ctx.TryGetProperty("uco-core", out _), "used prefix uco-core should be present");

            var unused = new[] { "uco-identity", "uco-location", "uco-role", "uco-victim",
                                 "uco-configuration", "uco-marking", "uco-pattern", "uco-time" };
            foreach (var prefix in unused)
            {
                Assert.False(ctx.TryGetProperty(prefix, out _), $"unused prefix should be pruned: {prefix}");
            }
        }

        [Fact]
        public void EmptyGraphHasEmptyContext()
        {
            var graph = new CaseGraph();
            var json = graph.Serialize();

            using var doc = JsonDocument.Parse(json);
            var ctx = doc.RootElement.GetProperty("@context");
            int count = 0;
            foreach (var _ in ctx.EnumerateObject()) count++;
            Assert.Equal(0, count);
        }

        [Fact]
        public void Load_MergesContextAndObjects()
        {
            var graph = new CaseGraph();
            var inputJson = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""uco-tool"": ""https://ontology.unifiedcyberontology.org/uco/tool/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:Tool-existing-001"",
                        ""@type"": ""uco-tool:Tool""
                    }
                ]
            }";

            graph.Load(inputJson);
            Assert.Equal(1, graph.Count);

            var json = graph.Serialize();
            Assert.Contains("kb:Tool-existing-001", json);
        }

        [Fact]
        public void Load_ThenAdd_CombinesObjects()
        {
            var graph = new CaseGraph();
            graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"" }, ""@graph"": [ { ""@id"": ""kb:Tool-loaded"", ""@type"": ""uco-tool:Tool"" } ] }");
            graph.Add(new Tool { Name = "New Tool" });
            Assert.Equal(2, graph.Count);
        }

        [Fact]
        public void Get_ReturnsDeepCopy()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:n1", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "N",
                ["uco-core:tag"] = new List<object> { "a", "b" },
                ["uco-core:hasFacet"] = new List<object>
                {
                    new Dictionary<string, object> { ["@id"] = "kb:f1" },
                },
            });
            var view = graph.Get("kb:n1");
            view["@id"] = "kb:mutated";
            ((List<object>)view["uco-core:tag"]).Add("c");
            ((Dictionary<string, object>)((List<object>)view["uco-core:hasFacet"])[0])["@id"] = "kb:mutated-facet";
            Assert.True(graph.Contains("kb:n1"));
            Assert.False(graph.Contains("kb:mutated"));
            Assert.Equal("N", graph.Get("kb:n1")["uco-core:name"]);
            Assert.Equal(2, ((List<object>)graph.Get("kb:n1")["uco-core:tag"]).Count);
            Assert.Equal("kb:f1", ((Dictionary<string, object>)((List<object>)graph.Get("kb:n1")["uco-core:hasFacet"])[0])["@id"]);
        }

        [Fact]
        public void Split_RejectsNonPositive()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:x", "uco-core:UcoObject");
            Assert.Throws<ArgumentOutOfRangeException>(() => graph.Split(0));
        }

        [Fact]
        public void Load_RejectsDuplicateByDefault()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:x", "uco-core:UcoObject");
            Assert.Throws<InvalidOperationException>(() =>
                graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"" }, ""@graph"": [ { ""@id"": ""kb:x"", ""@type"": ""uco-core:UcoObject"" } ] }"));
        }

        [Fact]
        public void Load_RejectsContextCollision()
        {
            var graph = new CaseGraph();
            Assert.Throws<ArgumentException>(() =>
                graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"", ""uco-core"": ""https://evil.example.org/uco/core/"" }, ""@graph"": [] }"));
        }

        [Fact]
        public void Load_MergeCompatible_ScalarConflictRaises()
        {
            var graph = new CaseGraph();
            graph.RejectDuplicates = false;
            graph.UpsertNode("kb:x", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "A",
            });
            Assert.Throws<InvalidOperationException>(() =>
                graph.Load(@"{ ""@context"": { ""kb"": ""http://example.org/kb/"" }, ""@graph"": [ { ""@id"": ""kb:x"", ""@type"": ""uco-core:UcoObject"", ""uco-core:name"": ""B"" } ] }"));
        }

        [Fact]
        public void ClearClassRegistryCache_DoesNotBreakFromJsonLd()
        {
            var json = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""uco-tool"": ""https://ontology.unifiedcyberontology.org/uco/tool/"",
                    ""uco-core"": ""https://ontology.unifiedcyberontology.org/uco/core/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:Tool-1"",
                        ""@type"": ""uco-tool:Tool"",
                        ""uco-core:name"": ""Cached""
                    }
                ]
            }";

            var first = CaseGraph.FromJsonLd(json);
            Assert.IsType<Tool>(first.Objects[0]);
            CaseGraph.ClearClassRegistryCache();
            var second = CaseGraph.FromJsonLd(json);
            Assert.IsType<Tool>(second.Objects[0]);
        }

        [Fact]
        public void PropertyBindingCache_WarmPath()
        {
            CaseGraph.ClearClassRegistryCache();
            Assert.Equal(0, CaseGraph.PropertyBindingCacheCount);

            var json = @"{
                ""@context"": {
                    ""kb"": ""http://example.org/kb/"",
                    ""uco-tool"": ""https://ontology.unifiedcyberontology.org/uco/tool/"",
                    ""uco-core"": ""https://ontology.unifiedcyberontology.org/uco/core/""
                },
                ""@graph"": [
                    {
                        ""@id"": ""kb:Tool-warm"",
                        ""@type"": ""uco-tool:Tool"",
                        ""uco-core:name"": ""Warm""
                    }
                ]
            }";

            CaseGraph.FromJsonLd(json);
            var afterCold = CaseGraph.PropertyBindingCacheCount;
            Assert.True(afterCold > 0);
            CaseGraph.FromJsonLd(json);
            Assert.Equal(afterCold, CaseGraph.PropertyBindingCacheCount);
            CaseGraph.ClearClassRegistryCache();
            Assert.Equal(0, CaseGraph.PropertyBindingCacheCount);
        }

        [Fact]
        public void WriteStreaming_Roundtrip()
        {
            var graph = new CaseGraph();
            graph.AddWithId(new Tool { Name = "Streamed" }, "kb:t-stream");
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-stream-{Guid.NewGuid()}.jsonld");
            try
            {
                var metrics = graph.WriteStreaming(path);
                Assert.Equal(1, metrics.Nodes);
                Assert.True(metrics.BytesWritten > 0);
                var loaded = new CaseGraph();
                loaded.OnDuplicate = "merge_compatible";
                loaded.Load(System.IO.File.ReadAllText(path));
                Assert.Equal("Streamed", loaded.Get("kb:t-stream")["uco-core:name"]);
            }
            finally
            {
                if (System.IO.File.Exists(path))
                    System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void WriteStreaming_ReplacesExistingWithoutDeleteFirst()
        {
            // Atomic WriteStreaming must replace in place via temp+File.Replace/Move,
            // not delete-then-write (which races readers and loses the prior file on failure).
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-replace-{Guid.NewGuid()}.jsonld");
            try
            {
                System.IO.File.WriteAllText(path, "OLD");
                Assert.Equal("OLD", System.IO.File.ReadAllText(path));

                var v1 = new CaseGraph();
                v1.AddWithId(new Tool { Name = "V1" }, "kb:t-replace");
                v1.WriteStreaming(path);
                Assert.Contains("V1", System.IO.File.ReadAllText(path));
                Assert.DoesNotContain("OLD", System.IO.File.ReadAllText(path));

                var v2 = new CaseGraph();
                v2.AddWithId(new Tool { Name = "V2" }, "kb:t-replace");
                v2.WriteStreaming(path);
                var text = System.IO.File.ReadAllText(path);
                Assert.Contains("V2", text);
                Assert.DoesNotContain("V1", text);

                // netstandard2.0: File.Replace for existing destinations; File.Move
                // only when the destination is absent. Never Delete-then-Move.
            }
            finally
            {
                if (System.IO.File.Exists(path))
                    System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void WriteStreaming_InducedReplaceFailure_PreservesOldBytes()
        {
            var path = System.IO.Path.Join(System.IO.Path.GetTempPath(), $"caseuco-fail-replace-{Guid.NewGuid()}.jsonld");
            CaseGraph.SimulateReplaceFailureForTests = null;
            try
            {
                System.IO.File.WriteAllText(path, "SURVIVE-ME");
                CaseGraph.SimulateReplaceFailureForTests = (tmp, dest) =>
                    new System.IO.IOException("induced replace failure");

                var graph = new CaseGraph();
                graph.AddWithId(new Tool { Name = "ShouldNotLand" }, "kb:t-fail");
                var ex = Assert.Throws<System.IO.IOException>(() => graph.WriteStreaming(path));
                Assert.Contains("induced replace failure", ex.Message);
                Assert.Equal("SURVIVE-ME", System.IO.File.ReadAllText(path));
            }
            finally
            {
                CaseGraph.SimulateReplaceFailureForTests = null;
                if (System.IO.File.Exists(path))
                    System.IO.File.Delete(path);
            }
        }

        [Fact]
        public void PartitionByRoots_IncludesIncomingRelationship()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:device", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "phone",
            });
            graph.UpsertNode("kb:file", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "photo",
            });
            var rel = graph.CreateRelationship("kb:file", "kb:device", "Contained_Within");
            var relId = (string)rel["@id"];

            var withIncoming = graph.PartitionByRoots(new[] { "kb:device" }, "replicate-identical", includeIncoming: true);
            Assert.True(withIncoming["kb:device"].Contains(relId));
            Assert.True(withIncoming["kb:device"].Contains("kb:file"));

            var outgoingOnly = graph.PartitionByRoots(new[] { "kb:device" }, "replicate-identical", includeIncoming: false);
            Assert.False(outgoingOnly["kb:device"].Contains(relId));
            Assert.False(outgoingOnly["kb:device"].Contains("kb:file"));
        }

        [Fact]
        public void PartitionByRoots_ReplicatesSharedNodes()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:shared", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "Shared",
            });
            graph.UpsertNode("kb:root-a", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });
            graph.UpsertNode("kb:root-b", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });

            var parts = graph.PartitionByRoots(new[] { "kb:root-a", "kb:root-b" });
            Assert.True(parts.TryGetValue("kb:root-a", out var partA));
            Assert.True(parts.TryGetValue("kb:root-b", out var partB));
            Assert.False(parts.ContainsKey("_shared"));
            Assert.True(partA.Contains("kb:shared"));
            Assert.True(partB.Contains("kb:shared"));
        }

        [Fact]
        public void PartitionByRoots_PlacesSharedNodesInSharedPartition()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:shared", "uco-core:UcoObject");
            graph.UpsertNode("kb:root-a", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });
            graph.UpsertNode("kb:root-b", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:object"] = new Dictionary<string, object> { ["@id"] = "kb:shared" },
            });

            var parts = graph.PartitionByRoots(new[] { "kb:root-a", "kb:root-b" }, "shared");
            Assert.True(parts.TryGetValue("_shared", out var sharedPart));
            Assert.True(sharedPart.Contains("kb:shared"));
        }

        [Fact]
        public void PartitionByLabel_GroupsByBoundaryKey()
        {
            var graph = new CaseGraph();
            graph.UpsertNode("kb:art-a", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "A",
            });
            graph.UpsertNode("kb:art-b", "uco-core:UcoObject", new Dictionary<string, object>
            {
                ["uco-core:name"] = "B",
            });
            graph.CreateRelationship("kb:art-a", "kb:art-b", "Related_To");

            var parts = graph.PartitionByLabel(node =>
            {
                if (node.TryGetValue("uco-core:name", out var name) && name as string == "A")
                    return "part-a";
                if (name as string == "B")
                    return "part-b";
                return null;
            });

            Assert.True(parts.ContainsKey("part-a"));
            Assert.True(parts.ContainsKey("part-b"));
            Assert.Equal(
                parts.Keys.OrderBy(x => x).ToArray(),
                graph.PartitionByLabel(node =>
                {
                    if (node.TryGetValue("uco-core:name", out var name) && name as string == "A")
                        return "part-a";
                    if (name as string == "B")
                        return "part-b";
                    return null;
                }).Keys.OrderBy(x => x).ToArray());
        }
    }
}
