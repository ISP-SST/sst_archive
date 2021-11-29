import os
import tempfile
from datetime import datetime

from astropy.io import fits
from django.test import TestCase, override_settings

from data_access.utils import generate_absolute_path_to_data_cube
from ingestion.ingesters.ingest_data_cube import ingest_data_cube
from observations.models import Instrument, DataCube
from observations.utils.generate_observation_id import generate_observation_id
from previews.ingesters.ingest_image_previews import THUMBNAIL_WIDTH_PX

"""
This test requires a science_data/ directory to be accessible in the local filesystem.

Make sure that the SCIENCE_DATA_ROOT is set correctly in the settings for the dev environment.
"""


TEST_FITS_FILE =\
    '2019-04-19/CRISP/nb_6173_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-05-28T15:08:12_im.fits'


@override_settings(
    MEDIA_ROOT=tempfile.gettempdir(),
)
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

        # Compare a small sample of the extracted metadata.
        self.assertEqual(cube.metadata.date_beg, datetime(2019, 4, 19, 17, 34, 55, 503950))
        self.assertEqual(cube.metadata.release, '2020-08-05')
        self.assertEqual(cube.metadata.cname3, 'Wavelength')

        # Check that preview images have been ingested.
        thumbnail_size = cube.previews.thumbnail.size
        self.assertGreater(thumbnail_size, 0)
        self.assertEqual(cube.previews.thumbnail.width, THUMBNAIL_WIDTH_PX)

        full_size_size = cube.previews.full_size.size
        self.assertGreater(full_size_size, 0)
        self.assertGreater(full_size_size, thumbnail_size)
        self.assertGreater(cube.previews.full_size.width, THUMBNAIL_WIDTH_PX)

        # Check that spectral line data preview has been ingested.
        self.assertGreater(cube.spectral_line_data.data_preview.size, 0)

    def test_ingest_missing_file(self):
        fits_file = '/tmp/missing_file.fits'

        oid = '2019-04-19T17:34:39_6173_0-4'

        with self.assertRaises(FileNotFoundError):
            ingest_data_cube(oid, fits_file)

    def test_generate_observation_id(self):
        self.assertTrue(os.path.exists(self.fits_file))

        with fits.open(self.fits_file) as hdus:
            self.assertEqual('2019-04-19T17:34:55.50395_6173_0-4', generate_observation_id(hdus))
