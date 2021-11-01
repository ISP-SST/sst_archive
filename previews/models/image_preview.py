from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe


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

