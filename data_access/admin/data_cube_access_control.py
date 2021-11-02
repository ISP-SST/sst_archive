from django.contrib import admin

from data_access.models import DataCubeAccessControl
from observations.admin import DataCubeAdmin, extend_admin
from observations.models import DataCube


@admin.register(DataCubeAccessControl)
class DataCubeAccessControlAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'release_date']
    autocomplete_fields = ['data_cube']


class DataCubeAccessControlInlineAdmin(admin.TabularInline):
    model = DataCubeAccessControl
    can_delete = False


extend_admin(DataCube, DataCubeAdmin, DataCubeAccessControlInlineAdmin, weight=3)
