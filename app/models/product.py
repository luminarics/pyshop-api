from datetime import datetime
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.user import Base
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product name between 1-100 characters",
    )
    price: float = Field(
        ...,
        gt=0,
        le=999999.99,
        description="Product price must be positive and <= 999999.99",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Product name cannot be empty or whitespace only")
        if any(char in v for char in "<>{}[]"):
            raise ValueError("Product name cannot contain HTML-like characters")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v != v:  # Check for NaN
            raise ValueError("Price cannot be NaN")
        if v == float("inf") or v == float("-inf"):
            raise ValueError("Price cannot be infinite")
        # Round to 2 decimal places for currency
        return round(v, 2)


class ProductCreate(ProductBase):
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Product name between 1-100 characters",
    )
    price: float | None = Field(
        None,
        gt=0,
        le=999999.99,
        description="Product price must be positive and <= 999999.99",
    )
    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Product name cannot be empty or whitespace only")
            if any(char in v for char in "<>{}[]"):
                raise ValueError("Product name cannot contain HTML-like characters")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float | None) -> float | None:
        if v is not None:
            if v != v:  # Check for NaN
                raise ValueError("Price cannot be NaN")
            if v == float("inf") or v == float("-inf"):
                raise ValueError("Price cannot be infinite")
            # Round to 2 decimal places for currency
            v = round(v, 2)
        return v


class ProductRead(ProductBase):
    id: int = Field(..., gt=0, description="Product ID must be positive")
    created_at: datetime = Field(..., description="Product creation timestamp")
    model_config = ConfigDict(from_attributes=True)
