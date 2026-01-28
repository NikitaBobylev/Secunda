from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T")


class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)


def pagination_params(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit)


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    offset: int
    limit: int
    total: int
    model_config = ConfigDict(from_attributes=True)
