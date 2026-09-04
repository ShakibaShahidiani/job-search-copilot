import datetime as dt

from pydantic import BaseModel, ConfigDict

from app.models.enums import Confidence, FeatureType


class PreferenceSignalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    feature_type: FeatureType
    feature_value: str
    weight: float
    evidence_count: int
    confidence: Confidence
    updated_at: dt.datetime
