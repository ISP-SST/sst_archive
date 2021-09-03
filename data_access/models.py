from django.db import models


class DataLocationAccessControl(models.Model):
    """Contains information about the access restrictions put on the data pointed to by the DataLocation."""
    data_location = models.OneToOneField('dataset.DataLocation', on_delete=models.CASCADE,
                                         related_name='access_control', null=False, unique=True)
    release_date = models.DateField(null=True)
    release_comment = models.TextField(verbose_name='Release comment', help_text='Comment about the release restrictions'
                                                                                 'for this data.', null=True)


class DataLocationAccessGrant(models.Model):
    """Creates a link between a user and a DataLocation, signalling that the user has read access to the file pointed
    to by the DataLocation."""
    # The email is used to link the access rights to a user without requiring the user to be registered in the system at
    # the time of the grant. Data can currently be ingested without a user account.
    # TODO: Would we rather have a strict requirement on the specific user being registered in the system prior to
    #       ingestion in the pipeline?
    user_email = models.CharField(verbose_name='User email', max_length=200)
    data_location = models.ForeignKey('dataset.DataLocation', verbose_name='Data location',
                                      help_text='The data location that this grant gives the user access to.',
                                      on_delete=models.CASCADE, related_name='access_grants', null=False)

    class Meta:
        ordering = ['user_email']
        verbose_name = 'Data location access grant'
        unique_together = [('user_email', 'data_location')]
        permissions = (
            ("can_access_protected_data", "Can access protected data"),
        )


    def __str__(self):
        return '%s - %s' % (self.data_location.file_name, self.user_email)
