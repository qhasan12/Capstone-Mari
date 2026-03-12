"""add otp_verified column"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'bc0d9968a35b'
down_revision: Union[str, Sequence[str], None] = 'b1be868832a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'auth_users',
        sa.Column('otp_verified', sa.Boolean(), nullable=True, server_default=sa.text('false'))
    )


def downgrade() -> None:
    op.drop_column('auth_users', 'otp_verified')