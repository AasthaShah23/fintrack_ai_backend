from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    UniqueConstraint
)

from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        UniqueConstraint(
            "name",
            name="uq_category_user_name"
        ),
    )

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    tag = Column(String(50))

    color = Column(String(20))

    is_system = Column(
        Boolean,
        default=False
    )

    is_delete = Column(
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

    user_categories = relationship(
        "UserCategory",
        back_populates="category"
    )