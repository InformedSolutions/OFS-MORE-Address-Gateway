from .base import *

# You should never enable this in production, even if it's temporarily
# All INSTALLED_APPS in django relies on this variable, like google-analytics app.
DEBUG = True

TEST_MODE = os.environ.get('TEST_MODE', False)

OS_API_KEY = os.environ.get('OS_API_KEY')

ALLOWED_HOSTS = ['*']
PUBLIC_APPLICATION_URL = 'http://localhost:8000/addressing-service'

PROD_APPS = [
    'whitenoise',
]

PROD_MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS
MIDDLEWARE = MIDDLEWARE + PROD_MIDDLEWARE

# SECURITY WARNING: keep the secret key used in production secret!
# Note docker mounts are used for adjusting settings used on production instances
SECRET_KEY = '^f)mh%0t_-jck5ir1#y^x79&y)2fexp3c&weq-a_k@_6x0cu*$'
