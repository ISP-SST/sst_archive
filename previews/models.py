from django.db import models


# TODO(daniel): These models that link to a file should probably be using the Django FilePathField instead.


class AnimatedGifPreview(models.Model):
    """Contains a relative link to an animated GIF preview of a DataCube."""
    data_cube = models.OneToOneField('observations.DataCube', related_name='animated_preview',
                                     null=False, on_delete=models.CASCADE)
    animated_gif = models.TextField('URL to animated GIF')


class ImagePreview(models.Model):
    """Represents a static image preview of the DataCube."""
    data_cube = models.OneToOneField('observations.DataCube', related_name='thumbnail', null=False,
                                     on_delete=models.CASCADE)
    image_url = models.TextField('Relative URL to image preview')
    image_path = models.TextField('Absolute path to image on disk')


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
