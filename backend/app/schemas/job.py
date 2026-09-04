import datetime as dt

from pydantic import BaseModel, ConfigDict

from app.models.enums import CompanyType, EmploymentType, JobStatus, SeniorityLevel, WorkModel


class Gap(BaseModel):
    skill: str
    severity: str


class RankedJobOut(BaseModel):
    """Compact representation used by the ranked job-card list."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    title: str
    location: str
    work_model: WorkModel
    employment_type: EmploymentType
    role_family: str
    domain: str
    company_type: CompanyType
    seniority_level: SeniorityLevel
    status: JobStatus

    top_matches: list[str]
    gaps: list[Gap]
    blockers: list[str]

    base_score: float
    preference_adjustment: float
    final_score: float
    preference_explanation: list[str]


class JobDetailOut(RankedJobOut):
    """Full job detail, including the raw MATCHER dimension breakdown."""

    source_url: str
    direct_application_url: str | None
    posted_date: dt.date | None
    discovered_at: dt.datetime
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    experience_requirement: str
    language_requirements: str
    technologies: list[str]

    technical_fit: float
    demonstrated_evidence: float
    seniority_fit: float
    domain_fit: float
    infrastructure_fit: float
    location_fit: float
    language_fit: float
    career_direction_fit: float
    preference_fit: float
    freshness: float
    rationale: str
