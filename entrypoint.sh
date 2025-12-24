#!/usr/bin/env sh
set -eu

: "${DJANGO_SETTINGS_MODULE:=proofstack.settings.prod}"
: "${GUNICORN_APP:=proofstack.wsgi:application}"
: "${APP_DIR:=/app}"
: "${SRC_DIR:=/app/src}"

exec gunicorn --chdir "$SRC_DIR" "$GUNICORN_APP" \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-2}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-60}"
