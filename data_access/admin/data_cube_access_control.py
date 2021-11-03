from django.contrib import admin

from data_access.models import DataCubeAccessControl
from observations.admin import DataCubeAdmin, extend_admin
from observations.models import DataCube


@admin.register(DataCubeAccessControl)
class DataCubeAccessControlAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'release_date']
    autocomplete_fields = ['data_cube']


class DataCubeAccessControlInlineAdmin(admin.TabularInline):
    """
    Inline admin form that is displayed in the DataCube's admin page.

    Does not allow for inline editing, but does provide a link to the main admin page for DataCubeAccessControls.
    """
    model = DataCubeAccessControl
    can_delete = False
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False


extend_admin(DataCube, DataCubeAdmin, DataCubeAccessControlInlineAdmin, weight=3)
