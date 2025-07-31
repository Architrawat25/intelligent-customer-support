# user.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
import uuid
from typing import List, Optional

from app.db.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    id: Mapped[str]       = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str]    = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool]  = mapped_column(Boolean, default=True)
    is_admin:  Mapped[bool]  = mapped_column(Boolean, default=False)

    tickets: Mapped[List["Ticket"]] = relationship(back_populates="user", cascade="all,delete-orphan")
    logs:    Mapped[List["UserLog"]] = relationship(back_populates="user", cascade="all,delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.email}>"
