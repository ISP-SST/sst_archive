from django.contrib.auth.models import User
from django.db import models


class DataCubeUserGrant(models.Model):
    """
    Creates a link between a user and a DataCube, signalling that the user has read access to the file pointed
    to by the DataCube.
    """
    user = models.ForeignKey(User, verbose_name='The User the permission has been granted to',
                             on_delete=models.CASCADE)
    data_cube = models.ForeignKey('observations.DataCube', verbose_name='Data Cube',
                                  help_text='The data cube that this token gives provides access to.',
                                  on_delete=models.CASCADE, related_name='user_grants', null=True)

    class Meta:
        ordering = ['user']
        unique_together = [('user', 'data_cube')]
        permissions = (
            ("can_access_protected_data", "Can access protected data"),
        )

    def __str__(self):
        return '%s - %s' % (self.data_cube.filename, str(self.user))
