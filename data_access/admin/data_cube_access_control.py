from django.contrib import admin

from data_access.models import DataCubeAccessControl


@admin.register(DataCubeAccessControl)
class DataCubeAccessControlAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'release_date']
    autocomplete_fields = ['data_cube']
