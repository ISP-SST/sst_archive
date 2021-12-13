from django.db import models


class DataCubeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')


class DataCube(models.Model):
    class GroupingTag(models.TextChoices):
        """
        Describes the grouping relationship to the parent Observation. If no such tag is present,
        a DataCube can still be tied to the same parent Observation. If that's the case, the relationship
        is implicit. That could mean that DataCubes happened to have the same default POINT_ID, i.e. DATE-BEG.

        The available options are:

        GROUPED - DataCube was explicitly put in a group with other DataCubes.
        MOSAIC - This DataCube is part of a mosaic set for the same observation.
        """
        GROUPED = "grouped"
        MOSAIC = "mosaic"

    oid = models.CharField('Observation ID',
                           help_text='Unique identification string for the observation metadata, usually in the form '
                                     'YYYYMMDDHHMMSS; cannot be modified once it is set',
                           unique=True, db_index=True, max_length=191)
    observation = models.ForeignKey('observations.Observation', help_text='Parent observation this DataCube belongs to',
                                    on_delete=models.CASCADE, related_name='cubes', null=True)
    grouping_tag = models.CharField(help_text='Tag that describes if the grouping relationship to the parent '
                                              'observation. See the GroupTag choices for more information',
                                    choices=GroupingTag.choices, null=True, max_length=16, default=None, blank=True)
    filename = models.CharField(help_text='File name including .FITS extension', max_length=512)
    path = models.TextField(help_text='Full path to the file')
    size = models.PositiveBigIntegerField(help_text='Size of the file in bytes')
    instrument = models.ForeignKey('observations.Instrument', on_delete=models.CASCADE)
    tags = models.ManyToManyField('observations.Tag', 'cubes', blank=True)

    features_ingested = models.BooleanField('Features have been ingested', default=False,
                                            help_text='If a proper list of FEATURES was present in the data cube this'
                                                      'will be set to True')
    events_ingested = models.BooleanField('Events have been ingested', default=False,
                                          help_text='If a proper list of EVENTS was present in the data cube this will'
                                                    'be set to True')

    objects = DataCubeManager()

    def __str__(self):
        return self.filename
