from typing import Optional
from uuid import UUID, uuid4
from fastapi_users import schemas
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class User(SQLModel, SQLAlchemyBaseUserTable[UUID], table=True):  # type: ignore[call-arg]
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)


class UserRead(schemas.BaseUser[UUID]):
    username: str
    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
