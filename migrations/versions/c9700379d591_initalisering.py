"""initalisering

Revision ID: c9700379d591
Revises: 
Create Date: 2020-01-15 10:40:26.501670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9700379d591'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grunddata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('basisPath', sa.String(length=80), nullable=True),
    sa.Column('aar', sa.String(length=10), nullable=True),
    sa.Column('resultatFilnavn', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('klub',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('langtnavn', sa.String(length=80), nullable=True),
    sa.Column('kortnavn', sa.String(length=40), nullable=True),
    sa.Column('tom', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('konkurrence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('konkurrence_type', sa.String(length=80), nullable=True),
    sa.Column('skov', sa.String(length=80), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('resultater', sa.String(length=4), nullable=True),
    sa.Column('dato', sa.String(length=15), nullable=True),
    sa.Column('path', sa.String(length=80), nullable=True),
    sa.Column('mappenavn', sa.String(length=40), nullable=True),
    sa.Column('klub_id', sa.Integer(), nullable=True),
    sa.Column('grunddata_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['grunddata_id'], ['grunddata.id'], ),
    sa.ForeignKeyConstraint(['klub_id'], ['klub.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_konkurrence_timestamp'), 'konkurrence', ['timestamp'], unique=False)
    op.create_table('medlemmer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('navn', sa.String(length=80), nullable=True),
    sa.Column('navn_ok', sa.Integer(), nullable=True),
    sa.Column('emitbrik', sa.Integer(), nullable=True),
    sa.Column('samlet_point', sa.Integer(), nullable=True),
    sa.Column('klub_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['klub_id'], ['klub.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('baner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('baneNavn', sa.String(length=20), nullable=True),
    sa.Column('baneLaengde', sa.Integer(), nullable=True),
    sa.Column('konkurrence_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['konkurrence_id'], ['konkurrence.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deltager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bane', sa.String(length=10), nullable=True),
    sa.Column('placering', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('statuskode', sa.Integer(), nullable=True),
    sa.Column('tid', sa.String(length=20), nullable=True),
    sa.Column('tidSekunder', sa.Integer(), nullable=True),
    sa.Column('strak', sa.String(length=200), nullable=True),
    sa.Column('point', sa.Integer(), nullable=True),
    sa.Column('emit_Brik', sa.Integer(), nullable=True),
    sa.Column('medlemmer_id', sa.Integer(), nullable=True),
    sa.Column('konkurrence_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['konkurrence_id'], ['konkurrence.id'], ),
    sa.ForeignKeyConstraint(['medlemmer_id'], ['medlemmer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deltager_strak',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deltager_id', sa.Integer(), nullable=True),
    sa.Column('postnr', sa.Integer(), nullable=True),
    sa.Column('post_code', sa.Integer(), nullable=True),
    sa.Column('tidTil', sa.Integer(), nullable=True),
    sa.Column('tidTilPlac', sa.Integer(), nullable=True),
    sa.Column('tidIalt', sa.Integer(), nullable=True),
    sa.Column('tidIaltPlac', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deltager_id'], ['deltager.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_baner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('postNr', sa.Integer(), nullable=True),
    sa.Column('controlNr', sa.Integer(), nullable=True),
    sa.Column('baner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['baner_id'], ['baner.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_baner')
    op.drop_table('deltager_strak')
    op.drop_table('deltager')
    op.drop_table('baner')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('medlemmer')
    op.drop_index(op.f('ix_konkurrence_timestamp'), table_name='konkurrence')
    op.drop_table('konkurrence')
    op.drop_table('followers')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('klub')
    op.drop_table('grunddata')
    # ### end Alembic commands ###
