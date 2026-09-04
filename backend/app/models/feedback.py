import datetime as dt

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import FeedbackAction, RejectReason


class Feedback(Base):
    """Append-only feedback history. Never updated or deleted by application
    code: a changed opinion is recorded as a NEW row, not an edit of an old
    one. This is the source of truth PreferenceSignal is recalculated from.
    """

    __tablename__ = "feedback"
    __table_args__ = (Index("ix_feedback_job_id_created_at", "job_id", "created_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"))
    action: Mapped[FeedbackAction] = mapped_column(Enum(FeedbackAction, name="feedback_action"))
    reason: Mapped[RejectReason | None] = mapped_column(
        Enum(RejectReason, name="reject_reason"), nullable=True
    )
    free_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    job: Mapped["Job"] = relationship(back_populates="feedback_events")
