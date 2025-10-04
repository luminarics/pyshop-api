#!/bin/bash
set -e

echo "🚀 Starting PyShop API development server..."

# Check if services are running
if ! docker compose ps | grep -q "db.*running"; then
    echo "Starting Docker services..."
    docker compose up -d
    echo "Waiting for database..."
    sleep 5
fi

# Run migrations
echo "Running database migrations..."
poetry run alembic upgrade head

# Start server with hot reload
echo "Starting server at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""

poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
