from collections.abc import AsyncGenerator
from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.exception import UnauthorizedError
from app.core.redis import get_redis, redis_keys
from app.core.security import bearer_scheme, decode_jwt_token


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]

RedisDep = Annotated[Redis, Depends(get_redis)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    redis: RedisDep,
) -> dict[str, Any]:
    if not credentials:
        raise UnauthorizedError()
    try:
        payload = decode_jwt_token(credentials.credentials)
        jti = payload.get("jti")
        if (
            payload.get("type") != "access"
            or not jti
            or await redis.exists(redis_keys.blacklist_jti(jti))
        ):
            raise UnauthorizedError()
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError(detail="Token has expired") from None
    except jwt.PyJWTError:
        raise UnauthorizedError() from None


CurrentUserDep = Annotated[dict[str, Any], Depends(get_current_user)]
