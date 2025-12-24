#!/usr/bin/env sh
set -eu

# Если Django-проект уже есть (proofstack.wsgi.py), запускаем gunicorn
if python -c "import importlib; importlib.import_module('proofstack.wsgi')" >/dev/null 2>&1; then
  exec gunicorn ${GUNICORN_APP:-proofstack.wsgi:application} \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-2} \
    --threads ${GUNICORN_THREADS:-4} \
    --timeout ${GUNICORN_TIMEOUT:-60}
fi

# Иначе — временная заглушка (чтобы CI/GitOps не блокировались)
echo "WARN: Django app module not found (config.wsgi). Starting placeholder server on :8000"
exec python -m http.server 8000
