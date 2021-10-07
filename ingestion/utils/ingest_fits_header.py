from astropy.io import fits

from metadata.models import FITSHeader
from observations.models import DataCube


def ingest_fits_header(fits_header: fits.Header, data_cube: DataCube):
    header, created = FITSHeader.objects.update_or_create(data_cube=data_cube, defaults={
        'fits_header': fits_header.tostring()
    })
