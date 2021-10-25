from django.contrib import admin

from previews.models import ImagePreview, R0Data, SpectralLineData, VideoPreview


@admin.register(VideoPreview)
class VideoPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
	fields = ['video_wings_tag', 'video_wings']
	readonly_fields = ['video_wings_tag']


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
