package org.caseontology.ext.aeo.identity;

import java.util.ArrayList;
import java.util.List;

public class Team {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/identity/Team";

    private List<Objective> hasObjective = new ArrayList<>();

    public List<Objective> getHasObjective() { return hasObjective; }
}