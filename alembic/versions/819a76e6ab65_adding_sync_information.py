"""adding sync information

Revision ID: 819a76e6ab65
Revises: 3ba15ead444f
Create Date: 2026-02-01 13:47:25.127525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '819a76e6ab65'
down_revision: Union[str, Sequence[str], None] = '3ba15ead444f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('synced', sa.Integer(), nullable=True))
    op.add_column('categories', sa.Column('synced', sa.Integer(), nullable=True))
    op.add_column('income', sa.Column('synced', sa.Integer(), nullable=True))
    op.add_column('spending', sa.Column('synced', sa.Integer(), nullable=True))
    op.add_column('savings_goals', sa.Column('synced', sa.Integer(), nullable=True))
    op.add_column('savings_contributions', sa.Column('synced', sa.Integer(), nullable=True))
    op.alter_column('users', 'synced', nullable=False)
    op.alter_column('categories', 'synced', nullable=False)
    op.alter_column('income', 'synced', nullable=False)
    op.alter_column('spending', 'synced', nullable=False)
    op.alter_column('savings_goals', 'synced', nullable=False)
    op.alter_column('savings_contributions', 'synced', nullable=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'synced')
    op.drop_column('categories', 'synced')
    op.drop_column('income', 'synced')
    op.drop_column('spending', 'synced')
    op.drop_column('savings_goals', 'synced')
    op.drop_column('savings_contributions', 'synced')
