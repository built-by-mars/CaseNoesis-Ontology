package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class Verdict {
    public static final String CLASS_IRI = "http://example.org/ontology/legalproc/Verdict";

    private List<CriminalCharge> concernsCharge = new ArrayList<>();
    private String verdictType;

    public List<CriminalCharge> getConcernsCharge() { return concernsCharge; }
    public String getVerdictType() { return verdictType; }
    public void setVerdictType(String verdictType) { this.verdictType = verdictType; }
}