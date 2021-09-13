from django.db import models, transaction

import os


class ExtraData(models.Model):
    data_location = models.ForeignKey('dataset.DataLocation', related_name='extra_data', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    new_field = models.TextField(verbose_name='NEW_FIELD', help_text='New Test Field', blank=True, null=True)


class AnimatedGifPreview(models.Model):
    data_location = models.OneToOneField('dataset.DataLocation', related_name='animated_preview', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    animated_gif = models.CharField('URL to animated GIF', max_length=255)

    """
    @transaction.atomic
    def delete(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Try to delete the GIF file on disk as well.
        os.unlink(self.animated_gif)
    """

class ImagePreview(models.Model):
    data_location = models.OneToOneField('dataset.DataLocation', related_name='thumbnail', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    image_url = models.CharField('Relative URL to image preview', max_length=255)
    image_path = models.CharField('Absolute path to image on disk', max_length=255)
