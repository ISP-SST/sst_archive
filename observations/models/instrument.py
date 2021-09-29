from django.db import models


class Instrument(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    description = models.TextField(help_text='Instrument description', blank=True, null=True)

    def __str__(self):
        return self.name
