from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserLogBase(BaseModel):
    action: str = Field(max_length=100)
    resource: Optional[str] = Field(None, max_length=100)
    resource_id: Optional[str] = None
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    # CHANGED: renamed from 'metadata' to 'extra_data'
    extra_data: Optional[Dict[str, Any]] = None

class UserLogCreate(UserLogBase):
    user_id: str

class UserLog(UserLogBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
