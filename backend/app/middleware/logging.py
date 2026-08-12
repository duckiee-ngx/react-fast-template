import time

from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.common.utils import utc_now
from app.core.logging import (
    color_method,
    color_status,
    get_access_logger,
    setup_logging,
)

logger = get_access_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            _log_request(request, status.HTTP_500_INTERNAL_SERVER_ERROR, duration_ms)
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        _log_request(request, response.status_code, duration_ms)
        return response


def _log_request(request: Request, status_code: int, duration_ms: float) -> None:
    timestamp = utc_now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(
        "[%s] %s %s -> %s (%.0fms)",
        timestamp,
        color_method(request.method),
        request.url.path,
        color_status(status_code),
        duration_ms,
    )


def register_request_logging(app: FastAPI) -> None:
    setup_logging()
    app.add_middleware(RequestLoggingMiddleware)
