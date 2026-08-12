from math import ceil
from typing import TypeVar

from pydantic import BaseModel, Field

from app.common.base_schema import BaseSchema

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class Page[T](BaseSchema):
    items: list[T]
    page: int
    page_size: int
    total_items: int
    total_pages: int

    @classmethod
    def create(
        cls, items: list[T], total_items: int, params: PaginationParams
    ) -> Page[T]:
        return cls(
            items=items,
            page=params.page,
            page_size=params.page_size,
            total_items=total_items,
            total_pages=ceil(total_items / params.page_size) if params.page_size else 0,
        )
