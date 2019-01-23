"""empty message

Revision ID: 4d1fd0769f25
Revises: 820de4b26117
Create Date: 2019-01-23 03:23:03.750827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d1fd0769f25'
down_revision = '820de4b26117'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('project_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'categories', 'projects', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.drop_column('categories', 'project_id')
    # ### end Alembic commands ###