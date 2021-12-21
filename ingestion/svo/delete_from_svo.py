import logging

from django.conf import settings

from ingestion.svo.svo_api import SvoApi

logger = logging.getLogger('SVO')
dry_run_logger = logging.getLogger('SVO dry-run')


def delete_from_svo(resource_uri, **kwargs):
    username = kwargs.get('username', settings.SVO_USERNAME)
    api_key = kwargs.get('api_key', settings.SVO_API_KEY)
    api_url = kwargs.get('api_url', settings.SVO_API_URL)

    dry_run = kwargs.get('dry_run', False)

    api = SvoApi(api_url, username, api_key)

    log = dry_run_logger if dry_run else logger

    log.debug('Deleting resource from SVO: %s' % resource_uri)
    api(resource_uri).delete()
