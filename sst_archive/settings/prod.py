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

HOSTNAME = 'https://dubshen.astro.su.se/'
ADMIN_EMAIL = 'noreply@dubshen.astro.su.se'

# TODO(daniel): This should be updated with the proper hostname of the service.
ALLOWED_HOSTS = ['*']

DEBUG = True

SECRET_KEY = get_secret('SECRET_KEY')

# TLS seems to not be set up for the localhost Postfix server.
EMAIL_USE_TLS = False

# Points to a read-only science data folder that has been mounted.
SCIENCE_DATA_ROOT = '/srv/www/dubshen/sst_archive/science_data/'

STATIC_URL = '/sst_archive/static/'
MEDIA_URL = '/sst_archive/media/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/sst_archive/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/sst_archive/sst_archive.log',
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

