import datetime as dt

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import FeedbackAction, RejectReason


class FeedbackCreate(BaseModel):
    job_id: int
    action: FeedbackAction
    reason: RejectReason | None = None
    free_text: str | None = None

    @model_validator(mode="after")
    def reason_only_with_reject(self) -> "FeedbackCreate":
        if self.reason is not None and self.action != FeedbackAction.REJECT:
            raise ValueError("reason is only allowed when action is REJECT")
        return self


class FeedbackOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    action: FeedbackAction
    reason: RejectReason | None
    free_text: str | None
    created_at: dt.datetime
