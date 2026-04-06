from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.VIEWER # Default to viewer for safety

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # Tells Pydantic to read data from SQLAlchemy models