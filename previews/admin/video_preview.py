from django.contrib import admin

from previews.models import VideoPreview


@admin.register(VideoPreview)
class VideoPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
	fields = ['video_wings_tag', 'video_wings']
	readonly_fields = ['video_wings_tag']
