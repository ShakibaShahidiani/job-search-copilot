"""Deterministic MATCHER-agent scoring (agents/MATCHER.md), used only by the
seed script to produce each job's one-time MatchScore. No LLM calls.
"""

import datetime as dt
from dataclasses import dataclass, field

from app.models.enums import SeniorityLevel
from app.services.candidate_profile import (
    CANDIDATE_TECH_SKILLS,
    CAREER_DIRECTION_FIT,
    DEFAULT_CAREER_DIRECTION_FIT,
    DEFAULT_LOCATION_FIT,
    DEMONSTRATED_EVIDENCE,
    DOMAIN_FIT,
    INFRA_TAGS,
    LOCATION_FIT,
    ROLE_FAMILY_TIER,
    SENIORITY_FIT,
    TAG_LABELS,
)

# Weights from agents/MATCHER.md "Initial deterministic weighting".
WEIGHTS: dict[str, float] = {
    "technical_fit": 0.22,
    "demonstrated_evidence": 0.18,
    "seniority_fit": 0.15,
    "career_direction_fit": 0.12,
    "preference_fit": 0.10,
    "infrastructure_fit": 0.08,
    "domain_fit": 0.06,
    "location_fit": 0.04,
    "language_fit": 0.03,
    "freshness": 0.02,
}

# Neutral baseline for preference_fit in the static MatchScore: live,
# feedback-driven adjustment happens separately in services/ranking.py.
BASELINE_PREFERENCE_FIT = 0.5

EVIDENCE_MATCH_THRESHOLD = 0.7
EVIDENCE_MEDIUM_THRESHOLD = 0.3


@dataclass
class ScoringInput:
    role_family: str
    domain: str
    location: str
    seniority_level: SeniorityLevel
    required_tags: list[str]
    preferred_tags: list[str]
    dutch_required: bool
    seniority_blocker: bool
    posted_date: dt.date
    reference_date: dt.date = field(default_factory=dt.date.today)


@dataclass
class MatchScoreResult:
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
    final_score: float
    rationale: str
    top_matches: list[str]
    gaps: list[dict]
    blockers: list[str]


def _technical_fit(tags: list[str]) -> float:
    if not tags:
        return 0.5
    hits = sum(1 for t in tags if t in CANDIDATE_TECH_SKILLS)
    return hits / len(tags)


def _demonstrated_evidence(tags: list[str]) -> float:
    if not tags:
        return 0.5
    return sum(DEMONSTRATED_EVIDENCE.get(t, 0.0) for t in tags) / len(tags)


def _infrastructure_fit(tags: list[str]) -> float:
    infra_in_job = [t for t in tags if t in INFRA_TAGS]
    if not infra_in_job:
        return 0.7
    return sum(DEMONSTRATED_EVIDENCE.get(t, 0.0) for t in infra_in_job) / len(infra_in_job)


def _freshness(posted_date: dt.date, reference_date: dt.date) -> float:
    age_days = (reference_date - posted_date).days
    if age_days <= 7:
        return 1.0
    if age_days <= 14:
        return 0.9
    if age_days <= 30:
        return 0.75
    if age_days <= 60:
        return 0.5
    return 0.2


def _gap_severity(tag: str, is_required: bool) -> str | None:
    evidence = DEMONSTRATED_EVIDENCE.get(tag, 0.0)
    if evidence >= EVIDENCE_MATCH_THRESHOLD:
        return None
    if is_required:
        return "HIGH" if evidence < EVIDENCE_MEDIUM_THRESHOLD else "MEDIUM"
    return "MEDIUM" if evidence < EVIDENCE_MEDIUM_THRESHOLD else "LOW"


def compute_match_score(inp: ScoringInput) -> MatchScoreResult:
    all_tags = inp.required_tags + inp.preferred_tags

    technical_fit = _technical_fit(all_tags)
    demonstrated_evidence = _demonstrated_evidence(all_tags)
    seniority_fit = SENIORITY_FIT[inp.seniority_level.value]
    domain_fit = DOMAIN_FIT.get(inp.domain, DOMAIN_FIT["other"])
    infrastructure_fit = _infrastructure_fit(all_tags)
    location_fit = LOCATION_FIT.get(inp.location, DEFAULT_LOCATION_FIT)
    language_fit = 0.0 if inp.dutch_required else 1.0
    tier = ROLE_FAMILY_TIER.get(inp.role_family)
    career_direction_fit = (
        CAREER_DIRECTION_FIT[tier] if tier else DEFAULT_CAREER_DIRECTION_FIT
    )
    preference_fit = BASELINE_PREFERENCE_FIT
    freshness = _freshness(inp.posted_date, inp.reference_date)

    dimensions = {
        "technical_fit": technical_fit,
        "demonstrated_evidence": demonstrated_evidence,
        "seniority_fit": seniority_fit,
        "domain_fit": domain_fit,
        "infrastructure_fit": infrastructure_fit,
        "location_fit": location_fit,
        "language_fit": language_fit,
        "career_direction_fit": career_direction_fit,
        "preference_fit": preference_fit,
        "freshness": freshness,
    }
    weighted_sum = sum(dimensions[dim] * weight for dim, weight in WEIGHTS.items())
    final_score = round(weighted_sum * 10, 2)

    top_matches = sorted(
        (t for t in all_tags if DEMONSTRATED_EVIDENCE.get(t, 0.0) >= EVIDENCE_MATCH_THRESHOLD),
        key=lambda t: DEMONSTRATED_EVIDENCE.get(t, 0.0),
        reverse=True,
    )
    top_matches = [TAG_LABELS.get(t, t) for t in top_matches[:5]]

    gaps: list[dict] = []
    for t in inp.required_tags:
        severity = _gap_severity(t, is_required=True)
        if severity:
            gaps.append({"skill": TAG_LABELS.get(t, t), "severity": severity})
    for t in inp.preferred_tags:
        severity = _gap_severity(t, is_required=False)
        if severity:
            gaps.append({"skill": TAG_LABELS.get(t, t), "severity": severity})

    blockers: list[str] = []
    if inp.dutch_required:
        blockers.append("mandatory_dutch")
        gaps.insert(0, {"skill": "Dutch language fluency", "severity": "BLOCKER"})
    if inp.seniority_blocker:
        blockers.append("seniority_blocker")
        gaps.insert(0, {"skill": "Years of experience / leadership scope", "severity": "BLOCKER"})

    gaps = gaps[:6]

    rationale_bits = [
        f"technical_fit={technical_fit:.2f}",
        f"demonstrated_evidence={demonstrated_evidence:.2f}",
        f"seniority_fit={seniority_fit:.2f}",
        f"career_direction_fit={career_direction_fit:.2f}",
    ]
    if blockers:
        rationale_bits.append(f"blockers={blockers}")
    rationale = "Deterministic MATCHER score: " + ", ".join(rationale_bits)

    return MatchScoreResult(
        technical_fit=technical_fit,
        demonstrated_evidence=demonstrated_evidence,
        seniority_fit=seniority_fit,
        domain_fit=domain_fit,
        infrastructure_fit=infrastructure_fit,
        location_fit=location_fit,
        language_fit=language_fit,
        career_direction_fit=career_direction_fit,
        preference_fit=preference_fit,
        freshness=freshness,
        final_score=final_score,
        rationale=rationale,
        top_matches=top_matches,
        gaps=gaps,
        blockers=blockers,
    )
