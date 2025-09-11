# Shopping Cart System Implementation Plan

## Overview
This document outlines the implementation plan for a comprehensive shopping cart system with full cart management and session handling for the PyShop API.

## Current Codebase Analysis
- **Framework**: FastAPI 0.115 with SQLModel/SQLAlchemy async ORM
- **Database**: PostgreSQL with asyncpg driver
- **Authentication**: FastAPI-Users with JWT (UUID-based users)
- **Existing Models**: User (UUID primary key), Product (integer ID with name/price)

## 1. Database Schema Design

### Core Cart Models

#### Cart Table
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to User, nullable for guest carts)
- session_id: VARCHAR(255) (For guest cart session tracking)
- status: ENUM('active', 'abandoned', 'converted', 'expired')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- expires_at: TIMESTAMP (for guest cart cleanup)
```

#### CartItem Table
```sql
- id: UUID (Primary Key)
- cart_id: UUID (Foreign Key to Cart)
- product_id: INTEGER (Foreign Key to Product)
- quantity: INTEGER (min 1, max configurable)
- unit_price: DECIMAL(10,2) (snapshot price at add time)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Constraints & Indexes
- Unique constraint: (cart_id, product_id) - one product per cart
- Index on user_id for authenticated cart lookup
- Index on session_id for guest cart lookup
- Index on expires_at for cleanup operations

## 2. Session Handling Strategy

### Authenticated Users
- **Primary**: Link carts to user_id via JWT token
- **Fallback**: Session-based cart for logged-out state
- **Merge Logic**: When user logs in, merge session cart with user cart

### Guest Users
- **Session ID Generation**: Secure random UUID stored in HTTP-only cookie
- **Cookie Configuration**: 
  - `SameSite=Lax`
  - `HttpOnly=True`
  - `Secure=True` (production)
  - TTL: 7 days (configurable)
- **Cart Expiry**: Guest carts expire after 7 days of inactivity

### Session Migration
```python
# When user logs in with existing session cart:
1. Check for existing user cart
2. If user cart exists: merge session cart items
3. If no user cart: convert session cart to user cart
4. Clear session cart data
5. Update cart ownership
```

## 3. API Design

### Core Endpoints

#### Cart Management
```
GET    /cart                    # Get current user's cart
POST   /cart/items             # Add item to cart
PUT    /cart/items/{item_id}   # Update item quantity
DELETE /cart/items/{item_id}   # Remove item from cart
DELETE /cart                   # Clear entire cart
POST   /cart/merge             # Merge session cart (auth users only)
```

#### Cart Operations
```
GET    /cart/summary           # Get cart totals and item count
POST   /cart/validate          # Validate cart items (price/availability)
PUT    /cart/bulk              # Bulk update cart items
POST   /cart/save-for-later    # Save items for later (future feature)
```

### Request/Response Models

