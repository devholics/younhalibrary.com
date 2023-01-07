from .common import *


ALLOWED_HOSTS = [] + SECRETS.get("allowed_hosts", [])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
