from django.db import models


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
