package org.caseontology.ext.aeo.attack;

import java.util.ArrayList;
import java.util.List;

public class DefensePattern {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/attack/DefensePattern";

    private List<Objective> hasObjective = new ArrayList<>();

    public List<Objective> getHasObjective() { return hasObjective; }
}