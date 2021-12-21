import json
import os
import tempfile
from pathlib import Path

from astropy.io import fits
from django.core.files import File

from observations.models import DataCube
from previews.ingesters.generate_spectral_line_profile_data import generate_spectral_line_profile_data_v3
from previews.ingesters.generate_spectral_line_profile_plot import \
    generate_spectral_line_profile_plot_in_separate_process
from previews.models import SpectralLineData


def ingest_spectral_line_profile_data(hdus: fits.HDUList, data_cube: DataCube):
    json_data = generate_spectral_line_profile_data_v3(hdus)

    if json_data is None:
        return None

    spectral_line_data, created = SpectralLineData.objects.update_or_create(data_cube=data_cube, defaults={
        'data_json': json.dumps(json_data)
    })

    tmp_file = Path(tempfile.gettempdir()).joinpath(Path(data_cube.filename).with_suffix('.svg'))
    generate_spectral_line_profile_plot_in_separate_process(data_cube.path, tmp_file, size=(4, 2))
    spectral_line_data.data_preview.save(os.path.basename(tmp_file),
                                         File(open(tmp_file, 'rb')))

    return spectral_line_data
