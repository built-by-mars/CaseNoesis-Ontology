package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class PlannedEvent {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/PlannedEvent";

    private List<UcoObject> eventContext = new ArrayList<>();
    private List<UcoObject> hasObjective = new ArrayList<>();

    public List<UcoObject> getEventContext() { return eventContext; }
    public List<UcoObject> getHasObjective() { return hasObjective; }
}