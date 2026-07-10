"""CAC Ontology - Crimes Against Children — cacontology-ai-csam module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AIAlteredCSAM:
    """Existing CSAM that has been modified using AI techniques to alter appearance, age, or other characteristics. Enhanced as gUFO Object with alteration tracking."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIAlteredCSAM"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class AICSAMInvestigation:
    """Investigation specifically focused on AI-generated child sexual abuse material, requiring specialized techniques and legal frameworks. Enhanced as gUFO Event for complex investigation modeling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AICSAMInvestigation"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    focus: list[str] = field(default_factory=list)
    investigation_form: list[str] = field(default_factory=list)
    investigation_status: Optional[str] = field(default=None)
    relevant_authorization: list[Authorization] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    investigation_challenge_level: Optional[str] = field(default=None)
    legal_framework_challenges: list[str] = field(default_factory=list)
    prosecution_difficulty: Optional[str] = field(default=None)
    victim_identification_difficulty: Optional[str] = field(default=None)


@dataclass
class AIContentDetection:
    """Process of identifying AI-generated or AI-altered content to distinguish from authentic material during investigations. Enhanced as gUFO Event for forensic process modeling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIContentDetection"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    detection_confidence: Optional[float] = field(default=None)
    detection_method: Optional[str] = field(default=None)
    evidence_admissibility: Optional[str] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    detection_time_point: list[datetime] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class AIContentGeneration:
    """Process of creating artificial CSAM using machine learning models, neural networks, or other AI technologies. Enhanced as gUFO Event for precise temporal and causal modeling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIContentGeneration"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class AIContentInvestigationSituation:
    """Complex situation involving multiple stakeholders, technologies, and legal frameworks for investigating AI-generated CSAM."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIContentInvestigationSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class AIDetectionPhase:
    """Anti-rigid phase during which AI-generated content undergoes detection and analysis processes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIDetectionPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)
    begin_time_point: list[datetime] = field(default_factory=list)


@dataclass
class AIDetectionTool:
    """Software tool specialized for detecting AI-generated content in digital media. Enhanced as gUFO Object for tool modeling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIDetectionTool"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    creator: Optional[Identity] = field(default=None)
    references: list[str] = field(default_factory=list)
    service_pack: Optional[str] = field(default=None)
    tool_type: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)
    false_positive_rate: Optional[float] = field(default=None)


@dataclass
class AIForensicAnalyst:
    """Anti-rigid role of specialist analyzing AI-generated content for authenticity and generation methods."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIForensicAnalyst"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class AIGeneratedCSAM:
    """Child sexual abuse material fully generated by artificial intelligence without depicting real victims, but still contributing to objectification and sexualization of children. Enhanced as gUFO Object """

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIGeneratedCSAM"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)
    ai_model_used: Optional[str] = field(default=None)
    artificialness_level: Optional[str] = field(default=None)
    real_victim_depicted: Optional[bool] = field(default=None)
    rendering_quality: Optional[str] = field(default=None)
    creation_time_point: list[datetime] = field(default_factory=list)


@dataclass
class AIModelAnalyst:
    """Anti-rigid role of specialist identifying and analyzing AI models used for content generation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AIModelAnalyst"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class AgeProgression:
    """AI technique for artificially aging or de-aging subjects in content, potentially creating illegal material from legal content. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#AgeProgression"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ArtifactAnalysis:
    """Analysis of digital artifacts and inconsistencies that may indicate AI generation, such as compression patterns or noise characteristics. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#ArtifactAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    detection_confidence: Optional[float] = field(default=None)
    detection_method: Optional[str] = field(default=None)
    evidence_admissibility: Optional[str] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    detection_time_point: list[datetime] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    analysis_completion_time_point: list[datetime] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)


@dataclass
class BiometricInconsistencyAnalysis:
    """Analysis of biometric inconsistencies in AI-generated content, such as unnatural eye movements or facial feature distortions. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#BiometricInconsistencyAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    detection_confidence: Optional[float] = field(default=None)
    detection_method: Optional[str] = field(default=None)
    evidence_admissibility: Optional[str] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    detection_time_point: list[datetime] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    analysis_completion_time_point: list[datetime] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)


@dataclass
class ContentGenerationPhase:
    """Anti-rigid phase during which AI systems generate illegal content."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#ContentGenerationPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)


