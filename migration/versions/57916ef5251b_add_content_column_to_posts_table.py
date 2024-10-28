"""add content column to posts table

Revision ID: 57916ef5251b
Revises: b95260f4ae05
Create Date: 2024-10-24 15:29:48.676997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57916ef5251b'
down_revision: Union[str, None] = 'b95260f4ae05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
