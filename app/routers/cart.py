from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.cart import (
    get_cart_service,
    get_current_cart,
    get_session_id,
    get_cart_resolution_service,
)
from app.services.cart_service import CartService
from app.models.cart import (
    Cart,
    CartRead,
    CartItemCreate,
    CartItemUpdate,
    CartItemRead,
    CartSummary,
    BulkCartUpdate,
    CartValidationResult,
)
from app.models.user import User
from app.routers.profile import current_active_user


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartRead)
async def get_cart(
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Get current user's cart with all items."""
    return await cart_service.get_cart_read_model(current_cart)


@router.post("/items", response_model=CartItemRead)
async def add_item_to_cart(
    item: CartItemCreate,
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Add item to cart or update quantity if item already exists."""
    try:
        cart_item = await cart_service.add_item(
            cart_id=current_cart.id, product_id=item.product_id, quantity=item.quantity
        )

        return CartItemRead(
            id=cart_item.id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            total_price=round(cart_item.quantity * cart_item.unit_price, 2),
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to add item to cart")


@router.put("/items/{item_id}", response_model=Optional[CartItemRead])
async def update_cart_item(
    item_id: UUID,
    item_update: CartItemUpdate,
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Update cart item quantity."""
    try:
        cart_item = await cart_service.update_item_quantity(
            cart_id=current_cart.id, item_id=item_id, quantity=item_update.quantity
        )

        if not cart_item:
            # Item was removed due to quantity <= 0
            return None

        return CartItemRead(
            id=cart_item.id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            total_price=round(cart_item.quantity * cart_item.unit_price, 2),
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update cart item")


@router.delete("/items/{item_id}")
async def remove_cart_item(
    item_id: UUID,
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Remove item from cart."""
    try:
        success = await cart_service.remove_item(
            cart_id=current_cart.id, item_id=item_id
        )

        if not success:
            raise HTTPException(status_code=404, detail="Cart item not found")

        return {"message": "Item removed from cart"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to remove cart item")


@router.delete("")
async def clear_cart(
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Remove all items from cart."""
    try:
        success = await cart_service.clear_cart(current_cart.id)

        if not success:
            raise HTTPException(status_code=404, detail="Cart not found")

        return {"message": "Cart cleared successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to clear cart")


@router.get("/summary", response_model=CartSummary)
async def get_cart_summary(
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Get cart summary with totals and item count."""
    try:
        return await cart_service.calculate_cart_summary(current_cart)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to calculate cart summary")


@router.put("/bulk", response_model=CartRead)
async def bulk_update_cart(
    bulk_update: BulkCartUpdate,
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
):
    """Bulk update multiple cart items."""
    try:
        # Update each item
        for item_data in bulk_update.items:
            item_id = UUID(item_data["id"])
            quantity = item_data["quantity"]

            await cart_service.update_item_quantity(
                cart_id=current_cart.id, item_id=item_id, quantity=quantity
            )

        # Return updated cart
        updated_cart = await cart_service.get_cart_by_id(current_cart.id)
        if updated_cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")
        return await cart_service.get_cart_read_model(updated_cart)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to bulk update cart")


@router.post("/merge")
async def merge_session_cart(
    current_user: User = Depends(current_active_user),
    cart_service: CartService = Depends(get_cart_service),
    session_id: Optional[str] = Depends(get_session_id),
):
    """
    Merge session cart with user cart when user logs in.
    This endpoint is typically called after authentication.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    if not session_id:
        return {"message": "No session cart to merge"}

    try:
        # Get user cart
        user_cart = await cart_service.get_or_create_cart(user_id=current_user.id)

        # Get session cart
        session_cart = await cart_service.get_or_create_cart(session_id=session_id)

        if user_cart.id == session_cart.id:
            return {"message": "Carts are already the same"}

        # Merge session cart into user cart
        merged_cart = await cart_service.merge_carts(
            source_cart_id=session_cart.id, target_cart_id=user_cart.id
        )

        return {
            "message": "Session cart merged successfully",
            "cart_id": str(merged_cart.id),
            "items_merged": len(session_cart.items),
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to merge carts")


# Admin/maintenance endpoints (could be restricted to admin users)
@router.post("/cleanup")
async def cleanup_expired_carts(
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(current_active_user),  # Require auth for cleanup
):
    """Clean up expired guest carts (admin endpoint)."""
    try:
        cleaned_count = await cart_service.cleanup_expired_carts()
        return {
            "message": f"Cleaned up {cleaned_count} expired carts",
            "count": cleaned_count,
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to cleanup expired carts")


# Cart Resolution and Validation Endpoints


@router.post("/validate", response_model=CartValidationResult)
async def validate_cart(
    current_cart: Cart = Depends(get_current_cart),
    resolution_service=Depends(get_cart_resolution_service),
):
    """
    Validate cart items, check for price changes, and verify availability.
    Returns validation result with errors, warnings, and updated items.
    """
    try:
        validation_result = await resolution_service.resolve_and_validate_cart(
            current_cart.id
        )
        return validation_result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to validate cart: {str(e)}"
        )


@router.post("/optimize")
async def optimize_cart(
    current_cart: Cart = Depends(get_current_cart),
    resolution_service=Depends(get_cart_resolution_service),
):
    """
    Optimize cart by removing invalid items and fixing quantity constraints.
    """
    try:
        changes_made, messages = await resolution_service.optimize_cart(current_cart.id)

        return {
            "optimized": changes_made,
            "messages": messages,
            "cart_id": str(current_cart.id),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to optimize cart: {str(e)}"
        )


@router.get("/health", response_model=dict)
async def get_cart_health(
    current_cart: Cart = Depends(get_current_cart),
    resolution_service=Depends(get_cart_resolution_service),
):
    """
    Get comprehensive health report for the current cart.
    """
    try:
        health_report = await resolution_service.get_cart_health_report(current_cart.id)
        return health_report
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get cart health report: {str(e)}"
        )


@router.post("/resolve-conflicts")
async def resolve_cart_conflicts(
    target_cart_id: UUID,
    current_cart: Cart = Depends(get_current_cart),
    cart_service: CartService = Depends(get_cart_service),
    resolution_service=Depends(get_cart_resolution_service),
    current_user: User = Depends(current_active_user),
):
    """
    Manually resolve conflicts between current cart and specified target cart.
    Typically used for advanced cart management scenarios.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        # Get target cart
        target_cart = await cart_service.get_cart_by_id(target_cart_id)
        if not target_cart:
            raise HTTPException(status_code=404, detail="Target cart not found")

        # Verify user owns target cart
        if target_cart.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied to target cart")

        resolved_cart, messages = await resolution_service.resolve_cart_conflicts(
            user_cart=target_cart, session_cart=current_cart
        )

        return {
            "resolved_cart_id": str(resolved_cart.id),
            "resolution_messages": messages,
            "items_count": len(resolved_cart.items),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to resolve cart conflicts: {str(e)}"
        )


# Admin endpoint for cleaning up abandoned carts
@router.post("/admin/cleanup-abandoned")
async def cleanup_abandoned_carts(
    days_old: int = 30,
    current_user: User = Depends(current_active_user),
    resolution_service=Depends(get_cart_resolution_service),
):
    """
    Clean up abandoned carts older than specified days (admin endpoint).
    """
    try:
        cleaned_count = await resolution_service.cleanup_abandoned_carts(days_old)

        return {
            "message": f"Cleaned up {cleaned_count} abandoned carts older than {days_old} days",
            "count": cleaned_count,
            "days_old": days_old,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to cleanup abandoned carts: {str(e)}"
        )
