# Deployment Guide

This guide covers deploying PyShop API to production environments.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Cloud Deployment](#cloud-deployment)
- [Security Considerations](#security-considerations)
- [Monitoring](#monitoring)

## Docker Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd pyshop-api
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your production values
```

3. Start services:
```bash
docker compose up -d
```

4. Check health:
```bash
curl http://localhost:8000/healthz
```

### Production Docker Compose

Create a `docker-compose.prod.yml` for production:

```yaml
version: '3.8'

services:
  api:
    image: ghcr.io/<your-username>/pyshop-api:latest
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
      - DEBUG=false
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  prometheus:
    image: prom/prometheus:latest
    restart: always
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    restart: always
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana.json:/etc/grafana/provisioning/dashboards/dashboard.json

volumes:
  postgres_data:
  prometheus_data:
  grafana_data:
```

Start production services:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## Environment Configuration

### Required Environment Variables

Create a `.env` file with the following variables:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Security (MUST be changed in production!)
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=production
DEBUG=false

# Optional
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Generating Secure Keys

```bash
# Generate SECRET_KEY
openssl rand -hex 32
```

## Database Setup

### Running Migrations

```bash
# Using Poetry
poetry run alembic upgrade head

# Using Docker
docker compose exec api alembic upgrade head
```

### Database Backup

```bash
# Backup
docker compose exec db pg_dump -U app fastapi > backup.sql

# Restore
docker compose exec -T db psql -U app fastapi < backup.sql
```

### Automated Backups

Add a cron job for automated backups:

```bash
# Backup daily at 2 AM
0 2 * * * cd /path/to/pyshop-api && docker compose exec db pg_dump -U app fastapi | gzip > backups/backup-$(date +\%Y\%m\%d).sql.gz
```

## Cloud Deployment

### AWS ECS/Fargate

1. Build and push Docker image:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t pyshop-api .
docker tag pyshop-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/pyshop-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/pyshop-api:latest
```

2. Create task definition with:
   - Container image: Your ECR image
   - Environment variables from Secrets Manager
   - RDS PostgreSQL database
   - Application Load Balancer

3. Create ECS service with auto-scaling

### Google Cloud Run

1. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/<project-id>/pyshop-api
gcloud run deploy pyshop-api \
  --image gcr.io/<project-id>/pyshop-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=<cloud-sql-connection>,SECRET_KEY=<secret>
```

2. Connect to Cloud SQL PostgreSQL
3. Run migrations from Cloud Build or locally

### DigitalOcean App Platform

1. Create `app.yaml`:
```yaml
name: pyshop-api
services:
- name: api
  dockerfile_path: Dockerfile
  github:
    repo: <your-repo>
    branch: main
  health_check:
    http_path: /healthz
  envs:
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
  - key: SECRET_KEY
    type: SECRET
    value: <your-secret>
databases:
- name: db
  engine: PG
  version: "15"
```

2. Deploy:
```bash
doctl apps create --spec app.yaml
```

### Kubernetes

1. Create deployment manifests in `k8s/`:

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pyshop-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pyshop-api
  template:
    metadata:
      labels:
        app: pyshop-api
    spec:
      containers:
      - name: api
        image: ghcr.io/<username>/pyshop-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: pyshop-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: pyshop-secrets
              key: secret-key
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

2. Deploy:
```bash
kubectl apply -f k8s/
```

## Security Considerations

### SSL/TLS

Use a reverse proxy (nginx, Traefik, Caddy) for SSL termination:

```nginx
server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Secrets Management

Never commit secrets to version control. Use:

- **AWS**: AWS Secrets Manager or Parameter Store
- **GCP**: Secret Manager
- **Azure**: Key Vault
- **Kubernetes**: Sealed Secrets or External Secrets Operator
- **Docker**: Docker Secrets

### Security Headers

Add security middleware in `app/main.py`:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.yourdomain.com"])
app.add_middleware(HTTPSRedirectMiddleware)
```

### Rate Limiting

Install and configure rate limiting:

```bash
poetry add slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/products/")
@limiter.limit("5/minute")
async def get_products(request: Request):
    ...
```

## Monitoring

### Prometheus + Grafana

Access monitoring dashboards:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Import the provided dashboard from `monitoring/grafana.json`

### Application Logs

View logs:
```bash
# Docker Compose
docker compose logs -f api

# Kubernetes
kubectl logs -f deployment/pyshop-api

# Cloud platforms
# AWS: CloudWatch Logs
# GCP: Cloud Logging
# Azure: Application Insights
```

### Alerts

Configure Prometheus alerts in `monitoring/alerts.yml`:

```yaml
groups:
- name: api_alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    annotations:
      summary: "High error rate detected"
```

## Scaling

### Horizontal Scaling

```bash
# Docker Compose
docker compose up -d --scale api=3

# Kubernetes
kubectl scale deployment pyshop-api --replicas=5
```

### Database Connection Pooling

Configured in `app/database.py`:
```python
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)
```

### Caching

Add Redis for caching:
```bash
poetry add redis fastapi-cache2
```

## Health Checks

The API provides a health check endpoint at `/healthz`:

```bash
curl http://localhost:8000/healthz
# {"status": "healthy"}
```

Configure your load balancer to use this endpoint for health checks.

## Troubleshooting

### Database Connection Issues

```bash
# Check database is reachable
docker compose exec api nc -zv db 5432

# Check database logs
docker compose logs db

# Verify credentials
docker compose exec db psql -U app -d fastapi
```

### Migration Issues

```bash
# Check current version
docker compose exec api alembic current

# View migration history
docker compose exec api alembic history

# Rollback one version
docker compose exec api alembic downgrade -1
```

### Performance Issues

```bash
# Check resource usage
docker stats

# View slow queries
docker compose exec db psql -U app -d fastapi -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

## CI/CD

The project includes GitHub Actions workflows:

- `.github/workflows/ci.yml` - Run tests and linting
- `.github/workflows/cd.yml` - Build and deploy Docker images

See [CI/CD documentation](../README.md#cicd) for details.

## Rollback Strategy

### Docker Tags

Always tag releases with semantic versioning:
```bash
docker tag pyshop-api:latest pyshop-api:v1.2.3
```

### Rollback Steps

1. Identify last known good version
2. Deploy previous version:
```bash
docker compose pull api:v1.2.2
docker compose up -d
```

3. Rollback migrations if needed:
```bash
docker compose exec api alembic downgrade <revision>
```

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Documentation: See `docs/` directory
