from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
)

from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.database import Base


class UserCategory(Base):
    __tablename__ = "user_categories"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    monthly_budget = Column(
        Numeric(10, 2),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
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

    category = relationship("Category", back_populates="user_categories")