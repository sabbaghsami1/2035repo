"""empty message

Revision ID: 3daa02f45070
Revises: 37c8f2c41f0e
Create Date: 2024-11-16 00:18:24.293095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3daa02f45070'
down_revision = '37c8f2c41f0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userid', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_posts_userid_users'), 'users', ['userid'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_posts_userid_users'), type_='foreignkey')
        batch_op.drop_column('userid')

    op.drop_table('users')
    # ### end Alembic commands ###