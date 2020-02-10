"""empty message

Revision ID: f64539caa1d0
Revises: 82f35ac0b8d4
Create Date: 2019-12-25 21:58:17.024605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f64539caa1d0'
down_revision = '82f35ac0b8d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manuals',
    sa.Column('uuid', sa.String(length=32), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('manuals')
    # ### end Alembic commands ###