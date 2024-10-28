"""add foreign-key to posts table

Revision ID: 4a3e1ee1b207
Revises: f01a6bf9899a
Create Date: 2024-10-24 15:43:13.682467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a3e1ee1b207'
down_revision: Union[str, None] = 'f01a6bf9899a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
  #  op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    pass
