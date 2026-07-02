"""initial schema

Revision ID: r1_initial_schema
Revises:
Create Date: 2026-07-01 00:00:00.000000

Hands-On 7, Task 1 (Steps 92-97): baseline migration generated from
the SQLAlchemy models in ../../orm/models.py, creating the five core
tables that mirror the Hands-On 1 SQL schema.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'r1_initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create departments, students, courses,
    enrollments and professors."""

    # departments first - everything else references it via FK
    op.create_table(
        'departments',
        sa.Column('department_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('dept_name', sa.String(length=100), nullable=False),
        sa.Column('hod_name', sa.String(length=100), nullable=True),
        sa.Column('budget', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.PrimaryKeyConstraint('department_id'),
    )

    op.create_table(
        'students',
        sa.Column('student_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('enrollment_year', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id']),
        sa.PrimaryKeyConstraint('student_id'),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'courses',
        sa.Column('course_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('course_name', sa.String(length=150), nullable=False),
        sa.Column('course_code', sa.String(length=20), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id']),
        sa.PrimaryKeyConstraint('course_id'),
        sa.UniqueConstraint('course_code'),
    )

    op.create_table(
        'enrollments',
        sa.Column('enrollment_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('enrollment_date', sa.Date(), nullable=True),
        sa.Column('grade', sa.String(length=2), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id']),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id']),
        sa.PrimaryKeyConstraint('enrollment_id'),
    )

    op.create_table(
        'professors',
        sa.Column('professor_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('prof_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('salary', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id']),
        sa.PrimaryKeyConstraint('professor_id'),
        sa.UniqueConstraint('email'),
    )


def downgrade() -> None:
    """Downgrade schema: drop tables in reverse dependency order."""
    op.drop_table('professors')
    op.drop_table('enrollments')
    op.drop_table('courses')
    op.drop_table('students')
    op.drop_table('departments')
