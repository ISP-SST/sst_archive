import json

from astropy.io import fits

from ingestion.utils.generate_r0_plot_data import generate_r0_plot_data_v3
from observations.models import DataCube
from previews.models import R0Data


def ingest_r0_data(hdus: fits.HDUList, data_cube: DataCube):
    json_data = generate_r0_plot_data_v3(hdus)

    r0data, created = R0Data.objects.update_or_create(data_cube=data_cube, defaults={
        'data_json': json.dumps(json_data),
        'data_version': 3
    })

    return r0data
