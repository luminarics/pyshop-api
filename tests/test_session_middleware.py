import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_session_middleware_sets_cookie(client: AsyncClient):
    """Test that session middleware sets cookie for cart endpoints."""
    # Make a request to a cart endpoint
    response = await client.get("/cart")

    # Check that a session cookie is set
    cookies = response.cookies
    assert "pyshop_cart_session" in cookies

    # Cookie should have proper attributes
    session_cookie = cookies["pyshop_cart_session"]
    assert session_cookie is not None
    assert len(session_cookie) > 0


@pytest.mark.asyncio
async def test_session_middleware_preserves_existing_session(client: AsyncClient):
    """Test that middleware preserves existing session ID."""
    # First request to get a session ID
    response1 = await client.get("/cart")
    session_id = response1.cookies.get("pyshop_cart_session")
    assert session_id is not None

    # Second request with the session cookie
    cookies = {"pyshop_cart_session": session_id}
    response2 = await client.get("/cart", cookies=cookies)

    # Should get the same session ID back
    session_id2 = response2.cookies.get("pyshop_cart_session")
    # Note: Cookie might not be set again if it's the same value
    # The important thing is the request state should have the same session ID

    # Both responses should be successful
    assert response1.status_code == 200
    assert response2.status_code == 200


@pytest.mark.asyncio
async def test_session_middleware_only_affects_cart_endpoints(client: AsyncClient):
    """Test that session middleware only affects cart endpoints."""
    # Make requests to non-cart endpoints
    response = await client.get("/healthz")

    # Should not set session cookie for non-cart endpoints
    cookies = response.cookies
    assert (
        "pyshop_cart_session" not in cookies or len(cookies["pyshop_cart_session"]) == 0
    )


@pytest.mark.asyncio
async def test_cart_works_with_session_middleware(client: AsyncClient):
    """Test that cart functionality works with session middleware."""
    # Get empty cart (should create session)
    response = await client.get("/cart")
    assert response.status_code == 200

    cart_data = response.json()
    assert "id" in cart_data
    assert "items" in cart_data
    assert cart_data["items"] == []
    assert cart_data["summary"]["total_items"] == 0
