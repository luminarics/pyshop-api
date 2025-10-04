#!/bin/bash
set -e

echo "🔍 Running code quality checks..."

# Parse arguments
FIX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--fix]"
            exit 1
            ;;
    esac
done

# Ruff linting
echo "Running Ruff..."
if [ "$FIX" = true ]; then
    poetry run ruff check . --fix
else
    poetry run ruff check .
fi

# Black formatting
echo "Running Black..."
if [ "$FIX" = true ]; then
    poetry run black .
else
    poetry run black --check .
fi

# MyPy type checking
echo "Running MyPy..."
poetry run mypy app tests

echo ""
echo "✅ All checks passed!"
