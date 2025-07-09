up:
docker compose up --build -d

logs:
docker compose logs -f

test:
poetry run pytest -q