from django.contrib import admin

from previews.models import AnimatedGifPreview, ImagePreview


@admin.register(AnimatedGifPreview)
class AnimatedGifPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
