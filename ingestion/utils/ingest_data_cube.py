import datetime
from pathlib import Path

from astropy.io import fits

from data_access.models import DataCubeAccessControl
from ingestion.svo.sync_with_svo import sync_with_svo
from ingestion.utils.generate_sparse_list_string import generate_sparse_list_string
from ingestion.utils.ingest_fits_header import ingest_fits_header
from ingestion.utils.ingest_metadata import ingest_metadata
from ingestion.utils.ingest_tags import ingest_tags, get_features_vocabulary, get_events_vocabulary
from observations.models import DataCube, Instrument, Observation
from previews.ingesters.ingest_image_previews import update_or_create_image_previews
from previews.ingesters.ingest_r0_data import ingest_r0_data
from previews.ingesters.ingest_spectral_line_profile_data import ingest_spectral_line_profile_data
from previews.ingesters.ingest_video_previews import update_or_create_video_previews


def _generate_access_control_entities(data_cube: DataCube, fits_header: fits.Header):
    # Create access control row for this observation.
    release_date_str = fits_header.get('RELEASE', None)

    if release_date_str:
        release_date = datetime.datetime.strptime(release_date_str, "%Y-%m-%d").date()
        release_comment = fits_header.get('RELEASEC', None)
    else:
        release_date = datetime.datetime(datetime.MAXYEAR, 1, 1)
        release_comment = 'No release information provided. Release information needs to be updated.'

    access_control, created = DataCubeAccessControl.objects.update_or_create(data_cube=data_cube, defaults={
        'release_date': release_date,
        'release_comment': release_comment,
    })


def _assign_to_observation(data_cube: DataCube, fits_header: fits.Header):

    point_id = fits_header.get('POINT_ID', None)

    if not point_id:
        point_id = fits_header.get('DATE-BEG')

    if point_id.endswith('_grouped'):
        data_cube.grouping_tag = DataCube.GroupingTag.GROUPED
    elif point_id.endswith('_mosaic'):
        data_cube.grouping_tag = DataCube.GroupingTag.MOSAIC

    observation, created = Observation.objects.get_or_create(point_id=point_id)

    data_cube.observation = observation
    data_cube.save()


class IngestionError(Exception):
    pass


def _descend_into_multi_dim_array(array, levels, index=0):
    result = array
    for i in range(levels):
        result = result[index]
    return result

def generate_observation_id(hdus: fits.HDUList):
    """
    Generates an observation ID the same way the SSTRED pipeline does it when exporting cubes. It will generate a string
    on the form: "2019-04-16T08:20:18.96758_6173_0-36,38,39"

    The first part is the DATE-BEG keyword, the second part is the spectral line and the last part is the list of scans.
    """
    primary_fits_header = hdus[0].header

    date_beg = primary_fits_header['DATE-BEG']
    filter1 = primary_fits_header['FILTER1']

    try:
        scannum_ext_index = hdus.index_of('VAR-EXT-SCANNUM')

        scannum_ext = hdus[scannum_ext_index]
        scannum_col_name = scannum_ext.header['TTYPE1']
        scannum_dim = scannum_ext.header['TDIM1']

        scannum_field = scannum_ext.data.field(scannum_col_name)[0]

        dimensions_to_ignore = len(scannum_dim[1:-1].split(',')) - 1

        scan_numbers = [_descend_into_multi_dim_array(scannum, dimensions_to_ignore) for scannum in scannum_field]

        scannum_list = generate_sparse_list_string(scan_numbers)
    except KeyError as e:
        scannum_list = str(primary_fits_header['SCANNUM'])

    return '%s_%s_%s' % (date_beg.strip(), filter1.strip(), scannum_list)


def update_or_create_data_cube(fits_cube: str, instrument: Instrument, fits_header: fits.Header, oid=None):
    if not oid:
        oid = generate_observation_id(fits_header)

    fits_file_path = Path(fits_cube)

    data_cube, created = DataCube.objects.update_or_create(oid=oid, defaults={
        'path': fits_file_path,
        'filename': fits_file_path.name,
        'size': fits_file_path.stat().st_size,
        'instrument': instrument
    })

    # Determine if this data cube belongs to a new or existing observation.
    _assign_to_observation(data_cube, fits_header)

    _generate_access_control_entities(data_cube, fits_header)

    return data_cube


def _get_instrument_for_fits_file(primary_hdu_header: fits.Header):
    instrument_name = primary_hdu_header.get('INSTRUME', None)

    if not instrument_name:
        raise IngestionError('INSTRUME not found in FITS primary HDU')

    instrument_name = str(instrument_name).strip()
    instrument = Instrument.objects.get(name__iexact=instrument_name)

    return instrument


def ingest_data_cube(oid: str, path: str, **kwargs):
    """
    Main entry point for ingesting a data cube into the database. To do this, we right now only need
    two things: the observation ID (generated at the call site) and the
    """
    generate_image_previews = kwargs.get('generate_image_previews', False)
    generate_video_previews = kwargs.get('generate_video_previews', False)
    force_regenerate_images = kwargs.get('force_regenerate_images', False)
    force_regenerate_video = kwargs.get('force_regenerate_videos', False)
    should_sync_with_svo = kwargs.get('sync_with_svo', False)

    with fits.open(path) as fits_hdus:
        primary_hdu_header = fits_hdus[0].header

        instrument = _get_instrument_for_fits_file(primary_hdu_header)

        data_cube = update_or_create_data_cube(path, instrument, primary_hdu_header, oid)

        ingest_fits_header(primary_hdu_header, data_cube)

        ingest_metadata(primary_hdu_header, data_cube)

        # TODO(daniel): Vocabulary is fetched from server. To speed this up we can cache it between runs.
        features_vocabulary = get_features_vocabulary()
        events_vocabulary = get_events_vocabulary()
        ingest_tags(primary_hdu_header, data_cube, features_vocabulary, events_vocabulary)

        ingest_r0_data(fits_hdus, data_cube)
        ingest_spectral_line_profile_data(fits_hdus, data_cube)

        if generate_image_previews:
            update_or_create_image_previews(fits_hdus, data_cube, regenerate_preview=force_regenerate_images)

        if generate_video_previews:
            update_or_create_video_previews(fits_hdus, data_cube, regenerate_preview=force_regenerate_video)

        if should_sync_with_svo:
            sync_with_svo(data_cube, primary_hdu_header)

    return data_cube
