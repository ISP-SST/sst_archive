from django.contrib import admin

from core.utils import extend_admin
from observations.admin import DataCubeAdmin
from observations.models import DataCube
from previews.models import ImagePreview


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename']
    fields = ['full_size_tag', 'full_size', 'thumbnail_tag', 'thumbnail']
    readonly_fields = ['full_size_tag', 'thumbnail_tag']


class ImagePreviewInlineAdmin(admin.TabularInline):
    fields = ['full_size_tag', 'full_size', 'thumbnail_tag', 'thumbnail']
    readonly_fields = ['full_size_tag', 'thumbnail_tag']
    model = ImagePreview
    can_delete = False


extend_admin(DataCube, DataCubeAdmin, ImagePreviewInlineAdmin, weight=0)
