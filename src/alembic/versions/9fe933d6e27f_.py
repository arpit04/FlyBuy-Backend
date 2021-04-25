"""empty message

Revision ID: 9fe933d6e27f
Revises: dce2dcaf219c
Create Date: 2021-04-25 17:26:46.507835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe933d6e27f'
down_revision = 'dce2dcaf219c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=256), nullable=True),
    sa.Column('last_name', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('phone_number', sa.String(length=256), nullable=True),
    sa.Column('address', sa.String(length=1000), nullable=True),
    sa.Column('country', sa.String(length=256), nullable=True),
    sa.Column('state', sa.String(length=256), nullable=True),
    sa.Column('city', sa.String(length=256), nullable=True),
    sa.Column('postal_code', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_address')
    # ### end Alembic commands ###