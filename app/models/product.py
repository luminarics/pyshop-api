from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):  # type: ignore[call-arg]
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    created_at: datetime = Field(default_factory=datetime.now)
