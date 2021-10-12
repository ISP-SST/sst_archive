from django.core.management.base import BaseCommand, CommandError

from ingestion.utils.ingest_metadata import get_fits_hdu
from ingestion.svo.sync_with_svo import sync_with_svo
from observations.models import DataCube


class Command(BaseCommand):
    help = 'Synchronizes the selected data cube with the SOLARNET virtual observatory.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--observation-id', required=True)

    def handle(self, *args, **options):
        oid = options['observation_id']

        try:
            data_cube = DataCube.objects.fetch_related('metadata', 'instrument', 'fits_header').get(oid=oid)
        except DataCube.DoesNotExist:
            raise CommandError('Unknown OID, could not find a matching data cube in database')

        primary_fits_hdu = get_fits_hdu(data_cube.fits_header.fits_header)

        sync_with_svo(data_cube, primary_fits_hdu)
