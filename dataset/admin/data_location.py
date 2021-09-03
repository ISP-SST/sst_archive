from django.contrib import admin

from dataset.models import DataLocation


@admin.register(DataLocation)
class DataLocationAdmin(admin.ModelAdmin):
    """Admin class for the DataLocation model"""
    list_display = ['file_name', 'file_path', 'file_size']
