from pydantic import EmailStr, Field

from app.common.base_schema import BaseSchema, IDSchema, TimestampSchema


class UserCreate(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=8)


class UserUpdate(BaseSchema):
    password: str | None = Field(default=None, min_length=8)


class UserResponse(IDSchema, TimestampSchema):
    email: EmailStr
    is_verified: bool
