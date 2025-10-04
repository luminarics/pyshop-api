"""E2E tests for API flows."""

import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.e2e
class TestAuthFlow:
    """Test authentication flow."""

    def test_user_registration_and_login(
        self, api_context: APIRequestContext, base_url: str
    ):
        """Test user can register and login."""
        import time

        timestamp = int(time.time() * 1000)
        user_data = {
            "email": f"e2e_test_{timestamp}@example.com",
            "username": f"e2e_user_{timestamp}",
            "password": "SecurePassword123!",
        }

        # Register user
        response = api_context.post(
            f"{base_url}/auth/register",
            data=user_data,
        )
        assert response.ok, f"Registration failed: {response.text()}"
        user = response.json()
        assert user["email"] == user_data["email"]
        assert user["username"] == user_data["username"]

        # Login with email
        response = api_context.post(
            f"{base_url}/auth/jwt/login",
            form={
                "username": user_data["email"],
                "password": user_data["password"],
            },
        )
        assert response.ok, f"Login failed: {response.text()}"
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

    def test_protected_endpoint_requires_auth(
        self, api_context: APIRequestContext, base_url: str
    ):
        """Test protected endpoints require authentication."""
        response = api_context.get(f"{base_url}/products/")
        assert response.status == 401


@pytest.mark.e2e
class TestProductFlow:
    """Test product CRUD flow."""

    def test_create_and_list_products(
        self,
        api_context: APIRequestContext,
        base_url: str,
        auth_headers: dict[str, str],
    ):
        """Test creating and listing products."""
        product_data = {
            "name": "Test Product E2E",
            "price": 99.99,
        }

        # Create product
        response = api_context.post(
            f"{base_url}/products/",
            headers=auth_headers,
            data=product_data,
        )
        assert response.ok, f"Product creation failed: {response.text()}"
        created_product = response.json()
        assert created_product["name"] == product_data["name"]
        assert created_product["price"] == product_data["price"]
        assert "id" in created_product

        # List products
        response = api_context.get(
            f"{base_url}/products/",
            headers=auth_headers,
        )
        assert response.ok
        products = response.json()
        assert isinstance(products, list)
        assert len(products) > 0

    def test_get_product_by_id(
        self,
        api_context: APIRequestContext,
        base_url: str,
        auth_headers: dict[str, str],
    ):
        """Test retrieving a product by ID."""
        # Create product first
        product_data = {"name": "Get Test Product", "price": 49.99}
        response = api_context.post(
            f"{base_url}/products/",
            headers=auth_headers,
            data=product_data,
        )
        assert response.ok
        created_product = response.json()
        product_id = created_product["id"]

        # Get product by ID
        response = api_context.get(
            f"{base_url}/products/{product_id}",
            headers=auth_headers,
        )
        assert response.ok
        product = response.json()
        assert product["id"] == product_id
        assert product["name"] == product_data["name"]

    def test_update_product(
        self,
        api_context: APIRequestContext,
        base_url: str,
        auth_headers: dict[str, str],
    ):
        """Test updating a product."""
        # Create product
        product_data = {"name": "Original Name", "price": 29.99}
        response = api_context.post(
            f"{base_url}/products/",
            headers=auth_headers,
            data=product_data,
        )
        assert response.ok
        product_id = response.json()["id"]

        # Update product
        updated_data = {"name": "Updated Name", "price": 39.99}
        response = api_context.patch(
            f"{base_url}/products/{product_id}",
            headers=auth_headers,
            data=updated_data,
        )
        assert response.ok
        updated_product = response.json()
        assert updated_product["name"] == updated_data["name"]
        assert updated_product["price"] == updated_data["price"]

    def test_delete_product(
        self,
        api_context: APIRequestContext,
        base_url: str,
        auth_headers: dict[str, str],
    ):
        """Test deleting a product."""
        # Create product
        product_data = {"name": "To Be Deleted", "price": 19.99}
        response = api_context.post(
            f"{base_url}/products/",
            headers=auth_headers,
            data=product_data,
        )
        assert response.ok
        product_id = response.json()["id"]

        # Delete product
        response = api_context.delete(
            f"{base_url}/products/{product_id}",
            headers=auth_headers,
        )
        assert response.ok

        # Verify product is deleted
        response = api_context.get(
            f"{base_url}/products/{product_id}",
            headers=auth_headers,
        )
        assert response.status == 404


@pytest.mark.e2e
class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check(self, api_context: APIRequestContext, base_url: str):
        """Test health check endpoint is accessible."""
        response = api_context.get(f"{base_url}/healthz")
        assert response.ok
        health_data = response.json()
        assert health_data["status"] == "healthy"
