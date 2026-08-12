from datetime import UTC, datetime
from uuid import UUID


def utc_now() -> datetime:
    return datetime.now(UTC)


def try_parse_uuid(value: object) -> UUID | None:
    try:
        return UUID(str(value))
    except ValueError, TypeError:
        return None
