"""Update User model to enable logging-in by email

Revision ID: 727f2c629428
Revises: 4604ed2fd7dd
Create Date: 2022-07-04 02:41:32.874816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '727f2c629428'
down_revision = '4604ed2fd7dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
