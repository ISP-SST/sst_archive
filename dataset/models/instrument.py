from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property


class Instrument(models.Model):
    """Model for the description of an instrument on a telescope"""
    name = models.CharField(primary_key=True, max_length=30)
    description = models.TextField(help_text='Instrument description', blank=True, null=True)

    metadata_content_type = models.OneToOneField(ContentType, on_delete=models.SET_NULL,
                                                 limit_choices_to=models.Q(app_label='metadata') & ~models.Q(
                                                     model='tag'), help_text='The model for this instrument metadata',
                                                 blank=True, null=True)


    @cached_property
    def metadata_model(self):
        if self.metadata_content_type is None:
            raise ValueError('metadata_content_type has not been set for this dataset')
        else:
            return self.metadata_content_type.model_class()


    def __str__(self):
        return self.name
