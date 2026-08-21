from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class PaginatedResponse(Generic[T]):

    items: list[T]

    page: int

    page_size: int

    total: int

    @property
    def total_pages(self) -> int:

        if self.page_size == 0:
            return 0

        return (
            self.total + self.page_size - 1
        ) // self.page_size