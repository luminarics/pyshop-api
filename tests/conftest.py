import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.database import get_session
from app.main import app as fastapi_app

# Import your models!
import app.models.product
import app.routers.products

ASYNC_SQLITE_URL = "sqlite+aiosqlite:///:memory:"

# StaticPool is critical!
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

# -- THE FIX: Use pytest_asyncio.fixture for async fixtures!
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # Create all tables (runs ONCE per test session)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Optional: drop tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

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

@pytest.fixture
def client():
    return TestClient(fastapi_app)
