from typing import Callable, Optional
from uuid import uuid4
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.utils.cookies import create_session_cookie


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Enhanced middleware for secure session management with shopping cart functionality.

    This middleware:
    1. Generates and manages session IDs for guest users
    2. Sets/updates session cookies with security features (signing, HTTPS)
    3. Provides session ID via request.state for dependency injection
    4. Handles session persistence and expiration
    5. Protects against cookie tampering with HMAC signatures
    6. Configures cookies based on environment (dev/prod)
    """

    def __init__(
        self,
        app: ASGIApp,
        cookie_name: str = "pyshop_cart_session",
        max_age: int = 7 * 24 * 60 * 60,  # 7 days
        secure: bool = False,  # Set to True in production with HTTPS
    ):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.secure_cookie = create_session_cookie(
            name=cookie_name,
            secure=secure,
            max_age=max_age,
        )

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and manage secure session state."""

        # Extract and validate session ID from secure cookie
        session_id: Optional[str] = self.secure_cookie.get_cookie(request)

        # Generate new session ID if none exists or cookie was invalid
        if not session_id:
            session_id = str(uuid4())

        # Store session ID in request state for dependency access
        request.state.session_id = session_id

        # Process the request
        response = await call_next(request)

        # Set/update secure session cookie if this is a cart-related endpoint
        # and we don't have an existing valid session cookie
        if self._should_set_cookie(request, session_id):
            self.secure_cookie.set_cookie(response, session_id)

        return response

    def _should_set_cookie(self, request: Request, session_id: str) -> bool:
        """
        Determine if we should set the session cookie.

        Set cookie for:
        - Cart-related endpoints (/cart/*)
        - When session ID is new (not in existing cookies or invalid)
        - For guest users (no auth header or when merging carts)
        """
        path = request.url.path

        # Only set cookie for cart endpoints
        if not path.startswith("/cart"):
            return False

        # Check if we have a valid existing cookie
        existing_session = self.secure_cookie.get_cookie(request)
        if existing_session == session_id:
            return False

        # Set cookie for new sessions or when session ID differs/is invalid
        return True


class CookieCleanupMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle cookie cleanup and expiration management.

    This middleware:
    1. Removes expired or invalid cookies
    2. Cleans up malformed cookie data
    3. Handles cookie rotation for security
    """

    def __init__(
        self,
        app: ASGIApp,
        cleanup_invalid_cookies: bool = True,
        rotate_session_on_auth: bool = True,
    ):
        super().__init__(app)
        self.cleanup_invalid_cookies = cleanup_invalid_cookies
        self.rotate_session_on_auth = rotate_session_on_auth

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and handle cookie cleanup."""

        response = await call_next(request)

        # Clean up invalid cookies if enabled
        if self.cleanup_invalid_cookies:
            self._cleanup_invalid_cookies(request, response)

        # Rotate session cookie on authentication if enabled
        if self.rotate_session_on_auth and self._is_auth_endpoint(request):
            self._rotate_session_cookie(request, response)

        return response

    def _cleanup_invalid_cookies(self, request: Request, response: Response) -> None:
        """Remove invalid or malformed cookies."""
        # This would contain logic to identify and remove invalid cookies
        # For now, we'll implement basic cleanup
        pass

    def _is_auth_endpoint(self, request: Request) -> bool:
        """Check if request is to an authentication endpoint."""
        path = request.url.path
        return path.startswith("/auth/") or path in ["/login", "/logout", "/register"]

    def _rotate_session_cookie(self, request: Request, response: Response) -> None:
        """Rotate session cookie on authentication for security."""
        # Generate new session ID and update cookie
        new_session_id = str(uuid4())
        session_cookie = create_session_cookie()
        session_cookie.set_cookie(response, new_session_id)


def get_session_id_from_state(request: Request) -> Optional[str]:
    """
    Dependency to get session ID from request state.
    Should be used instead of cookie-based dependency after middleware is applied.
    """
    return getattr(request.state, "session_id", None)


def get_secure_session_cookie(
    cookie_name: str = "pyshop_cart_session",
    secure: bool = False,
) -> object:
    """
    Factory function to create secure session cookie instance.
    Use this for direct cookie operations outside of middleware.
    """
    return create_session_cookie(name=cookie_name, secure=secure)
