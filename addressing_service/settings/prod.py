from .base import *

# You should never enable this in production, even if it's temporarily
# All INSTALLED_APPS in django relies on this variable, like google-analytics app.
DEBUG = False

TEST_MODE = False

ALLOWED_HOSTS = ['*']

PROD_APPS = [
]

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^f)mh%0t_-jck5ir1#y^x79&y)2fexp3c&weq-a_k@_6x0cu*$'
