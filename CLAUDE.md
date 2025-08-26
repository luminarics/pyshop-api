# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Local Development (Poetry)
```bash
poetry install --with dev
poetry run uvicorn app.main:app --reload
```

### Docker Development
```bash
docker compose up --build -d    # Start all services
docker compose logs -f          # View logs
```

### Testing & Quality
```bash
poetry run pytest -q            # Run tests
ruff .                          # Lint code
black --check .                 # Check formatting
mypy app tests                  # Type checking
```

### Database Migrations
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Architecture Overview

This is a **FastAPI 0.115 + SQLModel** e-commerce API with async PostgreSQL support, built for small SaaS/shops requiring JWT auth, metrics, and Docker deployment.

### Core Stack
- **FastAPI 0.115** with SQLModel for ORM
- **FastAPI-Users** for JWT authentication (UUID-based users)  
- **Async PostgreSQL** with asyncpg driver
- **Alembic** for database migrations
- **Prometheus** metrics + Grafana monitoring
- **Docker Compose** for development/deployment

### Project Structure
```
app/
├── main.py              # FastAPI app factory, lifespan management
├── database.py          # Async SQLAlchemy engine, session management
├── core/config.py       # Environment variables, settings
├── models/              # SQLModel tables + Pydantic schemas
│   ├── user.py         # User model with FastAPI-Users integration
│   └── product.py      # Product model with CRUD schemas
├── routers/            # API endpoints
│   ├── products.py     # Product CRUD (requires auth)
│   └── profile.py      # User profile endpoints
└── auth/
    └── user_manager.py # FastAPI-Users UserManager
```

### Database Models
- **User**: UUID primary key, FastAPI-Users integration with username field
- **Product**: Integer ID, name/price with timestamps
- Both models inherit from declarative base in `app.models.user.Base`

### Authentication Flow
- Registration: `POST /auth/register` (JSON)
- Login: `POST /auth/jwt/login` (form-encoded)  
- Protected routes require `Authorization: Bearer <token>` header
- JWT tokens expire in 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)

### Environment Variables
Required:
- `SECRET_KEY`: JWT signing key (must be long & random)

Optional:
- `DATABASE_URL`: Defaults to `postgresql+asyncpg://app:app@db:5432/fastapi`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT TTL, defaults to 30

### Testing Setup
- Uses **in-memory SQLite** with aiosqlite driver
- **pytest-asyncio** for async test support
- Automatic dependency override for database session in tests
- Test client available via `client` fixture

### Code Quality Configuration
- **Ruff**: Line length 88, excludes tests/ and alembic/
- **Black**: Line length 88, excludes alembic/versions/
- **MyPy**: Strict mode enabled for Python 3.10+
- **Pre-commit** hooks available for CI/CD integration

### Monitoring & Observability
- **Prometheus** metrics exposed at `/metrics` endpoint
- **Loguru** logging to `logs/api.log` with weekly rotation
- **Health check** endpoint at `/healthz`
- Ready-to-import Grafana dashboard in `monitoring/grafana.json`

### Development Notes
- Database migrations run automatically on container startup
- Uses async/await throughout for non-blocking I/O
- SQLModel provides both SQLAlchemy models and Pydantic schemas
- All product endpoints require authentication via OAuth2PasswordBearer