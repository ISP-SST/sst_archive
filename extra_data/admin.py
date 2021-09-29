from django.contrib import admin

from extra_data.models import AnimatedGifPreview, ImagePreview


@admin.register(AnimatedGifPreview)
class AnimatedGifPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
