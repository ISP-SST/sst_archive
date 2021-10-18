from django.conf import settings
from django.db import models

# TODO(daniel): These models that link to a file should probably be using the Django FilePathField instead.
from django.utils.safestring import mark_safe


class AnimatedGifPreview(models.Model):
    """Contains a relative link to an animated GIF preview of a DataCube."""
    data_cube = models.OneToOneField('observations.DataCube', related_name='animated_preview',
                                     null=False, on_delete=models.CASCADE)
    animated_gif = models.TextField('URL to animated GIF')

    full_size = models.ImageField('Preview animation stored in the managed upload folder', upload_to='gifs/full-size/',
                                  null=True)

    def full_size_tag(self):
        return mark_safe('<img src="%s/%s" />' % (settings.MEDIA_URL, self.full_size))

    full_size_tag.short_description = 'Full size image'

    def __str__(self):
        return self.full_size.name


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
