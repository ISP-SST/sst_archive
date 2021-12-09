import logging

from astropy.io import fits
from django.conf import settings

from ingestion.svo.delete_from_svo import delete_from_svo
from ingestion.svo.submit_to_svo import submit_to_svo
from ingestion.svo.svo_api import SvoApi
from ingestion.svo.svo_cache import SvoCache
from observations.models import DataCube, Instrument


REQUEST_METADATA_LIMIT = 50

logger = logging.getLogger('SVO')
dry_run_logger = logging.getLogger('SVO dry-run')


def _get_confirmation(info_message, confirmation_message):
    print(info_message)
    response = input(confirmation_message)
    if response.lower() in ['y', 'yes']:
        return True
    else:
        return False


def _submit_files_to_svo(filenames, **submit_kwargs):
    dry_run = submit_kwargs.get('dry_run', False)
    log = dry_run_logger if dry_run else logger

    cubes = DataCube.objects.filter(filename__in=filenames).select_related('fits_header')

    for cube in cubes:
        log.debug("Submitting cube with OID: %s" % cube.oid)
        hdus = fits.Header.fromstring(cube.fits_header.fits_header)
        submit_to_svo(cube, hdus, **submit_kwargs)


def _delete_resources_from_svo(resource_uris, **remove_kwargs):
    for uri in resource_uris:
        delete_from_svo(uri, **remove_kwargs)


def _get_list_string(elements):
    return ' * ' + '\n * '.join(elements)


def sync_with_svo(**kwargs):
    """
    Synchronize the metadata in the SOLARNET SVO with the contents of the local database. The rules for
    synchronization are:

     * Remove entries in the SVO that do not exist in the local database
     * Add entries to the SVO that only exist in the local database
     * Optionally update all entries that exist in both the SVO and the local database
    """
    username = kwargs.get('username', settings.SVO_USERNAME)
    api_key = kwargs.get('api_key', settings.SVO_API_KEY)
    api_url = kwargs.get('api_url', settings.SVO_API_URL)

    dry_run = kwargs.get('dry_run', False)
    prompt = kwargs.get('prompt', False)
    update_existing = kwargs.get('update_existing', False)

    logger.debug("Synchronizing with API at %s" % api_url)

    if dry_run:
        logger.debug("Doing a dry run")

    svo_api = SvoApi(api_url, username, api_key)
    svo_cache = SvoCache(svo_api)

    instruments = Instrument.objects.only('name').values_list('name', flat=True)

    cube_filenames_to_submit = []
    cube_filenames_to_update = []
    svo_obs_to_remove = set()

    for instrument in instruments:
        dataset = svo_api.dataset(instrument).get()

        metadata_root_uri = dataset['metadata']['resource_uri']

        metadata_results = svo_api(metadata_root_uri).get(limit=REQUEST_METADATA_LIMIT)

        missing_cubes = set(DataCube.objects.filter(instrument__name=instrument).only('filename').values_list(
            'filename', flat=True))

        while metadata_results:
            objects = metadata_results['objects']

            for object in objects:
                oid = object['oid']
                filename = object['filename']

                try:
                    data_cube = DataCube.objects.get(oid=oid)
                    missing_cubes.remove(filename)

                    if update_existing:
                        cube_filenames_to_update.append(filename)

                except DataCube.DoesNotExist:
                    # Observation exists only in SVO, should be removed.
                    svo_obs_to_remove.add((filename, object['resource_uri']))

            next = metadata_results['meta']['next']
            if next:
                offset = metadata_results['meta']['offset']
                limit = metadata_results['meta']['limit']
                metadata_results = svo_api(metadata_root_uri).get(limit=limit, offset=offset + limit)
            else:
                metadata_results = None

        cube_filenames_to_submit += missing_cubes

    if cube_filenames_to_update:
        _submit_files_to_svo(cube_filenames_to_update, svo_cache=svo_cache, **kwargs)

    if cube_filenames_to_submit:
        confirmed = True

        if prompt:
            filename_list = _get_list_string(cube_filenames_to_submit)
            info_message = "The following files are not present in the SOLARNET SVO but are present in the local " \
                           "database:\n" + filename_list
            confirmation_message = "Do you want to submit them (y/N)? "
            confirmed = _get_confirmation(info_message, confirmation_message)

        if confirmed:
            _submit_files_to_svo(cube_filenames_to_submit, svo_cache=svo_cache, **kwargs)

    if svo_obs_to_remove:
        confirmed = True

        if prompt:
            obs_id_list = _get_list_string([o[0] for o in svo_obs_to_remove])
            info_message = "The following files are present in the SOLARNET SVO but do not exist in the local " \
                           "database: \n" + obs_id_list
            confirmation_message = "Do you want to remove them from the SOLARNET SVO (y/N)? "
            confirmed = _get_confirmation(info_message, confirmation_message)

        if confirmed:
            resource_uris = [obs[1] for obs in svo_obs_to_remove]
            _delete_resources_from_svo(resource_uris, svo_cache=svo_cache, **kwargs)
