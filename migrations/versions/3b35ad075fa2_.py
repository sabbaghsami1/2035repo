"""empty message

Revision ID: 3b35ad075fa2
Revises: 3daa02f45070
Create Date: 2024-11-16 18:41:46.466695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b35ad075fa2'
down_revision = '3daa02f45070'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Add columns with a default value to avoid SQLite's NOT NULL restriction
        batch_op.add_column(
            sa.Column('multifactor', sa.String(length=100), nullable=False, server_default='default_value'))
        batch_op.add_column(
            sa.Column('multifactor_enabled', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))

    # Remove the server_default after initial addition to clean up
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('multifactor', server_default=None)
        batch_op.alter_column('multifactor_enabled', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('multifactor_enabled')
        batch_op.drop_column('multifactor')

    # ### end Alembic commands ###
