"""empty message

Revision ID: 86b1aaf50ad8
Revises: 79a090c697dd
Create Date: 2023-12-21 13:24:11.862630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2



# revision identifiers, used by Alembic.
revision: str = '86b1aaf50ad8'
down_revision: Union[str, None] = '79a090c697dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('home_owner_fkey', 'home', type_='foreignkey')
    op.create_foreign_key(None, 'home', 'user', ['owner'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'home', type_='foreignkey')
    op.create_foreign_key('home_owner_fkey', 'home', 'user', ['owner'], ['id'])
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('srid > 0 AND srid <= 998999', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    # ### end Alembic commands ###