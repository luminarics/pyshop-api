from pydantic import ConfigDict
from uuid import UUID, uuid4
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    """Base for SQLAlchemy models"""

    pass


class User(SQLAlchemyBaseUserTable[UUID], Base):
    """User model with UUID primary key"""

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class UserRead(schemas.BaseUser[UUID]):
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(schemas.BaseUserUpdate):
    username: str | None = None
    model_config = ConfigDict(from_attributes=True)
