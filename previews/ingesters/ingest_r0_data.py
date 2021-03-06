import json

from astropy.io import fits

from observations.models import DataCube
from previews.ingesters.generate_r0_plot_data import generate_r0_plot_data_v4
from previews.models import R0Data


def ingest_r0_data(hdus: fits.HDUList, data_cube: DataCube):
    json_data = generate_r0_plot_data_v4(hdus)

    if json_data is None:
        return None

    r0data, created = R0Data.objects.update_or_create(data_cube=data_cube, defaults={
        'data_json': json.dumps(json_data)
    })

    return r0data
