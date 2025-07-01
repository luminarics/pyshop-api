# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db        # your sync init
# from app.database import async_init_db  # if you later go async

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup -------------------------------------------------
    await init_db()              # or: await async_init_db()
    print("DB schema ensured")

    yield                  #  ▶  the app runs while we yield

    # --- shutdown -----------------------------------------------
    # close_db()           # if you add a close() helper later
    print("App shutdown complete")

app = FastAPI(lifespan=lifespan)

# Routers
from app.routers import products
app.include_router(products.router)