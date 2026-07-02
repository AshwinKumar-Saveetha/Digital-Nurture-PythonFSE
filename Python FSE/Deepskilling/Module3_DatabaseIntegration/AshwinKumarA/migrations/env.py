"""
env.py - Hands-On 7, Task 1 (Step 94)

Wires Alembic's autogenerate support to the SQLAlchemy models
defined in ../orm/models.py, so `alembic revision --autogenerate`
can diff the live database against Base.metadata.
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides access to the
# values within alembic.ini
config = context.config

# set up loggers from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Make ../orm importable so we can pull in the model metadata
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'orm')))
from models import Base  # noqa: E402

# target_metadata drives --autogenerate: Alembic compares this
# against the live database to produce upgrade()/downgrade() diffs
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode - emits SQL to stdout
    without needing a live DBAPI connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode - opens a real connection
    and applies migrations directly."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
