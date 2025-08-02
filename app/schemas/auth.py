from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=255)

class AuthResponse(BaseModel):
    user: dict
    token: Token
