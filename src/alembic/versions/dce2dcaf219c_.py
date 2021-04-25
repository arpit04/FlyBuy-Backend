"""empty message

Revision ID: dce2dcaf219c
Revises: 78ef5e699a03
Create Date: 2021-04-25 14:11:33.659511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dce2dcaf219c'
down_revision = '78ef5e699a03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_images', sa.Column('profile_img', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_images', 'profile_img')
    # ### end Alembic commands ###