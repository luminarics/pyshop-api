from app.auth.authentification import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models.user import User, UserCreate, UserRead

app = FastAPI()

router = APIRouter(prefix="/profile", tags=["profile"])


@app.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
):
    # 1. hash the password
    hashed_pw = get_password_hash(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserRead.from_orm(user)


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserRead)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
