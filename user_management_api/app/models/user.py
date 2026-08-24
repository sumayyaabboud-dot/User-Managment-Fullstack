from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"

# 1. general register
class UserRegisterSchema(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str
    city: str = Field(..., min_length=1)
    age: int = Field(..., gt=0, lt=120)
    password: str = Field(..., min_length=8)
   
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+?[1-9]\d{1,14}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number pattern")
        return v

# 2. create user from admin side
class AdminCreateUserSchema(UserRegisterSchema):
    type: UserRole = UserRole.CLIENT

# 3. login 
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# 4. update client data
class UserUpdateMeSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0, lt=120)
    password: Optional[str] = Field(None, min_length=8)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r"^\+?[1-9]\d{1,14}$", v):
            raise ValueError("Invalid phone number pattern")
        return v

# 5. update admin for users
class AdminUpdateUserSchema(UserUpdateMeSchema):
    type: Optional[UserRole] = None

# 6. response schema
class UserResponseSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    city: str
    age: int
    type: UserRole
    created_at: datetime
    updated_at: datetime