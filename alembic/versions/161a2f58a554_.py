"""empty message

Revision ID: 161a2f58a554
Revises: 1b2828f72f15
Create Date: 2019-01-02 17:39:02.406643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '161a2f58a554'
down_revision = '1b2828f72f15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('api_key', sa.String(length=45), nullable=True))
    op.create_unique_constraint(None, 'users', ['api_key'])
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'phone_num')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_num', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'api_key')
    # ### end Alembic commands ###