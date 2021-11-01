import os.path

from astropy.io import fits
from django.core.management.base import BaseCommand, CommandError

from ingestion.ingesters.ingest_data_cube import ingest_data_cube, generate_observation_id


class Command(BaseCommand):
    help = 'Ingests the specified FITS cube into the database.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fits-cube', required=True, type=str)
        parser.add_argument('-o', '--observation-id', required=False, default=None)
        parser.add_argument('--generate-image-previews', action='store_true')
        parser.add_argument('--generate-video-previews', action='store_true')
        parser.add_argument('--force-regenerate-videos', action='store_true')
        parser.add_argument('--force-regenerate-images', action='store_true')

    def handle(self, *args, **options):
        fits_file = options['fits_cube']

        if not os.path.exists(fits_file):
            raise CommandError('Provided FITS cube does not exist: %s' % fits_file)

        oid = options.get('observation_id', None)

        if not oid:
            try:
                with fits.open(fits_file) as hdus:
                    oid = generate_observation_id(hdus)
            except:
                raise CommandError('Cannot open provided FITS cube: %s' % fits_file)

        ingest_data_cube(oid, fits_file, **options)

