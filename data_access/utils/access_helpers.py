import datetime

import django
from pytz import utc

from data_access.models import DataLocationAccessGrant, DataLocationAccessToken


def data_location_requires_access_grant(data_location, datetime_now=None):
    """Tests if access to the provided DataLocation needs to be explicitly granted to any user."""
    if not datetime_now:
        datetime_now = django.utils.timezone.now()

    if not data_location.access_control or not data_location.access_control.release_date:
        return False
    else:
        release_datetime = utc.localize(datetime.datetime.combine(data_location.access_control.release_date, datetime.datetime.min.time()))
        return release_datetime > datetime_now


def has_access_to_data_location(user, data_location, datetime_now=None):
    """Tests if a user has access to a certain DataLocation."""
    if not datetime_now:
        datetime_now = django.utils.timezone.now()

    if data_location_requires_access_grant(data_location, datetime_now):
        try:
            DataLocationAccessGrant.objects.get(user_email=user.email, data_location=data_location)
            return True
        except DataLocationAccessGrant.DoesNotExist:
            return False

    return True


def has_valid_token_for_data_location(data_location, token_string, datetime_now=None):
    """Tests if a token grants access to a certain DataLocation."""
    if not datetime_now:
        datetime_now = django.utils.timezone.now()

    if data_location_requires_access_grant(data_location, datetime_now):
        try:
            token = DataLocationAccessToken.objects.get(token_string=token_string, data_location=data_location)
            # FIXME(daniel): We should take the grant date into account and only allow downloads after that date,
            #                but due to apparent time skew we can't always assume that datetime_now will be after
            #                grant date if the token was added very recently.
            return datetime_now < token.expiration_date
        except DataLocationAccessToken.DoesNotExist:
            return False

    return True


def get_data_location_release_comments(data_location):
    return data_location.access_control.release_comment
