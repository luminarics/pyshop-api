"""Pytest fixtures for E2E tests."""

import os
import time
from collections.abc import Generator
from typing import Any

import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright

# Disable asyncio mode for E2E tests to avoid conflicts with Playwright's sync API
pytest_plugins = ("pytest_playwright",)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return base URL for the API."""
    return os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def api_context(
    playwright: Playwright, base_url: str
) -> Generator[APIRequestContext, None, None]:
    """Create API request context for testing."""
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()


@pytest.fixture
def auth_headers(api_context: APIRequestContext, base_url: str) -> dict[str, str]:
    """Create authenticated user and return auth headers."""
    # Create unique user for this test
    timestamp = int(time.time() * 1000)
    test_user = {
        "email": f"test_{timestamp}@example.com",
        "username": f"testuser_{timestamp}",
        "password": "TestPassword123!",
    }

    # Register user
    response = api_context.post(
        f"{base_url}/auth/register",
        data={
            "email": test_user["email"],
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )
    assert response.ok, f"Registration failed: {response.text()}"

    # Login to get token
    response = api_context.post(
        f"{base_url}/auth/jwt/login",
        form={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    assert response.ok, f"Login failed: {response.text()}"

    token_data = response.json()
    return {"Authorization": f"Bearer {token_data['access_token']}"}


@pytest.fixture
def page_with_auth(page: Page, auth_headers: dict[str, str]) -> Page:
    """Return page with authentication headers set."""
    page.set_extra_http_headers(auth_headers)
    return page
