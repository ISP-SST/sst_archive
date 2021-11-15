from django.db import models


class Observation(models.Model):
    point_id = models.CharField('Point ID',
                           help_text='Point ID indicating the pointing and acting as a group identifier for multi-cube'
                                'observations',
                           unique=True, db_index=True, max_length=191)

    # Observation dates are also included in the Observation model to allow for more intuitive ordering of
    # search results, since relying on the date_beg and date_end fields in the Metadata model creates too
    # many levels of indirection.
    date_beg = models.DateTimeField('Observation began', help_text='Start time of the observation [UTC]', blank=True,
                                    null=True, db_index=True)
    date_end = models.DateTimeField('Observation ended', help_text='End time of the observation [UTC]', blank=True,
                                    null=True, db_index=True)

    def __str__(self):
        return self.point_id
