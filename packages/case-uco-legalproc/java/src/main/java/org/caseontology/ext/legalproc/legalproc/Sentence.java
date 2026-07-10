package org.caseontology.ext.legalproc.legalproc;

import java.util.ArrayList;
import java.util.List;

public class Sentence {
    public static final String CLASS_IRI = "http://example.org/ontology/legalproc/Sentence";

    private String sentenceStatus;
    private String sentenceTerm;

    public String getSentenceStatus() { return sentenceStatus; }
    public void setSentenceStatus(String sentenceStatus) { this.sentenceStatus = sentenceStatus; }
    public String getSentenceTerm() { return sentenceTerm; }
    public void setSentenceTerm(String sentenceTerm) { this.sentenceTerm = sentenceTerm; }
}