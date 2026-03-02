"""baseline

Revision ID: 7b64300fb493
Revises: de546aacb2a8
Create Date: 2026-03-03 01:41:46.446881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b64300fb493'
down_revision: Union[str, Sequence[str], None] = 'de546aacb2a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
