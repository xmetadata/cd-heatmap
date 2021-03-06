"""empty message

Revision ID: f067a7ee621e
Revises: 4727c742f8e5
Create Date: 2019-12-22 22:55:50.961346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f067a7ee621e'
down_revision = '4727c742f8e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('area', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dataset', 'area')
    # ### end Alembic commands ###
