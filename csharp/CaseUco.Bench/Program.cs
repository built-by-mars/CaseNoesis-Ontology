// Synthetic C# catalog serialize benchmark (#73).
using System.Diagnostics;
using System.Text.Json;
using CaseUco;
using CaseUco.Uco.Tool;

var tier = "small";
for (var i = 0; i < args.Length; i++)
{
    if (args[i] == "--tier" && i + 1 < args.Length)
        tier = args[i + 1];
}

var n = tier switch
{
    "small" => 1_000,
    "medium" => 10_000,
    "large" => 100_000,
    _ => throw new ArgumentException($"Unknown tier '{tier}'"),
};

var sw = Stopwatch.StartNew();
var graph = new CaseGraph("https://example.org/bench/");
for (var i = 0; i < n; i++)
    graph.AddWithId(new Tool { Name = $"Tool-{i}", Version = "1.0" }, $"kb:tool-{i}");
var buildSeconds = sw.Elapsed.TotalSeconds;

sw.Restart();
var payload = graph.Serialize();
var serializeSeconds = sw.Elapsed.TotalSeconds;

var result = new Dictionary<string, object?>
{
    ["suite"] = "case-uco-synthetic-benchmark",
    ["schema_version"] = "1.1.0",
    ["tier"] = tier,
    ["language"] = "csharp",
    ["result"] = new Dictionary<string, object?>
    {
        ["catalog"] = new Dictionary<string, object?>
        {
            ["workload"] = "catalog",
            ["nodes"] = n,
            ["build_seconds"] = Math.Round(buildSeconds, 6),
            ["serialize_seconds"] = Math.Round(serializeSeconds, 6),
            ["serialize_bytes"] = System.Text.Encoding.UTF8.GetByteCount(payload),
            ["estimate_triples"] = graph.EstimateTriples(),
        },
    },
};

Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
