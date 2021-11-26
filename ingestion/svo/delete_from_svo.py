from django.conf import settings

from ingestion.svo.svo_api import SvoApi


def delete_from_svo(resource_uri, **kwargs):
    username = kwargs.get('username', settings.SVO_USERNAME)
    api_key = kwargs.get('api_key', settings.SVO_API_KEY)
    api_url = kwargs.get('api_url', settings.SVO_API_URL)

    dry_run = kwargs.get('dry_run', False)

    api = SvoApi(api_url, username, api_key)

    if dry_run:
        print('[dry-run] Would have deleted resource from SVO: %s' % resource_uri)
    else:
        print('Deleting resource from SVO: %s' % resource_uri)
        api(resource_uri).delete()
