## Documentation

* **[API Documentation](docs/API.md)** - Complete API reference with examples
* **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
* **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)

---

## CI/CD

The project includes comprehensive GitHub Actions workflows:

* **CI Pipeline** (`.github/workflows/ci.yml`):
  - Multi-version Python testing (3.10, 3.11, 3.12)
  - Code quality checks (Ruff, Black, MyPy)
  - Unit tests with coverage reporting
  - E2E tests with Playwright
  - Security scanning (Safety, Bandit)
  - Docker build validation

* **CD Pipeline** (`.github/workflows/cd.yml`):
  - Automated Docker image builds and publishing to GitHub Container Registry
  - Multi-platform support (amd64, arm64)
  - Staging and production deployments
  - Automated versioning with semantic tags

* **Dependabot** - Automated dependency updates with auto-merge for patches

---