#### CartResponse
```python
{
    "id": "uuid",
    "user_id": "uuid|null",
    "session_id": "string|null", 
    "items": [CartItem],
    "total_items": int,
    "subtotal": float,
    "status": "active|abandoned|converted|expired",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

#### CartItem
```python
{
    "id": "uuid",
    "product_id": int,
    "product_name": "string",
    "quantity": int,
    "unit_price": float,
    "total_price": float,
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## 4. Implementation Architecture

### Model Structure
```
app/models/cart.py              # SQLModel cart and cart_item tables + schemas
app/services/cart_service.py    # Business logic for cart operations
app/routers/cart.py            # FastAPI route handlers
app/dependencies/cart.py       # Cart dependency injection
```

### Service Layer Design
```python
class CartService:
    async def get_or_create_cart() -> Cart
    async def add_item() -> CartItem
    async def update_item_quantity() -> CartItem
    async def remove_item() -> bool
    async def clear_cart() -> bool
    async def merge_carts() -> Cart
    async def calculate_totals() -> CartSummary
    async def validate_cart() -> ValidationResult
```

### Dependencies
```python
async def get_current_cart(
    current_user: User | None,
    session_id: str | None = Cookie(None)
) -> Cart:
    # Returns cart based on authentication state
```

## 5. Session Management Implementation

### Cookie Handling
- Custom middleware for session ID generation/validation
- Automatic cookie renewal on cart activity
- Secure cookie attributes based on environment

### Cart Resolution Logic
```python
def resolve_cart_identity():
    if user_authenticated:
        return {"user_id": user.id}
    elif session_cookie_exists:
        return {"session_id": session_id}
    else:
        return {"session_id": generate_new_session()}
```

## 6. Data Validation & Business Rules

### Quantity Management
- Min quantity: 1
- Max quantity per item: 99 (configurable)
- Max total items in cart: 100 (configurable)

### Price Handling
- Store unit_price snapshot when item added
- Validate against current product price on checkout
- Handle price changes gracefully

### Inventory Integration
- Real-time availability checks (future enhancement)
- Reserve items during checkout process
- Handle out-of-stock scenarios

## 7. Error Handling

### Common Scenarios
- Product not found: 404 with clear message
- Invalid quantity: 400 with validation details
- Cart not found: Auto-create new cart
- Duplicate items: Update existing item quantity
- Expired session: Clear cart and create new session

### Error Response Format
```python
{
    "error": "INVALID_QUANTITY",
    "message": "Quantity must be between 1 and 99",
    "field": "quantity",
    "code": "CART_001"
}
```

## 8. Performance Considerations

### Database Optimization
- Use SELECT FOR UPDATE on cart modifications
- Bulk operations for multiple item updates
- Efficient joins for cart + items + products
- Connection pooling for high concurrency

### Caching Strategy
- Redis cache for frequent cart lookups (future)
- Cache cart totals and item counts
- Invalidate cache on cart modifications

### Cleanup Jobs
- Background task for expired guest cart cleanup
- Archive old abandoned carts
- Metrics collection for cart conversion rates

## 9. Security Considerations

### Session Security
- Cryptographically secure session ID generation
- Session ID rotation on authentication changes
- Protection against session fixation attacks

### Data Protection
- Validate all input parameters
- Sanitize product quantities and IDs
- Rate limiting on cart modification endpoints
- CORS configuration for frontend integration

### Authentication Integration
- Respect existing FastAPI-Users auth flow
- Handle both authenticated and anonymous states
- Secure cart ownership transfer

## 10. Testing Strategy

### Unit Tests
- Cart service methods with mock dependencies
- Model validation and constraints
- Session handling logic
- Price calculation accuracy

### Integration Tests
- Full API endpoint testing
- Database transaction integrity
- Authentication flow integration
- Session-to-user cart migration

### Test Scenarios
```python
# Critical test cases:
- Add items to guest cart, login, verify merge
- Concurrent cart modifications
- Cart expiration and cleanup
- Price change handling
- Quantity boundary validation
- Session hijacking prevention
```

## 11. Migration Strategy

### Database Changes
```sql
-- Create cart and cart_item tables
-- Add foreign key constraints
-- Create necessary indexes
-- Set up cleanup procedures
```

### Deployment Steps
1. Run database migrations
2. Deploy cart models and services
3. Add cart API endpoints
4. Update frontend integration
5. Monitor cart conversion metrics

### Rollback Plan
- Database migration rollback scripts
- Feature flag for cart functionality
- Graceful degradation to product-only flow

## 12. Future Enhancements

### Advanced Features
- Save for later functionality
- Cart sharing via unique URLs
- Abandoned cart recovery emails
- Cart analytics and insights
- Multi-currency support
- Promotional code integration

### Performance Optimizations
- Redis caching layer
- Database query optimization
- CDN for static cart assets
- Real-time cart synchronization

### Integration Points
- Payment gateway preparation
- Inventory management system
- Customer notification system
- Analytics and reporting tools

## 13. Configuration

### Environment Variables
```python
# Cart-specific settings
CART_SESSION_TTL_DAYS = 7
CART_MAX_ITEMS = 100
CART_MAX_QUANTITY_PER_ITEM = 99
CART_CLEANUP_INTERVAL_HOURS = 24
CART_COOKIE_NAME = "pyshop_cart_session"
CART_COOKIE_SECURE = True  # Production only
```

### Feature Flags
- `ENABLE_GUEST_CARTS`
- `ENABLE_CART_MERGE`
- `ENABLE_CART_VALIDATION`
- `ENABLE_CART_ANALYTICS`

## Implementation Timeline

### Phase 1: Core Models (Week 1)
- Create Cart and CartItem models
- Database migrations
- Basic CRUD operations

### Phase 2: Session Handling (Week 2)
- Session middleware implementation
- Cookie management
- Cart resolution logic

### Phase 3: API Implementation (Week 3)
- Cart router endpoints
- Service layer implementation
- Input validation and error handling

### Phase 4: Testing & Integration (Week 4)
- Comprehensive testing suite
- Frontend integration
- Performance optimization
- Documentation updates

This plan provides a solid foundation for implementing a robust shopping cart system that scales with the existing PyShop API architecture while maintaining security and performance standards.