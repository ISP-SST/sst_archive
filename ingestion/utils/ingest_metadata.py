from datetime import datetime
import re

from astropy.io import fits

from django.utils.timezone import make_aware

from metadata.models import Metadata
from sst_archive import settings

try:
    import zoneinfo
except ImportError:
    # FIXME(daniel): This is a temporary fix for running on Python 3.7. Upgrading to 3.9 should remove the
    #                need for this special case. Note that for now backports.zoneinfo needs to be pip
    #                installed in order to run the service on Python < 3.9.
    from backports import zoneinfo


def _modelify_fits_keyword(keyword):
    """
    Transforms a FITS keyword to a valid variable name.
    """
    lower_keyword = str(keyword).lower()
    return re.sub(r'[\-\ \.]', '_', lower_keyword)


def create_or_update_metadata(fits_header_hdu, data_cube):
    model_type = Metadata

    fields = [field.name for field in model_type._meta.get_fields()]

    properties = {}

    for key in fits_header_hdu:
        model_keyword = _modelify_fits_keyword(key)
        if model_keyword in fields:
            properties[model_keyword] = fits_header_hdu.get(key)

    model, created = Metadata.objects.get_or_create(data_cube=data_cube, defaults=properties)

    # TODO(daniel): This update code ensures that dates are proplery timezoned before assigning
    #               to the Django model instance. However, since we use get_or_create() above,
    #               any brand new Metadata instances will first assign the dates without proper
    #               timezone attached to them. We could fix this by first iterating over the
    #               properties and determining which fields need to be converted, and then send
    #               all the processed properties into the get_or_create(). Or even better, use the
    #               create_or_update() helper.
    for (key, value) in properties.items():
        attr = getattr(model, key)
        if isinstance(attr, datetime):
            try:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

            timezone = zoneinfo.ZoneInfo(settings.OBSERVATION_TIMEZONE)
            value = make_aware(value, timezone=timezone)

        setattr(model, key, value)

    model.data_cube = data_cube
    model.save()


class InvalidFITSHeader(Exception):
   pass


def ingest_metadata(fits_header_data, data_cube):
    fits_header_hdu = fits.Header.fromstring(fits_header_data)

    # Apparently fromstring() never trows an exception, it just does
    # the best it can and serves us the result. The one thing we can check
    # for is a completely empty header.
    if not fits_header_hdu:
        raise InvalidFITSHeader('FITS header data is empty, damaged or otherwise invalid')

    return create_or_update_metadata(fits_header_hdu, data_cube)
