package org.caseontology.ext.aeo.attack;

import java.util.ArrayList;
import java.util.List;

public class AttackPattern {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/attack/AttackPattern";

    private List<Objective> hasObjective = new ArrayList<>();

    public List<Objective> getHasObjective() { return hasObjective; }
}