from django.db import models


class DataCubeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')


class DataCube(models.Model):
    oid = models.CharField('Observation ID',
                           help_text='Unique identification string for the observation metadata, usually in the form '
                                     'YYYYMMDDHHMMSS; cannot be modified once it is set',
                           unique=True, db_index=True, max_length=191)
    filename = models.CharField(help_text='File name including .FITS extension', max_length=512)
    path = models.TextField(help_text='Full path to the file', unique=True)
    size = models.PositiveBigIntegerField(help_text='Size of the file in bytes')
    instrument = models.ForeignKey('observations.Instrument', on_delete=models.CASCADE)
    tags = models.ManyToManyField('observations.Tag', 'cubes')

    objects = DataCubeManager()

    def __str__(self):
        return self.filename
