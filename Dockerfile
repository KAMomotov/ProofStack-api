FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.0 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Poetry
RUN curl -sSL https://install.python-poetry.org | python - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Сначала только метаданные — чтобы слой кэша работал
COPY pyproject.toml poetry.lock* /app/

# Ставим зависимости (без dev)
RUN poetry install --only main

# Теперь код
COPY . /app/

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
