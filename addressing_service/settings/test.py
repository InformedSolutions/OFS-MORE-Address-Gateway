from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

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
        'backupCount': 30
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