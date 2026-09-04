import datetime as dt

from sqlalchemy import DateTime, Enum, Float, Integer, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import Confidence, FeatureType


class PreferenceSignal(Base):
    """Derived state, fully recomputable from Feedback (see
    services/preference_learner.recalculate_all). Never treat this table as
    the source of truth -- it can always be rebuilt by replaying Feedback.
    """

    __tablename__ = "preference_signals"
    __table_args__ = (UniqueConstraint("feature_type", "feature_value"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    feature_type: Mapped[FeatureType] = mapped_column(Enum(FeatureType, name="feature_type"))
    feature_value: Mapped[str] = mapped_column(Text)
    weight: Mapped[float] = mapped_column(Float, default=0.0)
    evidence_count: Mapped[int] = mapped_column(Integer, default=0)
    confidence: Mapped[Confidence] = mapped_column(
        Enum(Confidence, name="confidence"), default=Confidence.OBSERVATION
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
