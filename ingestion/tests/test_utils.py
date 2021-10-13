from django.test import TestCase

from ingestion.svo.sync_with_svo import filter_file_path
from ingestion.utils.generate_sparse_list_string import generate_sparse_list_string


class TestUtils(TestCase):

    def test_filter_filename(self):
        self.assertEqual(
            filter_file_path(
                'nb_6302_2016-09-19T09:30:20_scans=12-16_stokes_corrected_export2019-06-14T14:48:13_im.fits'),
            'nb_6302_2016-09-19T093020_scans=12-16_stokes_corrected_export2019-06-14T144813_im.fits')

    def test_generate_sparse_list_string(self):
        self.assertEqual(generate_sparse_list_string([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), '0-9')
        self.assertEqual(generate_sparse_list_string([0, 2, 4, 6, 8, 10]), '0,2,4,6,8,10')
        self.assertEqual(generate_sparse_list_string([0, 1, 2, 3, 5, 6, 9]), '0-3,5-6,9')
