from typing import NoReturn

import jwt
from redis.asyncio import Redis

from app.common.utils import try_parse_uuid, utc_now
from app.core.config import app_settings
from app.core.exception import ConflictError, UnauthorizedError
from app.core.redis import redis_keys
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    hash_password,
    verify_password,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schema import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    TokenResponse,
)
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserCreate


class AuthService:
    def __init__(self, repo: AuthRepository, redis: Redis):
        self.repo = repo
        self.redis = redis
        self.user_repo = UserRepository(repo.db)

    def _refresh_key(self, token: str) -> str:
        return redis_keys.refresh_token(token)

    async def _issue_tokens(self, user: User) -> TokenResponse:
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        await self.redis.set(
            self._refresh_key(refresh_token),
            str(user.id),
            ex=app_settings.JWT_REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def _invalid_refresh(self, exc: Exception | None = None) -> NoReturn:
        err = UnauthorizedError("Invalid refresh token")
        if exc is not None:
            raise err from exc
        raise err

    async def register(self, body: UserCreate) -> User:
        if await self.user_repo.get_by_email(body.email):
            raise ConflictError("User with this email already exists")
        data = body.model_dump(exclude={"password"})
        data["password_hash"] = hash_password(body.password)
        return await self.user_repo.create(**data)

    async def login(self, body: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(body.email)
        if not user or not verify_password(body.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        return await self._issue_tokens(user)

    async def refresh(self, body: RefreshRequest) -> TokenResponse:
        token = body.refresh_token
        stored_user_id = await self.redis.getdel(self._refresh_key(token))
        if not stored_user_id:
            self._invalid_refresh()
        try:
            payload = decode_jwt_token(token)
        except jwt.PyJWTError as exc:
            self._invalid_refresh(exc)
        user_id = payload.get("sub")
        if payload.get("type") != "refresh" or not user_id or user_id != stored_user_id:
            self._invalid_refresh()
        user_uuid = try_parse_uuid(user_id)
        if not user_uuid:
            self._invalid_refresh()
        user = await self.user_repo.get(user_uuid)
        if not user:
            self._invalid_refresh()
        return await self._issue_tokens(user)

    async def logout(self, body: LogoutRequest) -> None:
        await self.redis.delete(self._refresh_key(body.refresh_token))

        if body.access_token:
            try:
                payload = decode_jwt_token(body.access_token)
                if payload.get("type") != "access":
                    return
                jti = payload.get("jti")
                exp = payload.get("exp")
                if not jti or exp is None:
                    return
                ttl = max(int(exp - utc_now().timestamp()), 1)
                await self.redis.set(redis_keys.blacklist_jti(jti), "1", ex=ttl)
            except jwt.PyJWTError:
                pass

    async def verify(self, token: str) -> User:
        # TODO: decode token and verify user
        raise NotImplementedError
