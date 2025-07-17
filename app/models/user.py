from typing import Optional
from uuid import UUID, uuid4
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlmodel import Field
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[UUID], Base):
    __tablename__ = "user"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)

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
