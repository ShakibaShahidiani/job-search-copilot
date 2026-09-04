"""Deterministic preference learner (agents/PREFERENCE_LEARNER.md).

PreferenceSignal is always rebuilt by replaying the full Feedback history in
chronological order -- it is never mutated incrementally in a way that could
drift from what the raw Feedback table says. This keeps "Feedback is the
source of truth, PreferenceSignal is derived" literally true, and makes the
whole learner replaceable later (e.g. by pairwise learning) without touching
anything upstream of Feedback.
"""

import math

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import Confidence, FeatureType, RejectReason
from app.models.feedback import Feedback
from app.models.job import Job
from app.models.preference_signal import PreferenceSignal

# Signed base weight per action. Stronger downstream signals (APPLY,
# INTERVIEW, OFFER) move preferences more than a simple LIKE; a REJECT
# without an explicit reason is treated as weaker evidence than one with a
# reason, per "explicit reason > inferred reason".
ACTION_WEIGHT: dict[str, float] = {
    "LIKE": 1.0,
    "SHORTLIST": 0.7,
    "APPLY": 1.5,
    "INTERVIEW": 2.0,
    "OFFER": 2.5,
    "REJECT": -1.0,
}

# Reject reasons that map onto a single, concrete feature. Reasons not
# listed here (compensation, language, visa, company, other) don't
# generalize to one of our modeled feature types -- e.g. "company" is
# usually about one employer, not a reusable preference -- so they only
# produce the same weak, non-targeted update as a reasonless reject.
REASON_FEATURE_MAP: dict[RejectReason, FeatureType] = {
    RejectReason.TOO_SENIOR: FeatureType.SENIORITY,
    RejectReason.TOO_JUNIOR: FeatureType.SENIORITY,
    RejectReason.CONSULTING: FeatureType.COMPANY_TYPE,
    RejectReason.DOMAIN: FeatureType.DOMAIN,
    RejectReason.TECHNOLOGY: FeatureType.TECHNOLOGY,
    RejectReason.ROLE_CONTENT: FeatureType.ROLE_FAMILY,
    RejectReason.LOCATION: FeatureType.LOCATION,
}

BASE_STEP = 0.05
REASON_STRONG_MULTIPLIER = 2.0
WEIGHT_BOUND = 1.0


def _confidence_for(evidence_count: int) -> Confidence:
    if evidence_count >= 7:
        return Confidence.STRONG
    if evidence_count >= 4:
        return Confidence.MEDIUM
    if evidence_count >= 2:
        return Confidence.WEAK
    return Confidence.OBSERVATION


def extract_features(job: Job) -> list[tuple[FeatureType, str]]:
    features: list[tuple[FeatureType, str]] = [
        (FeatureType.ROLE_FAMILY, job.role_family),
        (FeatureType.DOMAIN, job.domain),
        (FeatureType.COMPANY_TYPE, job.company_type.value),
        (FeatureType.SENIORITY, job.seniority_level.value),
        (FeatureType.LOCATION, job.location),
        (FeatureType.WORK_MODEL, job.work_model.value),
    ]
    features.extend((FeatureType.TECHNOLOGY, tag) for tag in job.technologies)
    return features


class _WorkingSignal:
    __slots__ = ("weight", "evidence_count")

    def __init__(self) -> None:
        self.weight = 0.0
        self.evidence_count = 0


def _replay(feedback_events: list[Feedback], jobs_by_id: dict[int, Job]) -> dict:
    signals: dict[tuple[FeatureType, str], _WorkingSignal] = {}

    for fb in feedback_events:
        job = jobs_by_id.get(fb.job_id)
        if job is None:
            continue

        action_weight = ACTION_WEIGHT.get(fb.action.value, 0.0)
        targeted_feature = REASON_FEATURE_MAP.get(fb.reason) if fb.reason else None

        for feature_type, feature_value in extract_features(job):
            key = (feature_type, feature_value)
            signal = signals.setdefault(key, _WorkingSignal())

            multiplier = (
                REASON_STRONG_MULTIPLIER if feature_type == targeted_feature else 1.0
            )
            # Diminishing step size as evidence accumulates, so no single
            # event can swing a feature's weight drastically.
            step = BASE_STEP * multiplier / math.sqrt(signal.evidence_count + 1)
            delta = action_weight * step

            signal.weight = max(-WEIGHT_BOUND, min(WEIGHT_BOUND, signal.weight + delta))
            signal.evidence_count += 1

    return signals


def recalculate_all(db: Session) -> None:
    """Wipe and rebuild PreferenceSignal from the full Feedback history."""
    feedback_events = list(
        db.scalars(select(Feedback).order_by(Feedback.created_at, Feedback.id))
    )
    jobs_by_id = {job.id: job for job in db.scalars(select(Job))}

    signals = _replay(feedback_events, jobs_by_id)

    db.query(PreferenceSignal).delete()

    for (feature_type, feature_value), working in signals.items():
        db.add(
            PreferenceSignal(
                feature_type=feature_type,
                feature_value=feature_value,
                weight=round(working.weight, 4),
                evidence_count=working.evidence_count,
                confidence=_confidence_for(working.evidence_count),
            )
        )
    db.commit()
