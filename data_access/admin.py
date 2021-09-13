from django.contrib import admin

from .models import DataLocationAccessControl, DataLocationAccessGrant, DataLocationAccessToken


@admin.register(DataLocationAccessControl)
class DataLocationAccessControlAdmin(admin.ModelAdmin):
    search_fields = ['data_location__file_name', 'release_date']


@admin.register(DataLocationAccessGrant)
class DataLocationAccessGrantAdmin(admin.ModelAdmin):
    search_fields = ['data_location__file_name', 'user__email']
    autocomplete_fields = ['data_location']


@admin.register(DataLocationAccessToken)
class DataLocationAccessTokenAdmin(admin.ModelAdmin):
    search_fields =  ['data_location__file_name', 'token_string']
    autocomplete_fields = ['data_location']
