# faq.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Integer
import uuid
from typing import Optional

from app.db.base import Base, TimestampMixin

class FAQ(Base, TimestampMixin):
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question: Mapped[str] = mapped_column(Text, index=True)
    answer: Mapped[str]   = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    keywords: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    helpfulness_score: Mapped[float] = mapped_column(default=0.0)
