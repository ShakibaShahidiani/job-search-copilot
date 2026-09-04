"""Reset and load the 10 deterministic fixture jobs.

Usage (from backend/):
    python -m app.seed.seed

Re-running this script wipes ALL existing Job/MatchScore/Feedback/
PreferenceSignal rows and reloads the fixed 10-job fixture set from
scratch, so the demo always starts from a known, deterministic state.
"""

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.feedback import Feedback
from app.models.job import Job
from app.models.match_score import MatchScore
from app.models.preference_signal import PreferenceSignal
from app.seed.seed_data import SEED_JOBS, TODAY
from app.services.scoring import ScoringInput, compute_match_score


def load_seed_jobs(db: Session) -> None:
    """Wipe all rows and insert the fixed 10-job fixture set with its
    deterministic MatchScore. Shared by the CLI script and by tests.
    """
    db.query(Feedback).delete()
    db.query(PreferenceSignal).delete()
    db.query(MatchScore).delete()
    db.query(Job).delete()
    db.commit()

    for seed_job in SEED_JOBS:
        job = Job(
            company=seed_job.company,
            title=seed_job.title,
            location=seed_job.location,
            work_model=seed_job.work_model,
            source_url=seed_job.source_url,
            direct_application_url=seed_job.direct_application_url,
            posted_date=seed_job.posted_date,
            description=seed_job.description,
            required_skills=seed_job.required_skills,
            preferred_skills=seed_job.preferred_skills,
            experience_requirement=seed_job.experience_requirement,
            language_requirements=seed_job.language_requirements,
            employment_type=seed_job.employment_type,
            role_family=seed_job.role_family,
            company_type=seed_job.company_type,
            seniority_level=seed_job.seniority_level,
            domain=seed_job.domain,
            technologies=seed_job.technologies,
        )
        db.add(job)
        db.flush()  # assign job.id

        result = compute_match_score(
            ScoringInput(
                role_family=seed_job.role_family,
                domain=seed_job.domain,
                location=seed_job.location,
                seniority_level=seed_job.seniority_level,
                required_tags=seed_job.required_tags,
                preferred_tags=seed_job.preferred_tags,
                dutch_required=seed_job.dutch_required,
                seniority_blocker=seed_job.seniority_blocker,
                posted_date=seed_job.posted_date,
                reference_date=TODAY,
            )
        )
        db.add(
            MatchScore(
                job_id=job.id,
                technical_fit=result.technical_fit,
                demonstrated_evidence=result.demonstrated_evidence,
                seniority_fit=result.seniority_fit,
                domain_fit=result.domain_fit,
                infrastructure_fit=result.infrastructure_fit,
                location_fit=result.location_fit,
                language_fit=result.language_fit,
                career_direction_fit=result.career_direction_fit,
                preference_fit=result.preference_fit,
                freshness=result.freshness,
                final_score=result.final_score,
                rationale=result.rationale,
                top_matches=result.top_matches,
                gaps=result.gaps,
                blockers=result.blockers,
            )
        )

    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        load_seed_jobs(db)
        print(f"Seeded {len(SEED_JOBS)} jobs with deterministic match scores.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
