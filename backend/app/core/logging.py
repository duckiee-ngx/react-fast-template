import logging
import sys

RESET = "\033[0m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
CYAN = "\033[96m"

METHOD_COLORS = {
    "GET": BLUE,
    "POST": GREEN,
    "PUT": YELLOW,
    "PATCH": MAGENTA,
    "DELETE": RED,
}

_use_color = sys.stdout.isatty()


def setup_logging() -> None:
    access_logger = logging.getLogger("app.access")
    access_logger.handlers.clear()
    access_logger.setLevel(logging.INFO)
    access_logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    access_logger.addHandler(handler)


def get_access_logger() -> logging.Logger:
    return logging.getLogger("app.access")


def color_method(method: str) -> str:
    if not _use_color:
        return method
    color = METHOD_COLORS.get(method, RESET)
    return f"{color}{method}{RESET}"


def color_status(status: int) -> str:
    if not _use_color:
        return str(status)
    if 200 <= status < 300:
        color = GREEN
    elif 300 <= status < 400:
        color = CYAN
    else:
        color = RED
    return f"{color}{status}{RESET}"
