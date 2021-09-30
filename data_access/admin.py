from django.contrib import admin

from .models import DataCubeAccessControl, DataCubeAccessGrant, DataCubeAccessToken


@admin.register(DataCubeAccessControl)
class DataCubeAccessControlAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'release_date']


@admin.register(DataCubeAccessGrant)
class DataCubeAccessGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'user__email']
    autocomplete_fields = ['data_cube']


@admin.register(DataCubeAccessToken)
class DataCubeAccessTokenAdmin(admin.ModelAdmin):
    search_fields =  ['data_cube__filename', 'token_string']
    autocomplete_fields = ['data_cube']
