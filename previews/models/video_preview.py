from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe


class VideoPreview(models.Model):
    data_cube = models.OneToOneField('observations.DataCube', related_name='video_preview',
                                     null=False, on_delete=models.CASCADE)
    video_wings = models.ImageField('Temporal video from wings stored in upload folder', upload_to='videos/temporal/wings/',
                                  null=True)

    def video_wings_tag(self):
        return mark_safe('<video src="%s/%s" controls>Videos are not supported</video>' %
                         (settings.MEDIA_URL, self.video_wings))

    video_wings_tag.short_description = 'Temporal video preview'

    def __str__(self):
        return self.video_wings.name
