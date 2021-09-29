from django.contrib import admin

from .models import DataLocationAccessControl, DataLocationAccessGrant, DataLocationAccessToken


@admin.register(DataLocationAccessControl)
class DataLocationAccessControlAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'release_date']


@admin.register(DataLocationAccessGrant)
class DataLocationAccessGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename', 'user__email']
    autocomplete_fields = ['data_cube']


@admin.register(DataLocationAccessToken)
class DataLocationAccessTokenAdmin(admin.ModelAdmin):
    search_fields =  ['data_cube__filename', 'token_string']
    autocomplete_fields = ['data_cube']
