from django.contrib.auth.models import Group
from django.db import models, transaction
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property


class DatasetManager(models.Manager):
    """Manager that optimize the queries by selecting the foreign objects"""

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user_group')
        return queryset

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Dataset(models.Model):
    """The Dataset model describes a single piece of science data (FITS cube) on a high level."""
    name = models.CharField(max_length=200, unique=True, help_text='Can contain any unicode character')
    description = models.TextField(blank=True, null=True, help_text='Can contain html with links, emphasis, etc.')
    contact_email = models.EmailField(help_text='Email of the dataset archive contact person', blank=True, null=True)
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)
    user_group = models.ForeignKey('auth.Group', on_delete=models.SET_NULL, related_name='user_groups',
                                   help_text='User of this group can modify the dataset', blank=True, null=True)
    metadata_content_type = models.OneToOneField(ContentType, on_delete=models.SET_NULL,
                                                 limit_choices_to=models.Q(app_label='metadata') & ~models.Q(
                                                     model='tag'), help_text='The model for this dataset metadata',
                                                 blank=True, null=True, unique=True)

    objects = DatasetManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Dataset'

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        """Save the current instance"""

        # If there is no user_group, create one with the permissions to view/add/change/delete the metadata
        if self.name and self.metadata_content_type and not self.user_group:
            self.user_group = Group.objects.create(name='%s manager' % self.name)
            self.user_group.permissions.add(*self.metadata_content_type.permission_set.all())

        super().save(*args, **kwargs)

    @cached_property
    def metadata_model(self):
        if self.metadata_content_type is None:
            raise ValueError('metadata_content_type has not been set for this dataset')
        else:
            return self.metadata_content_type.model_class()

    def estimated_metadata_count(self):
        return self.metadata_model.objects.count()
