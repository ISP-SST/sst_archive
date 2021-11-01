from django.contrib import admin

from data_access.models import DataCubeAccessToken


@admin.register(DataCubeAccessToken)
class DataCubeAccessTokenAdmin(admin.ModelAdmin):
    search_fields =  ['data_cube__filename', 'token_string']
    autocomplete_fields = ['data_cube']
