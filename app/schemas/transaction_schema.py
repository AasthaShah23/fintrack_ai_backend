from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.db.transaction import (
    TransactionType,
    TransactionMethod
)


class TransactionCreate(BaseModel):
    category_id: int

    amount: Decimal

    type: TransactionType

    remark: Optional[str] = None

    transaction_date: datetime

    transaction_method: TransactionMethod


class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None

    amount: Optional[Decimal] = None

    type: Optional[TransactionType] = None

    remark: Optional[str] = None

    transaction_date: Optional[datetime] = None

    transaction_method: Optional[TransactionMethod] = None


class TransactionResponse(BaseModel):
    id: int

    user_id: int
    category_id: int

    amount: Decimal

    type: TransactionType

    remark: Optional[str]

    transaction_date: datetime

    transaction_method: TransactionMethod

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True