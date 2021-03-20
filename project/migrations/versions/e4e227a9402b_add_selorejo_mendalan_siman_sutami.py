"""Add Selorejo Mendalan Siman Sutami

Revision ID: e4e227a9402b
Revises: 3251ca9c88d9
Create Date: 2021-03-17 18:50:25.688968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4e227a9402b'
down_revision = '3251ca9c88d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_waduk_siman',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ps1', sa.Float(), nullable=True),
    sa.Column('qs1', sa.Float(), nullable=True),
    sa.Column('ps2', sa.Float(), nullable=True),
    sa.Column('qs2', sa.Float(), nullable=True),
    sa.Column('ps3', sa.Float(), nullable=True),
    sa.Column('qs3', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('sms_h_p', table_name='data_waduk_sms')
    op.drop_table('data_waduk_sms')
    op.create_index('selorejo_h_p', 'data_waduk_selorejo', ['h', 'p'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('selorejo_h_p', table_name='data_waduk_selorejo')
    op.create_table('data_waduk_sms',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('h', sa.FLOAT(), nullable=True),
    sa.Column('p', sa.FLOAT(), nullable=True),
    sa.Column('q', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('sms_h_p', 'data_waduk_sms', ['h', 'p'], unique=1)
    op.drop_table('data_waduk_siman')
    # ### end Alembic commands ###