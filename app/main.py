# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import products, profile
from app.database import init_db
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

logger.add("logs/api.log", rotation="1 week", serialize=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("DB schema ensured")

    yield
    logger.info("App shutdown complete")


app = FastAPI(lifespan=lifespan)

instrumentator = Instrumentator()

instrumentator.instrument(app)

instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)

# Routers
app.include_router(products.router)

app.include_router(profile.router)


@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"status": "ok"}
