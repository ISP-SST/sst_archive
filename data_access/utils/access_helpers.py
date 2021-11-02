import datetime

import django
from django.contrib.auth.models import User
from pytz import utc

from data_access.models import DataCubeAccessToken, DataCubeUserGrant, DataCubeGroupGrant
from observations.models import DataCube


def data_cube_requires_access_grant(data_cube: DataCube, datetime_now=None):
    """
    Tests if access to the provided DataCube needs to be explicitly granted to any user.
    """
    if not datetime_now:
        datetime_now = django.utils.timezone.now()

    if not data_cube.access_control or not data_cube.access_control.release_date:
        return False
    else:
        release_datetime = utc.localize(datetime.datetime.combine(data_cube.access_control.release_date, datetime.datetime.min.time()))
        return release_datetime > datetime_now


def user_has_access_to_data_cube(user: User, data_cube: DataCube, datetime_now=None):
    """
    Tests if a user has access to a certain DataCube.
    """
    if not datetime_now:
        datetime_now = django.utils.timezone.now()

    if not data_cube_requires_access_grant(data_cube, datetime_now):
        return True

    try:
        DataCubeUserGrant.objects.get(user=user, data_cube=data_cube)
        return True
    except DataCubeUserGrant.DoesNotExist:
        pass

    groups = DataCubeGroupGrant.objects.filter(data_cube=data_cube).values_list('group', flat=True)
    if user.groups.filter(id__in=groups).exists():
        return True

    return False


def has_valid_token_for_data_cube(data_cube: DataCube, token_string: str, datetime_now=None):
    """
    Tests if a token grants access to a certain DataCube.
    """
    if not datetime_now:
        datetime_now = django.utils.timezone.now()

    if data_cube_requires_access_grant(data_cube, datetime_now):
        try:
            token = DataCubeAccessToken.objects.get(token_string=token_string, data_cube=data_cube)
            # FIXME(daniel): We should take the grant date into account and only allow downloads after that date,
            #                but due to apparent time skew we can't always assume that datetime_now will be after
            #                grant date if the token was added very recently.
            return datetime_now < token.expiration_date
        except DataCubeAccessToken.DoesNotExist:
            return False

    return True


def get_data_cube_release_comments(data_cube):
    return data_cube.access_control.release_comment
