from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlmodel import Field
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.user import Base

# Import Product model directly
from app.models.product import Product


class CartStatus(str, Enum):
    ACTIVE = "active"
    ABANDONED = "abandoned"
    CONVERTED = "converted"
    EXPIRED = "expired"


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    user_id: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, index=True
    )
    status: Mapped[CartStatus] = mapped_column(
        String(20), default=CartStatus.ACTIVE, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, index=True
    )

    # Relationships
    items: Mapped[List["CartItem"]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan", lazy="selectin"
    )
    # Note: User relationship handled by foreign key

    __table_args__ = (
        Index("idx_cart_user_active", "user_id", "status"),
        Index("idx_cart_session_active", "session_id", "status"),
        Index("idx_cart_expires_at", "expires_at"),
    )


class CartItem(Base):
    __tablename__ = "cart_item"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    cart_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("cart.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship(Product, lazy="selectin")

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
        Index("idx_cartitem_cart_id", "cart_id"),
    )


# Pydantic Models for API


class CartItemBase(BaseModel):
    product_id: int = Field(..., gt=0, description="Product ID must be positive")
    quantity: int = Field(
        ..., ge=1, le=99, description="Quantity must be between 1 and 99"
    )

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        if v > 99:
            raise ValueError("Quantity cannot exceed 99")
        return v


class CartItemCreate(CartItemBase):
    model_config = ConfigDict(from_attributes=True)


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        ..., ge=1, le=99, description="Quantity must be between 1 and 99"
    )
    model_config = ConfigDict(from_attributes=True)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        if v > 99:
            raise ValueError("Quantity cannot exceed 99")
        return v


class CartItemRead(BaseModel):
    id: UUID = Field(..., description="Cart item ID")
    product_id: int = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Item quantity")
    unit_price: float = Field(..., description="Price per unit when added to cart")
    total_price: float = Field(
        ..., description="Total price for this item (quantity * unit_price)"
    )
    created_at: datetime = Field(..., description="When item was added to cart")
    updated_at: datetime = Field(..., description="When item was last modified")
    model_config = ConfigDict(from_attributes=True)


class CartSummary(BaseModel):
    total_items: int = Field(..., description="Total number of items in cart")
    total_quantity: int = Field(..., description="Sum of all item quantities")
    subtotal: float = Field(..., description="Total price of all items")
    model_config = ConfigDict(from_attributes=True)


class CartRead(BaseModel):
    id: UUID = Field(..., description="Cart ID")
    user_id: Optional[UUID] = Field(None, description="User ID if authenticated cart")
    session_id: Optional[str] = Field(None, description="Session ID if guest cart")
    status: CartStatus = Field(..., description="Cart status")
    items: List[CartItemRead] = Field(default_factory=list, description="Items in cart")
    summary: CartSummary = Field(..., description="Cart totals and summary")
    created_at: datetime = Field(..., description="Cart creation timestamp")
    updated_at: datetime = Field(..., description="Cart last update timestamp")
    expires_at: Optional[datetime] = Field(
        None, description="Cart expiration time for guest carts"
    )
    model_config = ConfigDict(from_attributes=True)


class CartValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether cart is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    updated_items: List[CartItemRead] = Field(
        default_factory=list, description="Items with updated prices"
    )
    model_config = ConfigDict(from_attributes=True)


class BulkCartUpdate(BaseModel):
    items: List[dict] = Field(
        ..., description="List of item updates with id and quantity"
    )
    model_config = ConfigDict(from_attributes=True)

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[dict]) -> List[dict]:
        if len(v) == 0:
            raise ValueError("Items list cannot be empty")
        if len(v) > 100:
            raise ValueError("Cannot update more than 100 items at once")

        for item in v:
            if "id" not in item or "quantity" not in item:
                raise ValueError("Each item must have 'id' and 'quantity' fields")
            if (
                not isinstance(item["quantity"], int)
                or item["quantity"] < 1
                or item["quantity"] > 99
            ):
                raise ValueError("Quantity must be an integer between 1 and 99")

        return v
