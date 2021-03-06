"""Add body_html to Post model

Revision ID: d2055931d862
Revises: 93bb8fd93f92
Create Date: 2022-07-19 22:11:23.571770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2055931d862'
down_revision = '93bb8fd93f92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'body_html')
    # ### end Alembic commands ###
