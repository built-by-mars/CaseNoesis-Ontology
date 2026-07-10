package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class Narrative {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/Narrative";

    private List<UcoObject> hasObjective = new ArrayList<>();
    private List<UcoObject> hasStoryline = new ArrayList<>();

    public List<UcoObject> getHasObjective() { return hasObjective; }
    public List<UcoObject> getHasStoryline() { return hasStoryline; }
}