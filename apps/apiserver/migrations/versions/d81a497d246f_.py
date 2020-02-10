"""empty message

Revision ID: d81a497d246f
Revises: de374cb41f24
Create Date: 2019-11-22 22:58:46.733815

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd81a497d246f'
down_revision = 'de374cb41f24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('options', 'remark')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('options', sa.Column('remark', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###