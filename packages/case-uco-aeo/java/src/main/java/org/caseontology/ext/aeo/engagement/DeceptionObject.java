package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class DeceptionObject {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/DeceptionObject";

    private List<UcoObject> hasAttackSurface = new ArrayList<>();
    private List<UcoObject> hasCharacterization = new ArrayList<>();
    private List<UcoObject> hasPerceptionCharacterization = new ArrayList<>();

    public List<UcoObject> getHasAttackSurface() { return hasAttackSurface; }
    public List<UcoObject> getHasCharacterization() { return hasCharacterization; }
    public List<UcoObject> getHasPerceptionCharacterization() { return hasPerceptionCharacterization; }
}