"""empty message

Revision ID: f265ca430162
Revises: c03e1b6eacfb
Create Date: 2019-11-27 21:39:38.509623

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f265ca430162'
down_revision = 'c03e1b6eacfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blockset', sa.Column('center', sa.Text(), nullable=True))
    op.drop_column('blockset', 'centerpoint')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blockset', sa.Column('centerpoint', mysql.VARCHAR(length=32), nullable=True))
    op.drop_column('blockset', 'center')
    # ### end Alembic commands ###