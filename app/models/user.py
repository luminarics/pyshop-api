from typing import Optional
from uuid import UUID, uuid4
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[UUID], Base):
    __tablename__ = "user"

    id = Column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    username: str = Column(str, unique=True, index=True)
    email: str = Column(str, unique=True, index=True)
    hashed_password: str = Column(str, nullable=False)
    is_active: bool = Column(bool, default=True, nullable=False)
    is_superuser: bool = Column(bool, default=False, nullable=False)
    is_verified: bool = Column(bool, default=False, nullable=False)

    class Config:
        arbitrary_types_allowed = True


class UserRead(schemas.BaseUser[UUID]):
    username: str

    class Config:
        arbitrary_types_allowed = True


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
