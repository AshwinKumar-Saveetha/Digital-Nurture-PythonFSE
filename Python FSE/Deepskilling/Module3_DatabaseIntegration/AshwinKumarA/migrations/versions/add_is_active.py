"""add is_active to students

Revision ID: r2_add_is_active
Revises: r1_initial_schema
Create Date: 2026-07-01 05:25:39.972063

Hands-On 7, Task 2 (Steps 98-101): adds the is_active boolean flag
to the students table.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'r2_add_is_active'
down_revision: Union[str, Sequence[str], None] = 'r1_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('students', sa.Column('is_active', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('students', 'is_active')
