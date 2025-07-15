from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False, unique=True)
    email: Optional[str] = Field(index=True, nullable=True)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)


class User(UserBase):
    """
    The table that lives in Postgres.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)


class UserCreate(BaseModel):
    """
    What the client sends when registering.
    """

    username: str
    password: str
    email: Optional[str] = None


class UserRead(UserBase):
    """
    What we return in our API.
    """

    id: UUID


class UserDB(UserRead):
    """
    Internal schema: what we load from the database.
    """

    hashed_password: str
