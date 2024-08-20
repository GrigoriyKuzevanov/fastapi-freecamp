"""add content to posts table.

Revision ID: 9307707ccfa0
Revises: fc1c873f4e2f
Create Date: 2024-08-20 15:46:50.106831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9307707ccfa0'
down_revision: Union[str, None] = 'fc1c873f4e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
