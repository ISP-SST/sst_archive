import datetime

from astropy.io import fits

from data_access.models import DataCubeAccessControl, DataCubeUserGrant, grant_swedish_user_group_access_to_data_cube
from observations.models import DataCube


def ingest_access_control_entities(data_cube: DataCube, fits_header: fits.Header,
                                   owner_email_addresses=[],
                                   swedish_data=False):
    # Create access control row for this observation.
    release_date_str = fits_header.get('RELEASE', None)

    if release_date_str:
        release_date = datetime.datetime.strptime(release_date_str, "%Y-%m-%d").date()
        release_comment = fits_header.get('RELEASEC', None)
    else:
        release_date = datetime.datetime(datetime.MAXYEAR, 1, 1)
        release_comment = 'No release information provided. Release information needs to be updated.'

    # Allow updating of existing release information if the cube has already been ingested.
    access_control, created = DataCubeAccessControl.objects.update_or_create(data_cube=data_cube, defaults={
        'release_date': release_date,
        'release_comment': release_comment
    })

    if owner_email_addresses:
        for email_address in owner_email_addresses:
            grant = DataCubeUserGrant.objects.update_or_create(user_email=email_address, data_cube=data_cube)

    if swedish_data:
        grant_swedish_user_group_access_to_data_cube(data_cube)
