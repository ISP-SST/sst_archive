import os
import tempfile
from pathlib import Path

from django.core.files import File

from previews.ingesters.generate_image_preview import generate_image_preview
from previews.models import ImagePreview


THUMBNAIL_WIDTH_PX = 78


def ingest_image_previews(hdus, data_cube, regenerate_preview=False):
    image_preview, created = ImagePreview.objects.update_or_create(data_cube=data_cube)

    if regenerate_preview or not image_preview.full_size:
        tmp_file = Path(tempfile.gettempdir()).joinpath(Path(data_cube.filename).with_suffix('.jpg'))
        generate_image_preview(tmp_file, generate_if_missing=True, fits_hdus=hdus, data_cube=image_preview.data_cube)
        image_preview.full_size.save(os.path.basename(tmp_file),
                           File(open(tmp_file, 'rb')))

    if regenerate_preview or not image_preview.thumbnail:
        tmp_file = Path(tempfile.gettempdir()).joinpath(Path(data_cube.filename).with_suffix('.png'))
        generate_image_preview(tmp_file, generate_if_missing=True,
                             scale_x=THUMBNAIL_WIDTH_PX, fits_hdus=hdus, data_cube=image_preview.data_cube)
        image_preview.thumbnail.save(os.path.basename(tmp_file),
                                     File(open(tmp_file, 'rb')))

    image_preview.save()
