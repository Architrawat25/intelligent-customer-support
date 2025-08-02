from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class QuestionCategory(str, Enum):
    GENERAL = "general"
    TECHNICAL = "technical"
    BILLING = "billing"
    ACCOUNT = "account"

class AskQuestion(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    question: str = Field(min_length=10)
    category: Optional[QuestionCategory] = QuestionCategory.GENERAL
    priority: Optional[str] = "medium"

class AskResponse(BaseModel):
    ticket_id: str
    answer: Optional[str] = None
    confidence_score: Optional[float] = None
    source: str  # "faq", "llm", or "human"
    created_at: str
