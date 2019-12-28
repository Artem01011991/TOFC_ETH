"""create timestamp table

Revision ID: 749c16874ee9
Revises: 
Create Date: 2019-12-01 16:42:49.568805

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '749c16874ee9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'timestamps',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.DateTime),
        sa.Column('stock_name', sa.Unicode(20))
    )


def downgrade():
    op.drop_table('timestamps')
