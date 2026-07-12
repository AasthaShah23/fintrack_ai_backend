"""seed default categories

Revision ID: c6d2689b87ce
Revises: 2df98b2f1c04
Create Date: 2026-07-12 18:03:03.058372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision: str = 'c6d2689b87ce'
down_revision: Union[str, Sequence[str], None] = '2df98b2f1c04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

now = datetime.now(timezone.utc)



category_table = sa.table(
    "categories",
    sa.column("name", sa.String),
    sa.column("tag", sa.String),
    sa.column("color", sa.String),
    sa.column("is_system", sa.Boolean),
    sa.column("created_at", sa.DateTime(timezone=True)),
    sa.column("updated_at", sa.DateTime(timezone=True)),
)


def upgrade():
    op.bulk_insert(
        category_table,
        [
            {
                "name": "Food & Dining",
                "tag": "restaurant",
                "color": "#F97316",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Shopping",
                "tag": "shopping_cart",
                "color": "#3B82F6",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Transport",
                "tag": "directions_car",
                "color": "#10B981",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Bills",
                "tag": "receipt_long",
                "color": "#EF4444",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Health",
                "tag": "favorite",
                "color": "#EC4899",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Entertainment",
                "tag": "movie",
                "color": "#8B5CF6",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Education",
                "tag": "school",
                "color": "#06B6D4",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Travel",
                "tag": "flight",
                "color": "#F59E0B",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Salary",
                "tag": "payments",
                "color": "#22C55E",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
            {
                "name": "Investment",
                "tag": "trending_up",
                "color": "#6366F1",
                "is_system": True,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade():
    op.execute(
        """
        DELETE FROM categories
        WHERE is_system = TRUE;
        """
    )