from django.db import models


class Instrument(models.Model):
    """Model for the description of an instrument on a telescope"""
    name = models.CharField(primary_key=True, max_length=30)
    description = models.TextField(help_text='Instrument description', blank=True, null=True)

    def __str__(self):
        return self.name
