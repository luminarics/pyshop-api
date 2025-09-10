# 🚀 pyshop‑api
### Flagship Python Project - Production-Ready E-Commerce API

![CI](https://github.com/luminarics/pyshop-api/actions/workflows/python-tests.yml/badge.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?logo=docker&logoColor=white) ![Coverage](https://img.shields.io/badge/Coverage-90%25+-brightgreen) 

---

**An enterprise-grade, fully‑async e‑commerce API showcasing modern Python development excellence built with FastAPI 0.115 and SQLModel.** Features complete JWT authentication, real-time monitoring, and production-ready Docker deployment.

---

## TL;DR

```bash
git clone https://github.com/luminarics/pyshop-api.git && cd pyshop-api
cp .env.example .env              # edit values or keep the sane defaults
docker compose up --build         # API → http://localhost:8000 ⚡️
```

| URL        | What                                               |
| ---------- | -------------------------------------------------- |
| `/docs`    | Swagger‑UI (OpenAPI)                               |
| `/redoc`   | ReDoc docs                                         |
| `/health`  | Liveness/DB check                                  |
| `/metrics` | Prometheus metrics (scraped by the prom container) |
| `:9090`    | Prometheus UI                                      |
| `:3000`    | Grafana (admin / admin on first run)               |

---

### 🚀 Core Features

* **FastAPI 0.115 + SQLModel** (async engine, asyncpg driver)
* **FastAPI‑Users** JWT auth with pluggable back‑end
* **Docker + Compose** for DB, API, Prometheus, Grafana
* **Prometheus /metrics** + ready‑to‑import Grafana dashboard
* **Pytest**, **ruff**, **black**, **mypy** – wired in GitHub Actions CI
* **≥90 % comprehensive test suite** with pytest and async support
* **Alembic** migrations (auto‑generate & run on start‑up)

### 💎 What Makes This Project Stand Out

* **🏆 Enterprise Architecture** - Clean separation of concerns, SOLID principles, dependency injection
* **⚡ Performance First** - 100% async/await, connection pooling, optimized database queries
* **🔒 Security Focused** - JWT authentication, input validation, SQL injection protection
* **📈 Production Monitoring** - Comprehensive metrics, structured logging, health checks
* **🧪 Quality Assurance** - 90%+ test coverage, strict typing, automated code quality checks
* **🚀 Developer Experience** - Hot reload, comprehensive tooling, clear documentation
* **🔄 CI/CD Ready** - GitHub Actions, pre-commit hooks, automated deployment

Roadmap → [#milestones](#roadmap).

---

## Requirements

* Docker ≥ 25
* Make, if you like the optional helper targets
* Or: Python 3.12 + Poetry for a native setup

---

## Local development (Poetry)

```bash
poetry install --with dev
export SECRET_KEY=dev123
export DATABASE_URL=sqlite+aiosqlite:///:memory:
poetry run uvicorn app.main:app --reload
```

> **Tip:** SQLite is fine for unit tests; use Postgres in Docker for manual poking.

---

## Environment variables

| Var                           | Default (docker)                               | Required | Notes                                   |
| ----------------------------- | ---------------------------------------------- | -------- | --------------------------------------- |
| `SECRET_KEY`                  | *none*                                         | ✅        | JWT signing key – must be long & random |
| `DATABASE_URL`                | `postgresql+asyncpg://app:app@db:5432/fastapi` |          | SQLAlchemy URL                          |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`                                           |          | JWT TTL                                 |

See `.env.example` for a full list.

---

## Auth flow (curl cheatsheet)

```bash
# 1 — Register
curl -X POST http://localhost:8000/auth/register \
     -H 'Content-Type: application/json' \
     -d '{"email":"[email protected]","password":"hunter2","username":"deni"}'

# 2 — Login (form‑encoded!)
curl -X POST http://localhost:8000/auth/jwt/login \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=[email protected]&password=hunter2'

# 3 — Hit a protected route
TOKEN="$(jq -r .access_token <<< "$RESPONSE")"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/profile
```

---

## Running tests & linters

```bash
# inside venv / poetry shell
pytest -q                     # unit tests
ruff .                        # lint
black --check .               # formatting
mypy app tests                # static types
```

The CI workflow mirrors the same steps with automated testing.

---

## Migrations

```bash
alembic revision --autogenerate -m "add product table"
alembic upgrade head
```

The Docker image runs `alembic upgrade head` at start‑up so containers come up with the latest schema.

---

## Monitoring

* **Prometheus** scrapes `http://api:8000/metrics` every 15 s (see `monitoring/prometheus.yml`).
* **Grafana** starts with an empty workspace. Import `monitoring/grafana.json` or build your own.

![Grafana screenshot](./docs/grafana.png)

---

## Project layout

```
app/
 ├── api/                 # Routers / endpoints
 ├── core/                # Settings, security, utils
 ├── models/              # SQLModel tables & Pydantic schemas
 ├── services/            # CRUD / business logic
 ├── tests/               # Pytest suites
 └── main.py              # FastAPI factory & router mounting
monitoring/
 ├── prometheus.yml
 └── grafana.json
Dockerfile
docker-compose.yml
alembic/
```

---

## Roadmap

* 🚀 Deploy to **AWS Fargate** via Terraform
* 📊 Publish Grafana dashboards to Grafana Cloud
* 🛠️ Contribute two PRs to the FastAPI ecosystem
---

## Contributing

PRs, issues and *polite rants* are welcome. Before you open a PR:

1. Create a branch off **`main`**.
2. `pre-commit run --all-files` (installs hooks automatically).
3. Make sure `pytest` and `mypy` are 💚 locally.

If you’re new to FastAPI, check the [FastAPI docs](https://fastapi.tiangolo.com/) and [SQLModel docs](https://sqlmodel.tiangolo.com/) first — then hack away.

---

## License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.
