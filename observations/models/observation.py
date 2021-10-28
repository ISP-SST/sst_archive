from django.db import models


class Observation(models.Model):
    point_id = models.CharField('Point ID',
                           help_text='Point ID indicating the pointing and acting as a group identifier for multi-cube'
                                'observations',
                           unique=True, db_index=True, max_length=191)

    def __str__(self):
        return self.point_id
