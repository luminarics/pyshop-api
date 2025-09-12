from typing import Callable, Optional, Literal
from uuid import uuid4
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle session management for shopping cart functionality.

    This middleware:
    1. Generates and manages session IDs for guest users
    2. Sets/updates session cookies automatically
    3. Provides session ID via request.state for dependency injection
    4. Handles session persistence and expiration
    """

    def __init__(
        self,
        app: ASGIApp,
        cookie_name: str = "pyshop_cart_session",
        max_age: int = 7 * 24 * 60 * 60,  # 7 days
        httponly: bool = True,
        samesite: Literal["lax", "strict", "none"] = "lax",
        secure: bool = False,  # Set to True in production with HTTPS
        path: str = "/",
    ):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.max_age = max_age
        self.httponly = httponly
        self.samesite = samesite
        self.secure = secure
        self.path = path

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and manage session state."""

        # Extract session ID from cookie
        session_id: Optional[str] = request.cookies.get(self.cookie_name)

        # Generate new session ID if none exists
        if not session_id:
            session_id = str(uuid4())

        # Store session ID in request state for dependency access
        request.state.session_id = session_id

        # Process the request
        response = await call_next(request)

        # Set/update session cookie if this is a cart-related endpoint
        # and we don't have an existing valid session cookie
        if self._should_set_cookie(request, session_id):
            if isinstance(response, JSONResponse):
                response.set_cookie(
                    key=self.cookie_name,
                    value=session_id,
                    max_age=self.max_age,
                    httponly=self.httponly,
                    samesite=self.samesite,
                    secure=self.secure,
                    path=self.path,
                )
            else:
                # For non-JSON responses, we still set the cookie
                response.set_cookie(
                    key=self.cookie_name,
                    value=session_id,
                    max_age=self.max_age,
                    httponly=self.httponly,
                    samesite=self.samesite,
                    secure=self.secure,
                    path=self.path,
                )

        return response

    def _should_set_cookie(self, request: Request, session_id: str) -> bool:
        """
        Determine if we should set the session cookie.

        Set cookie for:
        - Cart-related endpoints (/cart/*)
        - When session ID is new (not in existing cookies)
        - For guest users (no auth header)
        """
        path = request.url.path

        # Only set cookie for cart endpoints
        if not path.startswith("/cart"):
            return False

        # Check if cookie already exists with same value
        existing_session = request.cookies.get(self.cookie_name)
        if existing_session == session_id:
            return False

        # Set cookie for new sessions or when session ID differs
        return True


def get_session_id_from_state(request: Request) -> Optional[str]:
    """
    Dependency to get session ID from request state.
    Should be used instead of cookie-based dependency after middleware is applied.
    """
    return getattr(request.state, "session_id", None)
