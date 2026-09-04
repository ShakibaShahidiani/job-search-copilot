import datetime as dt

from sqlalchemy import DateTime, Float, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MatchScore(Base):
    """Static, deterministic score computed once (see services/scoring.py),
    following the dimensions and weights in agents/MATCHER.md.

    This is NOT updated by feedback. Feedback-driven movement happens
    separately in PreferenceSignal / services/ranking.py, so the two
    influences on final ranking stay independently inspectable.
    """

    __tablename__ = "match_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), unique=True)

    technical_fit: Mapped[float] = mapped_column(Float)
    demonstrated_evidence: Mapped[float] = mapped_column(Float)
    seniority_fit: Mapped[float] = mapped_column(Float)
    domain_fit: Mapped[float] = mapped_column(Float)
    infrastructure_fit: Mapped[float] = mapped_column(Float)
    location_fit: Mapped[float] = mapped_column(Float)
    language_fit: Mapped[float] = mapped_column(Float)
    career_direction_fit: Mapped[float] = mapped_column(Float)
    preference_fit: Mapped[float] = mapped_column(Float)
    freshness: Mapped[float] = mapped_column(Float)

    final_score: Mapped[float] = mapped_column(Float)
    rationale: Mapped[str] = mapped_column(Text)
    top_matches: Mapped[list[str]] = mapped_column(JSONB, default=list)
    gaps: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    blockers: Mapped[list[str]] = mapped_column(JSONB, default=list)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    job: Mapped["Job"] = relationship(back_populates="match_score")
