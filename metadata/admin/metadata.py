from django.contrib import admin

from metadata.models import Metadata


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_beg'
    list_display = ['oid', 'date_beg']
    list_filter = []
    readonly_fields = []
    search_fields = ['data_cube__filename']
