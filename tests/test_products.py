import pytest
from sqlmodel import select
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.product import Product
from app.models.product import ProductCreate


@pytest.mark.asyncio
async def test_create_product(async_session: AsyncSession):
    # Hit the API
    payload = ProductCreate(name="Test Product", price=10.99)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        headers = await get_auth_headers(ac)
        response = await ac.post(
            "/products/", json=payload.model_dump(), headers=headers
        )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload.name
    assert data["price"] == payload.price

    # Verify DB row
    result = await async_session.execute(
        select(Product).where(Product.name == "Test Product")
    )
    assert len(result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_pagination(async_session: AsyncSession):
    # Seed 3 rows
    products = [Product(name=f"p{i}", price=float(i)) for i in range(3)]
    async_session.add_all(products)
    await async_session.commit()

    # Test first page
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        headers = await get_auth_headers(ac)
        response = await ac.get("/products/?offset=0&limit=2", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "p0"
    assert data[1]["name"] == "p1"

    # Test second page
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        headers = await get_auth_headers(ac)
        response = await ac.get("/products/?offset=2&limit=2", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "p2"


@pytest.mark.asyncio
async def test_update_product(async_session: AsyncSession):
    # Create a product first
    product = Product(name="Old Name", price=9.99)
    async_session.add(product)
    await async_session.commit()
    # Update it
    update_payload = {"name": "New Name", "price": 19.99}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        headers = await get_auth_headers(ac)
        response = await ac.put(
            f"/products/{product.id}", json=update_payload, headers=headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data["price"] == update_payload["price"]


@pytest.mark.asyncio
async def test_create_and_list_product(client):
    headers = await get_auth_headers(client)
    # create
    resp = await client.post(
        "/products/", json={"name": "Test", "price": 42}, headers=headers
    )
    assert resp.status_code == 201

    # list
    items = (await client.get("/products/", headers=headers)).json()
    assert any(p["name"] == "Test" for p in items)


@pytest.mark.asyncio
async def test_create_requires_auth(client):
    resp = await client.post("/products/", json={"name": "X", "price": 1})
    assert resp.status_code == 401


async def get_auth_headers(client: AsyncClient):
    # signup
    await client.post(
        "/auth/register",
        json={"email": "test@example.pl", "password": "hunter2", "username": "tester"},
    )
    login = await client.post(
        "/auth/jwt/login",
        data={"username": "test@example.pl", "password": "hunter2"},  # dict, not str
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    return headers
