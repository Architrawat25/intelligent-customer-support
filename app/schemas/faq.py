from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FAQBase(BaseModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    keywords: Optional[str] = Field(None, description="Comma-separated keywords for search")

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=1)
    answer: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    keywords: Optional[str] = None
    is_active: Optional[bool] = None

class FAQ(FAQBase):
    id: str
    is_active: bool = True
    view_count: int = 0
    helpfulness_score: float = 0.0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
