from .base import *

DEBUG = True

TEST_MODE = True

ALLOWED_HOSTS = ['*']
PUBLIC_APPLICATION_URL = 'http://mcriscd01:8000/addressing-service'
INTERNAL_IPS = "127.0.0.1"

DEV_APPS = [
  'debug_toolbar'
]

MIDDLEWARE_DEV = [
  'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^87(*&(*&Asdajlkjasdaau*()**)POAKLSMDA<<<<ZNc'

