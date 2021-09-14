from django.db import models


class ExtraData(models.Model):
    """This was just created as a proof of concept. Not used. Nothing to see here."""
    data_location = models.ForeignKey('dataset.DataLocation', related_name='extra_data', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    new_field = models.TextField(verbose_name='NEW_FIELD', help_text='New Test Field', blank=True, null=True)


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
