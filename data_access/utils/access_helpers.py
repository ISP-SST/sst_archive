import datetime

import django
from pytz import utc

from data_access.models import DataLocationAccessGrant, DataLocationAccessToken


def data_location_requires_access_grant(data_location, datetime_now=django.utils.timezone.now()):
    """Tests if access to the provided DataLocation needs to be explicitly granted to any user."""
    if not data_location.access_control or not data_location.access_control.release_date:
        return False
    else:
        release_datetime = utc.localize(datetime.datetime.combine(data_location.access_control.release_date, datetime.datetime.min.time()))
        return release_datetime > datetime_now


def has_access_to_data_location(user, data_location, datetime_now=django.utils.timezone.now()):
    """Tests if a user has access to a certain DataLocation."""
    if data_location_requires_access_grant(data_location, datetime_now):
        try:
            DataLocationAccessGrant.objects.get(user_email=user.email, data_location=data_location)
            return True
        except DataLocationAccessGrant.DoesNotExist:
            return False

    return True


def has_valid_token_for_data_location(data_location, token_string, datetime_now=django.utils.timezone.now()):
    """Tests if a token grants access to a certain DataLocation."""
    if data_location_requires_access_grant(data_location, datetime_now):
        try:
            token = DataLocationAccessToken.objects.get(token_string=token_string, data_location=data_location)
            return token.grant_date <= datetime_now < token.expiration_date
        except DataLocationAccessToken.DoesNotExist:
            return False

    return True


def get_data_location_release_comments(data_location):
    return data_location.access_control.release_comment
