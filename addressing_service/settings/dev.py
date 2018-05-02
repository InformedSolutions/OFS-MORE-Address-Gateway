from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = "127.0.0.1"

DEV_APPS = [
  'debug_toolbar'
]

MIDDLEWARE_DEV = [
  'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS