from .common import *


ALLOWED_HOSTS = [] + SECRETS.get("allowed_hosts", [])

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = str(DATA_DIR.joinpath("public", "static"))
