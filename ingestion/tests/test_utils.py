from django.test import TestCase

from ingestion.svo.sync_with_svo import filter_file_path


class TestUtils(TestCase):

    def test_filter_filename(self):
        self.assertEqual(
            filter_file_path(
                'nb_6302_2016-09-19T09:30:20_scans=12-16_stokes_corrected_export2019-06-14T14:48:13_im.fits'),
            'nb_6302_2016-09-19T093020_scans=12-16_stokes_corrected_export2019-06-14T144813_im.fits')
