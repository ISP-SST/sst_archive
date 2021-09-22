import secrets

import django
from django.db import models


class DataLocationAccessControl(models.Model):
    """Contains information about the access restrictions put on the data pointed to by the DataLocation."""
    data_location = models.OneToOneField('dataset.DataLocation', on_delete=models.CASCADE,
                                         related_name='access_control', null=False, unique=True)
    release_date = models.DateField(null=True)
    release_comment = models.TextField(verbose_name='Release comment',
                                       help_text='Comment about the release restrictions'
                                                 'for this data.', null=True)

    def __str__(self):
        return self.data_location.file_name


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


def generate_token():
    # TODO(daniel): While a 16 byte secure token is unlikely to create collisions in the database,
    #               we should still have a retry-loop that catches such errors and regenerates a
    #               new token. In practice there will be very few tokens active at the same time.
    return secrets.token_urlsafe(16)


class DataLocationAccessToken(models.Model):
    """Access token, or ticket, that grants the carrier of that token access to the specified DataLocation. Access can
    be further restricted by an expiration date that dictates for how long the token will be valid."""
    data_location = models.ForeignKey('dataset.DataLocation', verbose_name='Data location',
                                      help_text='The data location that this token gives provides access to.',
                                      on_delete=models.CASCADE, related_name='access_token')
    token_string = models.CharField('Token String', unique=True, max_length=255,
                                    help_text='Unique textual representation of token',
                                    default=generate_token)
    grant_date = models.DateTimeField('Grant Date', help_text='The time and date when this access token was created',
                                      default=django.utils.timezone.now)
    expiration_date = models.DateTimeField('Expiration date',
                                           help_text='The time and date when this access token expires',
                                           default=django.utils.timezone.now)
    comment = models.TextField('Comment')

    def __str__(self):
        return '%s (%s)' % (self.token_string, self.data_location.file_name)


# TODO(daniel): We might want a step that continuously prunes expired tokens from
#               the database.
