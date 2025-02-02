"""Created one to many relationship with goals and tasks

Revision ID: 4b085b01324d
Revises: b0782c8cc52d
Create Date: 2022-11-06 20:23:59.554677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b085b01324d'
down_revision = 'b0782c8cc52d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
