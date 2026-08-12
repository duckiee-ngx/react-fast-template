from typing import Annotated

from fastapi import Depends

from app.core.dependency import AsyncSessionDep, RedisDep
from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService


def get_auth_service(db: AsyncSessionDep, redis: RedisDep) -> AuthService:
    return AuthService(AuthRepository(db), redis)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
