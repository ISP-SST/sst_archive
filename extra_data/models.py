from django.db import models


# TODO(daniel): These models that link to a file should probably be using the Django FilePathField instead.


class AnimatedGifPreview(models.Model):
    """Contains a relative link to an animated GIF preview of a DataLocation."""
    data_location = models.OneToOneField('dataset.DataLocation', related_name='animated_preview', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    animated_gif = models.CharField('URL to animated GIF', max_length=255)


class ImagePreview(models.Model):
    """Represents a static image preview of the DataLocation."""
    data_location = models.OneToOneField('dataset.DataLocation', related_name='thumbnail', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    image_url = models.CharField('Relative URL to image preview', max_length=255)
    image_path = models.CharField('Absolute path to image on disk', max_length=255)
