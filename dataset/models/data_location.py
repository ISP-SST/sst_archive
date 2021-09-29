from django.db import models


class DataLocationManager(models.Manager):
    """Manager that optimize the queries by selecting the foreign objects"""

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('instrument')
        return queryset


class DataLocation(models.Model):
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE, null=True)
    file_path = models.CharField(help_text='Path to the file, relative to the file root and excluding the name of the '
                                           'file', max_length=191)
    file_name = models.CharField(help_text='Full file name including extension (.fits)', max_length=120, unique=True)
    file_size = models.PositiveBigIntegerField(help_text='Size of the file in bytes')

    objects = DataLocationManager()

    def __str__(self):
        return self.file_name
