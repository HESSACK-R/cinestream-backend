# cinestream\backend\cinecore\settings.py

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url
import cloudinary

# Load .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================
# 🔐 SECRET & DEBUG
# ======================================================
SECRET_KEY = os.getenv("SECRET_KEY", "local-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "cinestream-backend-33c3.onrender.com",
]

# ======================================================
# 📦 INSTALLED APPS
# ======================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # External
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "channels",
    "cloudinary",
    "cloudinary_storage",

    # Internal
    "users",
    "catalog",
    "orders",
    "homepage",
    "suggestions",
    "telegram_bot",
    "settings_app",
]

# ======================================================
# 🧑 AUTH
# ======================================================
AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ======================================================
# 🔌 MIDDLEWARE
# ======================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST BE FIRST
    "django.middleware.common.CommonMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cinecore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ======================================================
# 🌐 WSGI (pas de WebSocket)
# ======================================================
WSGI_APPLICATION = "cinecore.wsgi.application"

# ======================================================
# 🗄 DATABASE
# ======================================================
if DEBUG:
    print("🔧 MODE LOCAL : SQLite")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    print("🚀 MODE PRODUCTION : PostgreSQL Render")
    DATABASES = {
        "default": dj_database_url.config(conn_max_age=600, ssl_require=True)
    }

# ======================================================
# 🌍 I18N
# ======================================================
LANGUAGE_CODE = "fr-FR"
TIME_ZONE = "Africa/Douala"
USE_I18N = True
USE_TZ = True

# ======================================================
# 📁 STATIC & MEDIA
# ======================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------- CLOUDINARY ----------
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

# ======================================================
# 🔒 REST & CORS
# ======================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]

# === CORS FIX FOR VERCEL FRONTEND ===
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://cinestream-frontend.vercel.app",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://cinestream-frontend.vercel.app",
    "https://*.vercel.app",
    "https://cinestream-backend-33c3.onrender.com",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

