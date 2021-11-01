from django.contrib import admin

from data_access.models import DataCubeGroupGrant


@admin.register(DataCubeGroupGrant)
class DataCubeGroupGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'group__name']
    autocomplete_fields = ['data_cube', 'group']
