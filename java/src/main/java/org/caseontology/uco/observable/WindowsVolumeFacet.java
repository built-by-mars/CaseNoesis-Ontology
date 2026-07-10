// Auto-generated CASE/UCO ontology class — do not edit manually.
package org.caseontology.uco.observable;

import java.util.ArrayList;
import java.util.List;
import org.caseontology.uco.core.Facet;

/** A Windows volume facet is a grouping of characteristics unique to a single accessible storage area (volume) with a single Windows file system. [based on https://en.wikipedia.org/wiki/Volume_(computing */
public class WindowsVolumeFacet extends Facet {
    public static final String CLASS_IRI = "https://ontology.unifiedcyberontology.org/uco/observable/WindowsVolumeFacet";
    public static final String NAMESPACE_PREFIX = "uco-observable";

    private String driveLetter;
    private String driveType;
    private List<WindowsVolumeAttributeVocab> windowsVolumeAttributes;

    public WindowsVolumeFacet() {
        this.windowsVolumeAttributes = new ArrayList<>();
    }

    public String getDriveLetter() { return this.driveLetter; }
    public WindowsVolumeFacet setDriveLetter(String value) { this.driveLetter = value; return this; }

    public String getDriveType() { return this.driveType; }
    public WindowsVolumeFacet setDriveType(String value) { this.driveType = value; return this; }

    public List<WindowsVolumeAttributeVocab> getWindowsVolumeAttributes() { return this.windowsVolumeAttributes; }
    public WindowsVolumeFacet setWindowsVolumeAttributes(List<WindowsVolumeAttributeVocab> value) { this.windowsVolumeAttributes = value; return this; }

}