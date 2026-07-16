"""update is_system default value

Revision ID: ad89e347a40f
Revises: c6d2689b87ce
Create Date: 2026-07-15 23:50:57.748970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad89e347a40f'
down_revision: Union[str, Sequence[str], None] = 'c6d2689b87ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
