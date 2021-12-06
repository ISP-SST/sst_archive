import datetime

from django.contrib.auth.models import User

from data_access.models import DataCubeUserGrant, DataCubeGroupGrant
from observations.models import DataCube


def data_cube_requires_access_grant(data_cube: DataCube, datetime_now=None):
    """
    Tests if access to the provided DataCube needs to be explicitly granted to any user.
    """
    if not datetime_now:
        datetime_now = datetime.datetime.now()

    if not data_cube.access_control or not data_cube.access_control.release_date:
        return False
    else:
        release_datetime = datetime.datetime.combine(
            data_cube.access_control.release_date, datetime.datetime.min.time())
        return release_datetime > datetime_now


def user_has_access_to_data_cube(user: User, data_cube: DataCube, datetime_now=None):
    """
    Tests if a user has access to a certain DataCube.
    """
    if not datetime_now:
        datetime_now = datetime.datetime.now()

    if not data_cube_requires_access_grant(data_cube, datetime_now):
        return True

    try:
        DataCubeUserGrant.objects.get(user_email=user.email, data_cube=data_cube)
        return True
    except DataCubeUserGrant.DoesNotExist:
        pass

    groups = DataCubeGroupGrant.objects.filter(data_cube=data_cube).values_list('group', flat=True)
    if user.groups.filter(id__in=groups).exists():
        return True

    return False


def get_data_cube_release_comments(data_cube):
    return data_cube.access_control.release_comment
