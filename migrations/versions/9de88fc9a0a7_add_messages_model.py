"""Add messages Model

Revision ID: 9de88fc9a0a7
Revises: a2ef36633f7f
Create Date: 2024-08-28 11:01:06.170892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9de88fc9a0a7'
down_revision: Union[str, None] = 'a2ef36633f7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('user_role_id_fkey', 'user', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('user_role_id_fkey', 'user', 'role', ['role_id'], ['id'])
    op.drop_table('messages')
    # ### end Alembic commands ###
