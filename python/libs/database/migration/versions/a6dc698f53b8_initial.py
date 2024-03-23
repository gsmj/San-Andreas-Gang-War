"""'initial'

Revision ID: a6dc698f53b8
Revises: acb5e99a4eee
Create Date: 2024-03-23 21:56:36.403988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6dc698f53b8'
down_revision: Union[str, None] = 'acb5e99a4eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
