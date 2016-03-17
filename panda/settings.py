"""
Django settings for panda project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'r04=z95t^(mcw_9ahqtjkb=h(qflaadvow=kuh#-vl8g$qt4e+')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('ENV', False)

ALLOWED_HOSTS = [
    ".apipanda.com",
    "panda.dev"
]
INTERNAL_IPS = (
    '127.0.0.1',
    '104.196.59.185'
)

HOST = 'apipanda.com'
SITE_ID = 1

# ADMINS = [
#     ('Bernard', 'bernardojengwa@gmail.com'),
# ]
# MANAGERS = [
#     ('Bernard', 'bernardojengwa@gmail.com'),
# ]
# Application definition
# DEFAULT_FROM_EMAIL = 'bernard@apipanda.com'
# SERVER_EMAIL = 'server@apipanda.com'

INSTALLED_APPS = (
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
)


THIRD_PARTY_APPS = (
    'experiments',
    'tastypie',
    'jsonfield',
    'jsonfield2',
    'django_ace',
    'kong_admin',
    'django_extensions',
    'subdomains'
)

LOCAL_APPS = (
    'app',
    'workspace',
    'endpoint',
    'plugin'
)

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'experiments.middleware.ExperimentsRetentionMiddleware',
)

ROOT_URLCONF = 'panda.urls.default'

SUBDOMAIN_URLCONFS = {
    None: 'panda.urls.default',
    'www': 'panda.urls.default',
    'api': 'panda.urls.api',
    'admin': 'panda.urls.admin',
    # 'docs': 'panda.urls.docs',
    # 'hubs': 'panda.urls.hubs',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'public/app/views')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

WSGI_APPLICATION = 'panda.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'NAME': os.getenv('DB_NAME', 'panda'),
            'PORT': os.getenv('DB_PORT', 5432),
            'USER': os.getenv('DB_USER', 'bernard'),
            'PASSWORD': os.getenv('DB_PASS', '[]')
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_PREFIX': 'APIPANDA_CACHE'
    }
}

# Authntication Backends
AUTHENTICATION_BACKENDS = (
    "app.backends.AuthBackend",
)

CSRF_COOKIE_DOMAIN = '.apipanda.com'
CSRF_TRUSTED_ORIGINS = [
    '.apipanda.com'
]

LOGIN_REDIRECT_URL = '/account'
LOGIN_URL = '/login'

SESSION_COOKIE_DOMAIN = '.apipanda.com'
SESSION_COOKIE_SECURE = not DEBUG

SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG
# SECURE_HSTS_SECONDS =
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = not DEBUG

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_COOKIE_NAME = 'apipanda_language'
LANGUAGES = [
    ('en', _('English')),
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, "public")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "public/site"),
    os.path.join(BASE_DIR, "public/app")
)

TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_DEFAULT_FORMATS = ['json', 'jsonp']

TASTYPIE_API_VERSION = 'v1'

KONG_ADMIN_URL = 'http://localhost:8001'
KONG_ADMIN_SIMULATOR = False

JET_DEFAULT_THEME = 'light-gray'
