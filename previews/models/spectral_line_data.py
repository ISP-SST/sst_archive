from django.db import models


class SpectralLineData(models.Model):
    class Meta:
        verbose_name = 'Spectral Line Data'
        verbose_name_plural = 'Spectral Line Data'

    data_cube = models.OneToOneField('observations.DataCube', related_name='spectral_line_data', null=False,
                                     on_delete=models.CASCADE)
    data_json = models.TextField('JSON blob with data for the plot')
    data_preview = models.ImageField('Small preview image stored in managed upload folder',
                                     upload_to='spectral-line/thumbnails/', null=True)

    def __str__(self):
        if self.data_cube:
            return self.data_cube.filename
        else:
            return self.data_json
