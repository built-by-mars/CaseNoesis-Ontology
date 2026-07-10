package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class Breadcrumb {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/Breadcrumb";

    private List<UcoObject> breadcrumbTargetObject = new ArrayList<>();
    private List<UcoObject> hasCharacterization = new ArrayList<>();

    public List<UcoObject> getBreadcrumbTargetObject() { return breadcrumbTargetObject; }
    public List<UcoObject> getHasCharacterization() { return hasCharacterization; }
}