"""'add_users_and_tokens_tables

Revision ID: d7e2a2f0f54e
Revises: 
Create Date: 2023-11-19 19:57:07.517719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e2a2f0f54e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('tokens',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('token', sa.UUID(as_uuid=False), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
