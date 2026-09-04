from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.feedback import Feedback
from app.models.job import Job
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.services.preference_learner import recalculate_all

router = APIRouter(tags=["feedback"])


@router.post("/feedback", response_model=FeedbackOut, status_code=201)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)) -> FeedbackOut:
    job = db.get(Job, payload.job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {payload.job_id} not found")

    feedback = Feedback(
        job_id=payload.job_id,
        action=payload.action,
        reason=payload.reason,
        free_text=payload.free_text,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    # Recompute PreferenceSignal by replaying the full Feedback history, so
    # it always stays a pure derivation of the append-only feedback log.
    recalculate_all(db)

    return FeedbackOut.model_validate(feedback)


@router.get("/feedback/history", response_model=list[FeedbackOut])
def feedback_history(job_id: int | None = None, db: Session = Depends(get_db)) -> list[FeedbackOut]:
    query = db.query(Feedback)
    if job_id is not None:
        query = query.filter(Feedback.job_id == job_id)
    events = query.order_by(Feedback.created_at, Feedback.id).all()
    return [FeedbackOut.model_validate(e) for e in events]
