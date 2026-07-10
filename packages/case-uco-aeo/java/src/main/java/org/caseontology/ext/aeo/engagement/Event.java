package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class Event {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/Event";

    private List<Dictionary> eventAttribute = new ArrayList<>();
    private List<UcoObject> eventContext = new ArrayList<>();
    private List<String> eventType = new ArrayList<>();
    private List<String> endTime = new ArrayList<>();
    private List<String> startTime = new ArrayList<>();

    public List<Dictionary> getEventAttribute() { return eventAttribute; }
    public List<UcoObject> getEventContext() { return eventContext; }
    public List<String> getEventType() { return eventType; }
    public List<String> getEndTime() { return endTime; }
    public List<String> getStartTime() { return startTime; }
}