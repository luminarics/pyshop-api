from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/products/", json={"name": "Test Product", "price": 10.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 10.99