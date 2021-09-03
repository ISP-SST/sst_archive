from django.db import models


class InstrumentManager(models.Manager):
    """Manager that optimize the queries by selecting the foreign objects"""

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.select_related('telescope')
        return queryset


class Instrument(models.Model):
    """Model for the description of an instrument on a telescope"""
    name = models.CharField(primary_key=True, max_length=30)
    description = models.TextField(help_text='Instrument description', blank=True, null=True)
    # telescope = models.ForeignKey('Telescope', related_name='instruments', on_delete=models.PROTECT)

    objects = InstrumentManager()

    def __str__(self):
        return self.name
