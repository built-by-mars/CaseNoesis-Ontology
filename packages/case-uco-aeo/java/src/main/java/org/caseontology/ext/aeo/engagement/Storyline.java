package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class Storyline {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/Storyline";

    private List<Thread> hasEvent = new ArrayList<>();

    public List<Thread> getHasEvent() { return hasEvent; }
}