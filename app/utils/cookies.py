"""Cookie management utilities with security features."""

import hmac
import hashlib
import json
import base64
from typing import Any, Dict, Optional, Union, Literal

from fastapi import Request, Response
from cryptography.fernet import Fernet
from app.core.config import SECRET_KEY


class CookieManager:
    """Secure cookie management with encryption and signing capabilities."""

    def __init__(self, secret_key: str = SECRET_KEY):
        self.secret_key = (
            secret_key.encode() if isinstance(secret_key, str) else secret_key
        )
        # Create Fernet cipher for encryption
        key = base64.urlsafe_b64encode(self.secret_key.ljust(32)[:32])
        self.cipher = Fernet(key)

    def create_signature(self, value: str) -> str:
        """Create HMAC signature for cookie value."""
        return hmac.new(
            self.secret_key, value.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def verify_signature(self, value: str, signature: str) -> bool:
        """Verify HMAC signature for cookie value."""
        expected_signature = self.create_signature(value)
        return hmac.compare_digest(expected_signature, signature)

    def encrypt_value(self, value: str) -> str:
        """Encrypt cookie value."""
        encrypted = self.cipher.encrypt(value.encode("utf-8"))
        return base64.urlsafe_b64encode(encrypted).decode("utf-8")

    def decrypt_value(self, encrypted_value: str) -> Optional[str]:
        """Decrypt cookie value. Returns None if decryption fails."""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode("utf-8"))
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode("utf-8")
        except Exception:
            return None

    def serialize_data(self, data: Dict[str, Any]) -> str:
        """Serialize dictionary data to JSON string."""
        return json.dumps(data, separators=(",", ":"), sort_keys=True)

    def deserialize_data(self, data_str: str) -> Optional[Dict[str, Any]]:
        """Deserialize JSON string to dictionary. Returns None on error."""
        try:
            return json.loads(data_str)
        except (json.JSONDecodeError, TypeError):
            return None


class SecureCookie:
    """Secure cookie with encryption and signing."""

    def __init__(
        self,
        name: str,
        manager: CookieManager,
        max_age: int = 7 * 24 * 60 * 60,  # 7 days
        httponly: bool = True,
        secure: bool = False,
        samesite: Literal["lax", "strict", "none"] = "lax",
        path: str = "/",
        domain: Optional[str] = None,
        encrypt: bool = True,
        sign: bool = True,
    ):
        self.name = name
        self.manager = manager
        self.max_age = max_age
        self.httponly = httponly
        self.secure = secure
        self.samesite = samesite
        self.path = path
        self.domain = domain
        self.encrypt = encrypt
        self.sign = sign

    def set_cookie(
        self,
        response: Response,
        value: Union[str, Dict[str, Any]],
        max_age: Optional[int] = None,
    ) -> None:
        """Set secure cookie with encryption and/or signing."""
        # Serialize data if it's a dictionary
        if isinstance(value, dict):
            cookie_value = self.manager.serialize_data(value)
        else:
            cookie_value = str(value)

        # Encrypt if enabled
        if self.encrypt:
            cookie_value = self.manager.encrypt_value(cookie_value)

        # Sign if enabled
        if self.sign:
            signature = self.manager.create_signature(cookie_value)
            cookie_value = f"{cookie_value}.{signature}"

        # Set cookie with security attributes
        response.set_cookie(
            key=self.name,
            value=cookie_value,
            max_age=max_age or self.max_age,
            httponly=self.httponly,
            secure=self.secure,
            samesite=self.samesite,
            path=self.path,
            domain=self.domain,
        )

    def get_cookie(self, request: Request) -> Optional[str]:
        """Get and validate secure cookie as string."""
        cookie_value = request.cookies.get(self.name)
        if not cookie_value:
            return None

        # Verify signature if signing is enabled
        if self.sign:
            try:
                value_part, signature_part = cookie_value.rsplit(".", 1)
                if not self.manager.verify_signature(value_part, signature_part):
                    return None
                cookie_value = value_part
            except ValueError:
                # Invalid format (no signature)
                return None

        # Decrypt if encryption is enabled
        if self.encrypt:
            cookie_value = self.manager.decrypt_value(cookie_value)
            if cookie_value is None:
                return None

        return cookie_value

    def get_cookie_data(self, request: Request) -> Optional[Dict[str, Any]]:
        """Get and validate secure cookie as deserialized dictionary."""
        cookie_value = self.get_cookie(request)
        if cookie_value is None:
            return None

        return self.manager.deserialize_data(cookie_value)

    def delete_cookie(self, response: Response) -> None:
        """Delete cookie by setting it to expire."""
        response.set_cookie(
            key=self.name,
            value="",
            max_age=0,
            httponly=self.httponly,
            secure=self.secure,
            samesite=self.samesite,
            path=self.path,
            domain=self.domain,
        )


