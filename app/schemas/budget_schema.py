from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class BudgetCreate(BaseModel):
    month: int
    year: int

    limit_amount: Decimal


class BudgetUpdate(BaseModel):
    limit_amount: Decimal


class BudgetResponse(BaseModel):
    id: int

    user_id: int

    month: int
    year: int

    limit_amount: Decimal

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True