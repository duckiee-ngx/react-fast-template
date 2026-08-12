from datetime import timedelta
from typing import Any, Literal
from uuid import uuid4

import jwt
from bcrypt import checkpw, gensalt, hashpw
from fastapi.security import HTTPBearer

from app.common.utils import utc_now
from app.core.config import app_settings


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return checkpw(
        plain_password.encode(),
        hashed_password.encode(),
    )


def _create_jwt_token(
    payload: dict[str, Any], type: Literal["access", "refresh"], expire_minutes: int
) -> str:
    payload["type"] = type
    now = utc_now()
    return jwt.encode(
        payload={
            **payload,
            "jti": str(uuid4()),
            "iat": now,
            "exp": now + timedelta(minutes=expire_minutes),
        },
        key=app_settings.JWT_SECRET,
        algorithm=app_settings.JWT_ALGORITHM,
    )


def create_access_token(payload: dict[str, Any]) -> str:
    return _create_jwt_token(payload, "access", app_settings.JWT_EXPIRE_MINUTES)


def create_refresh_token(payload: dict[str, Any]) -> str:
    return _create_jwt_token(
        payload, "refresh", app_settings.JWT_REFRESH_EXPIRE_DAYS * 24 * 60
    )


def decode_jwt_token(
    token: str,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        app_settings.JWT_SECRET,
        algorithms=[app_settings.JWT_ALGORITHM],
    )


bearer_scheme = HTTPBearer(
    auto_error=False,
)
