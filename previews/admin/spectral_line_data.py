from django.contrib import admin

from previews.models import SpectralLineData


@admin.register(SpectralLineData)
class SpectralLineDataAdmin(admin.ModelAdmin):
	search_fields = ['data_cube__filename']
