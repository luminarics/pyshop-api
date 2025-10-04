#!/bin/bash
set -e

echo "🚀 Setting up PyShop API development environment..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install it first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "✓ Poetry found"

# Install dependencies
echo "📦 Installing dependencies..."
poetry install --with dev

# Install pre-commit hooks (if available)
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔗 Installing pre-commit hooks..."
    poetry run pre-commit install
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << EOF
# Database
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/fastapi

# Security
SECRET_KEY=$(openssl rand -hex 32)
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true
EOF
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Check if Docker is running
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "🐳 Docker is running"

    # Ask if user wants to start services
    read -p "Do you want to start Docker services? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose up -d
        echo "✓ Docker services started"
        echo "Waiting for database to be ready..."
        sleep 5

        # Run migrations
        echo "🔄 Running database migrations..."
        poetry run alembic upgrade head
        echo "✓ Migrations complete"
    fi
else
    echo "⚠️  Docker is not running. Start it manually to use database."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review and update .env file if needed"
echo "  2. Start the development server:"
echo "     poetry run uvicorn app.main:app --reload"
echo "  3. Visit http://localhost:8000/docs for API documentation"
echo ""
