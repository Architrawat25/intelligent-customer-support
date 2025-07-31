from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Customer Support System"
    VERSION: str = "1.0.0"
    DEBUG: bool = True  # toggle in prod

    DATABASE_URL: str = Field(
        default="sqlite:///./customer_support.db",
        description="SQLAlchemy DB URL"
    )

    SECRET_KEY: str = Field(
        default="CHANGE_ME",
        description="JWT & CSRF secret"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    HUGGINGFACE_API_URL: str = (
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    )
    HUGGINGFACE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
