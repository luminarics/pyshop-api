import os
from sqlalchemy.engine.url import URL, make_url

SECRET_KEY: str = os.getenv("SECRET_KEY", "test_secret")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

DATABASE_URL: str | URL = make_url(
    os.getenv("DATABASE_URL", "postgresql+asyncpg://app:app@db:5432/fastapi")
)

GIT_SHA: str = os.getenv("GIT_SHA", "unknown")
