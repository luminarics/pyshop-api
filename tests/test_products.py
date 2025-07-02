def test_create_product(client):
    payload = {"name": "Test Product", "price": 10.99}
    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
