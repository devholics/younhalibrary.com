from .common import *


ALLOWED_HOSTS = [
    'www.younhalibrary.com',
    'younhalibrary.com',
    'api.younhalibrary.com',
] + SECRETS.get("allowed_hosts", [])
ADMINS = [] + SECRETS.get("admins", [])

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = str(DATA_DIR.joinpath("public", "static"))

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIALIB_TAG_SEARCH_LIMIT = 5

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]
REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
    'rest_framework.permissions.IsAuthenticated',
]
