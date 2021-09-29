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

# TODO(daniel): This should be updated with the proper hostname of the service.
ALLOWED_HOSTS = ['*']

DEBUG = True

SECRET_KEY = get_secret('SECRET_KEY')

# Points to a read-only science data folder that has been mounted.
SCIENCE_DATA_ROOT = '/srv/www/dubshen/sst_archive/science_data/'

STATIC_URL = '/sst_archive/static/'
