import pytest
from sqlmodel import select
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.product import Product


@pytest.mark.asyncio
async def test_create_product(async_session: AsyncSession):
    # Hit the API
    payload = {"name": "Test Product", "price": 10.99}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/products/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]

    # Verify DB row
    result = await async_session.execute(
        select(Product).where(Product.name == "Test Product")
    )
    assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_pagination(async_session: AsyncSession):
    # Seed 3 rows
    async_session.add_all(
        [
            Product(name="p0", price=0),
            Product(name="p1", price=1),
            Product(name="p2", price=2),
        ]
    )
    await async_session.commit()

    # Query with limit/offset
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/products/list?limit=2&offset=1")

    assert response.status_code == 200
    body = response.json()
    print(body)
    assert len(body) == 2
    assert body[0]["name"] == "p1"
    assert body[1]["name"] == "p2"

    # Double-check total rows
    result = await async_session.execute(select(Product))
    assert len(result.scalars().all()) == 3
