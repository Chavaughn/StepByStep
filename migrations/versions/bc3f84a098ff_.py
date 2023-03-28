"""empty message

Revision ID: bc3f84a098ff
Revises: ee8819fd28a3
Create Date: 2023-03-28 03:33:44.159159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3f84a098ff'
down_revision = 'ee8819fd28a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.drop_constraint('assignments_student_id_fkey', type_='foreignkey')
        batch_op.drop_column('student_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('assignments_student_id_fkey', 'students', ['student_id'], ['id'])

    # ### end Alembic commands ###
