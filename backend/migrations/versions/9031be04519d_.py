"""empty message

Revision ID: 9031be04519d
Revises: 0f7275b909bb
Create Date: 2022-07-17 16:09:59.401002

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9031be04519d'
down_revision = '0f7275b909bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('create_time', sa.DateTime(), nullable=False))
    op.drop_column('token', 'exprid_datetime')
    op.drop_column('token', 'last_used')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('last_used', mysql.DATETIME(), nullable=False))
    op.add_column('token', sa.Column('exprid_datetime', mysql.DATETIME(), nullable=True))
    op.drop_column('token', 'create_time')
    # ### end Alembic commands ###
