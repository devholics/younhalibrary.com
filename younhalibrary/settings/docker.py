from .common import *


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "www.127.0.0.1"]

DEBUG = True
