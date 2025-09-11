"""Add Cart and CartItem models for shopping cart system

Revision ID: 709691f8a05f
Revises: d591c567f6a0
Create Date: 2025-09-11 20:23:43.217646

"""

from typing import Sequence, Union

from alembic import op  # type: ignore[attr-defined]
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "709691f8a05f"
down_revision: Union[str, Sequence[str], None] = "d591c567f6a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create cart table
    op.create_table(
        "cart",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )

    # Create indexes for cart table
    op.create_index("idx_cart_user_active", "cart", ["user_id", "status"])
    op.create_index("idx_cart_session_active", "cart", ["session_id", "status"])
    op.create_index("idx_cart_expires_at", "cart", ["expires_at"])
    op.create_index(op.f("ix_cart_user_id"), "cart", ["user_id"])
    op.create_index(op.f("ix_cart_session_id"), "cart", ["session_id"])

    # Create cart_item table
    op.create_table(
        "cart_item",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cart_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["cart_id"], ["cart.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )

    # Create indexes for cart_item table
    op.create_index("idx_cartitem_cart_id", "cart_item", ["cart_id"])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop cart_item table and its indexes
    op.drop_index("idx_cartitem_cart_id", table_name="cart_item")
    op.drop_table("cart_item")

    # Drop cart table and its indexes
    op.drop_index(op.f("ix_cart_session_id"), table_name="cart")
    op.drop_index(op.f("ix_cart_user_id"), table_name="cart")
    op.drop_index("idx_cart_expires_at", table_name="cart")
    op.drop_index("idx_cart_session_active", table_name="cart")
    op.drop_index("idx_cart_user_active", table_name="cart")
    op.drop_table("cart")
