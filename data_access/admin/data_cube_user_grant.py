from django.contrib import admin

from data_access.models import DataCubeUserGrant


@admin.register(DataCubeUserGrant)
class DataCubeUserGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'user__email']
    autocomplete_fields = ['data_cube', 'user']
