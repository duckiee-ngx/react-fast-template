from fastapi import FastAPI

from .cors import register_cors
from .logging import register_request_logging


def register_middlewares(app: FastAPI) -> None:
    register_cors(app)
    register_request_logging(app)
