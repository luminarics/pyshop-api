from typing import Optional
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models.user import User
from app.core.config import DATABASE_URL

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:  # type: ignore # FastAPI dependency
    async with async_session() as session:
        yield session


async def init_db(db_engine: Optional[AsyncEngine] = None) -> None:
    _engine = db_engine or engine
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_user_db(session: AsyncSession = Depends(get_session)):
    """
    FastAPI-Users database adapter dependency.
    Used by UserManager to perform database operations.
    """
    yield SQLAlchemyUserDatabase(session, User)
