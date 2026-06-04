from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Numeric,
    Text,
    Enum
)

from datetime import datetime, timezone
import enum

from app.database import Base


class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"


class TransactionMethod(enum.Enum):
    card = "card"
    netbanking = "netbanking"
    upi = "upi"
    cash = "cash"
    cheque = "cheque"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    type = Column(
        Enum(TransactionType),
        nullable=False
    )

    remark = Column(Text)

    transaction_date = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    transaction_method = Column(
        Enum(TransactionMethod),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )