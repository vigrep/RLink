"""v3_add_role

Revision ID: 455aabce5081
Revises: 43d8c4279917
Create Date: 2018-01-29 15:50:19.849895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '455aabce5081'
down_revision = '43d8c4279917'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_role',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('tb_user', sa.Column('role_id', sa.INTEGER(), nullable=True))
    op.drop_index('ix_tb_user_name', table_name='tb_user')
    op.create_index(op.f('ix_tb_user_name'), 'tb_user', ['name'], unique=True)
    op.drop_index('ix_tb_user_nickname', table_name='tb_user')
    op.create_index(op.f('ix_tb_user_nickname'), 'tb_user', ['nickname'], unique=True)
    op.create_unique_constraint(None, 'tb_user', ['email'])
    op.create_foreign_key(None, 'tb_user', 'tb_role', ['role_id'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tb_user', type_='foreignkey')
    op.drop_constraint(None, 'tb_user', type_='unique')
    op.drop_index(op.f('ix_tb_user_nickname'), table_name='tb_user')
    op.create_index('ix_tb_user_nickname', 'tb_user', ['nickname'], unique=False)
    op.drop_index(op.f('ix_tb_user_name'), table_name='tb_user')
    op.create_index('ix_tb_user_name', 'tb_user', ['name'], unique=False)
    op.drop_column('tb_user', 'role_id')
    op.drop_table('tb_role')
    # ### end Alembic commands ###
