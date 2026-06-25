import os
from pathlib import Path
from dotenv import load_dotenv

# Lädt die Umgebungsvariablen aus der .env Datei
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Sicherheitseinstellungen aus der .env laden
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-fallbackschaetzwert-falls-env-fehlt')

# DEBUG-Modus aus der .env laden
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 't')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Hier sagen wir Django explizit, dass unser Fundbüro-Portal existiert:
    'portal.apps.PortalConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fundbuero_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fundbuero_project.wsgi.application'


# Datenbank-Konfiguration (SQLite liegt sicher auf deinem USB-Stick)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Passwort-Validierung
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalisierung (Auf Deutsch eingestellt)
LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# Statische Dateien (CSS, Bilder)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Standard-ID-Feld-Typ
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Wohin geht es nach dem Login? Zur Liste der Gegenstände.
LOGIN_REDIRECT_URL = 'gegenstand_liste'

# Wohin geht es nach dem Logout? Zur Login-Seite.
LOGOUT_REDIRECT_URL = 'login'