package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class PocketLitter {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/PocketLitter";

    private List<UcoObject> hasCharacterization = new ArrayList<>();

    public List<UcoObject> getHasCharacterization() { return hasCharacterization; }
}