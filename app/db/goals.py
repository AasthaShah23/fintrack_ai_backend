from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    Boolean,
    String,
    DateTime,
)
from sqlalchemy.types import Date
from datetime import datetime, timezone

from app.database import Base

class Goal(Base):

    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String, nullable=False)

    target_amount = Column(
        Numeric(12,2),
        nullable=False
    )

    current_amount = Column(
        Numeric(12,2),
        default=0
    )

    target_date = Column(Date, nullable=False)

    is_completed = Column(
        Boolean,
        default=False
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