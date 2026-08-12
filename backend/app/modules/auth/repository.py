from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.model import User


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def verify(self, user: User) -> User:
        user.is_verified = True
        await self.db.flush()
        await self.db.refresh(user)
        return user
