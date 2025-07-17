from datetime import datetime
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.user import Base
from pydantic import BaseModel, ConfigDict


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(ProductBase):
    model_config = ConfigDict(from_attributes=True)


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
