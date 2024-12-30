"""DB CatbreedInfo

Revision ID: 63303e8f885c
Revises: 
Create Date: 2024-12-28 14:25:21.475395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63303e8f885c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cat_breed_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('breed_name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cat_breed_info')
    # ### end Alembic commands ###
