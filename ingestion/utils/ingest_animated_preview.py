"""

import os
import tempfile
from pathlib import Path

from django.core.files import File

from ingestion.utils.create_animated_preview import create_animated_preview
from previews.models import AnimatedGifPreview


def update_or_create_gif_preview(hdus, data_cube, regenerate_preview=False):
    preview, created = AnimatedGifPreview.objects.update_or_create(data_cube=data_cube)

    if regenerate_preview or not preview.full_size:
        tmp_file = Path(tempfile.gettempdir()).joinpath(Path(data_cube.filename).with_suffix('.gif'))
        create_animated_preview(tmp_file, generate_if_missing=True, data_cube=preview.data_cube, fits_hdus=hdus)
        preview.full_size.save(os.path.basename(tmp_file),
                           File(open(tmp_file, 'rb')))

    preview.save()

"""
