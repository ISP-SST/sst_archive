import datetime

from astropy.io import fits

from data_access.models import DataCubeAccessControl
from observations.models import DataCube


def ingest_access_control_entities(data_cube: DataCube, fits_header: fits.Header):
    # Create access control row for this observation.
    release_date_str = fits_header.get('RELEASE', None)

    if release_date_str:
        release_date = datetime.datetime.strptime(release_date_str, "%Y-%m-%d").date()
        release_comment = fits_header.get('RELEASEC', None)
    else:
        release_date = datetime.datetime(datetime.MAXYEAR, 1, 1)
        release_comment = 'No release information provided. Release information needs to be updated.'

    # TODO(daniel): Determine what should happen with this data when updating, since this information
    #               might only exist in the database. Overwriting everything is likely not something we'd like
    #               to have happen.
    access_control, created = DataCubeAccessControl.objects.update_or_create(data_cube=data_cube, defaults={
        'release_date': release_date,
        'release_comment': release_comment
    })
