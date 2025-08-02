from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Customer Support System"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./customer_support.db",
        description="Database connection URL"
    )

    # Security
    SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION",
        description="Secret key for JWT token generation"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Hugging Face
    HUGGINGFACE_API_URL: str = Field(
        default="https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        description="Hugging Face inference API endpoint"
    )
    HUGGINGFACE_API_KEY: Optional[str] = Field(
        default=None,
        description="Hugging Face API key"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
