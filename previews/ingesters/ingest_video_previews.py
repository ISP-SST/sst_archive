import os
import tempfile
from pathlib import Path

from django.core.files import File

from previews.ingesters.generate_video_preview import generate_video_preview
from previews.models import VideoPreview


def ingest_video_previews(hdus, data_cube, regenerate_preview=False):
    video_preview, created = VideoPreview.objects.update_or_create(data_cube=data_cube)

    if regenerate_preview or not video_preview.video_core:
        tmp_file = Path(tempfile.gettempdir()).joinpath(Path(data_cube.filename).with_suffix('.webm'))
        preview = generate_video_preview(tmp_file, fits_hdus=hdus, data_cube=data_cube)
        if preview:
            video_preview.video_core.save(os.path.basename(tmp_file),
                                          File(open(tmp_file, 'rb')))

    video_preview.save()
