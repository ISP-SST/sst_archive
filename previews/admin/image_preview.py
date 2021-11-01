from django.contrib import admin

from previews.models import ImagePreview


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename']
    fields = ['full_size_tag', 'full_size', 'thumbnail_tag', 'thumbnail']
    readonly_fields = ['full_size_tag', 'thumbnail_tag']
