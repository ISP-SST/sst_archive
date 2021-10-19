import json

from astropy.io import fits

from ingestion.utils.generate_spectral_line_profile_data import generate_spectral_line_profile_data
from observations.models import DataCube
from previews.models import SpectralLineData


def ingest_spectral_line_profile_data(hdus: fits.HDUList, data_cube: DataCube):
    json_data = generate_spectral_line_profile_data(hdus)

    spectral_line_data, created = SpectralLineData.objects.update_or_create(data_cube=data_cube, defaults={
        'data_json': json.dumps(json_data),
        'data_version': 1
    })

    return spectral_line_data
