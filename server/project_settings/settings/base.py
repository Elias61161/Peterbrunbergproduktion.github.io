"""
Django settings for project_settings project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# TODO: Check all settings and which forces new migration. Add comments as warnings.

from django.utils.log import DEFAULT_LOGGING
from django.utils.translation import gettext_lazy as _

try:
    from .local import *
except:
    from .local_template import *


def join_paths(*args, leading_slash=False, trailing_slash=True):
    return ("/" if leading_slash else "") + "/".join([str(arg).strip('/') for arg in args]) + ("/" if trailing_slash else "")


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Version settings
BASE_SETTINGS_VERSION = 1
assert BASE_SETTINGS_VERSION == LOCAL_SETTINGS_VERSION


# Security
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
if SECRET_KEY_PATH:
    with open(SECRET_KEY_PATH) as f:
        SECRET_KEY = f.read().strip()
else:
    SECRET_KEY = 'NOT-SO-SECRET-DEFAULT-KEY'
    
ADMINS = [('admin', 'webmaster@f.kth.se')]
MANAGERS = ADMINS


# Application definition
ROOT_URLCONF = 'project_settings.urls'
WSGI_APPLICATION = 'project_settings.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'guardian',
    'adminsortable',
    'authentication',
    'website'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_ROOT / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static'
            ],
        },
    },
]

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': PROJECT_ROOT / 'cache',
    }
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'sv'
LANGUAGES = [
    ('sv', _('Swedish')),
    ('en', _('English'))
]
LOCALE_PATHS = [
    PROJECT_ROOT / 'locale'
]
TIME_ZONE = 'Europe/Stockholm'
USE_I18N = True
USE_L10N = True
USE_TZ = True
FIRST_DAY_OF_WEEK = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = join_paths(ROOT_URL, 'public', 'staticfiles')
STATIC_ROOT = PUBLIC_ROOT / 'staticfiles'
STATICFILES_DIRS = [
    "static"
]

MEDIA_URL = join_paths(ROOT_URL, 'public', 'mediafiles')
MEDIA_ROOT = PUBLIC_ROOT / 'mediafiles'


# Assure that errors end up to Apache error logs via console output
# when debug mode is disabled
DEFAULT_LOGGING['handlers']['console']['filters'] = []
# Enable logging to console from our modules by configuring the root logger
DEFAULT_LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': True
}


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'URL_FIELD_NAME': 'detail_url'
}

AUTH_USER_MODEL = 'authentication.user'
ANONYMOUS_USER_NAME = None

# Årskursnamn
# (Attention! adding to, removing from or changing any of the objects of the list requires a migration)
CHAPTER_YEARS = [
    ("F-20", "F-20 Fotnot"), ("F-19", "F-19 Fasett"), ("F-18", "F-18 Flingsalt"), ("F-17", "F-17 Förarlös"),
    ("F-16", "F-16 Fuskbygge"), ("F-15", "F-15 Fanclub"), ("F-14", "F-14 Folkvett"), ("F-13", "F-13 Frågvis?")
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
