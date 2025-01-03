"""'initial'

Revision ID: 8f591c7ee369
Revises: a6dc698f53b8
Create Date: 2024-03-23 21:56:58.178361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f591c7ee369'
down_revision: Union[str, None] = 'a6dc698f53b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('House',
    sa.Column('uid', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('owner', sa.String(length=32), nullable=True),
    sa.Column('interior_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('pos_x', sa.Float(), nullable=True),
    sa.Column('pos_y', sa.Float(), nullable=True),
    sa.Column('pos_z', sa.Float(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('Squad',
    sa.Column('uid', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('tag', sa.String(length=6), nullable=True),
    sa.Column('classification', sa.String(length=32), nullable=True),
    sa.Column('color', sa.Integer(), nullable=True),
    sa.Column('color_hex', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('SquadGangZones',
    sa.Column('uid', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('squad_id', sa.Integer(), nullable=True),
    sa.Column('min_x', sa.Float(), nullable=True),
    sa.Column('min_y', sa.Float(), nullable=True),
    sa.Column('max_x', sa.Float(), nullable=True),
    sa.Column('max_y', sa.Float(), nullable=True),
    sa.Column('capture_cooldown', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('SquadMember',
    sa.Column('uid', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('squad_id', sa.Integer(), nullable=True),
    sa.Column('member', sa.String(length=32), nullable=True),
    sa.Column('rank', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('SquadRank',
    sa.Column('uid', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('squad_id', sa.Integer(), nullable=True),
    sa.Column('rank', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('SquadRankPermissions',
    sa.Column('uid', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('squad_id', sa.Integer(), nullable=True),
    sa.Column('rank_id', sa.Integer(), nullable=True),
    sa.Column('permissions', sa.String(length=16), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.drop_table('VIPCodes')
    op.drop_column('GangZone', 'gang_def_id')
    op.drop_column('GangZone', 'gang_atk_score')
    op.drop_column('GangZone', 'gang_def_score')
    op.drop_column('GangZone', 'gang_atk_id')
    op.drop_column('GangZone', 'capture_time')
    op.drop_column('GangZone', 'is_capture')
    op.add_column('PlayerSettings', sa.Column('spawn_in_house', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Vehicle', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('ServerAnalytics', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.drop_column('ServerAnalytics', 'current')
    op.alter_column('PlayerSettings', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.drop_column('PlayerSettings', 'spawn_in_house')
    op.alter_column('PlayerFreeroamGunSlots', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('Player', 'pin',
               existing_type=sa.String(length=6),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('Player', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.add_column('GangZone', sa.Column('is_capture', sa.BOOLEAN(), nullable=True))
    op.add_column('GangZone', sa.Column('capture_time', sa.INTEGER(), nullable=True))
    op.add_column('GangZone', sa.Column('gang_atk_id', sa.INTEGER(), nullable=True))
    op.add_column('GangZone', sa.Column('gang_def_score', sa.INTEGER(), nullable=True))
    op.add_column('GangZone', sa.Column('gang_atk_score', sa.INTEGER(), nullable=True))
    op.add_column('GangZone', sa.Column('gang_def_id', sa.INTEGER(), nullable=True))
    op.alter_column('GangZone', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('AdminSavedPositions', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('AdminLog', 'uid',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
    op.create_table('VIPCodes',
    sa.Column('uid', sa.INTEGER(), nullable=False),
    sa.Column('code', sa.VARCHAR(length=64), nullable=True),
    sa.Column('level', sa.INTEGER(), nullable=True),
    sa.Column('is_activated', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.drop_table('SquadRankPermissions')
    op.drop_table('SquadRank')
    op.drop_table('SquadMember')
    op.drop_table('SquadGangZones')
    op.drop_table('Squad')
    op.drop_table('House')
    # ### end Alembic commands ###
