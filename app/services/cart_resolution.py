from datetime import datetime
from typing import List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cart import (
    Cart,
    CartStatus,
    CartValidationResult,
)
from app.models.product import Product
from app.services.cart_service import CartService


class CartResolutionService:
    """
    Handles complex cart resolution logic including validation,
    conflict resolution, price checks, and optimization.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.cart_service = CartService(session)

    async def resolve_and_validate_cart(self, cart_id: UUID) -> CartValidationResult:
        """
        Comprehensive cart resolution with validation, price checks,
        and conflict resolution.
        """
        cart = await self.cart_service.get_cart_by_id(cart_id)
        if not cart:
            return CartValidationResult(
                is_valid=False,
                errors=["Cart not found"],
                warnings=[],
                updated_items=[],
            )

        errors = []
        warnings = []
        updated_items = []

        # 1. Validate cart items exist and are available
        for item in cart.items:
            # Check if product still exists
            product_query = select(Product).where(Product.id == item.product_id)
            product_result = await self.session.execute(product_query)
            product = product_result.scalar_one_or_none()

            if not product:
                errors.append(f"Product {item.product_id} is no longer available")
                continue

            # 2. Check price changes
            if abs(item.unit_price - product.price) > 0.01:  # Price changed
                warnings.append(
                    f"Price for '{product.name}' has changed from "
                    f"${item.unit_price:.2f} to ${product.price:.2f}"
                )
                # Update item with new price
                item.unit_price = product.price
                item.updated_at = datetime.utcnow()
                updated_items.append(item)

            # 3. Validate quantity constraints
            if item.quantity < 1:
                errors.append(
                    f"Invalid quantity {item.quantity} for product {product.name}"
                )
            elif item.quantity > 99:
                warnings.append(
                    f"Quantity {item.quantity} for '{product.name}' exceeds maximum (99)"
                )
                item.quantity = 99
                item.updated_at = datetime.utcnow()
                updated_items.append(item)

        # 4. Check cart-level constraints
        total_items = len(cart.items)
        if total_items > 100:
            errors.append(f"Cart has {total_items} items, maximum allowed is 100")

        total_quantity = sum(item.quantity for item in cart.items)
        if total_quantity > 500:
            warnings.append(f"Total quantity {total_quantity} is very high")

        # 5. Check cart expiration for guest carts
        if cart.expires_at and cart.expires_at < datetime.utcnow():
            errors.append("Cart has expired")

        # 6. Save any updates
        if updated_items:
            await self.session.commit()
            # Refresh cart to get updated items
            await self.session.refresh(cart)

        # Convert updated items to read models
        updated_items_read = []
        for item in updated_items:
            await self.session.refresh(item, ["product"])
            from app.models.cart import CartItemRead

            item_read = CartItemRead(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=round(item.quantity * item.unit_price, 2),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            updated_items_read.append(item_read)

        is_valid = len(errors) == 0
        return CartValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            updated_items=updated_items_read,
        )

    async def resolve_cart_conflicts(
        self, user_cart: Cart, session_cart: Cart
    ) -> Tuple[Cart, List[str]]:
        """
        Resolve conflicts when merging user and session carts.
        Returns the resolved cart and list of resolution messages.
        """
        resolution_messages = []

        if not session_cart.items:
            resolution_messages.append("Session cart is empty, no conflicts to resolve")
            return user_cart, resolution_messages

        if not user_cart.items:
            resolution_messages.append(
                "User cart is empty, adopting all session cart items"
            )
            # Transfer all session items to user cart
            for item in session_cart.items:
                item.cart_id = user_cart.id
                item.updated_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(user_cart)
            return user_cart, resolution_messages

        # Handle conflicts for items that exist in both carts
        for session_item in session_cart.items:
            # Find matching item in user cart
            user_item = None
            for user_cart_item in user_cart.items:
                if user_cart_item.product_id == session_item.product_id:
                    user_item = user_cart_item
                    break

            if user_item:
                # Conflict: same product in both carts
                old_quantity = user_item.quantity
                new_quantity = user_item.quantity + session_item.quantity

                # Respect quantity limits
                if new_quantity > 99:
                    new_quantity = 99
                    resolution_messages.append(
                        f"Product {session_item.product_id}: Combined quantity "
                        f"({user_item.quantity} + {session_item.quantity}) exceeds maximum, "
                        f"capped at 99"
                    )
                else:
                    resolution_messages.append(
                        f"Product {session_item.product_id}: Merged quantities "
                        f"({old_quantity} + {session_item.quantity} = {new_quantity})"
                    )

                user_item.quantity = new_quantity
                user_item.updated_at = datetime.utcnow()

                # Use the most recent price
                if session_item.updated_at > user_item.updated_at:
                    if abs(user_item.unit_price - session_item.unit_price) > 0.01:
                        resolution_messages.append(
                            f"Product {session_item.product_id}: Using newer price "
                            f"${session_item.unit_price:.2f} from session cart"
                        )
                        user_item.unit_price = session_item.unit_price
            else:
                # No conflict: add session item to user cart
                session_item.cart_id = user_cart.id
                session_item.updated_at = datetime.utcnow()
                resolution_messages.append(
                    f"Added product {session_item.product_id} from session cart"
                )

        # Mark session cart as abandoned
        session_cart.status = CartStatus.ABANDONED
        session_cart.updated_at = datetime.utcnow()

        # Update user cart timestamp
        user_cart.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(user_cart)

        return user_cart, resolution_messages

    async def optimize_cart(self, cart_id: UUID) -> Tuple[bool, List[str]]:
        """
        Optimize cart by removing invalid items, consolidating duplicates,
        and applying business rules.
        """
        cart = await self.cart_service.get_cart_by_id(cart_id)
        if not cart:
            return False, ["Cart not found"]

        optimization_messages = []
        changes_made = False

        # Remove items with invalid products
        items_to_remove = []
        for item in cart.items:
            product_query = select(Product).where(Product.id == item.product_id)
            product_result = await self.session.execute(product_query)
            product = product_result.scalar_one_or_none()

            if not product:
                items_to_remove.append(item)
                optimization_messages.append(
                    f"Removed unavailable product {item.product_id}"
                )
                changes_made = True

        # Remove invalid items
        for item in items_to_remove:
            await self.session.delete(item)

        # Fix quantity constraints
        for item in cart.items:
            if item not in items_to_remove:
                if item.quantity < 1:
                    await self.session.delete(item)
                    optimization_messages.append(
                        f"Removed item with invalid quantity: {item.quantity}"
                    )
                    changes_made = True
                elif item.quantity > 99:
                    item.quantity = 99
                    item.updated_at = datetime.utcnow()
                    optimization_messages.append(
                        f"Reduced quantity for product {item.product_id} to maximum (99)"
                    )
                    changes_made = True

        # Update cart if changes were made
        if changes_made:
            cart.updated_at = datetime.utcnow()
            await self.session.commit()

        if not optimization_messages:
            optimization_messages.append("Cart is already optimized")

        return changes_made, optimization_messages

    async def check_cart_availability(self, cart_id: UUID) -> CartValidationResult:
        """
        Check if all items in cart are available and have current pricing.
        This is typically called before checkout.
        """
        validation_result = await self.resolve_and_validate_cart(cart_id)

        # Additional availability checks can be added here
        # For example, integration with inventory management system

        return validation_result

    async def cleanup_abandoned_carts(self, days_old: int = 30) -> int:
        """
        Clean up abandoned carts older than specified days.
        """
        cutoff_date = datetime.utcnow().timestamp() - (days_old * 24 * 60 * 60)
        cutoff_datetime = datetime.fromtimestamp(cutoff_date)

        # Find abandoned carts older than cutoff
        query = select(Cart).where(
            Cart.status == CartStatus.ABANDONED, Cart.updated_at < cutoff_datetime
        )
        result = await self.session.execute(query)
        abandoned_carts = result.scalars().all()

        # Delete old abandoned carts (cascade will handle cart items)
        count = 0
        for cart in abandoned_carts:
            await self.session.delete(cart)
            count += 1

        await self.session.commit()
        return count

    async def get_cart_health_report(self, cart_id: UUID) -> dict:
        """
        Generate a comprehensive health report for a cart.
        """
        cart = await self.cart_service.get_cart_by_id(cart_id)
        if not cart:
            return {"error": "Cart not found"}

        validation_result = await self.resolve_and_validate_cart(cart_id)

        # Calculate cart metrics
        total_items = len(cart.items)
        total_quantity = sum(item.quantity for item in cart.items)
        total_value = sum(item.quantity * item.unit_price for item in cart.items)

        # Calculate cart age
        cart_age_hours = (datetime.utcnow() - cart.created_at).total_seconds() / 3600

        return {
            "cart_id": str(cart_id),
            "status": cart.status.value,
            "is_valid": validation_result.is_valid,
            "error_count": len(validation_result.errors),
            "warning_count": len(validation_result.warnings),
            "total_items": total_items,
            "total_quantity": total_quantity,
            "total_value": round(total_value, 2),
            "cart_age_hours": round(cart_age_hours, 2),
            "expires_at": cart.expires_at.isoformat() if cart.expires_at else None,
            "last_updated": cart.updated_at.isoformat(),
        }
