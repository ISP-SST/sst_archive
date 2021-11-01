from django.db import models


class DataCubeAccessControl(models.Model):
    """
    Contains information about the access restrictions put on the data pointed to by the DataCube.
    """

    class DataClass(models.TextChoices):
        """
        """
        SOLARNET = "solarnet"
        SWEDISH_UNIVERSITY = "swedish_university"
        INTERNATIONAL_PAYING_UNIVERSITY = "ipu"
        OPEN = "open"
        UNSPECIFIED = "unspecified"

    data_cube = models.OneToOneField('observations.DataCube', on_delete=models.CASCADE,
                                         related_name='access_control', null=True, unique=True)
    release_date = models.DateField(null=True)
    release_comment = models.TextField(verbose_name='Release comment',
                                       help_text='Comment about the release restrictions'
                                                 'for this data.', null=True)
    data_class = models.CharField(choices=DataClass.choices, max_length=32, default=DataClass.UNSPECIFIED)

    def __str__(self):
        return self.data_cube.filename if self.data_cube else str(self.release_date)
