#!/bin/bash
set -e

echo "🧪 Running PyShop API tests..."

# Parse arguments
RUN_E2E=false
RUN_COVERAGE=false
VERBOSE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --e2e)
            RUN_E2E=true
            shift
            ;;
        --coverage)
            RUN_COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--e2e] [--coverage] [-v|--verbose]"
            exit 1
            ;;
    esac
done

# Build test command
TEST_CMD="poetry run pytest"
COVERAGE_ARGS=""

if [ "$RUN_COVERAGE" = true ]; then
    COVERAGE_ARGS="--cov=app --cov-report=html --cov-report=term"
fi

# Run unit tests (exclude e2e)
if [ "$RUN_E2E" = false ]; then
    echo "Running unit tests only..."
    $TEST_CMD tests $VERBOSE $COVERAGE_ARGS -m "not e2e"
else
    # Check if services are running
    if ! curl -f http://localhost:8000/healthz &> /dev/null; then
        echo "⚠️  API server is not running. Starting services..."
        docker compose up -d
        echo "Waiting for services to be ready..."
        sleep 10

        # Run migrations
        echo "Running migrations..."
        poetry run alembic upgrade head

        # Wait for server
        for i in {1..30}; do
            if curl -f http://localhost:8000/healthz &> /dev/null; then
                echo "✓ Server is ready"
                break
            fi
            if [ $i -eq 30 ]; then
                echo "❌ Server failed to start"
                exit 1
            fi
            sleep 1
        done
    fi

    echo "Running all tests (including E2E)..."
    $TEST_CMD tests $VERBOSE $COVERAGE_ARGS
fi

echo ""
echo "✅ Tests complete!"

if [ "$RUN_COVERAGE" = true ]; then
    echo "📊 Coverage report generated in htmlcov/index.html"
fi
