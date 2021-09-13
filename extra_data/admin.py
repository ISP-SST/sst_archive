from django.contrib import admin

from extra_data.models import ExtraData, AnimatedGifPreview, ImagePreview


@admin.register(ExtraData)
class CrispAdmin(admin.ModelAdmin):
	pass


@admin.register(AnimatedGifPreview)
class AnimatedGifPreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_location__file_name']


@admin.register(ImagePreview)
class ImagePreviewAdmin(admin.ModelAdmin):
	search_fields = ['data_location__file_name']
