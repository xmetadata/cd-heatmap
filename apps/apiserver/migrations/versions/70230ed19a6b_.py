"""empty message

Revision ID: 70230ed19a6b
Revises: f265ca430162
Create Date: 2019-11-27 22:33:35.959795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70230ed19a6b'
down_revision = 'f265ca430162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dataset', 'complete')
    # ### end Alembic commands ###