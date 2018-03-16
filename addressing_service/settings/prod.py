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

# Automatic Django logging at the INFO level (i.e everything the comes to the console when ran locally)
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        },
  'handlers': {
    'django.server': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1 * 1024 * 1024,
        'filename': 'logs/output.log',
        'formatter': 'console',
        'maxBytes': 1 * 1024 * 1024,
        'backupCount': '30'
    },
   },
   'loggers': {
     'django.server': {
       'handlers': ['django.server'],
         'level': 'INFO',
           'propagate': True,
      },
    },
}