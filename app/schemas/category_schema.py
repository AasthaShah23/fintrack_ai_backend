from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    color: Optional[str] = None
    tag: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None
    color: Optional[str] = None
    is_system: bool

    model_config = {
        "from_attributes": True
    }