import os
from sqlalchemy.engine.url import URL, make_url

try:
    SECRET_KEY: str = os.environ["SECRET_KEY"]
except KeyError as exc:
    raise RuntimeError("SECRET_KEY env var missing") from exc

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

DATABASE_URL: str | URL = make_url(
    os.getenv("DATABASE_URL", "postgresql+asyncpg://app:app@db:5432/fastapi")
)
