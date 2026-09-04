"""Combines the static MatchScore (services/scoring.py) with the live,
feedback-derived PreferenceSignal table (services/preference_learner.py)
into an explainable, ranked job list. No LLM calls; pure application logic.
"""

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.job import Job
from app.models.preference_signal import PreferenceSignal
from app.services.preference_learner import extract_features

# Total preference contribution is capped so learned preferences nudge
# ranking rather than overwhelm the base MATCHER score.
PREFERENCE_ADJUSTMENT_BOUND = 2.5
EXPLANATION_LIMIT = 5
MIN_EXPLAINED_WEIGHT = 0.01

FEATURE_LABELS = {
    "role_family": "role",
    "technology": "tech",
    "domain": "domain",
    "company_type": "company type",
    "seniority": "seniority",
    "location": "location",
    "work_model": "work model",
}


@dataclass
class RankedJob:
    job: Job
    base_score: float
    preference_adjustment: float
    final_score: float
    preference_explanation: list[str]
    has_blocker: bool


def _format_contribution(feature_type: str, feature_value: str, weight: float) -> str:
    label = FEATURE_LABELS.get(feature_type, feature_type)
    sign = "+" if weight >= 0 else ""
    return f"{sign}{weight:.2f} {label}: {feature_value}"


def rank_jobs(db: Session) -> list[RankedJob]:
    jobs = list(
        db.scalars(
            select(Job).options(joinedload(Job.match_score)).order_by(Job.id)
        )
    )
    signal_rows = db.scalars(select(PreferenceSignal))
    signal_map: dict[tuple[str, str], float] = {
        (row.feature_type.value, row.feature_value): row.weight for row in signal_rows
    }

    ranked: list[RankedJob] = []
    for job in jobs:
        if job.match_score is None:
            continue
        base_score = job.match_score.final_score

        contributions: list[tuple[float, str]] = []
        raw_adjustment = 0.0
        for feature_type, feature_value in extract_features(job):
            weight = signal_map.get((feature_type.value, feature_value), 0.0)
            if abs(weight) < MIN_EXPLAINED_WEIGHT:
                continue
            raw_adjustment += weight
            contributions.append(
                (abs(weight), _format_contribution(feature_type.value, feature_value, weight))
            )

        preference_adjustment = max(
            -PREFERENCE_ADJUSTMENT_BOUND, min(PREFERENCE_ADJUSTMENT_BOUND, raw_adjustment)
        )
        final_score = max(0.0, min(10.0, base_score + preference_adjustment))

        contributions.sort(key=lambda c: c[0], reverse=True)
        explanation = [text for _, text in contributions[:EXPLANATION_LIMIT]]

        ranked.append(
            RankedJob(
                job=job,
                base_score=base_score,
                preference_adjustment=round(preference_adjustment, 2),
                final_score=round(final_score, 2),
                preference_explanation=explanation,
                has_blocker=bool(job.match_score.blockers),
            )
        )

    # Hard constraint: jobs with a blocker always sort below jobs without
    # one, regardless of score. Within each group, sort by final_score desc.
    ranked.sort(key=lambda r: (r.has_blocker, -r.final_score))
    return ranked
