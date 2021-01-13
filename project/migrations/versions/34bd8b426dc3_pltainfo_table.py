"""pltainfo table

Revision ID: 34bd8b426dc3
Revises: 0c869035673a
Create Date: 2020-11-29 03:09:08.941212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34bd8b426dc3'
down_revision = '0c869035673a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pltainfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('elevasi_akhir', sa.Float(), nullable=True),
    sa.Column('elevasi_awal', sa.Float(), nullable=True),
    sa.Column('elevasi_target', sa.Float(), nullable=True),
    sa.Column('inflow_outflow_mendalan', sa.Float(), nullable=True),
    sa.Column('inflow_selorejo', sa.Float(), nullable=True),
    sa.Column('inflow_siman', sa.Float(), nullable=True),
    sa.Column('limpas', sa.Float(), nullable=True),
    sa.Column('mw_mendalan', sa.Float(), nullable=True),
    sa.Column('mw_mendalan_1', sa.Float(), nullable=True),
    sa.Column('mw_mendalan_2', sa.Float(), nullable=True),
    sa.Column('mw_mendalan_3', sa.Float(), nullable=True),
    sa.Column('mw_mendalan_4', sa.Float(), nullable=True),
    sa.Column('mw_selorejo', sa.Float(), nullable=True),
    sa.Column('mw_siman', sa.Float(), nullable=True),
    sa.Column('mw_siman_1', sa.Float(), nullable=True),
    sa.Column('mw_siman_2', sa.Float(), nullable=True),
    sa.Column('mw_siman_3', sa.Float(), nullable=True),
    sa.Column('mwh_mendalan', sa.Float(), nullable=True),
    sa.Column('mwh_selorejo', sa.Float(), nullable=True),
    sa.Column('mwh_siman', sa.Float(), nullable=True),
    sa.Column('outflow_selorejo', sa.Float(), nullable=True),
    sa.Column('suplesi_siman', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pltainfo')
    # ### end Alembic commands ###