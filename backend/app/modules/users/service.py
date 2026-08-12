from uuid import UUID

from app.core.exception import NotFoundError
from app.core.security import hash_password
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserUpdate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get(self, user_id: UUID) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def update(self, user_id: UUID, user_update: UserUpdate) -> User:
        user = await self.get(user_id)
        data = user_update.model_dump(exclude_unset=True)
        if data.get("password") is not None:
            data["password_hash"] = hash_password(data.pop("password"))
        return await self.repo.update(user, **data)

    async def delete(self, user_id: UUID) -> None:
        user = await self.get(user_id)
        await self.repo.delete(user)
