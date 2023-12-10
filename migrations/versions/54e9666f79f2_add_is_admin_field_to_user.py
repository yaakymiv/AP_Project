"""Add is_admin field to User

Revision ID: 54e9666f79f2
Revises: 422b76657a13
Create Date: 2023-12-10 15:56:38.867402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e9666f79f2'
down_revision = '422b76657a13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
       batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='False'))

    connection = op.get_bind()
    connection.execute("UPDATE users SET is_admin = FALSE WHERE is_admin IS NULL")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
