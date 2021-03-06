from sst_archive.settings import *

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sst_archive',
        'USER': 'sst_archive',
        'HOST': 'localhost',
        'PASSWORD': get_secret('DB_PASSWORD'),
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES'
        }
    }
}

HOSTNAME = 'https://dubshen.astro.su.se'
ADMIN_EMAIL = 'noreply@dubshen.astro.su.se'

# TODO(daniel): This should be updated with the proper hostname of the service.
ALLOWED_HOSTS = ['dubshen.astro.su.se']

DEBUG = False

SECRET_KEY = get_secret('SECRET_KEY')

# TLS seems to not be set up for the localhost Postfix server.
EMAIL_USE_TLS = False

# Points to the science_data/ folder.
SCIENCE_DATA_ROOT = '/storage/science_data/'

PATH_ROOT = '/sst_archive'

STATIC_URL = PATH_ROOT + '/static/'
MEDIA_URL = PATH_ROOT + '/media/'

LOGIN_REDIRECT_URL = PATH_ROOT
LOGOUT_REDIRECT_URL = PATH_ROOT
ACCOUNT_LOGOUT_REDIRECT_URL = PATH_ROOT
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = PATH_ROOT
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = PATH_ROOT

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/sst_archive/sst_archive.log',
            'maxBytes': 10485760,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
