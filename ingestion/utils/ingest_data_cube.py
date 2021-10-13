from datetime import datetime
from pathlib import Path

from astropy.io import fits
from rest_framework.exceptions import ValidationError

from data_access.models import DataCubeAccessControl
from ingestion.utils.generate_sparse_list_string import generate_sparse_list_string
from ingestion.utils.ingest_animated_preview import update_or_create_gif_preview
from ingestion.utils.ingest_fits_header import ingest_fits_header
from ingestion.utils.ingest_image_preview import update_or_create_image_preview
from ingestion.utils.ingest_metadata import InvalidFITSHeader
from ingestion.utils.ingest_metadata import ingest_metadata
from ingestion.svo.sync_with_svo import sync_with_svo
from observations.models import DataCube, Instrument


def _generate_access_control_entities(data_cube: DataCube, fits_header: fits.header.Header):
    # Create access control row for this observation.
    release_date_str = fits_header['RELEASE']
    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()

    release_comment = fits_header['RELEASEC']

    access_control, created = DataCubeAccessControl.objects.update_or_create(data_cube=data_cube, defaults={
        'release_date': release_date,
        'release_comment': release_comment,
    })


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

    scannum_ext_index = hdus.index_of('VAR-EXT-SCANNUM')
    scannum_ext = hdus[scannum_ext_index]
    scannum_col_name = scannum_ext.header['TTYPE1']
    scannum_dim = scannum_ext.header['TDIM1']

    scannum_field = scannum_ext.data.field(scannum_col_name)[0]

    dimensions_to_ignore = len(scannum_dim[1:-1].split(',')) - 1

    scan_numbers = [_descend_into_multi_dim_array(scannum, dimensions_to_ignore) for scannum in scannum_field]

    scannum_list = generate_sparse_list_string(scan_numbers)

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

    _generate_access_control_entities(data_cube, fits_header)

    return data_cube


def ingest_data_cube(oid: str, path: str, tags_data=[], **kwargs):
    """

    :param oid:
    :param path:
    :param instrument: an instance of the Instrument model class, or a string containing the name of the instrument
    :param tags_data:
    :return:
    """
    generate_image_previews = kwargs.get('generate_image_previews', False)
    generate_animated_previews = kwargs.get('generate_animated_previews', False)
    regenerate_preview = False
    should_sync_with_svo = kwargs.get('sync_with_svo', False)

    instrument = kwargs['instrument'] if 'instrument' in kwargs else None

    with fits.open(path) as fits_hdus:
        primary_hdu_header = fits_hdus[0].header

        if not instrument:
            if 'INSTRUME' not in primary_hdu_header:
                raise IngestionError('INSTRUME not found in FITS primary HDU')

            instrument_name = str(primary_hdu_header['INSTRUME']).strip()
            instrument = Instrument.objects.get(name__iexact=instrument_name)

        data_cube = update_or_create_data_cube(path, instrument, primary_hdu_header, oid)

        ingest_fits_header(primary_hdu_header, data_cube)

        try:
            ingest_metadata(primary_hdu_header, data_cube)
        except InvalidFITSHeader as e:
            raise ValidationError(e)

        data_cube.tags.set(tags_data)

        if generate_image_previews:
            update_or_create_image_preview(fits_hdus, data_cube, regenerate_preview)

        if generate_animated_previews:
            update_or_create_gif_preview(fits_hdus, data_cube)

        if should_sync_with_svo:
            sync_with_svo(data_cube, primary_hdu_header)

    return data_cube
