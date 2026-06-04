from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    user_id: Optional[int]

    name: str
    is_system: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True