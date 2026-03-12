"""merge heads

Revision ID: b1be868832a6
Revises: 51db6e4aea61, 792bd1d85581
Create Date: 2026-03-12 06:54:13.958441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1be868832a6'
down_revision: Union[str, Sequence[str], None] = ('51db6e4aea61', '792bd1d85581')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
