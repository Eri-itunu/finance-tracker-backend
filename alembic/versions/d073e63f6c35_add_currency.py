"""add currency

Revision ID: d073e63f6c35
Revises: 54cb0a7e1390
Create Date: 2026-01-30 22:14:34.805599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd073e63f6c35'
down_revision: Union[str, Sequence[str], None] = '54cb0a7e1390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Add currency enum type (PostgreSQL)
    currency_enum = sa.Enum('NGN', 'GBP', 'USD', 'EUR', name='currency')
    currency_enum.create(op.get_bind(), checkfirst=True)
    
    # Add default_currency to users
    op.add_column('users', 
        sa.Column('default_currency', currency_enum, 
                  server_default='NGN', nullable=False)
    )
    
    # Add currency to income
    op.add_column('income', 
        sa.Column('currency', currency_enum, 
                  server_default='NGN', nullable=False)
    )
    
    # Add currency to spending
    op.add_column('spending', 
        sa.Column('currency', currency_enum, 
                  server_default='NGN', nullable=False)
    )
    
    # Add currency to savings_goals
    op.add_column('savings_goals', 
        sa.Column('currency', currency_enum, 
                  server_default='NGN', nullable=False)
    )
    
    # Add currency to savings_contributions
    op.add_column('savings_contributions', 
        sa.Column('currency', currency_enum, 
                  server_default='NGN', nullable=False)
    )
    pass   
def downgrade():
    op.drop_column('savings_contributions', 'currency')
    op.drop_column('savings_goals', 'currency')
    op.drop_column('spending', 'currency')
    op.drop_column('income', 'currency')
    op.drop_column('users', 'default_currency')
    
    # Drop enum type (PostgreSQL)
    sa.Enum(name='currency').drop(op.get_bind(), checkfirst=True)
    pass   