# syntax=docker/dockerfile:1.6
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.2.0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# --- deps stage ---
FROM base AS deps

# системные зависимости: curl для Poetry, + ca-certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==${POETRY_VERSION}"

# Кэшируем зависимости
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --only main --no-ansi \
    && rm -rf "$POETRY_CACHE_DIR"

# --- runtime stage ---
FROM base AS runtime

# non-root user
RUN useradd -m -u 10001 appuser

# зависимости из deps-стадии
COPY --from=deps /usr/local /usr/local

# проект
COPY ./src /app/src
COPY ./entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh \
    && chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app/src \
    DJANGO_SETTINGS_MODULE=proofstack.settings.prod \
    PORT=8000

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--chdir", "/app/src", "proofstack.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]