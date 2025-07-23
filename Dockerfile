FROM python:3.12-bookworm

ARG POETRY_VERSION=1.8.2
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --only main

COPY . /app

EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