class CookieStore:
    """Cookie-based data store with automatic serialization."""

    def __init__(
        self,
        cookie_name: str,
        secret_key: str = SECRET_KEY,
        max_age: int = 7 * 24 * 60 * 60,
        **cookie_kwargs,
    ):
        self.manager = CookieManager(secret_key)
        self.cookie = SecureCookie(
            name=cookie_name, manager=self.manager, max_age=max_age, **cookie_kwargs
        )

    def get_data(self, request: Request) -> Dict[str, Any]:
        """Get all data from cookie store."""
        data = self.cookie.get_cookie_data(request)
        return data or {}

    def set_data(
        self, response: Response, data: Dict[str, Any], max_age: Optional[int] = None
    ) -> None:
        """Set all data in cookie store."""
        self.cookie.set_cookie(response, data, max_age)

    def get_value(self, request: Request, key: str, default: Any = None) -> Any:
        """Get specific value from cookie store."""
        data = self.get_data(request)
        return data.get(key, default)

    def set_value(
        self,
        request: Request,
        response: Response,
        key: str,
        value: Any,
        max_age: Optional[int] = None,
    ) -> None:
        """Set specific value in cookie store."""
        data = self.get_data(request)
        data[key] = value
        self.set_data(response, data, max_age)

    def delete_value(self, request: Request, response: Response, key: str) -> None:
        """Delete specific value from cookie store."""
        data = self.get_data(request)
        data.pop(key, None)
        self.set_data(response, data)

    def clear(self, response: Response) -> None:
        """Clear all data from cookie store."""
        self.cookie.delete_cookie(response)


# Pre-configured cookie instances for common use cases
def create_session_cookie(
    name: str = "pyshop_cart_session",
    secure: bool = False,  # Set to True in production
    max_age: int = 7 * 24 * 60 * 60,
) -> SecureCookie:
    """Create secure session cookie for cart functionality."""
    return SecureCookie(
        name=name,
        manager=CookieManager(),
        max_age=max_age,
        httponly=True,
        secure=secure,
        samesite="lax",
        encrypt=False,  # Session IDs are already UUIDs
        sign=True,  # But we want to verify they're not tampered with
    )


def create_user_preference_cookie(
    name: str = "pyshop_preferences",
    secure: bool = False,
) -> CookieStore:
    """Create secure cookie store for user preferences."""
    return CookieStore(
        cookie_name=name,
        max_age=30 * 24 * 60 * 60,  # 30 days
        httponly=False,  # Accessible to JS for UI preferences
        secure=secure,
        samesite="lax",
        encrypt=True,
        sign=True,
    )


def create_remember_me_cookie(
    name: str = "pyshop_remember",
    secure: bool = False,
) -> SecureCookie:
    """Create secure remember-me cookie for authentication."""
    return SecureCookie(
        name=name,
        manager=CookieManager(),
        max_age=30 * 24 * 60 * 60,  # 30 days
        httponly=True,
        secure=secure,
        samesite="strict",  # Strict for auth cookies
        encrypt=True,
        sign=True,
    )