@dataclass
class CrossPlatformDetectionSituation:
    """Situation involving detection and analysis of AI-generated content across multiple platforms and technologies."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#CrossPlatformDetectionSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class DeepfakeCSAM:
    """CSAM created by using AI to alter genuine content, potentially making real victims appear in fabricated scenarios or altering existing abuse material. Enhanced as gUFO Object with manipulation trackin"""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#DeepfakeCSAM"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)
    manipulation_time_point: list[datetime] = field(default_factory=list)


@dataclass
class DeepfakeDetection:
    """Specialized analysis for detecting deepfake technology use in content, including face replacement and manipulation. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#DeepfakeDetection"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    detection_confidence: Optional[float] = field(default=None)
    detection_method: Optional[str] = field(default=None)
    evidence_admissibility: Optional[str] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    detection_time_point: list[datetime] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class DeepfakeDetectionSpecialist:
    """Anti-rigid role of specialist focused on detecting and analyzing deepfake technology use."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#DeepfakeDetectionSpecialist"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class DeepfakeDetectionTool:
    """Tool specifically designed to identify deepfake content and face manipulation techniques. Enhanced as gUFO Object."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#DeepfakeDetectionTool"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    creator: Optional[Identity] = field(default=None)
    references: list[str] = field(default_factory=list)
    service_pack: Optional[str] = field(default=None)
    tool_type: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)
    false_positive_rate: Optional[float] = field(default=None)


@dataclass
class FaceSwapping:
    """AI technique for replacing faces in existing content with different faces, potentially placing victims in abusive scenarios. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#FaceSwapping"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class ForensicAnalysisPhase:
    """Anti-rigid phase during which AI-generated content undergoes detailed forensic examination."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#ForensicAnalysisPhase"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_coordination_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_production_phase_end_point: Optional[dateTimeStamp] = field(default=None)
    has_legal_deadline: Optional[dateTimeStamp] = field(default=None)
    has_maximum_duration: Optional[str] = field(default=None)
    has_minimum_duration: Optional[str] = field(default=None)
    has_typical_duration: Optional[str] = field(default=None)
    phase_completion_rate: Optional[float] = field(default=None)
    phase_efficiency: Optional[float] = field(default=None)
    urgency_level: Optional[int] = field(default=None)


@dataclass
class GenerationSourceTracking:
    """Investigation process to identify the source, tools, and methods used to generate AI-CSAM. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#GenerationSourceTracking"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)


@dataclass
class HybridCSAM:
    """Content combining real and AI-generated elements, making it difficult to distinguish between authentic and artificial material. Enhanced as gUFO Object with composition modeling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#HybridCSAM"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)
    ai_model_used: Optional[str] = field(default=None)
    artificialness_level: Optional[str] = field(default=None)
    real_victim_depicted: Optional[bool] = field(default=None)
    rendering_quality: Optional[str] = field(default=None)
    creation_time_point: list[datetime] = field(default_factory=list)


@dataclass
class ImageGeneration:
    """Generation of static images using AI models such as diffusion models, GANs, or other generative techniques. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#ImageGeneration"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MetadataAnalysisTool:
    """Tool for analyzing metadata patterns that may indicate AI generation or manipulation. Enhanced as gUFO Object."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#MetadataAnalysisTool"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    creator: Optional[Identity] = field(default=None)
    references: list[str] = field(default_factory=list)
    service_pack: Optional[str] = field(default=None)
    tool_type: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)
    false_positive_rate: Optional[float] = field(default=None)


@dataclass
class ModelIdentification:
    """Process of identifying the specific AI model or algorithm used to generate illegal content. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#ModelIdentification"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)


@dataclass
class ModelTraining:
    """Process of training AI models on datasets that may include illegal content for the purpose of generating new CSAM. Enhanced as gUFO Event with training phases."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#ModelTraining"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class Nudification:
    """AI content generation/manipulation process that produces synthetic nudity (e.g., 'nudifying apps' / nudifying functionalities) from existing media. Modeled as a gUFO Event and UCO Action."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#Nudification"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)
    nudification_technique: Optional[str] = field(default=None)


@dataclass
class NudificationTool:
    """Software tool or functionality capable of performing AI-enabled nudification (synthetic nudity) of existing media."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#NudificationTool"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    creator: Optional[Identity] = field(default=None)
    references: list[str] = field(default_factory=list)
    service_pack: Optional[str] = field(default=None)
    tool_type: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)


