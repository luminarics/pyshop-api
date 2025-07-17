import os
from typing import Optional

SECRET_KEY = os.getenv(
    "SECRET_KEY", "your-secret-key-for-jwt"  # Change this in production!
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database configuration
DATABASE_URL: Optional[str] = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://app:app@localhost:5432/fastapi"
)
