from django.test import TestCase

from data_access.utils.get_file_url import get_file_url
from observations.models import DataCube
from django.conf import settings


class TestUtils(TestCase):
    def test_get_file_url(self):
        settings.HOSTNAME = 'http://localhost:80/'

        data_cube = DataCube(oid='dummy', filename='test.fits')
        self.assertEqual(get_file_url(data_cube), 'http://localhost:80/download/test.fits')
