from ast import literal_eval
from django.db import models
from django.conf import settings


class MetadataQuerySet(models.QuerySet):
    """Metadata QuerySet that adds an estimation of the number of items for a query"""

    def estimated_count(self):
        """Return an estimated count of the number of rows the QuerySet will return"""

        # Use postgres explain query to estimate the number of rows
        # if the estimated count is too small, return the actual count, because low estimates are off

        # HACK: use ast.literal_eval instead of json.loads because there is a bug in Django
        # the returned value of explain is not actual JSON https://code.djangoproject.com/ticket/32226
        execution_plan = literal_eval(self.explain(format='JSON'))
        count = execution_plan[0]['Plan']['Plan Rows']

        if count < settings.MIN_ESTIMATED_COUNT:
            count = self.count()

        return count


class MetadataManager(models.Manager):
    """Manager that optimize the queries by selecting the foreign objects"""

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('data_location')
        return queryset


class BaseMetadata(models.Model):
    """Abstract base model for the Metadata models"""
    oid = models.TextField('Observation ID',
                           help_text='Unique identification string for the observation metadata, usually in the form '
                                     'YYYYMMDDHHMMSS; cannot be modified once it is set',
                           unique=True, db_index=True)
    data_location = models.ForeignKey('dataset.DataLocation', related_name='%(app_label)s_%(class)s', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    fits_header = models.TextField(null=True, blank=True)
    date_beg = models.DateTimeField('DATE-BEG', help_text='Start time of the observation [UTC]', blank=True, null=True,
                                    db_index=True)
    date_end = models.DateTimeField('DATE-END', help_text='End time of the observation [UTC]', blank=True, null=True,
                                    db_index=True)
    wavemin = models.FloatField('WAVEMIN', help_text='Min value of the observation spectral range [nm]', blank=True,
                                null=True, db_index=True)
    wavemax = models.FloatField('WAVEMAX', help_text='Max value of the observation spectral range [nm]', blank=True,
                                null=True, db_index=True)

    objects = MetadataManager.from_queryset(MetadataQuerySet)()

    class Meta:
        abstract = True
        ordering = ['date_beg']

    def __str__(self):
        return self.oid
