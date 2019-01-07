"""empty message

Revision ID: 92122e6dadd5
Revises: 161a2f58a554
Create Date: 2019-01-07 16:28:25.375439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92122e6dadd5'
down_revision = '161a2f58a554'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('security_answer', sa.String(), nullable=False))
    op.add_column('projects', sa.Column('address', sa.String(), nullable=False))
    op.add_column('users', sa.Column('security_answer', sa.String(), nullable=False))
    op.drop_column('users', 'birthday')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birthday', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('users', 'security_answer')
    op.drop_column('projects', 'address')
    op.drop_column('admins', 'security_answer')
    # ### end Alembic commands ###