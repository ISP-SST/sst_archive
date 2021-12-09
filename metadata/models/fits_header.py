from django.db import models


class FITSHeader(models.Model):
    data_cube = models.OneToOneField('observations.DataCube', related_name='fits_header', null=True, blank=True,
                                     on_delete=models.CASCADE)
    fits_header = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'FITS Header'

    def __str__(self):
        return self.data_cube.filename if self.data_cube else '-'
