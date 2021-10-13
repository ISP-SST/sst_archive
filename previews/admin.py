from django.contrib import admin

from previews.models import AnimatedGifPreview, ImagePreview, R0Data


@admin.register(AnimatedGifPreview)
class AnimatedGifPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']


@admin.register(R0Data)
class R0DataAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
