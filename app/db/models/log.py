from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, JSON
import uuid
from typing import Optional, Dict, Any

from app.db.base import Base, TimestampMixin

class UserLog(Base, TimestampMixin):
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id", ondelete="CASCADE"), index=True)
    action: Mapped[str]  = mapped_column(String(100), index=True)
    resource: Mapped[Optional[str]] = mapped_column(String(100))
    resource_id: Mapped[Optional[str]] = mapped_column(String(36))
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    # CHANGED: renamed from 'metadata' to 'extra_data' to avoid SQLAlchemy conflict
    extra_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)

    user: Mapped["User"] = relationship(back_populates="logs")

    def __repr__(self) -> str:
        return f"<UserLog(id={self.id}, action={self.action}, user_id={self.user_id})>"

class SystemLog(Base, TimestampMixin):
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    level: Mapped[str] = mapped_column(String(20), index=True)
    message: Mapped[str] = mapped_column(Text)
    module: Mapped[Optional[str]] = mapped_column(String(100))
    function: Mapped[Optional[str]] = mapped_column(String(100))
    # CHANGED: renamed from 'metadata' to 'extra_data' to avoid SQLAlchemy conflict
    extra_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)

    def __repr__(self) -> str:
        return f"<SystemLog(id={self.id}, level={self.level}, message={self.message[:50]}...)>"
