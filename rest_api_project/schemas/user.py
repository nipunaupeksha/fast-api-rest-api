from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=5, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=20)
    last_name: str = Field(..., min_length=1, max_length=20)
    is_admin: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=10)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=10)
    new_password: str = Field(..., min_length=6, max_length=10)


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: UUID

    class Config:
        from_attributes = True
