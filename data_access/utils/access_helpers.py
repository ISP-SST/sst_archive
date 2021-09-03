import datetime

from data_access.models import DataLocationAccessGrant


def data_location_requires_login(data_location, date=datetime.date.today()):
    """Tests if access to the provided DataLocation needs to be explicitly granted to any user."""
    if not data_location.access_control or not data_location.access_control.release_date:
        return False
    else:
        return data_location.access_control.release_date > date


def has_access_to_data_location(user, data_location, date=datetime.date.today()):
    """Tests if a user has access to a certain DataLocation."""
    if data_location_requires_login(data_location, date):
        try:
            DataLocationAccessGrant.objects.get(user_email=user.email, data_location=data_location)
            return True
        except DataLocationAccessGrant.DoesNotExist:
            return False

    return True
