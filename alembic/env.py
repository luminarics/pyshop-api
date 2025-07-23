# alembic/env.py
import asyncio
import os

from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context  # type: ignore[attr-defined]
from sqlmodel import SQLModel

# -------------------------------------------------
config = context.config
fileConfig(config.config_file_name)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@db:5432/fastapi")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = SQLModel.metadata
# -------------------------------------------------


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        pool_pre_ping=True,
        echo=True,  # SQL echo
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
