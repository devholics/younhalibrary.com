import json
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

BASE_DIR = PROJECT_PACKAGE.parent

data_dir_key = "YOUNHA_DATA_DIR"
DATA_DIR = (
    Path(os.environ[data_dir_key]) if data_dir_key in os.environ else BASE_DIR.parent
)

try:
    with DATA_DIR.joinpath("conf", "secrets.json").open() as handle:
        SECRETS = json.load(handle)
except IOError:
    SECRETS = {
        "secret_key": "a"
    }


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(SECRETS["secret_key"])


# Application definition

INSTALLED_APPS = [
    'medialib.apps.MedialibConfig',

    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'rest_framework',
]

MIDDLEWARE = [
    'younha.middleware.APIMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'younha.urls.www'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PROJECT_PACKAGE.joinpath('templates'))],
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

WSGI_APPLICATION = 'younha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'younha',
        'USER': 'younha',
        'HOST': SECRETS.get('db_host', ''),
        'PASSWORD': SECRETS.get('db_password', ''),
        'PORT': SECRETS.get('db_port', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [str(PROJECT_PACKAGE.joinpath('static'))]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MediaLib

MEDIALIB_PAGINATION = 12
MEDIALIB_TAG_LIMIT = 30
MEDIALIB_CREATOR_LIMIT = 30
MEDIALIB_TAG_SEARCH_LIMIT = 2

# Django sites framework

SITE_ID = 1
