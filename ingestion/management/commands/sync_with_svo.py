import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from ingestion.svo.sync_with_svo import sync_with_svo


class Command(BaseCommand):
    help = 'Synchronizes the selected data cube with the SOLARNET Virtual Observatory.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--update-existing', action='store_true')
        parser.add_argument('--api-url', default=settings.SVO_API_URL)
        parser.add_argument('--api-username', default=settings.SVO_USERNAME)
        parser.add_argument('--api-key', default=settings.SVO_API_KEY)
        parser.add_argument('--verbose', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        update_existing = options['update_existing']

        api_url = options['api_url']
        api_username = options['api_username']
        api_key = options['api_key']
        verbose = options['verbose']

        if verbose:
            logger = logging.getLogger('SVO')
            dry_run_logger = logging.getLogger('SVO dry-run')

            formatter = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')

            for log in [logger, dry_run_logger]:
                log.setLevel(level=logging.DEBUG)

                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)
                ch.setFormatter(formatter)
                log.addHandler(ch)

        sync_with_svo(username=api_username, api_key=api_key, api_url=api_url, dry_run=dry_run,
                      update_existing=update_existing)
