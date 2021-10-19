from django.contrib import admin

from previews.models import AnimatedGifPreview, ImagePreview, R0Data, SpectralLineData


@admin.register(AnimatedGifPreview)
class AnimatedGifPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
	fields = ['full_size_tag', 'full_size']
	readonly_fields = ['full_size_tag']


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
	fields = ['full_size_tag', 'full_size', 'thumbnail_tag', 'thumbnail']
	readonly_fields = ['full_size_tag', 'thumbnail_tag']


@admin.register(R0Data)
class R0DataAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']


@admin.register(SpectralLineData)
class SpectralLineDataAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
