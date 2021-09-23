from sst_archive.settings import *

# Database
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'sst_archive',
		'USER': 'sst_archive',
		'HOST': 'localhost',
		'PASSWORD': get_secret('DB_PASSWORD'),
	}
}

# TODO(daniel): This should be updated with the proper hostname of the service.
ALLOWED_HOSTS = ['*']

DEBUG = False

SECRET_KEY = get_secret('SECRET_KEY')

SCIENCE_DATA_ROOT = '/storage/science_data/'
