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


class ImagePreview(models.Model):
    """Represents a static image preview of the DataCube."""
    data_cube = models.OneToOneField('observations.DataCube', related_name='previews', null=False,
                                     on_delete=models.CASCADE)
    full_size = models.ImageField('Preview image stored in the managed upload folder', upload_to='previews/', null=True)
    thumbnail = models.ImageField('Small preview image stored in managed upload folder', upload_to='thumbnails/',
                                  null=True)

    def full_size_tag(self):
        return mark_safe('<img src="%s/%s" />' % (settings.MEDIA_URL, self.full_size))

    full_size_tag.short_description = 'Full size image'

    def thumbnail_tag(self):
        return mark_safe('<img src="%s/%s" />' % (settings.MEDIA_URL, self.thumbnail))

    thumbnail_tag.short_description = 'Thumbnail'

    def __str__(self):
        return self.full_size.name


class R0Data(models.Model):
    class Meta:
        verbose_name = 'R0 Data'
        verbose_name_plural = 'R0 Data'

    data_cube = models.OneToOneField('observations.DataCube', related_name='r0data', null=False,
                                     on_delete=models.CASCADE)
    data_json = models.TextField('JSON blob with data for the plot')
    data_version = models.IntegerField('Version number that indicates the format of the JSON blob. If the JSON blob '
                                       'data format changes this field should be bumped as well')

    def __str__(self):
        if self.data_cube:
            return self.data_cube.filename
        else:
            return self.data_json


class SpectralLineData(models.Model):
    class Meta:
        verbose_name = 'Spectral Line Data'
        verbose_name_plural = 'Spectral Line Data'

    data_cube = models.OneToOneField('observations.DataCube', related_name='spectral_line_data', null=False,
                                     on_delete=models.CASCADE)
    data_json = models.TextField('JSON blob with data for the plot')
    data_version = models.IntegerField('Version number that indicates the format of the JSON blob. If the JSON blob '
                                       'data format changes this field should be bumped as well')
    data_preview = models.ImageField('Small preview image stored in managed upload folder',
                                     upload_to='spectral-line/thumbnails/', null=True)

    def __str__(self):
        if self.data_cube:
            return self.data_cube.filename
        else:
            return self.data_json
