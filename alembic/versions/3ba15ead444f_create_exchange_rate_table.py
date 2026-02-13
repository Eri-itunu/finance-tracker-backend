"""create exchange rate table

Revision ID: 3ba15ead444f
Revises: d073e63f6c35
Create Date: 2026-01-30 23:58:53.517800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ba15ead444f'
down_revision: Union[str, Sequence[str], None] = 'd073e63f6c35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
