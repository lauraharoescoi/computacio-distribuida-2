"""empty message

Revision ID: 7391cce2d049
Revises: ba58b6ade5f4
Create Date: 2023-12-07 16:22:33.991831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7391cce2d049'
down_revision: Union[str, None] = 'ba58b6ade5f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_home_user_id', table_name='home_user')
    op.drop_table('home_user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('home', 'location')
    op.create_table('home_user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('home', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['home'], ['home.id'], name='home_user_home_fkey'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], name='home_user_user_fkey'),
    sa.PrimaryKeyConstraint('id', name='home_user_pkey')
    )
    op.create_index('ix_home_user_id', 'home_user', ['id'], unique=False)
    # ### end Alembic commands ###
