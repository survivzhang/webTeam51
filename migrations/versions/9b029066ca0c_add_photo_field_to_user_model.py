"""Add photo field to User model

Revision ID: 9b029066ca0c
Revises: b00524eb9346
Create Date: 2025-05-04 13:34:08.359169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b029066ca0c'
down_revision = 'b00524eb9346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('photo')

    # ### end Alembic commands ###
