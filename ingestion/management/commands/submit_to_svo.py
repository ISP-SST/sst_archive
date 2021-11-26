from django.core.management.base import BaseCommand, CommandError

from ingestion.svo.submit_to_svo import submit_to_svo
from metadata.ingesters.ingest_metadata import get_fits_hdu
from observations.models import DataCube


class Command(BaseCommand):
    help = 'Submits the selected data cube in the database to the SOLARNET Virtual Observatory.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--observation-id', required=True)

    def handle(self, *args, **options):
        oid = options['observation_id']

        try:
            data_cube = DataCube.objects.fetch_related('metadata', 'instrument', 'fits_header').get(oid=oid)
        except DataCube.DoesNotExist:
            raise CommandError('Unknown OID, could not find a matching data cube in database')

        primary_fits_hdu = get_fits_hdu(data_cube.fits_header.fits_header)

        submit_to_svo(data_cube, primary_fits_hdu)
