# app/database.py  –  cleaned-up, working async DB layer
from typing import Optional
import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://app:app@localhost:5432/fastapi",  # sensible default
)
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:  # type: ignore # FastAPI dependency
    async with async_session() as session:
        yield session


async def init_db(db_engine: Optional[AsyncEngine] = None) -> None:
    """
    Create all tables. Pass a custom AsyncEngine in tests;
    use the module-level engine in production.
    """
    _engine = db_engine or engine
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
