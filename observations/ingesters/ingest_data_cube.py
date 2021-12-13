from pathlib import Path

from astropy.io import fits

from observations.models import Instrument, DataCube, Observation


def _assign_to_observation(data_cube: DataCube, primary_fits_hdu: fits.Header):
    point_id = primary_fits_hdu.get('POINT_ID', None)

    if not point_id:
        point_id = str(primary_fits_hdu.get('DATE-BEG')).strip()

    if point_id.endswith('_grouped'):
        data_cube.grouping_tag = DataCube.GroupingTag.GROUPED
    elif point_id.endswith('_mosaic'):
        data_cube.grouping_tag = DataCube.GroupingTag.MOSAIC

    observation, created = Observation.objects.get_or_create(point_id=point_id)

    data_cube.observation = observation
    data_cube.save()


def ingest_observation_data_cube(fits_cube: str, instrument: Instrument, primary_fits_hdu: fits.Header, oid,
                                 file_size=None):
    fits_file_path = Path(fits_cube)

    if file_size is None:
        file_size = fits_file_path.stat().st_size

    data_cube, created = DataCube.objects.update_or_create(oid=oid, defaults={
        'path': fits_file_path,
        'filename': fits_file_path.name,
        'size': file_size,
        'instrument': instrument
    })

    # Determine if this data cube belongs to a new or existing observation.
    _assign_to_observation(data_cube, primary_fits_hdu)

    return data_cube
