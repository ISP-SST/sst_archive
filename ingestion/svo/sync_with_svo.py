import os

from django.urls import reverse

from ingestion.svo.submit_record import SvoRecord
from sst_archive import settings


def get_file_url(filename):
    return reverse('download_data_cube', filename)


def get_file_path(instrument, date_beg):
    """
    Returns the SVO specific path based on instrument and observation date.
    SVO will use this relative path when creating a compressed archive of a selection of files.
    Each file will be placed in its corresponding file_path directory inside the compressed archive.
    """
    return os.path.join(str(date_beg), instrument)


def sync_with_svo(oid, filename, instrument, primary_fits_hdu):
    username = settings.SVO_USERNAME
    api_key = settings.SVO_API_KEY

    date_beg = primary_fits_hdu['DATE-BEG']

    file_path = get_file_path(instrument, date_beg)

    record = SvoRecord(oid=oid, fits_header=primary_fits_hdu, file_url=get_file_url(filename),
                       file_path=file_path, username=username, api_key=api_key, dataset=instrument,
                       thumbnail_url=None)

    if record.exists_in_svo():
        record.update()
    else:
        record.create()
