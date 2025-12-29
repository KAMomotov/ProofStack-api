from pathlib import Path
import environ

# abc.py находится тут: src/proofstack/settings/abc.py
SRC_DIR = Path(__file__).resolve().parents[2]     # .../src
REPO_DIR = SRC_DIR.parent                         # корень репозитория

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, []),

    POSTGRES_HOST=(str, ""),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ""),
    POSTGRES_USER=(str, ""),
    POSTGRES_PASSWORD=(str, ""),

    MINIO_ENDPOINT=(str, ""),
    MINIO_BUCKET=(str, ""),
    MINIO_REGION=(str, "us-east-1"),
    MINIO_ACCESS_KEY=(str, ""),
    MINIO_SECRET_KEY=(str, ""),
)

# локально можно иметь .env (в k8s обычно не нужен)
if (REPO_DIR / ".env").exists():
    env.read_env(REPO_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-unsafe-secret-key")
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS and DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "reversion",
    "rest_framework",
    "storages",

    "apps.core",
    "apps.profile",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "reversion.middleware.RevisionMiddleware",
]

ROOT_URLCONF = "proofstack.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]

WSGI_APPLICATION = "proofstack.wsgi.application"
ASGI_APPLICATION = "proofstack.asgi.application"

# База: если Postgres env не задан — используем sqlite для локальной разработки
if env("POSTGRES_HOST") and env("POSTGRES_DB") and env("POSTGRES_USER"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD", default=""),
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(SRC_DIR / "db.sqlite3"),
        }
    }

# [TODO] Определиться с региональными настройками
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- DRF минимально ---
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# --- MinIO / S3 (django-storages) ---
MINIO_ENDPOINT = env("MINIO_ENDPOINT")
MINIO_BUCKET = env("MINIO_BUCKET")

if MINIO_ENDPOINT and MINIO_BUCKET:
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3.S3Storage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }

    AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
    AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET
    AWS_ACCESS_KEY_ID = env("MINIO_ACCESS_KEY", default="")
    AWS_SECRET_ACCESS_KEY = env("MINIO_SECRET_KEY", default="")
    AWS_S3_REGION_NAME = env("MINIO_REGION")
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_DEFAULT_ACL = None
