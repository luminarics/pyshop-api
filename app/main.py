# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import products
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("DB schema ensured")

    yield
    print("App shutdown complete")


app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(products.router)


@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"status": "ok"}
