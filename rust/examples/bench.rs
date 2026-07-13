//! Synthetic cross-language benchmark harness — small CI tier (#73).

use case_uco::graph::CaseGraph;
use case_uco::uco::tool::Tool;
use serde_json::json;
use std::env;
use std::time::Instant;

fn build_catalog(n: usize) -> CaseGraph {
    let mut graph = CaseGraph::new("https://example.org/bench/");
    for i in 0..n {
        let tool = Tool::builder()
            .tool_type("bench".to_string())
            .version("1.0".to_string())
            .build();
        graph.create_with_id(&format!("kb:tool-{i}"), &tool);
    }
    graph
}

fn run_tier(n: usize) -> serde_json::Value {
    let t0 = Instant::now();
    let mut graph = build_catalog(n);
    let build_seconds = t0.elapsed().as_secs_f64();

    let t0 = Instant::now();
    let step = (n / 100).max(1);
    for i in (0..n).step_by(step) {
        assert!(graph.contains(&format!("kb:tool-{i}")));
        graph
            .add_property(
                &format!("kb:tool-{i}"),
                "uco-core:description",
                json!(format!("bench-{i}")),
            )
            .expect("add_property");
    }
    let lookup_enrich_seconds = t0.elapsed().as_secs_f64();

    let t0 = Instant::now();
    let payload = graph.serialize().expect("serialize");
    let serialize_seconds = t0.elapsed().as_secs_f64();

    json!({
        "nodes": n,
        "build_seconds": (build_seconds * 1_000_000.0).round() / 1_000_000.0,
        "lookup_enrich_seconds": (lookup_enrich_seconds * 1_000_000.0).round() / 1_000_000.0,
        "serialize_seconds": (serialize_seconds * 1_000_000.0).round() / 1_000_000.0,
        "serialize_bytes": payload.len(),
        "estimate_triples": graph.estimate_triples(),
    })
}

fn main() {
    let tier = env::args()
        .skip_while(|a| a != "--tier")
        .nth(1)
        .unwrap_or_else(|| "small".to_string());
    let n = match tier.as_str() {
        "small" => 1_000,
        "medium" => 10_000,
        "large" => 100_000,
        other => {
            eprintln!("Unknown tier '{other}', expected small|medium|large");
            std::process::exit(2);
        }
    };

    let result = json!({
        "suite": "case-uco-synthetic-benchmark",
        "tier": tier,
        "language": "rust",
        "result": run_tier(n),
    });
    println!("{}", serde_json::to_string_pretty(&result).expect("json"));
}
