"""empty message

Revision ID: 231b55ac9626
Revises: 
Create Date: 2025-06-20 22:26:52.479523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '231b55ac9626'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pair', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pair', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
