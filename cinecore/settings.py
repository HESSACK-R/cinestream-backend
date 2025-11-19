# cinestream\backend\cinecore\settings.py
# cinestream/backend/cinecore/settings.py

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

# Charger les variables d’environnement depuis le fichier .env
load_dotenv()

# =============================
# 📍 BASE DIRECTORY
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================
# 🔐 SECURITY & ENV VARS
# =============================
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# =============================
# 🔧 INSTALLED APPS
# =============================
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',

    # Local apps
    'users',
    'catalog',
    'orders',
    'homepage',
    'suggestions',
    'telegram_bot',
    'settings_app',
]

# =============================
# 👥 AUTH
# =============================
AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=int(os.getenv("ACCESS_TOKEN_LIFETIME", 1))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv("REFRESH_TOKEN_LIFETIME", 7))),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =============================
# 🧱 MIDDLEWARE
# =============================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================
# 🛣 URL & TEMPLATES
# =============================
ROOT_URLCONF = 'cinecore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =============================
# ⚙️ WSGI / ASGI
# =============================
WSGI_APPLICATION = 'cinecore.wsgi.application'
ASGI_APPLICATION = 'cinecore.asgi.application'

# =============================
# 🔄 CHANNELS (WebSockets)
# =============================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# =============================
# 🗄 DATABASE
# =============================
DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# =============================
# 🔐 PASSWORD VALIDATION
# =============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================
# 🌍 INTERNATIONALIZATION
# =============================
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# =============================
# 🖼 STATIC & MEDIA
# =============================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", str(BASE_DIR / "media"))

# =============================
# 🔒 DRF DEFAULTS
# =============================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

# =============================
# 🌐 CORS
# =============================
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

CORS_ALLOW_CREDENTIALS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
