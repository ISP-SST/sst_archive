import django
import secrets

from django.db import models


def generate_token():
    # TODO(daniel): While a 16 byte secure token is unlikely to create collisions in the database,
    #               we should still have a retry-loop that catches such errors and regenerates a
    #               new token. In practice there will be very few tokens active at the same time.
    return secrets.token_urlsafe(16)


class DataCubeAccessToken(models.Model):
    """
    Access token, or ticket, that grants the carrier of that token access to the specified DataCube. Access can
    be further restricted by an expiration date that dictates for how long the token will be valid.
    """
    data_cube = models.ForeignKey('observations.DataCube', verbose_name='Data Cube',
                                  help_text='The data cube that this token gives provides access to.',
                                  on_delete=models.CASCADE, related_name='access_token', null=True)
    token_string = models.CharField('Token String', unique=True, max_length=191,
                                    help_text='Unique textual representation of token',
                                    default=generate_token)
    grant_date = models.DateTimeField('Grant Date', help_text='The time and date when this access token was created',
                                      default=django.utils.timezone.now)
    expiration_date = models.DateTimeField('Expiration date',
                                           help_text='The time and date when this access token expires',
                                           default=django.utils.timezone.now)
    comment = models.TextField('Comment')

    class Meta:
        ordering = ['data_cube__filename']
        verbose_name = 'Data Cube Access Token'

    def __str__(self):
        return '%s (%s)' % (self.token_string, self.data_cube.filename)

# TODO(daniel): We might want a step that continuously prunes expired tokens from
#               the database.
