from typing import ClassVar

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for all application errors."""

    status: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str | None = None):
        self.detail = detail


class BadRequestError(AppError):
    """Raised when a bad request is made."""

    status = status.HTTP_400_BAD_REQUEST


class UnauthorizedError(AppError):
    """Raised when an unauthorized request is made."""

    status = status.HTTP_401_UNAUTHORIZED


class NotFoundError(AppError):
    """Raised when an entity is not found."""

    status = status.HTTP_404_NOT_FOUND


class ConflictError(AppError):
    """Raised when a conflict occurs."""

    status = status.HTTP_409_CONFLICT


async def _app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    error = exc if isinstance(exc, AppError) else AppError()
    return JSONResponse(
        status_code=error.status,
        content={"detail": error.detail or error.__class__.__doc__},
    )


def _500_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong"},
    )


def add_exception_handlers(app: FastAPI) -> None:
    for subclass in AppError.__subclasses__():
        app.add_exception_handler(subclass, _app_error_handler)

    app.add_exception_handler(
        Exception,
        _500_error_handler,
    )
