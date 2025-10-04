"""Playwright configuration for E2E tests."""

import os
from typing import Any

# Base URL for the API (can be overridden via environment variable)
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Browser configuration
BROWSER_CONFIG: dict[str, Any] = {
    "headless": True,
    "slow_mo": 0,  # Slow down operations by N milliseconds (useful for debugging)
}

# Test configuration
TEST_CONFIG = {
    "base_url": BASE_URL,
    "timeout": 30000,  # Default timeout in milliseconds
    "screenshot_on_failure": True,
    "video_on_failure": True,
}

# Browser context options
CONTEXT_OPTIONS = {
    "viewport": {"width": 1280, "height": 720},
    "ignore_https_errors": True,
}


def get_browser_config() -> dict[str, Any]:
    """Get browser configuration."""
    return BROWSER_CONFIG


def get_test_config() -> dict[str, Any]:
    """Get test configuration."""
    return TEST_CONFIG


def get_context_options() -> dict[str, Any]:
    """Get browser context options."""
    return CONTEXT_OPTIONS
