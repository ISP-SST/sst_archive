from django.core.management.base import BaseCommand

from ingestion.ingesters.ingest_data_cube import ingest_data_cube
from observations.models import DataCube


class Command(BaseCommand):
    help = 'Re-ingests all data cubes that exist in the local database.'

    def add_arguments(self, parser):
        parser.add_argument('--generate-image-previews', action='store_true', help='Creates image previews as part of '
                                                                                   'the ingestion')
        parser.add_argument('--generate-video-previews', action='store_true', help='Creates video previews as part of '
                                                                                   'the ingestion')
        parser.add_argument('--force-regenerate-videos', action='store_true', help='Re-generates the video preview even'
                                                                                   ' if it exists')
        parser.add_argument('--force-regenerate-images', action='store_true', help='Re-generates the image preview even'
                                                                                   ' if it exists')

    def handle(self, *args, **options):
        for cube in DataCube.objects.all():
            ingest_data_cube(cube.path, **options)
