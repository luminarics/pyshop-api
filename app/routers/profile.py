from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from sqlmodel import UUID

from app.auth.user_manager import get_user_manager
from app.models.user import User, UserRead, UserCreate, UserUpdate
from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Configure bearer transport
bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")


# Configure JWT Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET_KEY,
        lifetime_seconds=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        token_audience=["fastapi-users:auth"],
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](  # type: ignore[type-var]
    get_user_manager,
    [auth_backend],
)

# Include fastapi-users routers
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Export current_user dependencies
current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user_optional = fastapi_users.current_user(optional=True)


@router.get("/me")
async def get_me(user: User = Depends(current_active_user)):
    return user
