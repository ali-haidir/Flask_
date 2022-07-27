"""added username to Users Model

Revision ID: be9f7da30530
Revises: 66519372559f
Create Date: 2022-07-26 17:18:16.129870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be9f7da30530'
down_revision = '66519372559f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_name', sa.String(length=30), nullable=False))
    op.create_unique_constraint(None, 'users', ['user_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'user_name')
    # ### end Alembic commands ###