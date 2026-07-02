"""add CourseSchedule table

Revision ID: r3_add_course_schedule
Revises: r2_add_is_active
Create Date: 2026-07-01 06:10:00.000000

Hands-On 7, Task 2 (Step 102): adds the course_schedules table
(schedule_id, course_id FK, day_of_week, start_time, end_time).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'r3_add_course_schedule'
down_revision: Union[str, Sequence[str], None] = 'r2_add_is_active'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'course_schedules',
        sa.Column('schedule_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('day_of_week', sa.String(length=20), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id']),
        sa.PrimaryKeyConstraint('schedule_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('course_schedules')
