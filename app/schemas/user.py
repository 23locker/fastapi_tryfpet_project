from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base column user"""

    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating user"""

    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    """Schema for updating user profile"""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """Schema for response with user data"""

    user_id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for login"""

    email: EmailStr
    password: str
