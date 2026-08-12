from pydantic import EmailStr, Field

from app.common.base_schema import BaseSchema


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=8)


class LogoutRequest(BaseSchema):
    refresh_token: str
    access_token: str | None = None


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseSchema):
    refresh_token: str
