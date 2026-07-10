// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** Recoverability status of name, metadata, and content. */
public class RecoveredObjectFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/RecoveredObjectFacet";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    private String contentRecoveredStatus;
    private String metadataRecoveredStatus;
    private String nameRecoveredStatus;

    public RecoveredObjectFacet() {
    }

    public String getContentRecoveredStatus() { return this.contentRecoveredStatus; }
    public RecoveredObjectFacet setContentRecoveredStatus(String value) { this.contentRecoveredStatus = value; return this; }

    public String getMetadataRecoveredStatus() { return this.metadataRecoveredStatus; }
    public RecoveredObjectFacet setMetadataRecoveredStatus(String value) { this.metadataRecoveredStatus = value; return this; }

    public String getNameRecoveredStatus() { return this.nameRecoveredStatus; }
    public RecoveredObjectFacet setNameRecoveredStatus(String value) { this.nameRecoveredStatus = value; return this; }

}