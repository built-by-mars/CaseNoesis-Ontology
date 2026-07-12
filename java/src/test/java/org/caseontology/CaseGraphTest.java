// Tests for CaseGraph builder and JSON-LD serialization.
package org.caseontology;

import org.caseontology.uco.tool.Tool;
import org.caseontology.uco.observable.ObservableObject;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.ArrayList;
import java.util.Map;
import java.util.List;
import java.util.LinkedHashMap;

public class CaseGraphTest {

    @Test
    public void testCreateTool() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Tool A");
        tool.setVersion("7.0");
        tool.setToolType("forensic");

        String id = graph.add(tool);
        assertTrue(id.startsWith("kb:Tool-"));
        Map<String, Object> doc = graph.toMap();
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> graphList = (List<Map<String, Object>>) doc.get("@graph");
        assertTrue(graphList.get(0).containsKey("uco-core:name"));
        assertFalse(graphList.get(0).containsKey("uco-tool:name"));
    }

    @Test
    public void testGetId() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        String id = graph.add(tool);
        assertEquals(id, graph.getId(tool));
    }

    @Test
    public void testAddWithDeterministicId() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Tool A");

        String id = graph.addWithId(tool, "kb:Tool-my-stable-id");
        assertEquals("kb:Tool-my-stable-id", id);
        assertEquals("kb:Tool-my-stable-id", graph.getId(tool));

        String json = graph.serialize();
        assertTrue(json.contains("kb:Tool-my-stable-id"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testMultipleObjects() {
        CaseGraph graph = new CaseGraph();
        graph.add(new Tool());
        graph.add(new Tool());

        Map<String, Object> doc = graph.toMap();
        List<Map<String, Object>> graphList = (List<Map<String, Object>>) doc.get("@graph");
        assertEquals(2, graphList.size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testContextPrunesUnusedPrefixes() {
        CaseGraph graph = new CaseGraph();
        Tool tool = new Tool();
        tool.setName("Tool A");
        graph.add(tool);

        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");

        assertTrue("used prefix kb should be present", context.containsKey("kb"));
        assertTrue("used prefix uco-tool should be present", context.containsKey("uco-tool"));
        assertTrue("used prefix uco-core should be present", context.containsKey("uco-core"));

        String[] unused = {
            "uco-identity", "uco-location", "uco-role", "uco-victim",
            "uco-configuration", "uco-marking", "uco-pattern", "uco-time",
        };
        for (String prefix : unused) {
            assertFalse("unused prefix should be pruned: " + prefix, context.containsKey(prefix));
        }
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testEmptyGraphHasEmptyContext() {
        CaseGraph graph = new CaseGraph();
        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");
        assertTrue("empty graph should have empty context", context.isEmpty());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testCustomKbPrefix() {
        CaseGraph graph = new CaseGraph("http://mylab.example.org/case/");
        Tool tool = new Tool();
        graph.add(tool);
        Map<String, Object> doc = graph.toMap();
        Map<String, String> context = (Map<String, String>) doc.get("@context");
        assertEquals("http://mylab.example.org/case/", context.get("kb"));
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testBooleanTypedLiteral() {
        CaseGraph graph = new CaseGraph();
        ObservableObject observable = new ObservableObject();
        observable.setHasChanged(Boolean.TRUE);
        graph.add(observable);

        Map<String, Object> doc = graph.toMap();
        List<Map<String, Object>> graphList = (List<Map<String, Object>>) doc.get("@graph");
        Map<String, Object> observableJson = graphList.get(0);
        Map<String, String> typedLiteral = (Map<String, String>) observableJson.get("uco-observable:hasChanged");
        assertEquals("xsd:boolean", typedLiteral.get("@type"));
        assertEquals("true", typedLiteral.get("@value"));
    }

    @Test
    public void testSize() {
        CaseGraph graph = new CaseGraph();
        assertEquals(0, graph.size());
        graph.add(new Tool());
        assertEquals(1, graph.size());
        graph.add(new Tool());
        assertEquals(2, graph.size());
    }

    @Test
    public void testSerializeProducesJsonString() {
        CaseGraph graph = new CaseGraph();
        graph.add(new Tool());
        String json = graph.serialize();
        assertTrue(json.contains("@context"));
        assertTrue(json.contains("@graph"));
    }

    @Test
    public void testLoadMergesContextAndObjects() {
        CaseGraph graph = new CaseGraph();
        String inputJson = "{\n" +
            "  \"@context\": {\n" +
            "    \"kb\": \"http://example.org/kb/\",\n" +
            "    \"uco-tool\": \"https://ontology.unifiedcyberontology.org/uco/tool/\"\n" +
            "  },\n" +
            "  \"@graph\": [\n" +
            "    {\n" +
            "      \"@id\": \"kb:Tool-existing-001\",\n" +
            "      \"@type\": \"uco-tool:Tool\"\n" +
            "    }\n" +
            "  ]\n" +
            "}";

        graph.load(inputJson);
        assertEquals(1, graph.size());

        String json = graph.serialize();
        assertTrue(json.contains("kb:Tool-existing-001"));
    }

    @Test
    public void testLoadThenAddCombinesObjects() {
        CaseGraph graph = new CaseGraph();
        graph.load("{\"@context\":{\"kb\":\"http://example.org/kb/\"},\"@graph\":[{\"@id\":\"kb:Tool-loaded\",\"@type\":\"uco-tool:Tool\"}]}");
        graph.add(new Tool());
        assertEquals(2, graph.size());
    }

    @Test
    @SuppressWarnings("unchecked")
    public void testGetReturnsDeepCopy() {
        CaseGraph graph = new CaseGraph();
        Map<String, Object> props = new LinkedHashMap<>();
        props.put("uco-core:name", "N");
        props.put("uco-core:tag", new ArrayList<>(List.of("a", "b")));
        Map<String, Object> facet = new LinkedHashMap<>();
        facet.put("@id", "kb:f1");
        props.put("uco-core:hasFacet", new ArrayList<>(List.of(facet)));
        graph.upsertNode("kb:n1", "uco-core:UcoObject", props);
        Map<String, Object> view = graph.get("kb:n1");
        view.put("@id", "kb:mutated");
        ((List<Object>) view.get("uco-core:tag")).add("c");
        ((Map<String, Object>) ((List<Object>) view.get("uco-core:hasFacet")).get(0)).put("@id", "kb:mutated-facet");
        assertTrue(graph.contains("kb:n1"));
        assertFalse(graph.contains("kb:mutated"));
        assertEquals("N", graph.get("kb:n1").get("uco-core:name"));
        assertEquals(2, ((List<?>) graph.get("kb:n1").get("uco-core:tag")).size());
        assertEquals("kb:f1", ((Map<?, ?>) ((List<?>) graph.get("kb:n1").get("uco-core:hasFacet")).get(0)).get("@id"));
    }

    @Test
    public void testSplitRejectsNonPositive() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:x", "uco-core:UcoObject", null);
        try {
            graph.split(0);
            fail("expected IllegalArgumentException");
        } catch (IllegalArgumentException expected) {
            assertTrue(expected.getMessage().contains("positive"));
        }
    }

    @Test
    public void testLoadRejectsDuplicateByDefault() {
        CaseGraph graph = new CaseGraph();
        graph.upsertNode("kb:x", "uco-core:UcoObject", null);
        try {
            graph.load("{\"@context\":{\"kb\":\"http://example.org/kb/\"},\"@graph\":[{\"@id\":\"kb:x\",\"@type\":\"uco-core:UcoObject\"}]}");
            fail("expected IllegalStateException");
        } catch (IllegalStateException expected) {
            assertTrue(expected.getMessage().contains("Duplicate"));
        }
    }

    @Test
    public void testLoadRejectsContextCollision() {
        CaseGraph graph = new CaseGraph();
        try {
            graph.load("{\"@context\":{\"kb\":\"http://example.org/kb/\",\"uco-core\":\"https://evil.example.org/uco/core/\"},\"@graph\":[]}");
            fail("expected IllegalArgumentException");
        } catch (IllegalArgumentException expected) {
            assertTrue(expected.getMessage().contains("Context prefix collision"));
        }
    }
}
