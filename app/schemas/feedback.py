from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class FeedbackType(str, Enum):
    RATING = "rating"
    COMMENT = "comment"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"

class FeedbackCreate(BaseModel):
    type: FeedbackType
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
    ticket_id: Optional[str] = None
    faq_id: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: str
    message: str = "Thank you for your feedback!"
