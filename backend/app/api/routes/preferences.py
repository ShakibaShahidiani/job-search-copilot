from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.preference_signal import PreferenceSignal
from app.schemas.preference import PreferenceSignalOut

router = APIRouter(tags=["preferences"])


@router.get("/preferences", response_model=list[PreferenceSignalOut])
def list_preferences(db: Session = Depends(get_db)) -> list[PreferenceSignalOut]:
    rows = (
        db.query(PreferenceSignal)
        .order_by(PreferenceSignal.feature_type, PreferenceSignal.evidence_count.desc())
        .all()
    )
    return [PreferenceSignalOut.model_validate(r) for r in rows]
