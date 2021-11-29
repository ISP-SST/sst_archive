from astropy.io import fits

from data_access.ingesters.ingest_access_control_entities import ingest_access_control_entities
from ingestion.svo.submit_to_svo import submit_to_svo
from metadata.ingesters.ingest_fits_header import ingest_fits_header
from metadata.ingesters.ingest_metadata import ingest_metadata
from observations.ingesters.ingest_data_cube import ingest_observation_data_cube
from observations.ingesters.ingest_tags import ingest_tags, get_features_vocabulary, get_events_vocabulary
from observations.models import Instrument
from observations.utils.generate_observation_id import generate_observation_id
from previews.ingesters.ingest_image_previews import ingest_image_previews
from previews.ingesters.ingest_r0_data import ingest_r0_data
from previews.ingesters.ingest_spectral_line_profile_data import ingest_spectral_line_profile_data
from previews.ingesters.ingest_video_previews import ingest_video_previews


class IngestionError(Exception):
    pass


def _get_instrument_for_fits_file(primary_hdu_header: fits.Header):
    instrument_name = primary_hdu_header.get('INSTRUME', None)

    if not instrument_name:
        raise IngestionError('INSTRUME not found in FITS primary HDU')

    instrument_name = str(instrument_name).strip()
    instrument = Instrument.objects.get(name__iexact=instrument_name)

    return instrument


def ingest_data_cube(oid: str, path: str, **kwargs):
    """
    Main entry point for ingesting a data cube into the database.
    """
    generate_image_previews = kwargs.get('generate_image_previews', False)
    generate_video_previews = kwargs.get('generate_video_previews', False)
    force_regenerate_images = kwargs.get('force_regenerate_images', False)
    force_regenerate_video = kwargs.get('force_regenerate_videos', False)
    should_sync_with_svo = kwargs.get('sync_with_svo', False)

    owner_email_addresses = kwargs.get('owner_email_addresses', [])
    swedish_data = kwargs.get('swedish_data', False)

    with fits.open(path) as fits_hdus:
        primary_fits_hdu = fits_hdus[0].header

        if not oid:
            oid = generate_observation_id(fits_hdus)

        instrument = _get_instrument_for_fits_file(primary_fits_hdu)

        data_cube = ingest_observation_data_cube(path, instrument, primary_fits_hdu, oid)

        ingest_access_control_entities(data_cube, primary_fits_hdu, owner_email_addresses, swedish_data)

        ingest_fits_header(primary_fits_hdu, data_cube)

        ingest_metadata(primary_fits_hdu, data_cube)

        # TODO(daniel): Vocabulary is fetched from server. To speed this up when processing multiple
        #               cubes we can cache it between runs.
        features_vocabulary = get_features_vocabulary()
        events_vocabulary = get_events_vocabulary()
        ingest_tags(primary_fits_hdu, data_cube, features_vocabulary, events_vocabulary)

        ingest_r0_data(fits_hdus, data_cube)
        ingest_spectral_line_profile_data(fits_hdus, data_cube)

        if generate_image_previews:
            ingest_image_previews(fits_hdus, data_cube, regenerate_preview=force_regenerate_images)

        if generate_video_previews:
            ingest_video_previews(fits_hdus, data_cube, regenerate_preview=force_regenerate_video)

        if should_sync_with_svo:
            submit_to_svo(data_cube, primary_fits_hdu)

    return data_cube
