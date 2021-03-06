"""empty message

Revision ID: 780363d251b3
Revises: 7b21248163d2
Create Date: 2019-11-25 21:59:21.107569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '780363d251b3'
down_revision = '7b21248163d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blockset', sa.Column('area', sa.String(length=32), nullable=True))
    op.add_column('blockset', sa.Column('centerpoint', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blockset', 'centerpoint')
    op.drop_column('blockset', 'area')
    # ### end Alembic commands ###
