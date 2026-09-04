import datetime as dt

from sqlalchemy import Date, DateTime, Enum, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import CompanyType, EmploymentType, JobStatus, SeniorityLevel, WorkModel


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)

    company: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(Text)
    work_model: Mapped[WorkModel] = mapped_column(Enum(WorkModel, name="work_model"))

    source_url: Mapped[str] = mapped_column(Text)
    direct_application_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    posted_date: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    discovered_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    description: Mapped[str] = mapped_column(Text)
    required_skills: Mapped[list[str]] = mapped_column(JSONB, default=list)
    preferred_skills: Mapped[list[str]] = mapped_column(JSONB, default=list)
    experience_requirement: Mapped[str] = mapped_column(Text)
    language_requirements: Mapped[str] = mapped_column(Text)
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType, name="employment_type")
    )
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, name="job_status"), default=JobStatus.ACTIVE
    )

    # Structured fields that back deterministic scoring (services/scoring.py)
    # and preference-signal feature extraction (services/preference_learner.py).
    # Not in docs/DATA_MODEL.md's minimum list, but required to make the
    # role_family/technology/domain/company_type feature set concrete.
    role_family: Mapped[str] = mapped_column(Text)
    company_type: Mapped[CompanyType] = mapped_column(Enum(CompanyType, name="company_type"))
    seniority_level: Mapped[SeniorityLevel] = mapped_column(
        Enum(SeniorityLevel, name="seniority_level")
    )
    domain: Mapped[str] = mapped_column(Text)
    technologies: Mapped[list[str]] = mapped_column(JSONB, default=list)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    match_score: Mapped["MatchScore | None"] = relationship(
        back_populates="job", uselist=False, cascade="all, delete-orphan"
    )
    feedback_events: Mapped[list["Feedback"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
