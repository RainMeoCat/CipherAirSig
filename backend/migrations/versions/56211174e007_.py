"""empty message

Revision ID: 56211174e007
Revises: 
Create Date: 2022-07-19 03:30:11.048579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56211174e007'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('airsign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('hash_0', sa.BigInteger(), nullable=False),
    sa.Column('symbol_code', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('cr_token', sa.String(length=75), nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('symbol_code', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=50), nullable=True),
    sa.Column('account', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=75), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.Column('register_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('gsign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('phase', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=75), nullable=False),
    sa.Column('token_enabled', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token')
    op.drop_table('gsign')
    op.drop_table('user')
    op.drop_table('cr')
    op.drop_table('airsign')
    # ### end Alembic commands ###
