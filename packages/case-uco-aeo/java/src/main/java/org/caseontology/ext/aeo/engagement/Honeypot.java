package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class Honeypot {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/Honeypot";

    private List<Object> honeypotInteractionType = new ArrayList<>();

    public List<Object> getHoneypotInteractionType() { return honeypotInteractionType; }
}