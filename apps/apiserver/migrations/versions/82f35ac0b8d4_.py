"""empty message

Revision ID: 82f35ac0b8d4
Revises: f067a7ee621e
Create Date: 2019-12-22 23:00:41.323954

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '82f35ac0b8d4'
down_revision = 'f067a7ee621e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('inc_area', sa.Boolean(), nullable=True))
    op.drop_column('dataset', 'area')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('area', mysql.VARCHAR(length=32), nullable=True))
    op.drop_column('dataset', 'inc_area')
    # ### end Alembic commands ###
