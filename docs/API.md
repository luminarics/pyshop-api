# API Documentation

## Overview

PyShop API is a FastAPI-based e-commerce backend providing user authentication and product management functionality.

**Base URL**: `http://localhost:8000`
**Interactive Docs**: `http://localhost:8000/docs`
**OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Authentication

The API uses JWT (JSON Web Token) based authentication with Bearer token scheme.

### Register a New User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePassword123!"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

### Login

```http
POST /auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePassword123!
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Logout

```http
POST /auth/jwt/logout
Authorization: Bearer <access_token>
```

**Response** (204 No Content)

## Protected Endpoints

All product endpoints require authentication. Include the JWT token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

## Products

### List All Products

```http
GET /products/
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "price": 99.99,
    "created_at": "2025-10-04T12:00:00",
    "updated_at": "2025-10-04T12:00:00"
  }
]
```

### Get Product by ID

```http
GET /products/{product_id}
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Product Name",
  "price": 99.99,
  "created_at": "2025-10-04T12:00:00",
  "updated_at": "2025-10-04T12:00:00"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Product not found"
}
```

### Create Product

```http
POST /products/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "New Product",
  "price": 49.99
}
```

**Response** (201 Created):
```json
{
  "id": 2,
  "name": "New Product",
  "price": 49.99,
  "created_at": "2025-10-04T12:00:00",
  "updated_at": "2025-10-04T12:00:00"
}
```

### Update Product

```http
PATCH /products/{product_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Name",
  "price": 59.99
}
```

**Response** (200 OK):
```json
{
  "id": 2,
  "name": "Updated Name",
  "price": 59.99,
  "created_at": "2025-10-04T12:00:00",
  "updated_at": "2025-10-04T12:30:00"
}
```

### Delete Product

```http
DELETE /products/{product_id}
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "Product deleted successfully"
}
```

## User Profile

### Get Current User

```http
GET /users/me
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

### Update Current User

```http
PATCH /users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername"
}
```

## Health Check

### Check API Health

```http
GET /healthz
```

**Response** (200 OK):
```json
{
  "status": "healthy"
}
```

## Monitoring

### Prometheus Metrics

```http
GET /metrics
```

Returns Prometheus-formatted metrics for monitoring.

## Error Responses

All endpoints follow standard HTTP status codes:

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Error Format

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

Currently no rate limiting is implemented. This should be added for production deployments.

## CORS

CORS is configured to allow requests from configured origins. Update `app/main.py` to modify allowed origins for your deployment.

## Examples

### Python (requests)

```python
import requests

# Register
response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "email": "user@example.com",
        "username": "username",
        "password": "SecurePassword123!"
    }
)
print(response.json())

# Login
response = requests.post(
    "http://localhost:8000/auth/jwt/login",
    data={
        "username": "user@example.com",
        "password": "SecurePassword123!"
    }
)
token = response.json()["access_token"]

# Get products
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/products/", headers=headers)
print(response.json())
```

### JavaScript (fetch)

```javascript
// Register
const registerResponse = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    username: 'username',
    password: 'SecurePassword123!'
  })
});
const user = await registerResponse.json();

// Login
const loginResponse = await fetch('http://localhost:8000/auth/jwt/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    username: 'user@example.com',
    password: 'SecurePassword123!'
  })
});
const { access_token } = await loginResponse.json();

// Get products
const productsResponse = await fetch('http://localhost:8000/products/', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const products = await productsResponse.json();
```

### cURL

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"username","password":"SecurePassword123!"}'

# Login
curl -X POST http://localhost:8000/auth/jwt/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePassword123!"

# Get products
curl -X GET http://localhost:8000/products/ \
  -H "Authorization: Bearer <access_token>"
```
