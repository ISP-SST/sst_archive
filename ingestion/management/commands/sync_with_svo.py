from django.conf import settings
from django.core.management.base import BaseCommand

from ingestion.svo.sync_with_svo import sync_with_svo


class Command(BaseCommand):
    help = 'Synchronizes the selected data cube with the SOLARNET Virtual Observatory.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--update-existing', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        update_existing = options['update_existing']

        sync_with_svo(username=settings.SVO_USERNAME, api_key=settings.SVO_API_KEY, api_url=settings.SVO_API_URL,
                      dry_run=dry_run, update_existing=update_existing)
