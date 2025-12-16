#!/usr/bin/env sh
set -eu

# В k8s миграции будем делать отдельным Job/Hook'ом (позже).
# Тут оставим только запуск приложения.
exec gunicorn ${GUNICORN_APP:-config.wsgi:application} \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-2} \
  --threads ${GUNICORN_THREADS:-4} \
  --timeout ${GUNICORN_TIMEOUT:-60}
