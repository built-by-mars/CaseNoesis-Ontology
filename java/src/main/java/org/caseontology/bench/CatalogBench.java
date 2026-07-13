package org.caseontology.bench;

import org.caseontology.CaseGraph;
import org.caseontology.uco.tool.Tool;

import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Synthetic Java catalog serialize benchmark (#73).
 */
public final class CatalogBench {
    private CatalogBench() {}

    public static void main(String[] args) {
        String tier = "small";
        for (int i = 0; i < args.length; i++) {
            if ("--tier".equals(args[i]) && i + 1 < args.length) {
                tier = args[i + 1];
            }
        }
        int n;
        if ("small".equals(tier)) {
            n = 1_000;
        } else if ("medium".equals(tier)) {
            n = 10_000;
        } else if ("large".equals(tier)) {
            n = 100_000;
        } else {
            throw new IllegalArgumentException("Unknown tier '" + tier + "'");
        }

        long t0 = System.nanoTime();
        CaseGraph graph = new CaseGraph("https://example.org/bench/");
        for (int i = 0; i < n; i++) {
            Tool tool = new Tool();
            tool.setName("Tool-" + i);
            tool.setVersion("1.0");
            graph.addWithId(tool, "kb:tool-" + i);
        }
        double buildSeconds = (System.nanoTime() - t0) / 1_000_000_000.0;

        t0 = System.nanoTime();
        String payload = graph.serialize();
        double serializeSeconds = (System.nanoTime() - t0) / 1_000_000_000.0;

        Map<String, Object> catalog = new LinkedHashMap<>();
        catalog.put("workload", "catalog");
        catalog.put("nodes", n);
        catalog.put("build_seconds", Math.round(buildSeconds * 1_000_000.0) / 1_000_000.0);
        catalog.put("serialize_seconds", Math.round(serializeSeconds * 1_000_000.0) / 1_000_000.0);
        catalog.put("serialize_bytes", payload.getBytes(StandardCharsets.UTF_8).length);
        catalog.put("estimate_triples", graph.estimateTriples());

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("catalog", catalog);

        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("suite", "case-uco-synthetic-benchmark");
        doc.put("schema_version", "1.1.0");
        doc.put("tier", tier);
        doc.put("language", "java");
        doc.put("result", result);

        System.out.println(toJson(doc, 0));
    }

    @SuppressWarnings("unchecked")
    private static String toJson(Object value, int indent) {
        String pad = "  ".repeat(indent);
        String childPad = "  ".repeat(indent + 1);
        if (value instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) value;
            StringBuilder sb = new StringBuilder();
            sb.append("{\n");
            int i = 0;
            for (Map.Entry<String, Object> e : map.entrySet()) {
                sb.append(childPad).append(quote(e.getKey())).append(": ").append(toJson(e.getValue(), indent + 1));
                if (++i < map.size()) sb.append(',');
                sb.append('\n');
            }
            sb.append(pad).append('}');
            return sb.toString();
        }
        if (value instanceof String) {
            return quote((String) value);
        }
        if (value instanceof Number || value instanceof Boolean) {
            return String.valueOf(value);
        }
        return quote(String.valueOf(value));
    }

    private static String quote(String s) {
        return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }
}
