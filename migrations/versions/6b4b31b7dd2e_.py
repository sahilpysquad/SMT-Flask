"""empty message

Revision ID: 6b4b31b7dd2e
Revises: b7f72bf86014
Create Date: 2022-12-06 16:54:42.283537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b4b31b7dd2e'
down_revision = 'b7f72bf86014'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('area_zone', schema=None) as batch_op:
        batch_op.drop_constraint('area_zone_ass_supervisor_id_fkey', type_='foreignkey')
        batch_op.drop_column('ass_supervisor_id')

    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ass_supervisor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['ass_supervisor_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('ass_supervisor_id')

    with op.batch_alter_table('area_zone', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ass_supervisor_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('area_zone_ass_supervisor_id_fkey', 'user', ['ass_supervisor_id'], ['id'])

    # ### end Alembic commands ###
