from django.contrib import admin

from core.utils import extend_admin
from observations.admin import DataCubeAdmin
from observations.models import DataCube
from previews.models import VideoPreview


@admin.register(VideoPreview)
class VideoPreviewAdmin(admin.ModelAdmin):
    search_fields = ['data_cube__filename']
    fields = ['video_core_tag', 'video_core']
    readonly_fields = ['video_core_tag']


class VideoPreviewInlineAdmin(admin.TabularInline):
    fields = ['video_core_tag', 'video_core']
    readonly_fields = ['video_core_tag']
    model = VideoPreview
    can_delete = False


extend_admin(DataCube, DataCubeAdmin, VideoPreviewInlineAdmin, weight=1)
