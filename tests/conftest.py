import os
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("SECRET_KEY", "test_secret_for_pytest")

from app.database import get_session
from app.main import app as fastapi_app
from app.models.user import Base


# Configure test database
ASYNC_SQLITE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    ASYNC_SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

AsyncTestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    # Create all tables using Base.metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_session():
    async with AsyncTestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def override_get_session():
    async def _get_test_session():
        async with AsyncTestingSessionLocal() as session:
            yield session

    fastapi_app.dependency_overrides[get_session] = _get_test_session
    yield
    fastapi_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
