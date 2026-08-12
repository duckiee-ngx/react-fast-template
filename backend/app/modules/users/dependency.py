from typing import Annotated

from fastapi import Depends

from app.core.dependency import AsyncSessionDep
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserService


def get_user_service(db: AsyncSessionDep) -> UserService:
    return UserService(UserRepository(db))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
