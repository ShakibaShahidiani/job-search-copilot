from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job import JobDetailOut, RankedJobOut
from app.services.ranking import RankedJob, rank_jobs

router = APIRouter(tags=["jobs"])


def _base_fields(rj: RankedJob) -> dict:
    job = rj.job
    return {
        "id": job.id,
        "company": job.company,
        "title": job.title,
        "location": job.location,
        "work_model": job.work_model,
        "employment_type": job.employment_type,
        "role_family": job.role_family,
        "domain": job.domain,
        "company_type": job.company_type,
        "seniority_level": job.seniority_level,
        "status": job.status,
        "top_matches": job.match_score.top_matches,
        "gaps": job.match_score.gaps,
        "blockers": job.match_score.blockers,
        "base_score": rj.base_score,
        "preference_adjustment": rj.preference_adjustment,
        "final_score": rj.final_score,
        "preference_explanation": rj.preference_explanation,
    }


@router.get("/jobs", response_model=list[RankedJobOut])
def list_ranked_jobs(db: Session = Depends(get_db)) -> list[RankedJobOut]:
    ranked = rank_jobs(db)
    return [RankedJobOut(**_base_fields(rj)) for rj in ranked]


@router.get("/jobs/{job_id}", response_model=JobDetailOut)
def get_job(job_id: int, db: Session = Depends(get_db)) -> JobDetailOut:
    ranked = rank_jobs(db)
    match = next((rj for rj in ranked if rj.job.id == job_id), None)
    if match is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    job = match.job
    data = _base_fields(match)
    data.update(
        {
            "source_url": job.source_url,
            "direct_application_url": job.direct_application_url,
            "posted_date": job.posted_date,
            "discovered_at": job.discovered_at,
            "description": job.description,
            "required_skills": job.required_skills,
            "preferred_skills": job.preferred_skills,
            "experience_requirement": job.experience_requirement,
            "language_requirements": job.language_requirements,
            "technologies": job.technologies,
            "technical_fit": job.match_score.technical_fit,
            "demonstrated_evidence": job.match_score.demonstrated_evidence,
            "seniority_fit": job.match_score.seniority_fit,
            "domain_fit": job.match_score.domain_fit,
            "infrastructure_fit": job.match_score.infrastructure_fit,
            "location_fit": job.match_score.location_fit,
            "language_fit": job.match_score.language_fit,
            "career_direction_fit": job.match_score.career_direction_fit,
            "preference_fit": job.match_score.preference_fit,
            "freshness": job.match_score.freshness,
            "rationale": job.match_score.rationale,
        }
    )
    return JobDetailOut(**data)
