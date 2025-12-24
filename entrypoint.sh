#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-<empty>}"
echo "[entrypoint] PYTHONPATH=${PYTHONPATH:-<empty>}"

# минимальная проверка критичных переменных
: "${DJANGO_SETTINGS_MODULE:?DJANGO_SETTINGS_MODULE is required}"
: "${DJANGO_SECRET_KEY:?DJANGO_SECRET_KEY is required}"

# опционально: миграции (включать в k8s только если осознанно)
if [[ "${RUN_MIGRATIONS:-0}" == "1" ]]; then
  echo "[entrypoint] running migrations..."
  python /app/src/manage.py migrate --noinput
fi

# опционально: collectstatic (если реально используешь статику в API-образе)
if [[ "${RUN_COLLECTSTATIC:-0}" == "1" ]]; then
  echo "[entrypoint] collectstatic..."
  python /app/src/manage.py collectstatic --noinput
fi

echo "[entrypoint] starting: $*"
exec "$@"
