import os

from astropy.io import fits
from django.test import TestCase

from data_access.utils import generate_absolute_path_to_data_cube
from ingestion.ingesters.ingest_data_cube import ingest_data_cube
from observations.models import Instrument, DataCube
from observations.utils.generate_observation_id import generate_observation_id


TEST_FITS_FILE =\
    '2019-04-19/CRISP/nb_6173_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-05-28T15:08:12_im.fits'


class TestIngestDataCube(TestCase):
    def setUp(self):
        Instrument.objects.bulk_create(
            [Instrument(name='CHROMIS', description=''), Instrument(name='CRISP', description='')])

        self.fits_file = generate_absolute_path_to_data_cube(TEST_FITS_FILE)

    def test_ingest_simple(self):
        instrument = Instrument.objects.get(name='CRISP')
        size = os.path.getsize(self.fits_file)

        self.assertTrue(os.path.exists(self.fits_file))

        oid = '2019-04-19T17:34:39_6173_0-4'
        ingest_data_cube(oid, self.fits_file,
                         generate_image_previews=True,
                         generate_video_previews=True)

        cube: DataCube = DataCube.objects.get(oid=oid)

        self.assertEqual(cube.instrument, instrument)
        self.assertEqual(cube.path, generate_absolute_path_to_data_cube(TEST_FITS_FILE))
        self.assertEqual(cube.size, size)

    def test_ingest_missing_file(self):
        fits_file = '/tmp/missing_file.fits'

        oid = '2019-04-19T17:34:39_6173_0-4'

        with self.assertRaises(FileNotFoundError):
            ingest_data_cube(oid, fits_file)

    def test_generate_observation_id(self):
        self.assertTrue(os.path.exists(self.fits_file))

        with fits.open(self.fits_file) as hdus:
            self.assertEqual('2019-04-19T17:34:55.50395_6173_0-4', generate_observation_id(hdus))
