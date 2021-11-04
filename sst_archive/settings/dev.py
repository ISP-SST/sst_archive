from sst_archive.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

HOSTNAME = 'http://localhost:8000/'

SCIENCE_DATA_ROOT = '/Users/dani2978/science_data/'

SECRET_KEY = 'django-insecure-b0ddy$h-j+*9$emw*!92l4tip7&8q)vj%7-m$hr_ksj1xwf7ih'

DEBUG = True
INSTALLED_APPS += ['debug_toolbar']
DEBUG_QUERY_LOGGING = False

if DEBUG_QUERY_LOGGING:
    LOGGING = {
        'version': 1,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            }
        }
    }

# Use Gmail email server for local tests. Credentials need to be specified in the secrets.json file.
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
