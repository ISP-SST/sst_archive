from datetime import datetime
import re

import django.db.models.fields
from astropy.io import fits
from django.utils.timezone import make_aware

from metadata.models import Metadata
from observations.models import DataCube
from django.conf import settings

try:
    import zoneinfo
except ImportError:
    # FIXME(daniel): This is a temporary fix for running on Python 3.7. Upgrading to 3.9 should remove the
    #                need for this special case. Note that for now backports.zoneinfo needs to be pip
    #                installed in order to run the service on Python < 3.9.
    from backports import zoneinfo


class InvalidFITSHeader(Exception):
    pass


def get_fits_hdu(fits_header_data):
    fits_header_hdu = fits.Header.fromstring(fits_header_data)

    # Apparently fromstring() never trows an exception, it just does
    # the best it can and serves us the result. The one thing we can check
    # for is a completely empty header.
    if not fits_header_hdu:
        raise InvalidFITSHeader('FITS header data is empty, damaged or otherwise invalid')

    return fits_header_hdu


def _modelify_fits_keyword(keyword: str) -> str:
    """
    Transforms a FITS keyword to a valid variable name.
    """
    lower_keyword = str(keyword).lower()
    return re.sub(r'[\-\ \.]', '_', lower_keyword)


def _translate_field(field_value: str, field_type):
    """
    Translate the value to a type that can be safely converted into the target model field.
    This is especially important for DateTimeFields where the input string does not include
    timezone information.

    :param field_value:
    :param field_type:
    :return:
    """
    if field_type == django.db.models.fields.DateTimeField:
        try:
            field_value = datetime.strptime(field_value, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            field_value = datetime.strptime(field_value, '%Y-%m-%dT%H:%M:%S')

        timezone = zoneinfo.ZoneInfo(settings.OBSERVATION_TIMEZONE)
        return make_aware(field_value, timezone=timezone)

    return field_value


def ingest_metadata(fits_header_hdu: fits.header.Header, data_cube: DataCube):
    fields = {field.name: type(field) for field in Metadata._meta.get_fields()}

    properties = {}

    for key in fits_header_hdu:
        model_keyword = _modelify_fits_keyword(key)
        if model_keyword in fields:
            translated_value = _translate_field(fits_header_hdu.get(key), fields[model_keyword])
            properties[model_keyword] = translated_value

    model, created = Metadata.objects.get_or_create(data_cube=data_cube, defaults=properties)

    if not created:
        for (key, value) in properties.items():
            setattr(model, key, value)

    model.data_cube = data_cube
    model.save()
