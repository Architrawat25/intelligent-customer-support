from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TicketBase(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    question: str = Field(min_length=1)
    status: Optional[TicketStatus] = TicketStatus.OPEN
    priority: Optional[TicketPriority] = TicketPriority.MEDIUM
    answer: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=1, max_length=255)
    question: Optional[str] = Field(None, min_length=1)
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    answer: Optional[str] = None
    resolved_at: Optional[datetime] = None

class Ticket(TicketBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    confidence_score: Optional[float] = None

    model_config = {"from_attributes": True}
