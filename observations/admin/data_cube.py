from django.contrib import admin

from observations.models import DataCube


@admin.register(DataCube)
class DataCubeAdmin(admin.ModelAdmin):
    list_display = ['filename', 'path', 'size']
    search_fields = ['file_name']
