from typing import Optional
from uuid import UUID
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.models.user import User
from app.core.config import SECRET_KEY
from app.database import get_user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
