from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, and_, or_
from app.models.cart import (
    Cart,
    CartItem,
    CartStatus,
    CartRead,
    CartItemRead,
    CartSummary,
)
from app.models.product import Product


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_cart(
        self, user_id: Optional[UUID] = None, session_id: Optional[str] = None
    ) -> Cart:
        """Get existing cart or create new one based on user/session identity."""
        if not user_id and not session_id:
            raise ValueError("Either user_id or session_id must be provided")

        # Try to find existing active cart
        query = (
            select(Cart)
            .where(
                and_(
                    Cart.status == CartStatus.ACTIVE,
                    or_(
                        Cart.user_id == user_id if user_id else False,
                        Cart.session_id == session_id if session_id else False,
                    ),
                )
            )
            .options(selectinload(Cart.items).selectinload(CartItem.product))
        )

        result = await self.session.execute(query)
        cart = result.scalar_one_or_none()

        if cart:
            # Update cart activity
            cart.updated_at = datetime.utcnow()
            await self.session.commit()
            return cart

        # Create new cart
        cart = Cart(
            id=uuid4(),
            user_id=user_id,
            session_id=session_id,
            status=CartStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=7) if session_id else None,
        )

        self.session.add(cart)
        await self.session.commit()
        await self.session.refresh(cart)

        return cart

    async def get_cart_by_id(self, cart_id: UUID) -> Optional[Cart]:
        """Get cart by ID with items and products loaded."""
        query = (
            select(Cart)
            .where(Cart.id == cart_id)
            .options(selectinload(Cart.items).selectinload(CartItem.product))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add_item(
        self, cart_id: UUID, product_id: int, quantity: int = 1
    ) -> CartItem:
        """Add item to cart or update quantity if exists."""
        # Validate product exists
        product_query = select(Product).where(Product.id == product_id)
        product_result = await self.session.execute(product_query)
        product = product_result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        # Check if item already exists in cart
        existing_item_query = select(CartItem).where(
            and_(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        )
        existing_result = await self.session.execute(existing_item_query)
        existing_item = existing_result.scalar_one_or_none()

        if existing_item:
            # Update existing item quantity
            existing_item.quantity += quantity
            existing_item.updated_at = datetime.utcnow()
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                id=uuid4(),
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.session.add(cart_item)

        # Update cart timestamp
        cart_query = select(Cart).where(Cart.id == cart_id)
        cart_result = await self.session.execute(cart_query)
        cart = cart_result.scalar_one_or_none()
        if cart:
            cart.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(cart_item, ["product"])

        return cart_item

    async def update_item_quantity(
        self, cart_id: UUID, item_id: UUID, quantity: int
    ) -> Optional[CartItem]:
        """Update cart item quantity."""
        query = select(CartItem).where(
            and_(CartItem.id == item_id, CartItem.cart_id == cart_id)
        )
        result = await self.session.execute(query)
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            return None

        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            await self.session.delete(cart_item)
            cart_item = None
        else:
            cart_item.quantity = quantity
            cart_item.updated_at = datetime.utcnow()

        # Update cart timestamp
        cart_query = select(Cart).where(Cart.id == cart_id)
        cart_result = await self.session.execute(cart_query)
        cart = cart_result.scalar_one_or_none()
        if cart:
            cart.updated_at = datetime.utcnow()

        await self.session.commit()

        if cart_item:
            await self.session.refresh(cart_item, ["product"])

        return cart_item

    async def remove_item(self, cart_id: UUID, item_id: UUID) -> bool:
        """Remove item from cart."""
        query = select(CartItem).where(
            and_(CartItem.id == item_id, CartItem.cart_id == cart_id)
        )
        result = await self.session.execute(query)
        cart_item = result.scalar_one_or_none()

        if not cart_item:
            return False

        await self.session.delete(cart_item)

        # Update cart timestamp
        cart_query = select(Cart).where(Cart.id == cart_id)
        cart_result = await self.session.execute(cart_query)
        cart = cart_result.scalar_one_or_none()
        if cart:
            cart.updated_at = datetime.utcnow()

        await self.session.commit()
        return True

    async def clear_cart(self, cart_id: UUID) -> bool:
        """Remove all items from cart."""
        # Delete all cart items
        delete_query = delete(CartItem).where(CartItem.cart_id == cart_id)
        await self.session.execute(delete_query)

        # Update cart timestamp
        cart_query = select(Cart).where(Cart.id == cart_id)
        cart_result = await self.session.execute(cart_query)
        cart = cart_result.scalar_one_or_none()

        if not cart:
            return False

        cart.updated_at = datetime.utcnow()
        await self.session.commit()
        return True

    async def calculate_cart_summary(self, cart: Cart) -> CartSummary:
        """Calculate cart totals and summary."""
        total_items = len(cart.items)
        total_quantity = sum(item.quantity for item in cart.items)
        subtotal = sum(item.quantity * item.unit_price for item in cart.items)

        return CartSummary(
            total_items=total_items,
            total_quantity=total_quantity,
            subtotal=round(subtotal, 2),
        )

    async def get_cart_read_model(self, cart: Cart) -> CartRead:
        """Convert cart to read model with calculated summary."""
        summary = await self.calculate_cart_summary(cart)

        cart_items = []
        for item in cart.items:
            cart_item_read = CartItemRead(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=round(item.quantity * item.unit_price, 2),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            cart_items.append(cart_item_read)

        return CartRead(
            id=cart.id,
            user_id=cart.user_id,
            session_id=cart.session_id,
            status=cart.status,
            items=cart_items,
            summary=summary,
            created_at=cart.created_at,
            updated_at=cart.updated_at,
            expires_at=cart.expires_at,
        )

    async def merge_carts(self, source_cart_id: UUID, target_cart_id: UUID) -> Cart:
        """Merge source cart items into target cart."""
        # Get both carts
        source_cart = await self.get_cart_by_id(source_cart_id)
        target_cart = await self.get_cart_by_id(target_cart_id)

        if not source_cart or not target_cart:
            raise ValueError("Source or target cart not found")

        # Merge items from source to target
        for source_item in source_cart.items:
            # Check if target cart already has this product
            existing_target_item = None
            for target_item in target_cart.items:
                if target_item.product_id == source_item.product_id:
                    existing_target_item = target_item
                    break

            if existing_target_item:
                # Update quantity in existing item
                existing_target_item.quantity += source_item.quantity
                existing_target_item.updated_at = datetime.utcnow()
            else:
                # Move item to target cart
                source_item.cart_id = target_cart_id
                source_item.updated_at = datetime.utcnow()

        # Mark source cart as abandoned
        source_cart.status = CartStatus.ABANDONED
        source_cart.updated_at = datetime.utcnow()

        # Update target cart
        target_cart.updated_at = datetime.utcnow()

        await self.session.commit()

        # Refresh target cart with updated items
        await self.session.refresh(target_cart)
        # Re-fetch to ensure relationships are loaded and non-None
        merged = await self.get_cart_by_id(target_cart_id)
        if merged is None:
            raise ValueError("Target cart not found after merge")
        return merged

    async def cleanup_expired_carts(self) -> int:
        """Clean up expired guest carts. Returns number of carts cleaned up."""
        now = datetime.utcnow()

        # Find expired carts
        query = select(Cart).where(
            and_(
                Cart.expires_at.is_not(None),
                Cart.expires_at < now,
                Cart.status == CartStatus.ACTIVE,
            )
        )
        result = await self.session.execute(query)
        expired_carts = result.scalars().all()

        # Mark as expired
        count = 0
        for cart in expired_carts:
            cart.status = CartStatus.EXPIRED
            cart.updated_at = now
            count += 1

        await self.session.commit()
        return count
