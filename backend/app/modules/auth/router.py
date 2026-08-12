from fastapi import APIRouter, status

from app.modules.auth.dependency import AuthServiceDep
from app.modules.auth.schema import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    TokenResponse,
)
from app.modules.users.model import User
from app.modules.users.schema import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(body: UserCreate, service: AuthServiceDep) -> User:
    return await service.register(body)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, service: AuthServiceDep) -> TokenResponse:
    return await service.login(body)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, service: AuthServiceDep) -> TokenResponse:
    return await service.refresh(body)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: LogoutRequest, service: AuthServiceDep) -> None:
    await service.logout(body)


@router.get("/verify", response_model=UserResponse)
async def verify(token: str, service: AuthServiceDep) -> None:
    return await service.verify(token)
