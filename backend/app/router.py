from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.core.dependency import AsyncSessionDep, RedisDep
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router

master_router = APIRouter()

master_router.include_router(auth_router)
master_router.include_router(users_router)


@master_router.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


@master_router.get("/ready", include_in_schema=False)
async def ready(
    response: Response,
    db: AsyncSessionDep,
    redis: RedisDep,
) -> dict[str, str]:
    checks: dict[str, str] = {}
    try:
        await db.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception:
        checks["postgres"] = "error"
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"
    if any(v != "ok" for v in checks.values()):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable", **checks}
    return {"status": "ok", **checks}
