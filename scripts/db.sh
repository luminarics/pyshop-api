#!/bin/bash
set -e

COMMAND=${1:-help}

case $COMMAND in
    migrate)
        echo "🔄 Running database migrations..."
        poetry run alembic upgrade head
        echo "✅ Migrations complete!"
        ;;

    rollback)
        STEPS=${2:-1}
        echo "⏪ Rolling back $STEPS migration(s)..."
        poetry run alembic downgrade -$STEPS
        echo "✅ Rollback complete!"
        ;;

    reset)
        echo "⚠️  This will reset the database! All data will be lost."
        read -p "Are you sure? (yes/no) " -r
        echo
        if [[ $REPLY == "yes" ]]; then
            echo "Dropping all tables..."
            poetry run alembic downgrade base
            echo "Running all migrations..."
            poetry run alembic upgrade head
            echo "✅ Database reset complete!"
        else
            echo "Cancelled."
        fi
        ;;

    revision)
        MESSAGE=${2:-"Auto-generated migration"}
        echo "📝 Creating new migration: $MESSAGE"
        poetry run alembic revision --autogenerate -m "$MESSAGE"
        echo "✅ Migration file created!"
        ;;

    current)
        echo "📍 Current database version:"
        poetry run alembic current
        ;;

    history)
        echo "📜 Migration history:"
        poetry run alembic history
        ;;

    shell)
        echo "🐘 Opening PostgreSQL shell..."
        docker compose exec db psql -U app -d fastapi
        ;;

    help|*)
        echo "Database management script"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  migrate              Run pending migrations"
        echo "  rollback [steps]     Rollback migrations (default: 1)"
        echo "  reset                Reset database (WARNING: deletes all data)"
        echo "  revision <message>   Create new migration"
        echo "  current              Show current migration version"
        echo "  history              Show migration history"
        echo "  shell                Open PostgreSQL shell"
        echo "  help                 Show this help"
        ;;
esac
