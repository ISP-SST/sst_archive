from django.contrib import admin
from django.core.exceptions import ValidationError

from dataset.models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """Admin class for the Dataset model"""
    list_display = ['name', 'instrument', 'contact_email']
    readonly_fields = ['name', 'instrument', 'user_group', 'metadata_content_type']

    def get_readonly_fields(self, request, obj=None):
        """Return a list or tuple of field names that will be displayed as read-only"""
        # Allow superuser to change everything
        if request.user.is_superuser:
            return []
        else:
            return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        # Display only the datasets for which the user has access to
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user_group__in=request.user.groups.all())

    def has_change_permission(self, request, obj=None):
        """Return True if editing obj is permitted, False otherwise. If obj is None, return True or False to indicate
        whether editing of objects of this type is permitted in general"""

        # Allow the user to only change a dataset if he is a user of that dataset's user_group
        default_permission = super().has_change_permission(request, obj)
        if request.user.is_superuser or obj is None:
            return default_permission
        else:
            return default_permission and obj.user_group in request.user.groups.all()

    def get_object(self, request, object_id, from_field=None):
        """Return an instance matching the field and value provided"""

        # Redefine get_object because the default one uses get_queryset where we filter out the instances that are
        # not accessible by the request user as a consequence has_change_permission and has_delete_permission will
        # receive None instead of an instance when trying to change/delete an object that is not accessible by the
        # request user instead just use the _default_manager of the model
        field = self.model._meta.pk if from_field is None else self.model._meta.get_field(from_field)
        try:
            object_id = field.to_python(object_id)
            queryset = self.model._default_manager.get_queryset()
            return queryset.get(**{field.name: object_id})
        except (self.model.DoesNotExist, ValidationError, ValueError):
            return None
