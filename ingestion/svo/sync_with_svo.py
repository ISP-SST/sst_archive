import os
import re

from data_access.utils.get_file_url import get_file_url
from ingestion.svo.submit_record import SvoRecord
from django.conf import settings


def filter_file_path(path):
    """
    Filters out characters that the SVO does not like to see in the file paths.
    """
    return re.sub(r'[\:]', '', path)


def get_file_path(data_cube):
    """
    Returns the SVO specific path based on instrument and observation date.
    SVO will use this relative path when creating a compressed archive of a selection of files.
    Each file will be placed in its corresponding file_path directory inside the compressed archive.
    """
    date_beg = data_cube.metadata.date_beg.date()
    return os.path.join(str(date_beg), data_cube.instrument.name, filter_file_path(data_cube.filename))


def sync_with_svo(data_cube, primary_fits_hdu, **kwargs):
    username = kwargs.get('username', settings.SVO_USERNAME)
    api_key = kwargs.get('api_key', settings.SVO_API_KEY)
    api_url = kwargs.get('api_url', settings.SVO_API_URL)

    file_url = kwargs.get('file_url', get_file_url(data_cube))
    file_path = kwargs.get('file_path',  get_file_path(data_cube))

    record = SvoRecord(oid=data_cube.oid, fits_header=primary_fits_hdu, file_url=file_url,
                       file_path=file_path, file_size=data_cube.size, username=username, api_key=api_key,
                       api_url=api_url, dataset=data_cube.instrument.name, thumbnail_url=None)

    if record.exists_in_svo():
        record.update()
    else:
        record.create()
