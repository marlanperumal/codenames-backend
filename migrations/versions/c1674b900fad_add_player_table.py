"""Add player table

Revision ID: c1674b900fad
Revises: 25c26353c300
Create Date: 2020-04-20 20:49:53.073825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1674b900fad'
down_revision = '25c26353c300'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('captain', sa.Boolean(), nullable=True),
    sa.Column('team', sa.String(length=50), nullable=True),
    sa.Column('game_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_player_game_id_game')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_player'))
    )
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_player_game_id'), ['game_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_player_game_id'))

    op.drop_table('player')
    # ### end Alembic commands ###
