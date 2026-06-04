from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
from app.validators.password_validator import validate_password
from app.validators.phone_number_validator import validate_phone_number


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        return validate_phone_number(value)

    password: str
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    is_email_verified: bool
    is_phone_verified: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True