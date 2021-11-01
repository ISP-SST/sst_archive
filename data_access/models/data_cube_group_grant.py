from django.contrib.auth.models import Group
from django.db import models


class DataCubeGroupGrant(models.Model):
    """
    Creates a link between a Group and a DataCube that means that users in that group has access
    to this file.
    """

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    data_cube = models.ForeignKey('observations.DataCube', verbose_name='Data Cube',
                                  on_delete=models.CASCADE, related_name='group_grants', null=True)

    class Meta:
        ordering = ['data_cube__filename']
        unique_together = [('group', 'data_cube')]

    def __str__(self):
        return '%s - %s' % (self.data_cube.filename, self.group)
