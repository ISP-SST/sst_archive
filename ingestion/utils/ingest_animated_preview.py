import os
from pathlib import Path

from ingestion.utils.generate_animated_preview import generate_animated_gif_preview
from previews.models import AnimatedGifPreview
from django.conf import settings


def update_or_create_gif_preview(hdus, data_cube):
    # TODO(daniel): This needs to be cleaned up. Must happen when image previews are implemented for real.
    try:
        preview = AnimatedGifPreview.objects.get(data_cube=data_cube)
        gif_uri = preview.animated_gif
        filename = os.path.basename(gif_uri)
        expected_gif_uri = os.path.join(settings.GIF_URL_ROOT, filename)
        gif_path = os.path.join(settings.GIF_ROOT, filename)

        if gif_uri != expected_gif_uri:
            preview.animated_gif = expected_gif_uri
            preview.save()
    except AnimatedGifPreview.DoesNotExist:
        gif_filename = Path(data_cube.filename).with_suffix('.gif')
        gif_path = os.path.join(settings.GIF_ROOT, gif_filename)
        gif_uri = os.path.join(settings.GIF_URL_ROOT, gif_filename)
        preview = AnimatedGifPreview(data_cube=data_cube, animated_gif=gif_uri)
        preview.save()

    if not os.path.isfile(gif_path):
        generate_animated_gif_preview(hdus, gif_path)
