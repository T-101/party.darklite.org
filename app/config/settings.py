"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import logging
import os
import sys

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # reading .env file

SITE_ROOT = root()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

DEBUG_TOOLBAR_CONFIG = {
    # Display Django Debug Toolbar in docker when DEBUG = True
    'SHOW_TOOLBAR_CALLBACK': lambda _: DEBUG,
}

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # packages
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'django_countries',
    'django_object_actions',
    'crispy_forms',
    'crispy_bootstrap5',
    'tempus_dominus',
    'django_simple_plausible',
    'drf_spectacular',
    # Our apps
    'authentication',
    'party',
    'logviewer',
    'django_simple_user_agents',
]

if DEBUG and "test" not in sys.argv:
    INSTALLED_APPS.append('debug_toolbar')

AUTH_USER_MODEL = 'authentication.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_simple_user_agents.middleware.UserAgentMiddleware',
    'common.middleware.UserIPAddressMiddleware',
]

if DEBUG and "test" not in sys.argv:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage"
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TZ')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'common.permissions.IsSuperUserOrReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


class IPAddressFilter(logging.Filter):
    def filter(self, record):
        record.ip = "-"
        if hasattr(record, 'request') and hasattr(record.request, "META"):
            # request is an WSGIRequest object ONLY with 4xx/5xx errors
            meta = record.request.META
            if meta.get("HTTP_X_FORWARDED_FOR"):
                record.ip = meta.get("HTTP_X_FORWARDED_FOR")
            if not record.ip or meta.get("REMOTE_ADDR"):
                record.ip = meta.get("REMOTE_ADDR")
        return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamp': {
            'format': '{ip:s} - - {asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'ip_address_filter': {
            '()': 'config.settings.IPAddressFilter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['ip_address_filter'],
            'formatter': 'timestamp'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False
        },
    },
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Darklite Partywiki',
    'DESCRIPTION': "You'll never travel alone - Even if you'd want to",
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['common.permissions.IsSuperUserOrReadOnly'],
}

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

TEMPUS_DOMINUS_LOCALIZE = True

STATIC_ROOT = env('STATIC_ROOT')
STATIC_URL = env('STATIC_URL')

MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SCENEID_LOGIN = env.bool('SCENEID_LOGIN')
SCENEID_HOST = env('SCENEID_HOST')
SCENEID_CLIENT_ID = env('SCENEID_CLIENT_ID')
SCENEID_SECRET = env('SCENEID_SECRET')
SCENEID_RETURN_BASE_URL = env('SCENEID_RETURN_BASE_URL')

FAIL2BAN_JAILS = env.list("FAIL2BAN_JAILS", default=[])

PLAUSIBLE_SITES = env.str("PLAUSIBLE_SITES", None)
PLAUSIBLE_SCRIPT_URL = env.str("PLAUSIBLE_SCRIPT_URL", None)
