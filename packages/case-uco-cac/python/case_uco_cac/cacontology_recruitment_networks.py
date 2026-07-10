"""CAC Ontology - Crimes Against Children — cacontology-recruitment-networks module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AcademicStruggles:
    """Academic difficulties creating vulnerability to recruitment offers."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#AcademicStruggles"
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
    label: Optional[str] = field(default=None)
    vulnerability_score: Optional[float] = field(default=None)
    academic_performance_level: Optional[str] = field(default=None)


@dataclass
class AfterSchoolRecruitment:
    """Recruitment occurring after school hours when supervision is reduced."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#AfterSchoolRecruitment"
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
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class AttendanceProblems:
    """School attendance issues that may indicate or facilitate trafficking involvement."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#AttendanceProblems"
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
    label: Optional[str] = field(default=None)
    vulnerability_score: Optional[float] = field(default=None)
    attendance_rate: Optional[float] = field(default=None)


@dataclass
class ClassmateIntroduction:
    """Introduction of new victim to trafficker through existing victim who is a classmate."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#ClassmateIntroduction"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)
    average_recruitment_time: Optional[float] = field(default=None)
    introduces_to: Optional[Person] = field(default=None)


@dataclass
class ClassmateRecruitmentNetwork:
    """Recruitment network operating within educational institutions using existing victims to recruit classmates."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#ClassmateRecruitmentNetwork"
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
    includes_recruiting_victim: list[Person] = field(default_factory=list)
    network_size: Optional[int] = field(default=None)
    victim_recruiters_count: Optional[int] = field(default=None)
    schools_involved: Optional[int] = field(default=None)
    targets_school: list[EducationalInstitution] = field(default_factory=list)


@dataclass
class CoercedPeerRecruitment:
    """Recruitment where existing victims are forced or coerced to recruit their peers."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#CoercedPeerRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class EducationalInstitution:
    """School or educational facility where recruitment occurs or reporting takes place."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#EducationalInstitution"
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
    label: Optional[str] = field(default=None)
    school_type: Optional[str] = field(default=None)
    socioeconomic_level: Optional[str] = field(default=None)
    student_population: Optional[int] = field(default=None)


@dataclass
class ExtracurricularRecruitment:
    """Recruitment occurring during extracurricular activities or school events."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#ExtracurricularRecruitment"
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
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class FriendshipExploitation:
    """Exploitation of existing friendships and trust relationships between minors for recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#FriendshipExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)


@dataclass
class LunchBreakRecruitment:
    """Recruitment occurring during lunch breaks or between classes."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#LunchBreakRecruitment"
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
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class MandatoryReportingActivation:
    """Activation of mandatory reporting requirements by school personnel."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#MandatoryReportingActivation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    mandatory_reporting_trigger: Optional[bool] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_staff_role: list[str] = field(default_factory=list)
    start_time: list[datetime] = field(default_factory=list)


@dataclass
class PeerInfluenceRecruitment:
    """Recruitment leveraging peer pressure and social influence among minors."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#PeerInfluenceRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)


@dataclass
class PeerPressureVulnerability:
    """Susceptibility to peer pressure enabling recruitment through classmates."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#PeerPressureVulnerability"
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
    label: Optional[str] = field(default=None)
    vulnerability_score: Optional[float] = field(default=None)


@dataclass
class PeerRecruitmentNetwork:
    """Network of traffickers utilizing existing victims to recruit new victims through peer relationships and social connections."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#PeerRecruitmentNetwork"
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
    includes_recruiting_victim: list[Person] = field(default_factory=list)
    network_size: Optional[int] = field(default=None)
    victim_recruiters_count: Optional[int] = field(default=None)


@dataclass
class RecruitmentIncentive:
    """Incentives offered to existing victims for successful recruitment of new victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#RecruitmentIncentive"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class RecruitmentPunishment:
    """Punishment threatened or applied to victims who fail to recruit new victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#RecruitmentPunishment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class RecruitmentQuota:
    """System where existing victims must recruit specified number of new victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#RecruitmentQuota"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class RecruitmentTiming:
    """Temporal patterns and timing of recruitment activities within educational environments."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#RecruitmentTiming"
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
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SchoolBasedRecruitment:
    """Trafficking recruitment occurring within or through school environments and relationships."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolBasedRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    grade_level: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SchoolBasedReporting:
    """Reporting of trafficking incidents through educational institution personnel."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolBasedReporting"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    mandatory_reporting_trigger: Optional[bool] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_staff_role: list[str] = field(default_factory=list)
    start_time: list[datetime] = field(default_factory=list)


@dataclass
class SchoolCounselor:
    """School counselor who may receive disclosures from trafficking victims."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolCounselor"
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
    employed_at: Optional[EducationalInstitution] = field(default=None)


