from .common import *


ALLOWED_HOSTS = [] + SECRETS.get("allowed_hosts", [])
ADMINS = [] + SECRETS.get("admins", [])

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = str(DATA_DIR.joinpath("public", "static"))

MEDIALIB_TAG_SEARCH_LIMIT = 5
