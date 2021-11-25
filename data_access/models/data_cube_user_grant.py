from django.db import models


class DataCubeUserGrant(models.Model):
    """
    Creates a link between a user's e-mail address and a DataCube, signalling that the user has read
    access to the file pointed to by the DataCube. Since the connection uses the e-mail address it's
    possible to create a link even before the user is created and then allow it to take effect once
    the user is in place in the database.
    """
    user_email = models.CharField(verbose_name='E-mail address of the user with the grant',
                                  max_length=190)
    data_cube = models.ForeignKey('observations.DataCube', verbose_name='Data Cube',
                                  help_text='The data cube that this token gives provides access to.',
                                  on_delete=models.CASCADE, related_name='user_grants', null=True)

    class Meta:
        ordering = ['user_email']
        unique_together = [('user_email', 'data_cube')]
        permissions = (
            ("can_access_protected_data", "Can access protected data"),
        )

    def __str__(self):
        return '%s - %s' % (self.data_cube.filename, self.user_email)