@dataclass
class SchoolHoursRecruitment:
    """Recruitment occurring during regular school hours through peer interactions."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolHoursRecruitment"
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
    end_time: Optional[datetime] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class SchoolPoliceContact:
    """Contact made by school personnel to law enforcement regarding trafficking concerns."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolPoliceContact"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    mandatory_reporting_trigger: Optional[bool] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_staff_role: list[str] = field(default_factory=list)
    start_time: list[datetime] = field(default_factory=list)


@dataclass
class SchoolSocialWorker:
    """Social worker employed by educational institution who receives victim reports."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolSocialWorker"
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
    employed_at: Optional[EducationalInstitution] = field(default=None)
    label: Optional[str] = field(default=None)


@dataclass
class SchoolStaffMember:
    """Employee of educational institution involved in reporting or responding to trafficking."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolStaffMember"
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
    employed_at: Optional[EducationalInstitution] = field(default=None)


@dataclass
class SchoolVulnerabilityFactor:
    """Factors within educational environment that increase vulnerability to recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SchoolVulnerabilityFactor"
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
    label: Optional[str] = field(default=None)
    vulnerability_score: Optional[float] = field(default=None)


@dataclass
class SocialConnectionLeverage:
    """Leveraging existing social connections between victims to facilitate new recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SocialConnectionLeverage"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)


@dataclass
class SocialIsolationAtSchool:
    """Student isolation within school environment making them vulnerable to recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SocialIsolationAtSchool"
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
    label: Optional[str] = field(default=None)
    vulnerability_score: Optional[float] = field(default=None)


@dataclass
class SocialWorkerReport:
    """Report made by school social worker to law enforcement regarding trafficking victim."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#SocialWorkerReport"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    mandatory_reporting_trigger: Optional[bool] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_staff_role: list[str] = field(default_factory=list)
    start_time: list[datetime] = field(default_factory=list)
    contacts_law_enforcement: Optional[SchoolPoliceContact] = field(default=None)


@dataclass
class StudentNetworkExploitation:
    """Exploitation of student social networks and peer relationships for trafficking recruitment."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#StudentNetworkExploitation"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    grade_level: Optional[str] = field(default=None)
    start_time: Optional[datetime] = field(default=None)


@dataclass
class TeacherReporter:
    """Teacher who identifies signs of trafficking or receives disclosures from students."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#TeacherReporter"
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
    employed_at: Optional[EducationalInstitution] = field(default=None)


@dataclass
class VictimMediatedRecruitment:
    """Recruitment of new victims through existing trafficking victims acting as intermediaries."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#VictimMediatedRecruitment"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    facilitated_by: Optional[Person] = field(default=None)
    recruitment_attempts: Optional[int] = field(default=None)
    successful_recruitments: Optional[int] = field(default=None)


@dataclass
class VictimSchoolDisclosure:
    """Disclosure by trafficking victim to school personnel about their situation."""

    CLASS_IRI: str = "https://cacontology.projectvic.org/recruitment-networks#VictimSchoolDisclosure"
    has_begin_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    has_end_point_in_xsd_date_time_stamp: Optional[dateTimeStamp] = field(default=None)
    label: list[str] = field(default_factory=list)
    mandatory_reporting_trigger: Optional[bool] = field(default=None)
    reporting_delay: Optional[float] = field(default=None)
    reporting_staff_role: list[str] = field(default_factory=list)
    start_time: list[datetime] = field(default_factory=list)
    receives_report: Optional[SchoolStaffMember] = field(default=None)

