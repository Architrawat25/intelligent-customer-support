from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declared_attr, Mapped, mapped_column
from datetime import datetime, timezone
import re
from typing import Any

from app.core.config import settings

class Base(DeclarativeBase):
    id: Any

    @declared_attr
    def __tablename__(cls) -> str:       # CamelCase → snake_case
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
