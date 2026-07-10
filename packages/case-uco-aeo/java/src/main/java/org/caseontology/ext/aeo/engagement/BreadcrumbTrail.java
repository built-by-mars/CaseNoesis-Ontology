package org.caseontology.ext.aeo.engagement;

import java.util.ArrayList;
import java.util.List;

public class BreadcrumbTrail {
    public static final String CLASS_IRI = "https://ontology.adversaryengagement.org/ae/engagement/BreadcrumbTrail";

    private List<UcoObject> breadcrumbTargetObject = new ArrayList<>();
    private List<Thread> hasBreadcrumb = new ArrayList<>();
    private List<Objective> hasObjective = new ArrayList<>();

    public List<UcoObject> getBreadcrumbTargetObject() { return breadcrumbTargetObject; }
    public List<Thread> getHasBreadcrumb() { return hasBreadcrumb; }
    public List<Objective> getHasObjective() { return hasObjective; }
}