from django.contrib import admin

from core.utils import extend_admin
from metadata.models import Metadata
from observations.admin import DataCubeAdmin
from observations.models import DataCube


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_beg'
    list_display = ['data_cube', 'date_beg']
    list_filter = []
    readonly_fields = []
    search_fields = ['data_cube__filename']


class MetadataInlineAdmin(admin.StackedInline):
    model = Metadata
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False


extend_admin(DataCube, DataCubeAdmin, MetadataInlineAdmin)
