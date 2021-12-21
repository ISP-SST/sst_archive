from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse

from observations.models import DataCube


def get_file_url(data_cube: DataCube):
    return urljoin(settings.HOSTNAME, reverse('download_data_cube', args=[data_cube.filename]))
