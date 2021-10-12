import os
from pathlib import Path

from ingestion.utils.generate_image_preview import generate_image_preview
from previews.models import ImagePreview
from django.conf import settings


def update_or_create_image_preview(hdus, data_cube, regenerate_preview=False):
    try:
        preview = ImagePreview.objects.get(data_cube=data_cube)
        image_path = preview.image_path
        image_url_path = preview.image_url
    except ImagePreview.DoesNotExist:
        image_filename = Path(data_cube.filename).with_suffix('.png')
        image_path = os.path.join(settings.GENERATED_ROOT, 'images', image_filename)
        image_url_path = os.path.join(settings.GENERATED_URL_ROOT, 'images', image_filename)
        preview = ImagePreview(data_cube=data_cube, image_path=image_path, image_url=image_url_path)

    if regenerate_preview or not os.path.isfile(image_path):
        generate_image_preview(hdus, image_path)

    preview.save()
