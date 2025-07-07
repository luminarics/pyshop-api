from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine

DATABASE_URL = "postgresql+asyncpg://app:app@localhost:5432/fastapi"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
async def get_session():
    async with async_session() as session:
        yield session

async def init_db(engine: Optional[AsyncEngine] = None) -> None:
    """
    Create all tables. By default uses the module‐level `engine`,
    but callers can pass in their own AsyncEngine.
    """
    _engine = engine or globals()["engine"]
    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db(): 
    db = async_session()
    try:
        yield db
    finally:
        db.close()