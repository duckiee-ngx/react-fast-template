from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import close_db
from app.core.exception import add_exception_handlers
from app.core.logging import RED, RESET, YELLOW
from app.core.redis import close_redis, init_redis
from app.middleware import register_middlewares
from app.router import master_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    print(f"{YELLOW}🚀 Starting server...{RESET}")
    await init_redis()

    yield

    await close_redis()
    await close_db()

    print(f"{RED}🛑 Shutting down server...{RESET}")


description = """
### FastAPI Template.
"""

app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Template",
    description=description,
    version="0.0.1",
)


app.include_router(master_router)
add_exception_handlers(app)
register_middlewares(app)
