package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class Plea {
    public static final String CLASS_IRI = "http://example.org/ontology/legalproc/Plea";

    private List<CriminalCharge> concernsCharge = new ArrayList<>();
    private String pleaType;

    public List<CriminalCharge> getConcernsCharge() { return concernsCharge; }
    public String getPleaType() { return pleaType; }
    public void setPleaType(String pleaType) { this.pleaType = pleaType; }
}