@dataclass
class NudifiedCSAM:
    """Child sexual abuse material created by AI-enabled nudification (synthetic nudity) of an existing image or video. This models 'nudifying functionalities' discussed in policy contexts."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#NudifiedCSAM"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)


@dataclass
class SyntheticImageDetector:
    """Tool for detecting synthetically generated images using machine learning classifiers. Enhanced as gUFO Object."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#SyntheticImageDetector"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    creator: Optional[Identity] = field(default=None)
    references: list[str] = field(default_factory=list)
    service_pack: Optional[str] = field(default=None)
    tool_type: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)
    false_positive_rate: Optional[float] = field(default=None)


@dataclass
class SyntheticMediaAnalysis:
    """Forensic analysis of media to determine if it was artificially generated and identify generation techniques used. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#SyntheticMediaAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    detection_confidence: Optional[float] = field(default=None)
    detection_method: Optional[str] = field(default=None)
    evidence_admissibility: Optional[str] = field(default=None)
    processing_time: Optional[float] = field(default=None)
    detection_time_point: list[datetime] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    analysis_completion_time_point: list[datetime] = field(default_factory=list)
    performer: Optional[Person] = field(default=None)


@dataclass
class SyntheticMediaCSAM:
    """Completely synthetic media generated using AI models trained on large datasets, creating realistic but artificial depictions. Enhanced as gUFO Object for synthetic media modeling."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#SyntheticMediaCSAM"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    has_changed: Optional[bool] = field(default=None)
    state: Optional[str] = field(default=None)
    label: list[str] = field(default_factory=list)
    ai_model_used: Optional[str] = field(default=None)
    artificialness_level: Optional[str] = field(default=None)
    real_victim_depicted: Optional[bool] = field(default=None)
    rendering_quality: Optional[str] = field(default=None)
    creation_time_point: list[datetime] = field(default_factory=list)


@dataclass
class SyntheticMediaExaminer:
    """Anti-rigid role of expert examining synthetic media for forensic artifacts and generation signatures."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#SyntheticMediaExaminer"
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    label: list[str] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    participates_in_investigation: list[CACInvestigation] = field(default_factory=list)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_authority_level: Optional[str] = field(default=None)
    has_responsiveness: Optional[str] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_effectiveness: Optional[float] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)
    has_role_begin_point: Optional[dateTimeStamp] = field(default=None)
    has_role_end_point: Optional[dateTimeStamp] = field(default=None)


@dataclass
class TechnicalAnalysisSituation:
    """Situation requiring coordination between technical experts, forensic analysts, and legal teams for AI content analysis."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#TechnicalAnalysisSituation"
    label: list[str] = field(default_factory=list)


@dataclass
class TrainingDataAnalysis:
    """Analysis of datasets potentially used to train AI models for generating illegal content. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#TrainingDataAnalysis"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    created_by: Optional[IdentityAbstraction] = field(default=None)
    description: list[str] = field(default_factory=list)
    external_reference: list[ExternalReference] = field(default_factory=list)
    has_facet: list[Facet] = field(default_factory=list)
    modified_time: list[datetime] = field(default_factory=list)
    name: Optional[str] = field(default=None)
    object_created_time: Optional[datetime] = field(default=None)
    object_marking: list[MarkingDefinitionAbstraction] = field(default_factory=list)
    object_status: Optional[str] = field(default=None)
    spec_version: Optional[str] = field(default=None)
    tag: list[str] = field(default_factory=list)
    action_count: Optional[int] = field(default=None)
    action_status: list[str] = field(default_factory=list)
    end_time: Optional[datetime] = field(default=None)
    environment: Optional[UcoObject] = field(default=None)
    error: list[UcoObject] = field(default_factory=list)
    instrument: list[UcoObject] = field(default_factory=list)
    location: list[Location] = field(default_factory=list)
    object: list[UcoObject] = field(default_factory=list)
    participant: list[UcoObject] = field(default_factory=list)
    performer: Optional[UcoObject] = field(default=None)
    result: list[UcoObject] = field(default_factory=list)
    start_time: Optional[datetime] = field(default=None)
    subaction: list[Action] = field(default_factory=list)
    was_informed_by: list[InvestigativeAction] = field(default_factory=list)


@dataclass
class VideoGeneration:
    """Generation of video content using AI models capable of creating temporal sequences and motion. Enhanced as gUFO Event."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/ai-csam#VideoGeneration"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    generation_complexity: Optional[str] = field(default=None)
    generation_technique: Optional[str] = field(default=None)
    technical_expertise_required: Optional[str] = field(default=None)
    generation_duration: Optional[str] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)

