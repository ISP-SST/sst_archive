import os

from django.test import TestCase

from ingestion.utils.ingest_data_cube import ingest_data_cube
from observations.models import Instrument, DataCube

TEST_FITS_FILE = '/Users/dani2978/local_science_data/2019-04-19/CRISP/nb_6173_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-05-28T15:08:12_im.fits'


class TestIngestDataCube(TestCase):
    def setUp(self):
        Instrument.objects.bulk_create(
            [Instrument(name='CHROMIS', description=''), Instrument(name='CRISP', description='')])

    def test_ingest_simple(self):
        fits_file = TEST_FITS_FILE
        instrument = Instrument.objects.get(name='CRISP')
        size = os.path.getsize(fits_file)

        self.assertTrue(os.path.exists(fits_file))

        oid = '2019-04-19T17:34:39_6173_0-4'
        ingest_data_cube(oid, fits_file)

        cube: DataCube = DataCube.objects.get(oid=oid)

        self.assertEqual(cube.instrument, instrument)
        self.assertEqual(cube.path, TEST_FITS_FILE)
        self.assertEqual(cube.size, size)

    def test_ingest_missing_file(self):
        fits_file = '/tmp/missing_file.fits'

        oid = '2019-04-19T17:34:39_6173_0-4'

        with self.assertRaises(FileNotFoundError):
            ingest_data_cube(oid, fits_file)
